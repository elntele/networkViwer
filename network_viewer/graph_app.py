import tkinter as tk
from tkintermapview import TkinterMapView

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Topologia de Rede Óptica")
        self.root.geometry("800x600")

        # Criando um menu
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir .GML", command=self.trigger_open_file)  # Aqui estava o problema
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        self.root.config(menu=menubar)

        # Criando a área do mapa
        self.map_widget = TkinterMapView(self.root, width=800, height=500)
        self.map_widget.pack(fill="both", expand=True, padx=10, pady=10)

        self.open_file = None  # Inicializa como None

    def trigger_open_file(self):
        """Chama a função `open_file` definida no main.py."""
        if self.open_file:
            self.open_file()

    def run(self):
        self.root.mainloop()
