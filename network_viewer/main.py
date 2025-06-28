import tkinter as tk
from graph_app import GraphApp
from file_loader import FileLoader
from graph_renderer import GraphRenderer
from html_map_exporter import export_graph_to_google_maps
from load_chromosome_igraph import process_graph_with_igraph

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    loader = FileLoader()
    renderer = GraphRenderer(app.map_widget)

    def open_file():
        graph = loader.load_gml()
        if graph:
            renderer.plot_nodes(graph)
            renderer.plot_edges(graph)
            export_graph_to_google_maps(graph)

    # Conectar funções ao app
    app.open_file = open_file
    app.load_chromosome = lambda: process_graph_with_igraph(app)
    app.generate_gml = lambda: process_graph_with_igraph(app)  # <-- ESSA LINHA É ESSENCIAL

    app.run()
