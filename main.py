import base64
import html
import io

import folium
import matplotlib.pyplot as plt
import numpy as np
from folium import DivIcon, Map, Marker

# Retain your original waterfall drawing utility
from waterfall import draw_waterfall

# Single source of truth for configuration data and analytical telemetry
MARKERS_DATA = [
    {
        "name": "School",
        "lat": 50.562102,
        "lon": 22.066066,
        "color": "#ef4444",  # Transformed to hex for seamless native inline style matching
        "icon": "graduation-cap",
        "description": "Primary local educational facility context node.",
        "dataset": "datasets-good/inside1.txt",
    },
    {
        "name": "Skatepark",
        "lat": 50.563262,
        "lon": 22.073622,
        "color": "#10b981",  # Transformed to hex for seamless native inline style matching
        "icon": "tree",
        "description": "Recreational outdoor activity sports park asset.",
        "dataset": "datasets-good/skatepark.txt",
    },
    {
        "name": "Garden",
        "lat": 50.5626,
        "lon": 22.066072,
        "color": "#ef4444",  # Transformed to hex for seamless native inline style matching
        "icon": "tree",
        "description": "Garden of school",
        "dataset": "datasets-good/garden.txt",
    },
]


def generate_waterfall_base64(dataset_path: str) -> str:
    """Invokes draw_waterfall, extracts the Matplotlib figure canvas,

    and encodes the binary image into a safe browser-ready Base64 string.
    """
    plt.clf()
    draw_waterfall(dataset_path)
    fig = plt.gcf()

    # High-quality DPI processing guarantees crisp axis scales on wide layouts
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    encoded_img = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_img}"


def generate_rssi_avg_base64(asset_name: str) -> str:
    """Computes a deterministic diurnal RSSI average tracking data array

    and compiles a standalone time-domain telemetry visualization line graph.
    """
    plt.clf()

    # Establish asset-specific signature seeds based on character arrays
    seed_val = sum(ord(char) for char in asset_name)
    np.random.seed(seed_val)

    # Generate 24 hours timeline with 15 minute processing intervals (96 blocks)
    time_slots = np.linspace(0, 24, 96)

    # Construct base profiling transformations to map environmental parameters
    if "School" in asset_name:
        # Heavily bounded usage peaks matching primary daylight operating shifts
        base_rssi = -85 + 28 * np.exp(-((time_slots - 12) ** 2) / 14)
    elif "Skatepark" in asset_name:
        # Delayed afternoon distributions matching outdoor recreational trends
        base_rssi = -90 + 32 * np.exp(-((time_slots - 17) ** 2) / 10)
    else:
        # Uniform low variance background noise threshold profile
        base_rssi = -95 + 8 * np.sin(time_slots / 3.5)

    gaussian_noise = np.random.normal(0, 2.5, 96)
    rssi_telemetry = np.clip(base_rssi + gaussian_noise, -110, -30)

    # Instantiate crisp canvas structures isolated for clean dashboard sizing
    fig, ax = plt.subplots(figsize=(7, 2.8), dpi=140)
    ax.plot(
        time_slots, rssi_telemetry, color="#2563eb", linewidth=2, label="Average RSSI"
    )
    ax.fill_between(time_slots, rssi_telemetry, -110, color="#2563eb", alpha=0.12)

    # Structural normalization parameters for the grid coordinates
    ax.set_xlim(0, 24)
    ax.set_ylim(-110, -30)
    ax.set_xlabel("Timeline", fontsize=9, color="#64748b")
    ax.set_ylabel("RSSI (dBm)", fontsize=9, color="#64748b")
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.set_xticklabels(
        ["01:00", "01:10", "01:20", "01:30", "01:40", "01:50", "02:00"],
        fontsize=8,
        color="#94a3b8",
    )
    ax.tick_params(colors="#cbd5e1", labelsize=8)
    ax.grid(True, linestyle="--", alpha=0.4, color="#cbd5e1")

    # Strip peripheral bounding borders to maximize functional scannability
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e2e8f0")
    ax.spines["bottom"].set_color("#e2e8f0")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight", transparent=True)
    plt.close(fig)
    buf.seek(0)

    encoded_img = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_img}"


def compile_analytics_payloads() -> None:
    """Mutates global data array by appending compiled Base64 image payloads

    to minimize processing overhead down the deployment line.
    """
    for data in MARKERS_DATA:
        data["img_src"] = generate_waterfall_base64(data["dataset"])
        data["rssi_src"] = generate_rssi_avg_base64(data["name"])


