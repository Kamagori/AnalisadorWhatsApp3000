import sqlite3, unicodedata, re
from collections import Counter

def norm(s):
    s=unicodedata.normalize("NFKD",s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))

c=sqlite3.connect("coleta.db"); cur=c.cursor()
cur.execute("SELECT corpo FROM mensagens WHERE autor LIKE '%@lid' AND tipo='chat' AND corpo IS NOT NULL")
msgs=[norm(r[0]) for r in cur.fetchall() if r[0]]
c.close()
print(f"Mensagens de texto analisadas: {len(msgs)}\n")

CAND = {
 "A_substancias_praticas": [

   "anaboliz","esteroid","ciclo","trembo","trembolona","durateston","deca","stano","stanozolol",
   "winstrol","oxandrolona"," oxa ","dianabol","dbol","hemogenin","boldenona","bold ","primobolan",
   "primo ","masteron","sustanon","enantato","cipionato","propionato","testosterona","testo ",
   "hormonio","gh ","hgh","clembuterol","clen ","oximetolona","landerlan","gainer",

   "sarm","ostarine","ostarina","ligandrol","lgd","rad140","rad 140","cardarine","enobosarm","yk11",

   "sibutramina","anfepramona","femproporex","ozempic","semaglutida","wegovy","saxenda","mounjaro",
   "tirzepatida","diuretico","furosemida","lasix","laxante","termogenico","efedrina","dnp",
   "anorexigeno","manipulado","insulina","t3 ","citomel",

   "vomit","por o dedo","botar o dedo","jejum","restricao","secar","seca tudo","inducao",
 ],
 "B_desinformacao": [
   "cura","milagr","detox","desintoxic","emagrece","elimina","queima gordura","sem dieta",
   "sem exercicio","garantido","comprovado","natural","cha ","receita caseira","perde ","kg em",
   "quilos em","resultado garantido",
 ],
 "C_spam_golpe": [
   "pix","golpe","renda extra","investimento","investir","ganhe","ganhar dinheiro","lucro","retorno",
   "deposito","saque","cadastr","link","clica","clique","canal","grupo vip","whatsapp.com/channel",
   "divulg","vendo","a venda","promocao","desconto","frete","compre","oferta","afiliad","trabalhe em casa",
 ],
}

print("=== Prevalência de termos (nº de mensagens que contêm o termo) ===")
for cat, terms in CAND.items():
    print(f"\n## {cat}")
    cnt=Counter()
    for t in terms:
        n=sum(1 for m in msgs if t in m)
        if n>0: cnt[t]=n
    for t,n in cnt.most_common():
        print(f"   {t:<22} {n:>4}  ({100*n/len(msgs):.1f}%)")

    cov=sum(1 for m in msgs if any(t in m for t in terms))
    print(f"   --> mensagens com ≥1 termo de {cat}: {cov} ({100*cov/len(msgs):.1f}%)")
