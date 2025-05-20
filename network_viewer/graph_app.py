import tkinter as tk
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
        file_menu.add_command(label="Sair", command=self.root.quit)
        file_menu.add_command(label="Exportar Mapa como PDF", command=self.export_map_to_pdf)
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

    def export_map_to_pdf(self):
        """Captura a tela do mapa como uma imagem e salva como um PDF."""
        # Definindo a área para captura da tela
        x = self.root.winfo_rootx() + self.map_widget.winfo_x()
        y = self.root.winfo_rooty() + self.map_widget.winfo_y()
        width = self.map_widget.winfo_width()
        height = self.map_widget.winfo_height()

        # Captura da tela da área do mapa
        image = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Salva a imagem como PDF
        pdf_path = "map_image.pdf"
        image.save(pdf_path, "PDF")
        print(f"Mapa salvo como PDF em: {pdf_path}")

    def run(self):
        self.root.mainloop()

# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    app.run()
