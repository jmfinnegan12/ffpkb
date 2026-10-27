# -*- coding: utf-8 -*-
"""SEED SCRIPT (from an eastern-BC "SE Kootenay -> Kakwa" remote scouting report,
updated after a review flagged the roads as invisible on the shipped maps).
Copy into the working scratchpad and edit the bbox/points/overlays per sub-region for the new
report's geography; don't try to make this a generic parameterized tool before it's earned that
through a few more reports. See references/bc-geodata-toolkit.md for the endpoint list,
axis-order gotchas, and honest limits this script's design already works around.

BC ONLY — every overlay endpoint below is a BC/DataBC or Canada-wide (NRCan) government system.

Usage pattern (see bottom of file): call build_map() once per sub-region map, then again for a
zone-level orientation overview with draw_streams=False, draw_roads=False, boxes=[...] instead
of points.
Needs: matplotlib, numpy, Pillow -- stdlib urllib for fetches, no extra installs.

v2 change: roads are now pulled as WFS VECTORS (like streams), not a WMS raster overlay — the
WMS overlay's default road styling is nearly invisible against the hillshade, which was the
single biggest complaint on the first real use of this script. Gravel/FSR roads (the whole
point of a "remote access" report) now render as a bold dashed line, styled by ROAD_SURFACE.
"""
import io, math, json, urllib.request, urllib.parse
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

NRCAN = "https://datacube.services.geo.ca/ows/elevation"
WFS = "https://openmaps.gov.bc.ca/geo/pub/wfs"
def databc_wms(layer): return f"https://openmaps.gov.bc.ca/geo/pub/{layer}/ows"

