import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json, numpy as np, networkx as nx, random, warnings
from scipy.stats import spearmanr
from wazap_network import load_network
warnings.filterwarnings("ignore")
plt.rcParams.update({"font.size":12,"axes.titlesize":13,"axes.titleweight":"bold","figure.facecolor":"white"})
NAVY="#15233b"; TEAL="#0f766e"; ORANGE="#dd6b20"; BLUE="#2b6cb0"; RED="#c0392b"; GREY="#94a3b8"; PURPLE="#805ad5"
def save(fig,n): fig.tight_layout(); fig.savefig(f"rc_fig/{n}.png",dpi=160,bbox_inches="tight"); plt.close(fig)

G,meta=load_network(); prof=json.load(open("content_profiles.json"))
UG=G.to_undirected(); GC=UG.subgraph(max(nx.connected_components(UG),key=len)).copy()
bet=nx.betweenness_centrality(GC,normalized=True)
top30=set(sorted(bet,key=bet.get,reverse=True)[:30]) & set(prof)
prob_top=sum(prof[x]["prob"] for x in top30); prob_all=sum(prof[x]["prob"] for x in prof)

fig,ax=plt.subplots(figsize=(5.8,4.3))
ax.bar(["% dos\nusuários","% do conteúdo\nproblemático"],[100*len(top30)/len(prof),100*prob_top/prob_all],
       color=[GREY,ORANGE])
for i,v in enumerate([100*len(top30)/len(prof),100*prob_top/prob_all]):
    ax.text(i,v,f"{v:.0f}%",ha="center",va="bottom",fontsize=14)
ax.set_ylabel("%"); ax.set_ylim(0,28)
ax.set_title("H2 — As 30 maiores pontes concentram\na disseminação de conteúdo problemático")
save(fig,"h2_content_share")

nodes=[x for x in GC.nodes() if x in prof]
ng=np.array([G.nodes[x]["n_groups"] for x in nodes]); fp=np.array([prof[x]["frac_prob"] for x in nodes])
rho,_=spearmanr(ng,fp)
fig,ax=plt.subplots(figsize=(6.0,4.3))
jit=ng+np.random.RandomState(0).uniform(-0.15,0.15,len(ng))
ax.scatter(jit,100*fp,s=18,alpha=0.45,color=BLUE,edgecolors="none")

import collections
agg=collections.defaultdict(list)
for g,f in zip(ng,fp): agg[g].append(100*f)
gs=sorted(agg); means=[np.mean(agg[g]) for g in gs]
ax.plot(gs,means,"o-",color=ORANGE,lw=2,label="média por nº de grupos")
ax.set_xlabel("nº de grupos do usuário"); ax.set_ylabel("% de conteúdo problemático")
ax.set_title(f"H2 — Usuários multigrupo postam mais\nconteúdo problemático (Spearman {rho:+.2f})")
ax.legend(fontsize=9); save(fig,"h2_content_groups")

for x in GC.nodes():
    GC.nodes[x]["label"]=prof.get(x,{}).get("label","outro")
    GC.nodes[x]["grp"]=sorted(G.nodes[x]["groups"])[0] if G.nodes[x]["groups"] else "?"
a_lab=nx.attribute_assortativity_coefficient(GC,"label")
a_grp=nx.attribute_assortativity_coefficient(GC,"grp")
fig,ax=plt.subplots(figsize=(5.8,4.3))
ax.bar(["Conteúdo\n(rótulo)","Grupo"],[a_lab,a_grp],color=[GREY,TEAL])
for i,v in enumerate([a_lab,a_grp]):
    ax.text(i,v,f"{v:+.2f}",ha="center",va="bottom" if v>=0 else "top",fontsize=14)
ax.axhline(0,color="black",lw=0.8); ax.set_ylabel("assortatividade"); ax.set_ylim(-0.15,0.8)
ax.set_title("H3 — A interação é estruturada pelo GRUPO,\nnão pela similaridade de conteúdo")
save(fig,"h3_assortativity")

import os; print("figuras de conteúdo:", [f for f in sorted(os.listdir("rc_fig")) if "content" in f or "h3" in f])
