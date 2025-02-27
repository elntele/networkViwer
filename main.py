import tkinter as tk
from tkinter import filedialog
import networkx as nx
from tkintermapview import TkinterMapView
import time
import requests

class GraphMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Topologia de Rede Óptica")
        self.root.geometry("800x600")  # Tamanho inicial da janela

        # Criando um menu
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir .GML", command=self.open_gml_file)
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        self.root.config(menu=menubar)

        # Criando a área do mapa (ajustável ao redimensionar a janela)
        self.map_widget = TkinterMapView(self.root, width=800, height=500)
        self.map_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def open_gml_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("GraphML Files", "*.gml")])
        if file_path:
            print(f"Arquivo selecionado: {file_path}")

            try:
                # Tentar abrir o arquivo GML usando utf-8 como codificação
                with open(file_path, 'r', encoding='utf-8') as f:
                    G = nx.parse_gml(f)

                # Exibir as informações dos nós e arestas
                print("\nNós do grafo:")
                node_positions = {}
                for node, data in G.nodes(data=True):
                    label = data.get('label', 'Desconhecido')
                    longitude = data.get('Longitude', None)
                    latitude = data.get('Latitude', None)
                    print(f"ID: {node}, Nome: {label}, Longitude: {longitude}, Latitude: {latitude}")

                    # Verificar se as coordenadas estão disponíveis
                    if longitude and latitude:
                        # Adicionar marcador no mapa
                        self.add_marker_to_map(latitude, longitude, label)
                        node_positions[node] = (latitude, longitude)

                print("\nArestas do grafo:")
                self.draw_edges_on_map(G, node_positions)

            except Exception as e:
                print(f"Erro ao ler o arquivo GML: {e}")

    def add_marker_to_map(self, latitude, longitude, label):
        # Aguarda 1.5 segundos entre as requisições para evitar bloqueios
        time.sleep(1.5)

        # Usar a API do OpenStreetMap para buscar dados de localização
        url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=jsonv2&addressdetails=1"
        headers = {
            'User-Agent': 'GraphMapApp/1.0 (meuemail@dominio.com)'  # Substitua por um email real
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Lança um erro para códigos de status 4xx/5xx
            data = response.json()

            if data:
                address = data.get('display_name', 'Localização não encontrada')
                print(f"Localização para {label}: {address}")
                # Adiciona o marcador no mapa usando o método correto
                self.map_widget.set_marker(latitude, longitude, text=label)
            else:
                print(f"Erro ao buscar localização para {label}: Nenhum dado encontrado")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar localização para {label}: {e}")

    def draw_edges_on_map(self, G, node_positions):
        for node1, node2 in G.edges():
            if node1 in node_positions and node2 in node_positions:
                lat1, lon1 = node_positions[node1]
                lat2, lon2 = node_positions[node2]
                self.map_widget.set_path([(lat1, lon1), (lat2, lon2)])

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphMapApp(root)
    root.mainloop()
