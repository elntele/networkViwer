import tkinter as tk
import os
import webbrowser
from tkintermapview import TkinterMapView
from PIL import ImageGrab  # Para capturar a tela


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Topologia de Rede Óptica")
        self.root.geometry("800x600")

        # Criando um menu
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir .GML", command=self.trigger_open_file)
        file_menu.add_command(label="Abrir .CSV", command=self.load_from_chromosome)  # Novo
        file_menu.add_command(label="Gerar .GML de .CSV", command=self.generate_gml_from_csv)  # Novo
        file_menu.add_command(label="Exportar Mapa como PDF", command=self.export_map_to_pdf)
        file_menu.add_command(label="Abrir Mapa no Navegador", command=self.open_html_map)
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        self.root.config(menu=menubar)

        # Criando a área do mapa
        self.map_widget = TkinterMapView(self.root, width=800, height=500)
        self.map_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Definir o zoom inicial e a posição do mapa
        self.map_widget.set_position(40.7128, -74.0060)  # Coordenadas de exemplo (Nova York)
        self.map_widget.set_zoom(10)

        # Botão para capturar e salvar a imagem
        self.save_button = tk.Button(self.root, text="Salvar Mapa em PDF", command=self.export_map_to_pdf)
        self.save_button.pack(side="top", padx=10, pady=10)

    def trigger_open_file(self):
        """Chama a função `open_file` definida no main.py."""
        if self.open_file:
            self.open_file()

    def load_from_chromosome(self):
        """Chama a função `load_chromosome` se estiver definida externamente."""
        if hasattr(self, 'load_chromosome') and self.load_chromosome:
            self.load_chromosome()
        else:
            print("🚧 Função 'load_chromosome' ainda não implementada.")

    def generate_gml_from_csv(self):
        """Chama a função `generate_gml` se estiver definida externamente."""
        if hasattr(self, 'generate_gml') and self.generate_gml:
            self.generate_gml()
        else:
            print("🚧 Função 'generate_gml' ainda não implementada.")

    def export_map_to_pdf(self):
        """Captura a tela do mapa como uma imagem e salva como um PDF."""
        x = self.root.winfo_rootx() + self.map_widget.winfo_x()
        y = self.root.winfo_rooty() + self.map_widget.winfo_y()
        width = self.map_widget.winfo_width()
        height = self.map_widget.winfo_height()

        image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        pdf_path = "map_image.pdf"
        image.save(pdf_path, "PDF")
        print(f"Mapa salvo como PDF em: {pdf_path}")

    def open_html_map(self):
        """Abre o HTML gerado com o mapa do Google Maps."""
        html_path = "grafo_google_maps.html"
        if os.path.exists(html_path):
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
        else:
            print("❌ Arquivo HTML ainda não foi gerado.")

    def run(self):
        self.root.mainloop()


# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    app.run()
