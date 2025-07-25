import os
import pandas as pd
import igraph as ig
import chardet
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# >>> CONFIGURAÇÕES GERAIS <<<
nodes_gml = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "base_graph", "base_graph.gml"))
var_filename = "VAR1000.csv"
max_exec = 30

# >>> AJUSTES VISUAIS <<<
tick_fontsize = 12
label_fontsize = 16

# >>> LISTA DE ABORDAGENS COM CORES E MARCADORES DISTINTOS <<<
experimentos = [
    {
        "nome": "NSGA-II + MN-C",
        "base_path": r"C:\Users\elnte\Desktop\result 24.6.25\SBX_CROS+MN-C\VARSandFUNS",
        "cor": "blue",
        "marcador": "o"
    },
    {
        "nome": "ENC",
        "base_path": r"C:\Users\elnte\Desktop\result 24.6.25\CN-C+MN-C\VARSandFUNS",
        "cor": "green",
        "marcador": "s"
    },
    {
        "nome": "NSGA-II",
        "base_path": r"C:\Users\elnte\Desktop\result 24.6.25\SBX_CROS+INTE_POL_MUT\VARSandFUNS",
        "cor": "red",
        "marcador": "^"
    },
    {
        "nome": "NSGA-II + CN-C",
        "base_path": r"C:\Users\elnte\Desktop\result 24.6.25\CN-C+INTE_POL_MUT\VARSandFUNS",
        "cor": "black",
        "marcador": "D"
    }
]

# >>> LER GML <<<
with open(nodes_gml, 'rb') as f:
    raw = f.read()
    encoding = chardet.detect(raw)['encoding']
    gml_text = raw.decode(encoding)

temp_utf8_gml = nodes_gml + "_utf8_temp.gml"
with open(temp_utf8_gml, 'w', encoding='utf-8') as f:
    f.write(gml_text)

base_graph = ig.Graph.Read_GML(temp_utf8_gml)
num_nodes = len(base_graph.vs)
expected_links = num_nodes * (num_nodes - 1) // 2

plt.figure(figsize=(12, 6))

# >>> ARMAZENAR AS MÉDIAS PARA CÁLCULO DO MAIOR VALOR <<<
todas_medias = []

for experimento in experimentos:
    nome = experimento["nome"]
    base_path = experimento["base_path"]
    cor = experimento["cor"]
    marcador = experimento["marcador"]

    densities_by_rede = []

    for exec_id in range(1, max_exec + 1):
        csv_path = os.path.join(base_path, f"execution{exec_id}", var_filename)
        if not os.path.exists(csv_path):
            print(f"⚠️ Arquivo não encontrado: {csv_path}")
            continue

        df = pd.read_csv(csv_path, header=None)

        for idx, row in df.iterrows():
            genes = list(map(int, row.dropna()))
            if len(genes) < expected_links + num_nodes:
                continue
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
            if len(densities_by_rede) <= idx:
                densities_by_rede.append([])
            densities_by_rede[idx].append(densidade)

    # >>> CÁLCULO DAS MÉDIAS <<<
    avg_densities = [sum(d) / len(d) for d in densities_by_rede]
    media_geral = sum(avg_densities) / len(avg_densities)
    todas_medias.append(max(avg_densities))  # para posicionar a legenda

    x_vals = list(range(1, len(avg_densities) + 1))

    # >>> PLOTAR OS PONTOS <<<
    plt.scatter(x_vals, avg_densities,
                label=f"{nome}: média das médias = {media_geral:.3f}",
                color=cor, marker=marcador, s=30)

# >>> FORMATAR EIXO <<<
plt.xticks(ticks=list(range(0, len(avg_densities) + 1, 10)), fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)
plt.xlabel("Rede", fontsize=label_fontsize, fontweight='bold')
plt.ylabel("Densidade Média", fontsize=label_fontsize, fontweight='bold')
plt.title(f"Densidade Média por Rede ({max_exec} execuções)", fontsize=label_fontsize, fontweight='bold')
plt.grid(True)

# >>> POSICIONAR LEGENDA AUTOMATICAMENTE ACIMA DO MAIOR PONTO <<<
ymax = max(todas_medias)
plt.ylim(top=ymax + 0.02)
plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize=18, frameon=False)

plt.tight_layout()
plt.show()

#tinha isso em uma abordagem antiga, não deve funfar mais:
# descomente esses dois pra plotar o grafico com y em percentagem
#plt.ylim(0, 1.0)
#plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))