def create_base_map() -> Map:
    """Instantiates the Folium map engine with boundaries and initial view configurations."""
    local_map = Map(
        location=[50.562682, 22.069844],
        width="100%",
        height="100%",
        min_zoom=15,
        max_zoom=20,
        zoom_control=True,
        scroll_wheel_zoom=True,
        double_click_zoom=True,
        max_bounds=True,
        min_lat=50.5615,
        max_lat=50.5638,
        min_lon=22.0650,
        max_lon=22.0745,
    )

    # Injecting clean hardware-accelerated outline shadows, scales, and pulse loops into the map engine
    marker_visibility_css = """
    <style>
        .custom-glow-marker {
            position: relative;
            width: 32px;
            height: 32px;
            border: 3px solid #ffffff;
            border-radius: 50%;
            box-shadow: 0 0 8px rgba(0,0,0,0.4), inset 0 0 2px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
        }
        .custom-glow-marker i {
            color: #ffffff;
            font-size: 13px;
        }
        .custom-glow-marker:hover {
            transform: scale(1.25);
            box-shadow: 0 0 14px rgba(0,0,0,0.6);
            z-index: 9999 !important;
        }
        .pulse-ring {
            position: absolute;
            top: -7px;
            left: -7px;
            width: 40px;
            height: 40px;
            border: 3px solid;
            border-radius: 50%;
            opacity: 0.6;
            animation: beacon-pulse 2s infinite ease-out;
            pointer-events: none;
        }
        @keyframes beacon-pulse {
            0% {
                transform: scale(0.6);
                opacity: 0.9;
            }
            100% {
                transform: scale(1.5);
                opacity: 0;
            }
        }
    </style>
    """
    local_map.get_root().header.add_child(folium.Element(marker_visibility_css))
    return local_map


def add_dashboard_markers(local_map: Map) -> None:
    """Constructs map coordinates featuring an HTML tooltip hover graph, alongside

    a direct JavaScript click binding that bypasses popups completely.
    """
    for data in MARKERS_DATA:
        # 1. HOVER ACTIONS: Compact micro-graph visual viewport tooltip card
        tooltip_html = f"""
        <div style="font-family: Arial, sans-serif; width: 220px; padding: 4px; pointer-events: none;">
            <strong style="color: #2c3e50; display: block; margin-bottom: 4px; font-size: 11px;">
                 Preview: {data["name"]}
            </strong>
            <img src="{data["img_src"]}" style="width: 100%; border-radius: 2px;">
        </div>
        """

        # 2. MARKER LAYOUT GENERATION: Structural custom HTML composition using folium.DivIcon
        marker_html = f"""
        <div class="custom-glow-marker" style="background-color: {data["color"]};">
            <i class="fa fa-{data["icon"]}"></i>
            <div class="pulse-ring" style="border-color: {data["color"]};"></div>
        </div>
        """

        # Initialize the marker using the new lightweight unstyled vector container wrapper
        marker = Marker(
            location=[data["lat"], data["lon"]],
            tooltip=tooltip_html,
            icon=DivIcon(html=marker_html, icon_size=(32, 32), icon_anchor=(16, 16)),
        )
        marker.add_to(local_map)

        # 3. CLICK ACTIONS: Inject direct script bindings straight into Leaflet's engine.
        click_js = f"""
        {marker.get_name()}.on('click', function(e) {{
            window.parent.updateBottomPanel('{data["name"]}', '{data["img_src"]}', '{data["rssi_src"]}');
        }});
        """
        marker.add_child(folium.Element(click_js))


def build_marker_list_html() -> str:
    """Assembles the clickable multi-row UI element structure for the location directory pane."""
    html_elements = []
    for data in MARKERS_DATA:
        element = f"""
        <div class="marker-card" onclick="flyToMarker({data["lat"]}, {data["lon"]}); updateBottomPanel('{data["name"]}', '{data["img_src"]}', '{data["rssi_src"]}');">
            <div class="marker-status-dot" style="background-color: {data["color"]};"></div>
            <div class="marker-info">
                <div class="marker-title">{data["name"]}</div>
                <div class="marker-coords">{data["lat"]:.5f}, {data["lon"]:.5f}</div>
                <div class="marker-body">{data["description"]}</div>
            </div>
        </div>
        """
        html_elements.append(element)
    return "\n".join(html_elements)


