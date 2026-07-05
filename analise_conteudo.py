import re, unicodedata, json, random, numpy as np, networkx as nx, warnings
from collections import defaultdict
from scipy.stats import spearmanr, mannwhitneyu
from wazap_network import load_network
warnings.filterwarnings("ignore")

def norm(s):
    s=unicodedata.normalize("NFKD",s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))

SUBST = [r"anaboliz\w*",r"esteroid\w*",r"trembolona",r"trembo\b",r"durateston",r"stanozolol",r"\bstano\b",
   r"winstrol",r"oxandrolona",r"dianabol",r"\bdbol\b",r"hemogenin",r"boldenona",r"primobolan",r"masteron",
   r"sustanon",r"enantato",r"cipionato",r"propionato",r"testosterona",r"clembuterol",r"oximetolona",
   r"landerlan",r"\bsarms?\b",r"ostarin\w*",r"ligandrol",r"\blgd\b",r"rad\s?140",r"cardarine",r"yk11",
   r"sibutramina",r"anfepramona",r"femproporex",r"ozempic",r"semaglutida",r"wegovy",r"saxenda",r"mounjaro",
   r"tirzepatida",r"furosemida",r"\blasix\b",r"termogenic\w*",r"efedrina",r"\bdnp\b",r"anorexigen\w*",
   r"\bsarm\b",r"\bgh\b",r"\bhgh\b",r"diuretic\w*"]
SUBST_CTX = [r"\bciclo\b",r"\bsecar\b",r"\bjejum\b",r"insulina",r"hormoni\w*",r"\btesto\b"]
MISINFO = [r"emagrec\w*",r"\bdetox\b",r"desintoxic\w*",r"milagr\w*",r"queima\s+gordura",r"sem\s+dieta",
   r"sem\s+exercicio",r"resultado\s+garantido",r"\d+\s*kg\s+em\s+\d+",r"perde\s+\d+\s*kg",
   r"elimina\s+\d+",r"cha\s+emagrec\w*",r"seca\s+barriga",r"chá",r"\bcura\b"]
SPAM = [r"\bpix\b",r"\bgolpe\b",r"renda\s+extra",r"investiment\w*",r"\binvestir\b",r"ganhar\s+dinheiro",
   r"\blucro\b",r"deposit\w*",r"\bsaque\b",r"cadastr\w*",r"grupo\s+vip",r"whatsapp\.com/channel",
   r"divulg\w*",r"\ba\s+venda\b",r"promoc\w*",r"afiliad\w*",r"trabalhe\s+em\s+casa",r"\boferta\b",
   r"\bdesconto\b",r"\bfrete\b",r"compre\s+\w*",r"\blink\b",r"\bclique\b",r"\bclica\b"]

reSUB=re.compile("|".join(SUBST)); reCTX=re.compile("|".join(SUBST_CTX))
reMIS=re.compile("|".join(MISINFO)); reSPAM=re.compile("|".join(SPAM))

def classify(t):
    tn=norm(t)
    subst = bool(reSUB.search(tn)) or bool(reCTX.search(tn))
    mis   = bool(reMIS.search(tn))
    spam  = bool(reSPAM.search(tn))
    problem = subst or mis
    return problem, spam, subst, mis

G,meta=load_network()
node_msgs=meta["node_msgs"]
prof={}
tot_msgs=tot_prob=tot_spam=0
for u,msgs in node_msgs.items():
    nm=len(msgs)
    if nm==0: continue
    p=s=0
    for m in msgs:
        pr,sp,_,_=classify(m); p+=pr; s+=sp
    prof[u]={"n":nm,"prob":p,"spam":s,"frac_prob":p/nm,"frac_spam":s/nm}
    tot_msgs+=nm; tot_prob+=p; tot_spam+=s

print(f"Mensagens classificadas: {tot_msgs} | usuários com texto: {len(prof)}")
print(f"  problemáticas (saúde): {tot_prob} ({100*tot_prob/tot_msgs:.1f}%)")
print(f"  spam/golpe:            {tot_spam} ({100*tot_spam/tot_msgs:.1f}%)")

def label(p):
    if p["frac_prob"]>=0.15 or p["prob"]>=3: return "prob"
    if p["frac_spam"]>=0.30 or p["spam"]>=5: return "spam"
    return "outro"
for u in prof: prof[u]["label"]=label(prof[u])
from collections import Counter
print("  rótulos de usuário:", dict(Counter(p["label"] for p in prof.values())))

random.seed(7)
all_msgs=[(u,m) for u,ms in node_msgs.items() for m in ms if len(m)>20]
flagged=[(u,m) for u,m in all_msgs if classify(m)[0]]
unflag =[(u,m) for u,m in all_msgs if not classify(m)[0]]
print(f"\n=== AMOSTRA p/ validação — 10 FLAGGED como problemático (saúde) ===")
for u,m in random.sample(flagged,10): print("  [P]", m[:95].replace(chr(10)," "))
print(f"\n=== 8 NÃO-flagged (controle) ===")
for u,m in random.sample(unflag,8): print("  [-]", m[:95].replace(chr(10)," "))

json.dump(prof, open("content_profiles.json","w"))
print("\n[perfis salvos em content_profiles.json]")
