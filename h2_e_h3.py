import json, numpy as np, networkx as nx, random, warnings
from scipy.stats import spearmanr, mannwhitneyu
from wa_network import load_network
warnings.filterwarnings("ignore")

G,meta=load_network()
prof=json.load(open("content_profiles.json"))
UG=G.to_undirected()
GC=UG.subgraph(max(nx.connected_components(UG),key=len)).copy()
bet=nx.betweenness_centrality(GC,normalized=True)

nodes=[x for x in GC.nodes() if x in prof]
b=np.array([bet[x] for x in nodes]); fp=np.array([prof[x]["frac_prob"] for x in nodes])
ng=np.array([G.nodes[x]["n_groups"] for x in nodes])
rho_bf,p_bf=spearmanr(b,fp)
rho_gf,p_gf=spearmanr(ng,fp)
top30=set(sorted(bet,key=bet.get,reverse=True)[:30]) & set(prof)
rest=[x for x in nodes if x not in top30]
fp_top=[prof[x]["frac_prob"] for x in top30]; fp_rest=[prof[x]["frac_prob"] for x in rest]
U,pU=mannwhitneyu(fp_top,fp_rest,alternative="greater")

prob_top=sum(prof[x]["prob"] for x in top30); prob_all=sum(prof[x]["prob"] for x in prof)
share_users=len(top30)/len(prof)
print("===== H2 — CONTEÚDO (pontes disseminam conteúdo problemático?) =====")
print(f"  Spearman(betweenness, frac. problemático) = {rho_bf:+.2f} (p={p_bf:.1e})")
print(f"  Spearman(nº de grupos, frac. problemático) = {rho_gf:+.2f} (p={p_gf:.1e})")
print(f"  frac. problemático — TOP-30 pontes: mediana {np.median(fp_top):.2f} | demais: {np.median(fp_rest):.2f}  (Mann-Whitney p={pU:.3f})")
print(f"  o top-30 betweenness ({100*share_users:.0f}% dos usuários) gera {100*prob_top/prob_all:.0f}% das mensagens problemáticas")

for x in GC.nodes():
    GC.nodes[x]["label"]=prof.get(x,{}).get("label","outro")
    GC.nodes[x]["grp"]=sorted(G.nodes[x]["groups"])[0] if G.nodes[x]["groups"] else "?"
assort_label=nx.attribute_assortativity_coefficient(GC,"label")
assort_grp=nx.attribute_assortativity_coefficient(GC,"grp")

labels={x:GC.nodes[x]["label"] for x in GC.nodes()}
def same_frac(lab):
    return np.mean([1 if lab[u]==lab[v] else 0 for u,v in GC.edges()])
obs=same_frac(labels)
vals=list(labels.values()); rng=random.Random(0); null=[]
for _ in range(500):
    perm=vals[:]; rng.shuffle(perm)
    lab={x:perm[i] for i,x in enumerate(labels)}
    null.append(same_frac(lab))
null=np.array([null]).ravel(); z=(obs-null.mean())/null.std()
p_perm=np.mean(null>=obs)
print("\n===== H3 — HOMOFILIA (usuários de conteúdo similar interagem mais?) =====")
print(f"  Assortatividade por rótulo de conteúdo = {assort_label:+.3f}")
print(f"  Assortatividade por GRUPO (controle)   = {assort_grp:+.3f}")
print(f"  Arestas com mesmo rótulo: observado {100*obs:.1f}% | null {100*null.mean():.1f}%±{100*null.std():.1f}  (z={z:+.1f}, p={p_perm:.3f})")
print("  Obs.: a rede é construída por proximidade DENTRO do grupo → parte da homofilia de conteúdo")
print("        pode refletir a estrutura de grupos (mesmo grupo → conteúdo e arestas correlacionados).")
