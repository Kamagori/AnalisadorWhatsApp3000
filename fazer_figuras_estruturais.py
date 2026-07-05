import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, networkx as nx, warnings
from collections import defaultdict
from scipy.stats import spearmanr
import powerlaw
from wazap_network import load_network, proximity_events
warnings.filterwarnings("ignore")
plt.rcParams.update({"font.size":12,"axes.titlesize":13,"axes.titleweight":"bold","figure.facecolor":"white"})
NAVY="#15233b"; TEAL="#0f766e"; ORANGE="#dd6b20"; BLUE="#2b6cb0"; RED="#c0392b"; GREY="#94a3b8"
def save(fig,n): fig.tight_layout(); fig.savefig(f"rc_fig/{n}.png",dpi=160,bbox_inches="tight"); plt.close(fig)
import os; os.makedirs("rc_fig",exist_ok=True)

G,meta=load_network()
UG=G.to_undirected()
GC=UG.subgraph(max(nx.connected_components(UG),key=len)).copy()
bet=nx.betweenness_centrality(GC,normalized=True)

C=nx.average_clustering(GC); L=nx.average_shortest_path_length(GC)
nc,mc=GC.number_of_nodes(),GC.number_of_edges()
Cr,Lr=[],[]
for s in range(8):
    R=nx.gnm_random_graph(nc,mc,seed=s); Rg=R.subgraph(max(nx.connected_components(R),key=len))
    Cr.append(nx.average_clustering(Rg)); Lr.append(nx.average_shortest_path_length(Rg))
Cr,Lr=np.mean(Cr),np.mean(Lr)
fig,ax=plt.subplots(1,2,figsize=(8,4))
ax[0].bar(["Rede real","Aleatória\n(ER)"],[C,Cr],color=[ORANGE,GREY]); ax[0].set_title("Clustering (C)")
ax[0].set_ylabel("coef. de clustering")
for i,v in enumerate([C,Cr]): ax[0].text(i,v,f"{v:.3f}",ha="center",va="bottom")
ax[1].bar(["Rede real","Aleatória\n(ER)"],[L,Lr],color=[BLUE,GREY]); ax[1].set_title("Caminho médio (L)")
ax[1].set_ylabel("distância média")
for i,v in enumerate([L,Lr]): ax[1].text(i,v,f"{v:.2f}",ha="center",va="bottom")
fig.suptitle(f"H1 — Small-world: C ≫ C_rand e L ≈ L_rand  (σ = {(C/Cr)/(L/Lr):.1f})",fontweight="bold")
save(fig,"h1_smallworld")

deg=np.array([d for _,d in UG.degree() if d>0])
fit=powerlaw.Fit(deg,discrete=True,verbose=False)
vals=np.sort(deg); ccdf=1.0-np.arange(len(vals))/len(vals)
fig,ax=plt.subplots(figsize=(6.2,4.4))
ax.loglog(vals,ccdf,"o",ms=4,color=NAVY,alpha=0.7,label="dados")
fit.power_law.plot_ccdf(ax=ax,color=ORANGE,ls="--",lw=2,label=f"power-law (α={fit.power_law.alpha:.2f})")
fit.lognormal.plot_ccdf(ax=ax,color=TEAL,ls=":",lw=2,label="lognormal")
ax.set_xlabel("grau k"); ax.set_ylabel("P(K ≥ k)")
top10=sum(sorted(deg,reverse=True)[:len(deg)//10])/sum(deg)
ax.set_title(f"H1 — Cauda pesada: top 10% concentram {100*top10:.0f}% do grau")
ax.legend(fontsize=9); save(fig,"h1b_degree")

fig,ax=plt.subplots(figsize=(7.6,6.2))
pos=nx.spring_layout(GC,seed=42,k=0.45,iterations=60)
multi=[GC.nodes[x] if False else x for x in GC.nodes()]
ngrp={x:G.nodes[x]["n_groups"] for x in GC.nodes()}
node_color=[ORANGE if ngrp[x]>1 else "#cbd5e1" for x in GC.nodes()]
node_size=[30+4000*bet[x] for x in GC.nodes()]
nx.draw_networkx_edges(GC,pos,alpha=0.12,width=0.6,ax=ax)
nx.draw_networkx_nodes(GC,pos,node_color=node_color,node_size=node_size,linewidths=0.3,edgecolors="white",ax=ax)
ax.set_title("H2 — Pontes: nós laranja = multigrupo; tamanho ∝ intermediação (betweenness)")
ax.axis("off")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=ORANGE,markersize=9,label='multigrupo'),
                   Line2D([0],[0],marker='o',color='w',markerfacecolor="#cbd5e1",markersize=9,label='um grupo')],
          loc="lower left",fontsize=9)
