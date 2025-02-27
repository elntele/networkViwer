from tkintermapview import TkinterMapView
from PIL import Image, ImageDraw, ImageTk

class GraphRenderer:
    def __init__(self, map_widget):
        self.map_widget = map_widget

    def create_circle_icon(self, color="#800000", size=5):
        """Cria um ícone circular para o marcador com cor vinho e tamanho reduzido."""
        image = Image.new("RGBA", (size*2, size*2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, size*2, size*2), fill=color)

        # Convertendo a imagem PIL para PhotoImage compatível com Tkinter
        return ImageTk.PhotoImage(image)

    def plot_nodes(self, graph):
        """Adiciona os nós ao mapa com círculos vinho preenchidos."""
        self.node_positions = {}  # Armazena coordenadas dos nós
        for node, data in graph.nodes(data=True):
            label = data.get('label', 'Desconhecido')
            longitude = data.get('Longitude', None)
            latitude = data.get('Latitude', None)

            if longitude and latitude:
                # Cria o ícone de círculo vinho
                circle_icon = self.create_circle_icon(color="#800000", size=5)
                # Define o marcador com o ícone de círculo
                self.map_widget.set_marker(latitude, longitude, text=label, icon=circle_icon)
                self.node_positions[node] = (latitude, longitude)  # Salva a posição do nó

    def plot_edges(self, graph):
        """Desenha as arestas no mapa com a cor vermelha."""
        for node1, node2 in graph.edges():
            if node1 in self.node_positions and node2 in self.node_positions:
                lat1, lon1 = self.node_positions[node1]
                lat2, lon2 = self.node_positions[node2]

                # Desenha uma linha vermelha conectando os nós
                self.map_widget.set_path([(lat1, lon1), (lat2, lon2)], color="black", width=2)
