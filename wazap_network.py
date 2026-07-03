import sqlite3, math
from collections import defaultdict
import networkx as nx

CONTENT_TYPES = {"chat", "image", "ptt", "sticker", "video", "audio",
                 "album", "document", "vcard", "interactive"}

def dense_window(ts, coverage=0.99):
    ts = sorted(ts); n = len(ts); need = max(1, math.ceil(coverage * n))
    if need >= n:
        return ts[0], ts[-1]
    best = None
    for i in range(0, n - need + 1):
        span = ts[i + need - 1] - ts[i]
        if best is None or span < best[0]:
            best = (span, ts[i], ts[i + need - 1])
    return best[1], best[2]

def load_network(db="coleta.db", window=600, coverage=0.99, keep_text=True):
    conn = sqlite3.connect(db); cur = conn.cursor()
    cur.execute("SELECT autor, grupo_id, grupo, timestamp, tipo, corpo FROM mensagens")
    rows = []
    for autor, gid, gnome, ts, tipo, corpo in cur.fetchall():
        if not autor or not autor.endswith("@lid") or tipo not in CONTENT_TYPES:
            continue
        try:
            ts = int(ts)
        except (TypeError, ValueError):
            continue
        grupo = gid if gid else f"NOME::{gnome}"
        rows.append((ts, autor, grupo, tipo, corpo or ""))
    conn.close()

    t0, t1 = dense_window([r[0] for r in rows], coverage)
    rows = sorted((r for r in rows if t0 <= r[0] <= t1), key=lambda r: r[0])

    uid = {}
    def anon(a):
        if a not in uid:
            uid[a] = f"u{len(uid)}"
        return uid[a]

    G = nx.DiGraph()
    node_groups = defaultdict(set); node_msgs = defaultdict(list); node_times = defaultdict(list)
    last = defaultdict(list)
    for ts, autor, grupo, tipo, corpo in rows:
        u = anon(autor)
        node_groups[u].add(grupo); node_times[u].append(ts)
        if keep_text and tipo == "chat" and corpo:
            node_msgs[u].append(corpo)
        if u not in G:
            G.add_node(u)
        buf = last[grupo]
        while buf and buf[0][0] < ts - window:
            buf.pop(0)
        partner = None
        for k in range(len(buf) - 1, -1, -1):
            if buf[k][1] != u:
                partner = buf[k][1]; break
        if partner is not None:
            if G.has_edge(u, partner):
                G[u][partner]["weight"] += 1
            else:
                G.add_edge(u, partner, weight=1)
        buf.append((ts, u))

    for n in G.nodes():
        G.nodes[n]["groups"] = node_groups[n]
        G.nodes[n]["n_groups"] = len(node_groups[n])
        G.nodes[n]["n_msgs"] = len(node_times[n])
    meta = dict(t0=t0, t1=t1, n_uid=len(uid),
                node_groups=dict(node_groups), node_msgs=dict(node_msgs), node_times=dict(node_times))
    return G, meta

def proximity_events(db="coleta.db", window=600, coverage=0.99):
    conn = sqlite3.connect(db); cur = conn.cursor()
    cur.execute("SELECT autor, grupo_id, grupo, timestamp, tipo FROM mensagens")
    rows = []
    for autor, gid, gnome, ts, tipo in cur.fetchall():
        if not autor or not autor.endswith("@lid") or tipo not in CONTENT_TYPES:
            continue
        try: ts = int(ts)
        except (TypeError, ValueError): continue
        rows.append((ts, autor, gid if gid else f"NOME::{gnome}"))
    conn.close()
    t0, t1 = dense_window([r[0] for r in rows], coverage)
    rows = sorted((r for r in rows if t0 <= r[0] <= t1), key=lambda r: r[0])
    uid = {}
    def anon(a):
        if a not in uid: uid[a] = f"u{len(uid)}"
        return uid[a]
    last = defaultdict(list); events = []
    for ts, autor, grupo in rows:
        u = anon(autor); buf = last[grupo]
        while buf and buf[0][0] < ts - window: buf.pop(0)
        partner = None
        for k in range(len(buf)-1, -1, -1):
            if buf[k][1] != u: partner = buf[k][1]; break
        if partner is not None:
            events.append((ts, u, partner))
        buf.append((ts, u))
    return events

if __name__ == "__main__":
    import datetime as dt
    G, meta = load_network()
    print(f"Janela densa: {dt.datetime.fromtimestamp(meta['t0'])} -> {dt.datetime.fromtimestamp(meta['t1'])}")
    print(f"Nós (usuários @lid ativos): {G.number_of_nodes()}")
    print(f"Arestas dirigidas: {G.number_of_edges()}")
    tot_w = sum(d['weight'] for _,_,d in G.edges(data=True))
    print(f"Peso total (eventos de proximidade): {tot_w}")
    multi = sum(1 for n in G.nodes() if G.nodes[n]['n_groups'] > 1)
    print(f"Nós multigrupo: {multi} ({100*multi/G.number_of_nodes():.1f}%)")
