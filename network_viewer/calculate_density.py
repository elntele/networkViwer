import pandas as pd
import igraph as ig
import chardet
import os

# >>> CONFIGURAÇÃO DE CAMINHOS <<<
nodes_gml = os.path.join(os.path.dirname(__file__), "..", "base_graph", "base_graph.gml")
csv_path = r"C:\Users\elnte\Desktop\result 24.6.25\CN-C+MN-C\VARSandFUNS\execution2\VAR360.csv"
output_path = r"C:\Users\elnte\Desktop\result 24.6.25\CN-C+MN-C\VARSandFUNS\execution2\densidade_redes.csv"

# >>> LER GML COM CORREÇÃO DE ENCODING <<<
with open(nodes_gml, 'rb') as f:
    raw = f.read()
    encoding = chardet.detect(raw)['encoding']
    gml_text = raw.decode(encoding)

temp_utf8_gml = nodes_gml + "_utf8_temp.gml"
with open(temp_utf8_gml, 'w', encoding='utf-8') as f:
    f.write(gml_text)

base_graph = ig.Graph.Read_GML(temp_utf8_gml)
num_nodes = len(base_graph.vs)

# >>> LER CSV <<<
df = pd.read_csv(csv_path, header=None)

# >>> CALCULAR DENSIDADE <<<
resultados = []
for idx, row in df.iterrows():
    genes = list(map(int, row.dropna()))
    expected_links = num_nodes * (num_nodes - 1) // 2
    if len(genes) < expected_links + num_nodes:
        densidade = None
    else:
        matrix = genes[:expected_links]
        g = ig.Graph()
        g.add_vertices(num_nodes)
        edges = []
        k = 0
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if matrix[k] > 0:
                    edges.append((i, j))
                k += 1
        g.add_edges(edges)
        densidade = g.density()
    resultados.append({"Rede": idx + 1, "Densidade": densidade})

# >>> CALCULAR MÉDIA <<<
media_densidade = sum(r["Densidade"] for r in resultados if r["Densidade"] is not None) / sum(1 for r in resultados if r["Densidade"] is not None)
resultados.append({"Rede": "Média", "Densidade": media_densidade})


# >>> SALVAR CSV <<<
pd.DataFrame(resultados).to_csv(output_path, index=False)
print(f"✅ Densidades salvas em: {output_path}")
