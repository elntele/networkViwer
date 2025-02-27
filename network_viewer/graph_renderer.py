# network_service.py
import time
import requests

class GraphRenderer:
    def __init__(self, map_widget):
        self.map_widget = map_widget

    def plot_nodes(self, graph):
        """Adiciona os nós ao mapa com círculos vermelhos preenchidos."""
        self.node_positions = {}  # Armazena coordenadas dos nós

        for node, data in graph.nodes(data=True):
            label = data.get('label', 'Desconhecido')
            longitude = data.get('Longitude', None)
            latitude = data.get('Latitude', None)

            if longitude and latitude:
                # Usando o método correto para criar um marcador (sem parâmetros de cor diretamente)
                self.map_widget.set_marker(latitude, longitude, text=label)
                self.node_positions[node] = (latitude, longitude)  # Salva a posição do nó

    def plot_edges(self, graph):
        """Desenha as arestas no mapa com a cor vermelha."""
        for node1, node2 in graph.edges():
            if node1 in self.node_positions and node2 in self.node_positions:
                lat1, lon1 = self.node_positions[node1]
                lat2, lon2 = self.node_positions[node2]

                # Desenha uma linha vermelha conectando os nós
                self.map_widget.set_path([(lat1, lon1), (lat2, lon2)], color="red", width=2)
