import tkinter as tk
from graph_app import GraphApp
from file_loader import FileLoader
from graph_renderer import GraphRenderer

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


    app.open_file = open_file
    app.run()