def _get(url, timeout=100):
    req = urllib.request.Request(url, headers={"User-Agent": "bc-fish-map/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def _wms(endpoint, layers, bbox, w, h, transparent):
    lon0, lat0, lon1, lat1 = bbox  # WMS 1.3.0 + EPSG:4326 => bbox minLat,minLon,maxLat,maxLon
    params = {"service": "WMS", "version": "1.3.0", "request": "GetMap", "layers": layers,
              "crs": "EPSG:4326", "bbox": f"{lat0},{lon0},{lat1},{lon1}",
              "width": str(w), "height": str(h), "format": "image/png",
              "transparent": "true" if transparent else "false"}
    try:
        b = _get(endpoint + "?" + urllib.parse.urlencode(params))
        if b[:8].hex().startswith("89504e47"):
            im = Image.open(io.BytesIO(b)).convert("RGBA")
            return im.resize((w, h)) if im.size != (w, h) else im
    except Exception as e:
        print(f"  [wms skip] {layers}: {e.__class__.__name__}")
    return None

def fetch_stream_lines(bbox, min_order=3, timeout=95):
    """WFS vector pull -- fine on a per-map (tight) bbox; can time out on a full research-pass
    (~1deg square) bbox. Keep the map bbox tighter than the research bbox that fed it."""
    lon0, lat0, lon1, lat1 = bbox
    cql = f"STREAM_ORDER>={min_order} AND BBOX(GEOMETRY,{lon0},{lat0},{lon1},{lat1},'EPSG:4326')"
    p = {"service": "WFS", "version": "2.0.0", "request": "GetFeature",
         "typeNames": "pub:WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP", "outputFormat": "application/json",
         "srsName": "EPSG:4326", "count": "8000", "propertyName": "STREAM_ORDER,GEOMETRY", "CQL_FILTER": cql}
    try:
        j = json.loads(_get(WFS + "?" + urllib.parse.urlencode(p), timeout=timeout))
    except Exception as e:
        print(f"  [wfs streams FAILED -> WMS fallback] {e.__class__.__name__}")
        return None
    out = []
    for f in j.get("features", []):
        g = f.get("geometry") or {}
        o = f.get("properties", {}).get("STREAM_ORDER", 3) or 3
        t = g.get("type")
        segs = [g["coordinates"]] if t == "LineString" else (g["coordinates"] if t == "MultiLineString" else [])
        for s in segs:
            out.append((s, o))
    return out

def fetch_road_lines(bbox, timeout=60):
    """WFS vector pull for roads, styled by ROAD_SURFACE. Fast (~1-2s) on a per-map bbox."""
    lon0, lat0, lon1, lat1 = bbox
    cql = f"BBOX(GEOMETRY,{lon0},{lat0},{lon1},{lat1},'EPSG:4326')"
    p = {"service": "WFS", "version": "2.0.0", "request": "GetFeature",
         "typeNames": "pub:WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP", "outputFormat": "application/json",
         "srsName": "EPSG:4326", "count": "6000",
         "propertyName": "ROAD_SURFACE,ROAD_CLASS,GEOMETRY", "CQL_FILTER": cql}
    try:
        j = json.loads(_get(WFS + "?" + urllib.parse.urlencode(p), timeout=timeout))
    except Exception as e:
        print(f"  [wfs roads FAILED] {e.__class__.__name__}")
        return None
    out = []
    for f in j.get("features", []):
        g = f.get("geometry") or {}
        props = f.get("properties", {})
        cls = (props.get("ROAD_CLASS") or "").lower()
        if cls in ("skid", "trail"):
            continue  # not real vehicle roads
        surf = (props.get("ROAD_SURFACE") or "unknown").lower()
        t = g.get("type")
        segs = [g["coordinates"]] if t == "LineString" else (g["coordinates"] if t == "MultiLineString" else [])
        for s in segs:
            out.append((s, surf))
    return out

def build_map(bbox, points, title, out_path, towns=None, px_w=1500,
              overlays=("lakes", "parks", "fires"), min_stream_order=3,
              draw_streams=True, draw_roads=True, boxes=None):
    """bbox=(lon0,lat0,lon1,lat1). points/towns=[{lon,lat,label,kind}], kind in
    primary/secondary/access. boxes=[(lon0,lat0,lon1,lat1,label),...] for an orientation
    overview map instead of candidate points (pass draw_streams=False, draw_roads=False,
    overlays=("parks",) too -- an overview doesn't need the river/road clutter)."""
    lon0, lat0, lon1, lat1 = bbox
    lon_span, lat_span = (lon1 - lon0), (lat1 - lat0)
    px_h = max(200, int(px_w * lat_span / lon_span))

    # base: land tone, then hillshade with white NoData knocked out (NRCan returns pure white
    # for missing-elevation gaps, which are common on valley floors -- exactly where the rivers
    # are, so an un-fixed gap reads as a blank hole right through the fishing water).
    land = Image.new("RGBA", (px_w, px_h), (237, 235, 227, 255))
    hs = _wms(NRCAN, "dtm-hillshade", bbox, px_w, px_h, transparent=False)
    if hs is not None:
        a = np.array(hs)
        white = (a[:, :, 0] > 247) & (a[:, :, 1] > 247) & (a[:, :, 2] > 247)
        a[white, 3] = 0
        canvas = Image.alpha_composite(land, Image.fromarray(a))
    else:
        canvas = land

    ov = {"lakes": "WHSE_BASEMAPPING.FWA_LAKES_POLY",
          "parks": "WHSE_TANTALIS.TA_PARK_ECORES_PA_SVW",
          "fires": "WHSE_LAND_AND_NATURAL_RESOURCE.PROT_CURRENT_FIRE_POLYS_SP"}
    for key in overlays:
        img = _wms(databc_wms(ov[key]), f"pub:{ov[key]}", bbox, px_w, px_h, transparent=True)
        if img is not None:
            canvas = Image.alpha_composite(canvas, img)

    fig_w = 12.5
    fig, ax = plt.subplots(figsize=(fig_w, fig_w * px_h / px_w), dpi=130)
    ax.imshow(canvas, extent=[lon0, lon1, lat0, lat1], origin="upper", zorder=0)
    midlat = (lat0 + lat1) / 2.0
    ax.set_aspect(1.0 / math.cos(math.radians(midlat)))

    # rivers as vectors, weighted by stream order (fallback: WMS stream raster, nearly
    # invisible against the hillshade by default -- vectors read far better)
    lines = None
    if draw_streams:
        lines = fetch_stream_lines(bbox, min_stream_order)
        if lines:
            lw_ramp = {3: 0.6, 4: 1.0, 5: 1.5, 6: 2.2, 7: 2.9, 8: 3.4}
            for coords, o in lines:
                xs = [c[0] for c in coords]; ys = [c[1] for c in coords]
                ax.plot(xs, ys, color="#2f6fb0", lw=lw_ramp.get(min(int(o), 8), 0.6),
                        solid_capstyle="round", zorder=2, alpha=0.9)
        else:
            img = _wms(databc_wms("WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP"),
                       "pub:WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP", bbox, px_w, px_h, transparent=True)
            if img is not None:
                ax.imshow(img, extent=[lon0, lon1, lat0, lat1], origin="upper", zorder=2)

    # roads as vectors: gravel/loose FSR = bold dashed orange (usually the core access
    # criterion for this kind of report), paved = solid grey, decommissioned/overgrown =
    # thin faint grey (still shown, de-emphasized). This is the v2 fix -- v1 relied on the
    # WMS raster overlay's default styling, which doesn't render visibly against the hillshade.
    if draw_roads:
        roads = fetch_road_lines(bbox)
        road_style = {
            "loose":          dict(c="#c9720a", lw=1.5, ls=(0, (5, 2)), a=0.9, z=3),
            "rough":          dict(c="#c9720a", lw=1.1, ls=(0, (4, 2)), a=0.75, z=3),
            "paved":          dict(c="#555555", lw=1.8, ls="-", a=0.85, z=3),
            "overgrown":      dict(c="#999999", lw=0.6, ls=(0, (1, 2)), a=0.45, z=3),
            "decommissioned": dict(c="#999999", lw=0.6, ls=(0, (1, 2)), a=0.45, z=3),
            "unknown":        dict(c="#888888", lw=0.7, ls=(0, (3, 2)), a=0.5, z=3),
        }
        if roads:
            for coords, surf in roads:
                s = road_style.get(surf, road_style["unknown"])
                xs = [c[0] for c in coords]; ys = [c[1] for c in coords]
                ax.plot(xs, ys, color=s["c"], lw=s["lw"], ls=s["ls"], alpha=s["a"], zorder=s["z"],
                        solid_capstyle="round")

    style = {"primary":   dict(marker="*", s=460, c="#d92b2b", ec="white", lw=1.5, z=6),
             "secondary": dict(marker="o", s=130, c="#f6a417", ec="#222", lw=1.0, z=5),
             "access":    dict(marker="^", s=100, c="#1f8f4e", ec="white", lw=1.0, z=5)}
    for p in points:
        s = style.get(p.get("kind", "secondary"), style["secondary"])
        ax.scatter([p["lon"]], [p["lat"]], marker=s["marker"], s=s["s"], c=s["c"],
                   edgecolors=s["ec"], linewidths=s["lw"], zorder=s["z"])
        ax.annotate(p["label"], (p["lon"], p["lat"]), xytext=(7, 5), textcoords="offset points",
                    fontsize=9, fontweight="bold", color="#111", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.78))
    for t in (towns or []):
        ax.scatter([t["lon"]], [t["lat"]], marker="s", s=54, c="#444", edgecolors="white", lw=0.8, zorder=5)
        ax.annotate(t["label"], (t["lon"], t["lat"]), xytext=(5, -11), textcoords="offset points",
                    fontsize=8.5, style="italic", color="#333", zorder=7)

    for bx in (boxes or []):
        bl0, ba0, bl1, ba1, blab = bx
        ax.add_patch(plt.Rectangle((bl0, ba0), bl1 - bl0, ba1 - ba0, fill=False,
                                   ec="#d92b2b", lw=2.2, zorder=6))
        ax.annotate(blab, ((bl0 + bl1) / 2, ba1), ha="center", va="bottom", fontsize=10,
                    fontweight="bold", color="#b81d1d", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))

    km_per_deg_lon = 111.32 * math.cos(math.radians(midlat))
    bar_deg = 10.0 / km_per_deg_lon
    x0 = lon0 + lon_span * 0.05; y0 = lat0 + lat_span * 0.05
    ax.plot([x0, x0 + bar_deg], [y0, y0], c="#111", lw=3.2, zorder=8, solid_capstyle="butt")
    ax.annotate("10 km", (x0 + bar_deg / 2, y0), xytext=(0, 4), textcoords="offset points",
                ha="center", fontsize=8, fontweight="bold", zorder=8,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    ax.annotate("N▲", (lon1 - lon_span * 0.045, lat1 - lat_span * 0.06), ha="center",
                fontsize=13, fontweight="bold", zorder=8)

    legend = [Line2D([0], [0], marker="*", color="w", markerfacecolor="#d92b2b", markeredgecolor="white", markersize=18, label="Primary pick"),
              Line2D([0], [0], marker="o", color="w", markerfacecolor="#f6a417", markeredgecolor="#222", markersize=10, label="Candidate"),
              Line2D([0], [0], marker="^", color="w", markerfacecolor="#1f8f4e", markeredgecolor="white", markersize=10, label="Access point"),
              Line2D([0], [0], color="#2f6fb0", lw=2.4, label="River / stream (by size)"),
              Line2D([0], [0], color="#c9720a", lw=1.5, ls=(0, (5, 2)), label="Gravel / FSR road"),
              Line2D([0], [0], color="#555555", lw=1.8, label="Paved road"),
              Line2D([0], [0], color="#999999", lw=0.8, ls=(0, (1, 2)), label="Deactivated/overgrown road")]
    ax.legend(handles=legend, loc="lower right", fontsize=7.5, framealpha=0.9)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=8)
    ax.set_xlabel("Longitude", fontsize=8); ax.set_ylabel("Latitude", fontsize=8)
    ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("MAP SAVED:", out_path, f"({px_w}x{px_h}, {len(lines) if lines else 0} stream segs)")

if __name__ == "__main__":
    # EDIT ME: worked example -- replace bbox/points/towns with the new report's sub-region,
    # one build_map() call per sub-region map (keep each map's area tight; don't try to fit
    # a whole multi-zone report on one map -- it gets crowded and unreadable).
    build_map(
        bbox=(-115.75, 49.30, -115.05, 49.80),
        points=[
            {"lon": -115.30, "lat": 49.52, "label": "Example reach (bull trout)", "kind": "primary"},
            {"lon": -115.55, "lat": 49.45, "label": "Example creek (cutthroat)", "kind": "secondary"},
            {"lon": -115.60, "lat": 49.42, "label": "FSR bridge access", "kind": "access"},
        ],
        towns=[{"lon": -115.69, "lat": 49.50, "label": "Example Town"}],
        title="EXAMPLE — replace with the new sub-region's title",
        out_path="example_map.png",
    )