def get_master_layout_html(map_html_source: str, list_items_html: str) -> str:
    """Compiles structural page frame layout and configures cross-frame JavaScript listeners."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>HESTIA</title>
        <style>
            /* Design System Tokens for Smooth Theme Interpolation */
            :root {{
                --bg-main: #ffffff;
                --bg-alt: #f8fafc;
                --border-color: #e2e8f0;
                --border-hover: #cbd5e1;
                --text-primary: #0f172a;
                --text-secondary: #1e293b;
                --text-muted: #64748b;
                --text-coords: #94a3b8;
                --card-bg: #ffffff;
                --card-hover: #f8fafc;
                --map-filter: none;
                --btn-bg: #e2e8f0;
                --btn-text: #1e293b;
                --btn-hover: #cbd5e1;
                --btn-accent-bg: #2563eb;
                --btn-accent-text: #ffffff;
                --btn-accent-hover: #1d4ed8;
            }}
            
            body.dark-mode {{
                --bg-main: #0f172a;
                --bg-alt: #0b0f19;
                --border-color: #1e293b;
                --border-hover: #334155;
                --text-primary: #f8fafc;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;
                --text-coords: #64748b;
                --card-bg: #1e293b;
                --card-hover: #334155;
                --map-filter: invert(90%) hue-rotate(180deg) brightness(95%) contrast(95%);
                --btn-bg: #1e293b;
                --btn-text: #f1f5f9;
                --btn-hover: #334155;
                --btn-accent-bg: #3b82f6;
                --btn-accent-text: #ffffff;
                --btn-accent-hover: #2563eb;
            }}

            body, html {{
                margin: 0; padding: 0; height: 100%; width: 100%;
                overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: var(--bg-main);
                color: var(--text-primary);
                transition: background-color 0.25s ease, color 0.25s ease;
            }}
            .dashboard-frame {{
                display: flex; width: 100vw; height: 100vh;
            }}
            .map-pane {{
                width: 50%; height: 100%; position: relative;
                border-right: 2px solid var(--border-color); box-sizing: border-box;
                transition: border-color 0.25s ease;
            }}
            .map-pane iframe {{ 
                width: 100%; height: 100%; border: none; 
                filter: var(--map-filter);
                transition: filter 0.3s ease;
            }}
            .analytics-pane {{
                width: 50%; height: 100%; display: flex; flex-direction: column;
            }}
            .top-half {{
                height: 50%; width: 100%; border-bottom: 2px solid var(--border-color);
                box-sizing: border-box; background-color: var(--bg-main); overflow-y: auto;
                padding: 20px;
                transition: background-color 0.25s ease, border-color 0.25s ease;
            }}
            .bottom-half {{
                height: 50%; width: 100%; background-color: var(--bg-alt);
                box-sizing: border-box; overflow: hidden; position: relative;
                transition: background-color 0.25s ease;
                display: flex; flex-direction: column;
            }}
            
            /* Directory Panel & Action Styles */
            .panel-header {{
                margin: 0 0 16px 0; color: var(--text-primary); font-size: 18px; font-weight: 700;
                display: flex; align-items: center; justify-content: space-between; gap: 8px;
            }}
            .theme-toggle {{
                padding: 6px 12px; font-size: 12px; font-weight: 600;
                background-color: var(--btn-bg); color: var(--btn-text);
                border: none; border-radius: 6px; cursor: pointer;
                transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 6px;
            }}
            .theme-toggle:hover {{
                background-color: var(--btn-hover);
            }}

            /* Workspace Control Bar & Large Action Elements */
            .workspace-control-bar {{
                display: flex; justify-content: space-between; align-items: center;
                padding: 14px 20px; border-bottom: 2px solid var(--border-color);
                background-color: var(--bg-main); box-sizing: border-box; height: 60px;
                transition: background-color 0.25s ease, border-color 0.25s ease;
            }}
            .analysis-panel-title {{
                margin: 0; color: var(--text-secondary); font-size: 15px; font-weight: 600;
            }}
            .workspace-action-group {{
                display: flex; gap: 10px; align-items: center;
            }}
            .download-btn-large, .history-btn-large, .toggle-view-btn-large {{
                padding: 10px 20px; font-size: 13px; font-weight: 700;
                border: none; border-radius: 6px; cursor: pointer;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                display: inline-flex; align-items: center; gap: 6px;
            }}
            .download-btn-large {{
                background-color: var(--btn-accent-bg); color: var(--btn-accent-text);
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
            }}
            .download-btn-large:hover:not(:disabled) {{
                background-color: var(--btn-accent-hover);
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);
            }}
            .history-btn-large, .toggle-view-btn-large {{
                background-color: var(--btn-bg); color: var(--btn-text);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
            }}
            .history-btn-large:hover:not(:disabled), .toggle-view-btn-large:hover:not(:disabled) {{
                background-color: var(--btn-hover);
                transform: translateY(-1px);
            }}
            .download-btn-large:active, .history-btn-large:active, .toggle-view-btn-large:active {{
                transform: translateY(0);
            }}
            .download-btn-large:disabled, .history-btn-large:disabled, .toggle-view-btn-large:disabled {{
                opacity: 0.35; cursor: not-allowed; transform: none;
                background-color: var(--btn-bg); color: var(--text-coords);
                box-shadow: none;
            }}

            .marker-card {{
                display: flex; align-items: flex-start; gap: 14px; padding: 12px;
                margin-bottom: 10px; background: var(--card-bg); border: 1px solid var(--border-color);
                border-radius: 8px; cursor: pointer; transition: all 0.2s ease;
            }}
            .marker-card:hover {{
                background: var(--card-hover); border-color: var(--border-hover); transform: translateY(-1px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            }}
            .marker-status-dot {{
                width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0;
            }}
            .marker-info {{ flex: 1; }}
            .marker-title {{ font-weight: 600; color: var(--text-secondary); font-size: 14px; }}
            .marker-coords {{ font-family: monospace; color: var(--text-coords); font-size: 11px; margin: 2px 0; }}
            .marker-body {{ color: var(--text-muted); font-size: 12px; margin-top: 4px; line-height: 1.4; }}
            
            .placeholder {{
                display: flex; flex-direction: column; align-items: center;
                justify-content: center; height: 100%; color: var(--text-coords); text-align: center;
            }}
            .analysis-container {{
                padding: 16px; height: 100%; display: flex; flex-direction: column; box-sizing: border-box;
            }}
            .analysis-viewport {{
                flex: 1; text-align: center; display: flex; align-items: center; justify-content: center; overflow: hidden;
            }}
            .analysis-img {{
                max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 4px;
            }}
        </style>
        <script>
            let activeNodeTitle = "";
            let cacheWaterfallSrc = "";
            let cacheRssiSrc = "";
            let currentViewMode = "waterfall";

            // Synchronizes map location viewport focus to requested node and handles view transitions
            function flyToMarker(lat, lon) {{
                const iframe = document.querySelector('iframe');
                if (!iframe) return;
                const iframeWin = iframe.contentWindow;
                
                let leafletMap = null;
                for (let key in iframeWin) {{
                    if (key.startsWith('map_')) {{
                        leafletMap = iframeWin[key];
                        break;
                    }}
                }}
                
                if (leafletMap) {{
                    leafletMap.flyTo([lat, lon], 18, {{ animate: true, duration: 1.2 }});
                }}
            }}

            // Updates layout variables and manages internal template canvas redrawing mechanisms
            function updateBottomPanel(titleText, base64Waterfall, base64RSSI) {{
                activeNodeTitle = titleText;
                cacheWaterfallSrc = base64Waterfall;
                cacheRssiSrc = base64RSSI;
                
                // Lift active lockout boundaries on workspace interface triggers
                document.getElementById('workspace-download-btn').removeAttribute('disabled');
                document.getElementById('workspace-history-btn').removeAttribute('disabled');
                document.getElementById('workspace-view-btn').removeAttribute('disabled');
                
                renderActivePlotLayout();
            }}

            // Renders selected node asset arrays into standard view template formats
            function renderActivePlotLayout() {{
                const viewport = document.getElementById('bottom-analysis-viewport');
                const titleNode = document.getElementById('workspace-title-node');
                const toggleBtn = document.getElementById('workspace-view-btn');
                
                if (currentViewMode === "waterfall") {{
                    titleNode.innerText = `Spectrum Analysis: ${{activeNodeTitle}}`;
                    toggleBtn.innerText = "Show Avg.";
                    viewport.innerHTML = `
                        <div class="analysis-container">
                            <div class="analysis-viewport">
                                <img src="${{cacheWaterfallSrc}}" class="analysis-img">
                            </div>
                        </div>
                    `;
                }} else {{
                    titleNode.innerText = `RSSI Average Profile: ${{activeNodeTitle}}`;
                    toggleBtn.innerText = "Show Waterfall";
                    viewport.innerHTML = `
                        <div class="analysis-container">
                            <div class="analysis-viewport">
                                <img src="${{cacheRssiSrc}}" class="analysis-img">
                            </div>
                        </div>
                    `;
                }}
            }}

            // Changes current monitoring data plots inside workspace containers
            function switchWorkspaceViewMode() {{
                currentViewMode = currentViewMode === "waterfall" ? "rssi" : "waterfall";
                renderActivePlotLayout();
            }}

            // Toggles design theme state class binding across top-level body node
            function toggleDarkMode() {{
                document.body.classList.toggle('dark-mode');
            }}

            // Triggers structural fallback confirmation sequence for mock download execution
            function triggerMockDownload() {{
                const payloadScope = activeNodeTitle ? ` for "${{activeNodeTitle}}"` : "";
                alert(`Telemetry Export Sequence Initiated:\n\nCompiling analytical workspace arrays, geo-coordinates, and spectrum image buffers into a unified archive payload${{payloadScope}}.`);
            }}

            // Triggers structural log simulation sequence for mock history viewing
            function triggerMockHistory() {{
                const payloadScope = activeNodeTitle ? ` for "${{activeNodeTitle}}"` : "";
                alert(`Historical Log Retrieval Sequence Initiated:\n\nQuerying archival data matrix indexes, historical delta transformations, and past workspace sweeps${{payloadScope}}.`);
            }}
        </script>
    </head>
    <body>
        <div class="dashboard-frame">
            <!-- Left Pane: Map Context -->
            <div class="map-pane">
                <iframe srcdoc="{html.escape(map_html_source)}"></iframe>
            </div>
            
            <!-- Right Pane: Analytics Stack -->
            <div class="analytics-pane">
                <!-- Top Panel: Location Directory -->
                <div class="top-half">
                    <h2 class="panel-header">
                        <span>Locations</span>
                        <button class="theme-toggle" onclick="toggleDarkMode()">Mode</button>
                    </h2>
                    {list_items_html}
                </div>
                
                <!-- Bottom Panel: Dynamic Analytical Workspace Viewport -->
                <div class="bottom-half">
                    <!-- Standardized Control Header Array -->
                    <div class="workspace-control-bar">
                        <h3 class="analysis-panel-title" id="workspace-title-node">Analytical Workspace</h3>
                        <div class="workspace-action-group">
                            <button class="toggle-view-btn-large" id="workspace-view-btn" onclick="switchWorkspaceViewMode()" disabled>Show Avg.</button>
                            <button class="history-btn-large" id="workspace-history-btn" onclick="triggerMockHistory()" disabled>Show History</button>
                            <button class="download-btn-large" id="workspace-download-btn" onclick="triggerMockDownload()" disabled>Download Data</button>
                        </div>
                    </div>
                    
                    <div id="bottom-analysis-viewport" style="flex: 1; position: relative; overflow: hidden;">
                        <div class="placeholder">
                            <p style="margin: 0; font-size: 14px; font-weight: 500;">No Visualization Active</p>
                            <p style="margin: 2px 0 0 0; font-size: 12px; color: var(--text-coords);">Select an asset above or pick a map pin to compute the waterfall matrix.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def save_dashboard(html_content: str, filename: str) -> None:
    """Writes the compiled unified framework string data directly out to disk storage."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


def main() -> None:
    """Manages compilation lifecycle sequence from image building to final I/O delivery."""
    # 1. Map data sets into base64 cache image strings
    compile_analytics_payloads()

    # 2. Build the basic spatial map interface
    local_map = create_base_map()

    # 3. Add pins featuring the clean script hooks
    add_dashboard_markers(local_map)

    # 4. Generate layout structures and save down artifacts
    map_html_source = local_map.get_root().render()
    list_items_html = build_marker_list_html()
    master_layout = get_master_layout_html(map_html_source, list_items_html)

    output_filename = "dashboard_map.html"
    save_dashboard(master_layout, output_filename)

    print(
        f"Compilation Successful! Integrated dashboard exported to '{output_filename}'"
    )


if __name__ == "__main__":
    main()
