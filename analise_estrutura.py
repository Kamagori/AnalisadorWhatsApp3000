import numpy as np, networkx as nx, math, warnings
from collections import defaultdict
from scipy.stats import spearmanr
import powerlaw
from wa_network import load_network, proximity_events
warnings.filterwarnings("ignore")

G, meta = load_network()
n, m = G.number_of_nodes(), G.number_of_edges()
UG = G.to_undirected()
gcc_nodes = max(nx.connected_components(UG), key=len)
GC = UG.subgraph(gcc_nodes).copy()
print(f"REDE: {n} nós, {m} arestas dirigidas | maior componente: {GC.number_of_nodes()} nós "
      f"({100*GC.number_of_nodes()/n:.1f}%), {GC.number_of_edges()} arestas\n")

C = nx.average_clustering(GC)
L = nx.average_shortest_path_length(GC)
ncc, mcc = GC.number_of_nodes(), GC.number_of_edges()
k_avg = 2*mcc/ncc

Cr, Lr = [], []
for s in range(8):
    R = nx.gnm_random_graph(ncc, mcc, seed=s)
    Rg = R.subgraph(max(nx.connected_components(R), key=len))
    Cr.append(nx.average_clustering(Rg)); Lr.append(nx.average_shortest_path_length(Rg))
Cr, Lr = np.mean(Cr), np.mean(Lr)
sigma = (C/Cr)/(L/Lr)
print("== H1a — SMALL-WORLD ==")
print(f"  grau médio <k> = {k_avg:.2f}")
print(f"  Clustering:   C = {C:.4f}   |  C_rand = {Cr:.4f}   ->  C/C_rand = {C/Cr:.1f}")
print(f"  Caminho médio: L = {L:.3f}   |  L_rand = {Lr:.3f}   ->  L/L_rand = {L/Lr:.2f}")
print(f"  sigma = (C/Cr)/(L/Lr) = {sigma:.2f}  ->  {'SMALL-WORLD (sigma>1)' if sigma>1 else 'não small-world'}\n")

deg = [d for _,d in UG.degree()]
deg = [d for d in deg if d > 0]
deg_sorted = sorted(deg, reverse=True)
top10 = sum(deg_sorted[:max(1,len(deg_sorted)//10)]) / sum(deg_sorted)
fit = powerlaw.Fit(deg, discrete=True, verbose=False)
R_ln, p_ln = fit.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
R_exp, p_exp = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
print("== H1b — LIVRE-DE-ESCALA (distribuição de grau) ==")
print(f"  top 10% dos nós concentram {100*top10:.1f}% do grau total")
print(f"  alpha (power-law) = {fit.power_law.alpha:.2f}, xmin = {fit.power_law.xmin:.0f}")
print(f"  power-law vs lognormal:   R = {R_ln:+.2f}, p = {p_ln:.3f}  "
      f"({'lognormal melhor' if R_ln<0 and p_ln<0.05 else 'power-law melhor' if R_ln>0 and p_ln<0.05 else 'indistinguível'})")
print(f"  power-law vs exponencial: R = {R_exp:+.2f}, p = {p_exp:.3f}  "
      f"({'power-law melhor' if R_exp>0 and p_exp<0.05 else 'indistinguível'})\n")

bet = nx.betweenness_centrality(GC, weight=None, normalized=True)
top30 = sorted(bet, key=bet.get, reverse=True)[:30]
base_multi = np.mean([1 if G.nodes[x]["n_groups"]>1 else 0 for x in G.nodes()])
top_multi = np.mean([1 if G.nodes[x]["n_groups"]>1 else 0 for x in top30])

xs = [bet[x] for x in GC.nodes()]; ys = [G.nodes[x]["n_groups"] for x in GC.nodes()]
rho_bg, p_bg = spearmanr(xs, ys)
print("== H2 (estrutural) — PONTES (alta intermediação) ==")
print(f"  multigrupo entre TOP-30 betweenness: {100*top_multi:.0f}%   |   linha de base: {100*base_multi:.0f}%")
print(f"  Spearman(betweenness, nº de grupos) = {rho_bg:+.2f} (p={p_bg:.1e})\n")

events = proximity_events()
ts_all = [e[0] for e in events]
t_split = np.median(ts_all)
first = [(u,v) for ts,u,v in events if ts <= t_split]
second = [(u,v) for ts,u,v in events if ts > t_split]

deg1 = defaultdict(int); seen1 = defaultdict(set)
for u,v in first:
    if v not in seen1[u]: seen1[u].add(v); deg1[u]+=1; deg1[v]+=1

growth = defaultdict(int)
for u,v in second:
    growth[u]+=1; growth[v]+=1
nodes1 = [x for x in deg1 if deg1[x]>0]
kx = [deg1[x] for x in nodes1]; gy = [growth.get(x,0) for x in nodes1]
rho_pa, p_pa = spearmanr(kx, gy)
print("== H4 — PREFERENTIAL ATTACHMENT (crescimento ~ grau prévio) ==")
print(f"  nós presentes na 1ª metade: {len(nodes1)}")
print(f"  Spearman(grau na 1ª metade, novas interações na 2ª) = {rho_pa:+.2f} (p={p_pa:.1e})")
print(f"  -> {'SUSTENTADO (correlação positiva)' if rho_pa>0.2 and p_pa<0.05 else 'NÃO sustentado'}")

nx.write_graphml(G, "coleta_network.graphml")
print("\n[grafo salvo em coleta_network.graphml]")
