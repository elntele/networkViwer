# file_loader.py
import networkx as nx
from tkinter import filedialog


class FileLoader:
    def __init__(self):
        self.graph = None

    def load_gml(self):
        file_path = filedialog.askopenfilename(filetypes=[("GraphML Files", "*.gml")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.graph = nx.parse_gml(f)
                return self.graph
            except Exception as e:
                print(f"Erro ao carregar o arquivo GML: {e}")
        return None

