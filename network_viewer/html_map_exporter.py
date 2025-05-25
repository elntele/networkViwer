import os
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def export_graph_to_google_maps(graph, output_path="grafo_google_maps.html"):
    if not API_KEY:
        print("❌ API Key do Google Maps não encontrada no .env.")
        return

    node_data = []
    node_positions = {}

    for v in graph.vs:
        lat = v["Latitude"] if "Latitude" in v.attributes() else None
        lon = v["Longitude"] if "Longitude" in v.attributes() else None
        label = v["label"] if "label" in v.attributes() else "Desconhecido"
        numnode = v["numnode"] if "numnode" in v.attributes() else "?"

        if lat is not None and lon is not None:
            node_positions[v.index] = {"lat": lat, "lon": lon}
            node_data.append({
                "lat": lat,
                "lon": lon,
                "label": label,
                "numnode": numnode
            })

    edge_data = []
    for e in graph.es:
        s, t = e.source, e.target
        if s in node_positions and t in node_positions:
            edge_data.append([node_positions[s], node_positions[t]])

    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Grafo em Google Maps</title>
        <meta charset="utf-8">
        <style>
            #map { height: 100vh; width: 100%; }
        </style>
        <script src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}"></script>
        <script>
            function initMap() {
                const map = new google.maps.Map(document.getElementById("map"), {
                    mapTypeId: "roadmap"
                });

                const bounds = new google.maps.LatLngBounds();
                const nodes = {{ nodes | safe }};

                for (const node of nodes) {
                    const position = { lat: node.lat, lng: node.lon };
                    bounds.extend(position);
                    new google.maps.Marker({
                        position: position,
                        map,
                        title: node.label,
                        label: {
                            text: node.numnode.toString(),
                            color: "white",
                            fontSize: "12px",
                            fontWeight: "bold"
                        }
                    });
                }

                const edges = {{ edges | safe }};
                for (const edge of edges) {
                    const path = [
                        { lat: edge[0].lat, lng: edge[0].lon },
                        { lat: edge[1].lat, lng: edge[1].lon }
                    ];
                    new google.maps.Polyline({
                        path: path,
                        geodesic: true,
                        strokeColor: "#000000",
                        strokeOpacity: 1.0,
                        strokeWeight: 2,
                        map: map
                    });
                }

                google.maps.event.addListenerOnce(map, 'idle', function () {
                    map.fitBounds(bounds, {
                        top: 50,
                        bottom: 50,
                        left: 50,
                        right: 50
                    });
                });
            }
        </script>
    </head>
    <body onload="initMap()">
        <div id="map"></div>
    </body>
    </html>
    """)

    rendered_html = html_template.render(
        api_key=API_KEY,
        nodes=node_data,
        edges=edge_data
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(f"✅ Mapa exportado para: {output_path}")
