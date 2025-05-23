import csv
import os
import igraph as ig
import chardet
import tkinter as tk
from tkinter import filedialog, messagebox

def process_graph_with_igraph(app):
    def run_processing():
        try:
            line_number = int(entry_line.get())
            num_nodes = int(entry_nodes.get())

            if not csv_path_var.get() or not gml_path_var.get():
                messagebox.showerror("Erro", "Por favor, selecione os dois arquivos.")
                return

            base_path = os.path.dirname(csv_path_var.get())
            csv_path = csv_path_var.get()
            gml_path = gml_path_var.get()
            output_path = os.path.join(base_path, f"topologia_linha_{line_number}.gml")

            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                all_lines = list(reader)

            if line_number > len(all_lines):
                messagebox.showerror("Erro", f"O arquivo possui apenas {len(all_lines)} linhas.")
                return

            raw_values = all_lines[line_number - 1]
            genes = list(map(int, [g.strip() for g in raw_values]))

            expected_links = num_nodes * (num_nodes - 1) // 2
            if len(genes) < expected_links + num_nodes:
                messagebox.showerror("Erro", "Número insuficiente de genes para matriz + ROADMs.")
                return

            matrix_genes = genes[:expected_links]
            roadm_genes = genes[-(num_nodes + 1):-1]

            # >>>>> DETECTAR E CONVERTER CODIFICAÇÃO DO GML <<<<<
            with open(gml_path, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                decoded_gml = raw_data.decode(detected['encoding'])

            temp_utf8_path = os.path.join(base_path, "temp_utf8_graph.gml")
            with open(temp_utf8_path, 'w', encoding='utf-8') as f:
                f.write(decoded_gml)

            # >>>>> LER GML CONVERTIDO COM IGRAPH <<<<<
            g = ig.Graph.Read_GML(temp_utf8_path)

            if len(g.vs) != num_nodes:
                messagebox.showerror("Erro", "Número de nós no GML não corresponde ao especificado.")
                return

            g.vs["num_node"] = list(range(num_nodes))
            g.vs["ROADM"] = roadm_genes

            new_g = ig.Graph()
            new_g.add_vertices(num_nodes)

            for attr in g.vs.attributes():
                new_g.vs[attr] = g.vs[attr]

            edge_list = []
            edge_labels = []
            k = 0
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if matrix_genes[k] > 0:
                        edge_list.append((i, j))
                        edge_labels.append(matrix_genes[k])
                    k += 1

            new_g.add_edges(edge_list)
            new_g.es["LinkLabel"] = edge_labels

            new_g.write_gml(output_path)
            messagebox.showinfo("Sucesso", f"Arquivo salvo: {output_path}")
            dialog.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar: {e}")

    def select_csv():
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.CSV")], title="Selecione o arquivo do cromossomo (.CSV)")
        if path:
            csv_path_var.set(path)

    def select_gml():
        path = filedialog.askopenfilename(filetypes=[("GML Files", "*.gml")], title="Selecione o arquivo dos nós (.GML)")
        if path:
            gml_path_var.set(path)

    # >>>>> MODAL <<<<<
    dialog = tk.Toplevel(app.root)
    dialog.title("Importar Cromossomo com iGraph")
    dialog.geometry("440x300")

    csv_path_var = tk.StringVar()
    gml_path_var = tk.StringVar()

    label_line = tk.Label(dialog, text="Informe a linha da topologia:")
    label_line.pack(pady=(10, 2))
    entry_line = tk.Entry(dialog)
    entry_line.pack(pady=2)

    label_nodes = tk.Label(dialog, text="Informe o número de nós do grafo:")
    label_nodes.pack(pady=(10, 2))
    entry_nodes = tk.Entry(dialog)
    entry_nodes.pack(pady=2)

    button_csv = tk.Button(dialog, text="Selecionar arquivo CSV (Cromossomo)", command=select_csv)
    button_csv.pack(pady=(10, 2))

    button_gml = tk.Button(dialog, text="Selecionar arquivo GML (Nós)", command=select_gml)
    button_gml.pack(pady=2)

    button_process = tk.Button(dialog, text="Gerar topologia", command=run_processing)
    button_process.pack(pady=15)

    dialog.transient(app.root)
    dialog.grab_set()
    app.root.wait_window(dialog)
