import igraph as ig
import chardet
from tkinter import filedialog


class FileLoader:
    def __init__(self):
        self.graph = None

    def load_gml(self):
        file_path = filedialog.askopenfilename(filetypes=[("GraphML Files", "*.gml")])
        if file_path:
            try:
                # Detecta codificação correta
                with open(file_path, 'rb') as f:
                    raw = f.read()
                    detected = chardet.detect(raw)
                    gml_text = raw.decode(detected['encoding'])

                # Salva temporariamente como UTF-8 para o igraph ler
                temp_utf8_path = file_path + "_utf8_temp.gml"
                with open(temp_utf8_path, 'w', encoding='utf-8') as f:
                    f.write(gml_text)

                # Lê com igraph
                self.graph = ig.Graph.Read_GML(temp_utf8_path)
                return self.graph

            except Exception as e:
                print(f"Erro ao carregar o arquivo GML com igraph: {e}")
        return None