save(fig,"h2_network")

top30=sorted(bet,key=bet.get,reverse=True)[:30]
top_multi=np.mean([1 if G.nodes[x]["n_groups"]>1 else 0 for x in top30])
base_multi=np.mean([1 if G.nodes[x]["n_groups"]>1 else 0 for x in G.nodes()])
fig,ax=plt.subplots(figsize=(5.6,4.2))
ax.bar(["Top-30\nbetweenness","Todos os nós\n(base)"],[100*top_multi,100*base_multi],color=[ORANGE,GREY])
for i,v in enumerate([100*top_multi,100*base_multi]): ax.text(i,v,f"{v:.0f}%",ha="center",va="bottom",fontsize=13)
ax.set_ylabel("% multigrupo"); ax.set_ylim(0,100)
ax.set_title("H2 — Pontes conectam múltiplos grupos")
save(fig,"h2_multigroup")

events=proximity_events(); ts=np.array([e[0] for e in events]); tsp=np.median(ts)
first=[(u,v) for t,u,v in events if t<=tsp]; second=[(u,v) for t,u,v in events if t>tsp]
neigh1=defaultdict(set)
for u,v in first: neigh1[u].add(v); neigh1[v].add(u)
deg1={x:len(neigh1[x]) for x in neigh1}
newp=defaultdict(int); act=defaultdict(int); run={x:set(neigh1[x]) for x in neigh1}
for u,v in second:
    act[u]+=1
    for a,b in ((u,v),(v,u)):
        if b not in run.get(a,set()): run.setdefault(a,set()).add(b); newp[a]+=1
nodes=[x for x in deg1 if deg1[x]>0]
k=np.array([deg1[x] for x in nodes])
raw=np.array([newp.get(x,0) for x in nodes])
rho_raw,_=spearmanr(k,raw)
nr=[x for x in nodes if act.get(x,0)>0]; kr=np.array([deg1[x] for x in nr])
ratio=np.array([newp.get(x,0)/act[x] for x in nr]); rho_ctl,_=spearmanr(kr,ratio)
fig,ax=plt.subplots(figsize=(6.4,4.3))
ax.bar(["Bruto\n(novos laços)","Controlado\npor atividade"],[rho_raw,rho_ctl],color=[GREY,RED])
for i,v in enumerate([rho_raw,rho_ctl]): ax.text(i,v,f"{v:+.2f}",ha="center",va="bottom" if v>0 else "top",fontsize=13)
ax.axhline(0,color="black",lw=0.8); ax.set_ylabel("Spearman(grau prévio, crescimento)")
ax.set_title("H4 — A correlação positiva some ao controlar a atividade\n→ não há preferential attachment")
save(fig,"h4_activity")

H=G.copy()
for nd in H.nodes(): H.nodes[nd]["groups"]=";".join(sorted(H.nodes[nd]["groups"]))
nx.write_graphml(H,"coleta_network.graphml")
print("figuras salvas em rc_fig/:", sorted(os.listdir("rc_fig")))
print("grafo salvo: coleta_network.graphml")
