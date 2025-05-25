from tkintermapview import TkinterMapView
from PIL import Image, ImageDraw, ImageTk, ImageFont


class GraphRenderer:
    def __init__(self, map_widget):
        self.map_widget = map_widget

    def get_attr(self, vertex, key, default=None):
        """Lê um atributo de um vértice com segurança."""
        return vertex[key] if key in vertex.attributes() else default

    def create_circle_icon(self, roadm="?", num_node="?", color="#800000", size=28):
        """Cria um ícone com ROADM central e num_node acima do círculo."""
        image = Image.new("RGBA", (size, size + 12), (0, 0, 0, 0))  # espaço extra acima
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Círculo
        circle_bounds = (2, 12, size - 2, size + 12 - 2)
        draw.ellipse(circle_bounds, outline=color, width=2)

        # Texto ROADM dentro do círculo
        roadm_text = str(roadm)
        bbox = draw.textbbox((0, 0), roadm_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        center_x = (size - text_w) / 2
        center_y = 12 + ((size - 12 - text_h) / 2)
        draw.text((center_x, center_y), roadm_text, font=font, fill=color)

        # Texto num_node acima do círculo
        num_text = str(num_node)
        bbox2 = draw.textbbox((0, 0), num_text, font=font)
        num_w = bbox2[2] - bbox2[0]
        num_x = (size - num_w) / 2
        draw.text((num_x, 0), num_text, font=font, fill=color)

        return ImageTk.PhotoImage(image)

    def plot_nodes(self, graph):
        """Plota os nós do grafo no mapa usando igraph."""
        self.node_positions = {}
        for v in graph.vs:
            label = self.get_attr(v, 'label', 'ZZZ')
            latitude = self.get_attr(v, 'Latitude')
            longitude = self.get_attr(v, 'Longitude')
            num_node = self.get_attr(v, 'num_node', '?')
            roadm = self.get_attr(v, 'ROADM', '?')

            if latitude is not None and longitude is not None:
                icon = self.create_circle_icon(roadm=roadm, num_node=num_node, color="#800000", size=28)
                self.map_widget.set_marker(latitude, longitude, text=label, icon=icon)
                self.node_positions[v.index] = (latitude, longitude)

    def plot_edges(self, graph):
        """Desenha arestas com base no grafo igraph."""
        for e in graph.es:
            src = e.source
            tgt = e.target

            if src in self.node_positions and tgt in self.node_positions:
                lat1, lon1 = self.node_positions[src]
                lat2, lon2 = self.node_positions[tgt]
                self.map_widget.set_path([(lat1, lon1), (lat2, lon2)], color="black", width=2)
