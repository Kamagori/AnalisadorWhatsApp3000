import numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
from wa_network import proximity_events

events = proximity_events()
ts = np.array([e[0] for e in events])
t_split = np.median(ts)
first  = [(u,v) for t,u,v in events if t <= t_split]
second = [(u,v) for t,u,v in events if t >  t_split]
print(f"eventos: {len(events)} | 1ª metade: {len(first)} | 2ª metade: {len(second)}\n")

neigh1 = defaultdict(set)
for u,v in first: neigh1[u].add(v); neigh1[v].add(u)
deg1 = {x: len(neigh1[x]) for x in neigh1}

raw_events = defaultdict(int)
new_partners = defaultdict(int)
own_activity = defaultdict(int)
attracted = defaultdict(int)
neigh_run = {x:set(neigh1[x]) for x in neigh1}
for u,v in second:
    raw_events[u]+=1; raw_events[v]+=1
    own_activity[u]+=1; attracted[v]+=1
    for a,b in ((u,v),(v,u)):
        if b not in neigh_run.get(a,set()):
            neigh_run.setdefault(a,set()).add(b); new_partners[a]+=1

nodes = [x for x in deg1 if deg1[x]>0]
k   = np.array([deg1[x] for x in nodes])
def corr(metric, label):
    y = np.array([metric.get(x,0) for x in nodes])
    rho,p = spearmanr(k,y)
    print(f"  Spearman(grau_1ªmetade, {label:<28}) = {rho:+.3f}  (p={p:.1e})")
    return rho
print("== Correlações (n={} nós presentes na 1ª metade) ==".format(len(nodes)))
corr(raw_events,   "eventos brutos 2ª metade")
corr(new_partners, "NOVOS vizinhos distintos")
corr(own_activity, "atividade própria (origem)")
corr(attracted,    "interações atraídas (alvo)")

ratio = {x: new_partners.get(x,0)/own_activity[x] for x in nodes if own_activity.get(x,0)>0}
nodes_r = list(ratio); kr=np.array([deg1[x] for x in nodes_r]); yr=np.array([ratio[x] for x in nodes_r])
rho_r,p_r = spearmanr(kr,yr)
print(f"\n  CONTROLE de atividade: Spearman(grau, novos_vizinhos/atividade) = {rho_r:+.3f} (p={p_r:.1e})")

print("\n== Kernel de anexação: novos vizinhos médios por faixa de grau ==")
bins = [1,2,3,5,8,13,21,1000]
for lo,hi in zip(bins,bins[1:]):
    grp = [x for x in nodes if lo<=deg1[x]<hi]
    if grp:
        mean_new = np.mean([new_partners.get(x,0) for x in grp])
        print(f"  grau [{lo:>3},{hi if hi<1000 else '∞':>3}): {len(grp):>3} nós, novos vizinhos médios = {mean_new:.2f}")
