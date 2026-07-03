const pptxgen=require("pptxgenjs");
const React=require("react"); const ReactDOMServer=require("react-dom/server");
const sharp=require("sharp"); const fa=require("react-icons/fa");

const NAVY="15233B",INK="1F2A37",MUTED="64748B",WHITE="FFFFFF",SLATE="F1F5F9";
const H1C="2B6CB0",H2C="DD6B20",H3C="0F766E",H4C="805AD5",RED="C0392B",TEAL="0F766E";
const HEAD="Cambria",BODY="Calibri";
const shadow=()=>({type:"outer",color:"000000",blur:7,offset:3,angle:90,opacity:0.13});

const V={CONF:["047857","D1FAE5"],APOIO:["047857","D1FAE5"],PARC:["92400E","FEF3C7"],NAO:["B91C1C","FEE2E2"]};

async function icon(C,color,size=256){
  const svg=ReactDOMServer.renderToStaticMarkup(React.createElement(C,{color,size:String(size)}));
  return "image/png;base64,"+(await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}
async function fitImage(slide,path,x,y,maxW,maxH){
  const m=await sharp(path).metadata(); const r=m.width/m.height;
  let w=maxW,h=w/r; if(h>maxH){h=maxH;w=h*r;}
  slide.addImage({path,x:x+(maxW-w)/2,y:y+(maxH-h)/2,w,h});
}

(async()=>{
  const p=new pptxgen(); p.defineLayout({name:"W",width:13.333,height:7.5}); p.layout="W";
  p.author="Marcos Biscotto de Oliveira"; p.title="Redes Complexas — WhatsApp Saúde";
  const W=13.333;

  const icNet=await icon(fa.FaProjectDiagram,"#"+WHITE);
  const icBridge=await icon(fa.FaExchangeAlt,"#"+WHITE);
  const icUsers=await icon(fa.FaUsers,"#"+WHITE);
  const icGrow=await icon(fa.FaChartLine,"#"+WHITE);
  const icDb=await icon(fa.FaDatabase,"#"+WHITE);
  const icWarn=await icon(fa.FaExclamationTriangle,"#"+WHITE);
  const icPills=await icon(fa.FaPills,"#"+WHITE);
  const icQ=await icon(fa.FaQuestion,"#"+WHITE);
  const icScale=await icon(fa.FaBalanceScale,"#"+WHITE);
  const icBook=await icon(fa.FaBookOpen,"#"+WHITE);

  function titleBar(s,txt,badge){
    s.addText(txt,{x:0.55,y:0.34,w:11.0,h:0.85,fontFace:HEAD,fontSize:27,bold:true,color:INK,valign:"middle",margin:0});
    if(badge) s.addShape(p.shapes.OVAL,{x:12.05,y:0.46,w:0.6,h:0.6,fill:{color:badge}});
  }
  function circleIcon(s,data,x,y,d,bg){
    s.addShape(p.shapes.OVAL,{x,y,w:d,h:d,fill:{color:bg}});
    const pad=d*0.26; s.addImage({data,x:x+pad,y:y+pad,w:d-2*pad,h:d-2*pad});
  }
  function verdictPill(s,x,y,w,label,key){
    const[fg,bg]=V[key];
    s.addShape(p.shapes.ROUNDED_RECTANGLE,{x,y,w,h:0.55,fill:{color:bg},rectRadius:0.1});
    s.addText(label,{x,y,w,h:0.55,fontFace:BODY,fontSize:15,bold:true,color:fg,align:"center",valign:"middle",margin:0});
  }
  
  function whyFixRight(s,x,y,w,verdict,vkey,why,fix){
    verdictPill(s,x,y,w,verdict,vkey);
    s.addText("Por quê?",{x,y:y+0.78,w,h:0.34,fontFace:BODY,fontSize:14,bold:true,color:INK,margin:0});
    s.addText(why,{x,y:y+1.12,w,h:2.0,fontFace:BODY,fontSize:13,color:"374151",margin:0,valign:"top",lineSpacingMultiple:1.04});
    s.addText("O que ajudaria?",{x,y:y+3.15,w,h:0.34,fontFace:BODY,fontSize:14,bold:true,color:TEAL,margin:0});
    s.addText(fix,{x,y:y+3.49,w,h:1.5,fontFace:BODY,fontSize:13,color:"374151",margin:0,valign:"top",lineSpacingMultiple:1.04});
  }
  
  function whyFixBand(s,verdict,vkey,why,fix){
    verdictPill(s,0.6,5.15,2.7,verdict,vkey);
    s.addText([{text:"Por quê?  ",options:{bold:true,color:INK}},{text:why,options:{color:"374151"}}],
      {x:3.5,y:5.0,w:9.3,h:0.85,fontFace:BODY,fontSize:12.5,margin:0,valign:"middle",lineSpacingMultiple:1.02});
    s.addText([{text:"O que ajudaria?  ",options:{bold:true,color:TEAL}},{text:fix,options:{color:"374151"}}],
      {x:3.5,y:5.95,w:9.3,h:0.75,fontFace:BODY,fontSize:12.5,margin:0,valign:"middle",lineSpacingMultiple:1.02});
  }

  
  let s=p.addSlide(); s.background={color:NAVY};
  s.addText("Quem Dissemina Conteúdo de Saúde Problemático?",{x:0.9,y:1.45,w:11.5,h:1.0,fontFace:HEAD,fontSize:34,bold:true,color:WHITE,margin:0});
  s.addText("Uma análise de rede de grupos de WhatsApp sobre saúde e emagrecimento",{x:0.9,y:2.55,w:11.5,h:0.7,fontFace:HEAD,fontSize:23,bold:true,color:"CADCFC",margin:0});
  s.addText("INF 791 — Tópicos Especiais II: Redes Complexas",{x:0.9,y:3.5,w:11.5,h:0.5,fontFace:BODY,fontSize:17,color:"AEBED9",margin:0});
  s.addText("Marcos Biscotto de Oliveira  ·  Matrícula 4236",{x:0.9,y:4.0,w:11.5,h:0.5,fontFace:BODY,fontSize:15,bold:true,color:WHITE,margin:0});
  const hyps=[["H1",H1C],["H2",H2C],["H3",H3C],["H4",H4C]];
  hyps.forEach((h,i)=>{const x=0.95+i*2.0;
    s.addShape(p.shapes.OVAL,{x,y:5.5,w:0.34,h:0.34,fill:{color:h[1]}});
    s.addText(h[0],{x:x+0.42,y:5.45,w:1.5,h:0.45,fontFace:BODY,fontSize:14,bold:true,color:WHITE,valign:"middle",margin:0});});
  s.addNotes("Análise da rede de interações em grupos públicos de WhatsApp sobre saúde/emagrecimento, com foco em quem dissemina conteúdo problemático (anabolizantes, emagrecedores, desinformação). Quatro perguntas estruturais (H1-H4).");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Motivação e problema");
  circleIcon(s,icPills,0.6,1.55,0.9,H2C);
  s.addText([
    {text:"Grupos de WhatsApp de saúde e emagrecimento circulam conteúdo potencialmente perigoso",options:{bold:true,color:INK}},
    {text:" — anabolizantes e SARMs, emagrecedores usados sem prescrição (tirzepatida, sibutramina), desinformação (\u201csecar em 20 dias\u201d, \u201cdetox\u201d) — para um público frequentemente vulnerável.",options:{}},
  ],{x:1.75,y:1.55,w:10.9,h:1.5,fontFace:BODY,fontSize:16,color:"374151",margin:0,lineSpacingMultiple:1.05});
  s.addText([
    {text:"A pergunta: ",options:{bold:true,color:INK}},
    {text:"como esse conteúdo se ",options:{}},
    {text:"propaga pela rede de interações",options:{bold:true,color:TEAL}},
    {text:", e ",options:{}},
    {text:"quem são os atores centrais",options:{bold:true,color:TEAL}},
    {text:" nessa disseminação? A análise de redes complexas permite mapear a estrutura e identificar esses papéis.",options:{}},
  ],{x:0.6,y:3.3,w:12,h:1.5,fontFace:BODY,fontSize:16,color:"374151",margin:0,lineSpacingMultiple:1.05});
  s.addText("Relevância: entender a estrutura da disseminação é o primeiro passo para mitigar danos à saúde pública.",
    {x:0.6,y:5.4,w:12,h:0.6,fontFace:BODY,fontSize:13.5,italic:true,color:MUTED,margin:0});
  s.addNotes("Motivação de saúde pública: esses grupos espalham conteúdo perigoso. Queremos entender a estrutura da rede e quem são os atores que disseminam, usando ferramentas de redes complexas.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Perguntas de pesquisa");
  const Q=[
    [H1C,icNet,"H1 — Estrutura","A rede é mundo pequeno e livre de escala, com poucos usuários concentrando as interações?"],
    [H2C,icBridge,"H2 — Pontes","Os nós de maior intermediação (bridges) são os principais disseminadores de conteúdo problemático?"],
    [H3C,icUsers,"H3 — Homofilia","Usuários que compartilham conteúdo semelhante tendem a interagir preferencialmente entre si?"],
    [H4C,icGrow,"H4 — Crescimento","A rede tem preferential attachment: usuários mais ativos atraem progressivamente mais interações?"],
  ];
  Q.forEach((q,i)=>{const y=1.5+i*1.35;
    s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:0.6,y,w:12.1,h:1.2,fill:{color:"F8FAFC"},line:{color:"E2E8F0",width:1},rectRadius:0.08});
    s.addShape(p.shapes.RECTANGLE,{x:0.6,y,w:0.12,h:1.2,fill:{color:q[0]}});
    circleIcon(s,q[1],0.85,y+0.28,0.64,q[0]);
    s.addText(q[2],{x:1.7,y:y+0.12,w:3.0,h:0.95,fontFace:BODY,fontSize:16,bold:true,color:q[0],valign:"middle",margin:0});
    s.addText(q[3],{x:4.8,y:y+0.1,w:7.7,h:1.0,fontFace:BODY,fontSize:14,color:"374151",valign:"middle",margin:0,lineSpacingMultiple:1.03});});
  s.addNotes("As quatro perguntas que orientam o trabalho: estrutura (mundo pequeno/livre de escala), pontes (disseminação), homofilia (conteúdo similar interage?) e crescimento (preferential attachment).");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Trabalhos relacionados");
  const TR=[
    ["Mundo pequeno (Watts & Strogatz, 1998)","Redes reais combinam alto clustering com caminhos curtos — base teórica para H1."],
    ["Livre de escala (Barabási & Albert, 1999)","Crescimento por anexação preferencial gera hubs e cauda pesada — base para H1 e H4."],
    ["Redes sociais e desinformação","Estudos de difusão em redes sociais; pontes e hubs como vetores de propagação — base para H2."],
    ["Estudos de WhatsApp","Coleta e análise de grupos públicos; foco em política/notícias."],
  ];
  TR.forEach((t,i)=>{const y=1.55+i*1.02;
    s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:0.6,y,w:12.1,h:0.9,fill:{color:WHITE},line:{color:"E2E8F0",width:1},rectRadius:0.06});
    s.addText(t[0],{x:0.85,y:y+0.08,w:4.6,h:0.74,fontFace:BODY,fontSize:14,bold:true,color:INK,valign:"middle",margin:0});
    s.addText(t[1],{x:5.6,y:y+0.06,w:6.95,h:0.78,fontFace:BODY,fontSize:12.5,color:"374151",valign:"middle",margin:0,lineSpacingMultiple:1.0});});
  s.addText([{text:"Nossa diferença:  ",options:{bold:true,color:TEAL}},
    {text:"dados próprios e inéditos de grupos de saúde/emagrecimento, com foco na disseminação de conteúdo problemático e uma rede construída por proximidade conversacional.",options:{color:"374151"}}],
    {x:0.6,y:5.75,w:12.1,h:0.9,fontFace:BODY,fontSize:13.5,margin:0,valign:"middle",lineSpacingMultiple:1.03});
  s.addNotes("Trabalhos relacionados: as bases teóricas (Watts-Strogatz, Barabási-Albert) e estudos de difusão/WhatsApp. Nossa diferença é o dado próprio de saúde e o foco em conteúdo problemático.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Dados");
  s.addText([
    {text:"Coleta própria",options:{bold:true,color:INK}},
    {text:" via whatsapp-web.js em grupos públicos de saúde/emagrecimento, armazenada em SQLite. Cada registro: autor, grupo, texto, timestamp e tipo.",options:{}},
  ],{x:0.6,y:1.5,w:6.1,h:1.5,fontFace:BODY,fontSize:15,color:"374151",margin:0,lineSpacingMultiple:1.05});
  s.addText([
    {text:"Recorte: ",options:{bold:true,color:INK}},
    {text:"janela temporal densa (~33 dias, mai–jun/2026), descartando uma cauda esparsa de mensagens antigas. Conteúdo: discussão real de saúde/corpo + um volume relevante de spam/golpe.",options:{}},
  ],{x:0.6,y:3.2,w:6.1,h:1.8,fontFace:BODY,fontSize:15,color:"374151",margin:0,lineSpacingMultiple:1.05});
  
  const stt=[["21.378","mensagens",H1C],["72","grupos",H2C],["814","usuários",H3C]];
  stt.forEach((c,i)=>{const y=1.5+i*1.35;
    s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:7.05,y,w:5.7,h:1.15,fill:{color:"F8FAFC"},line:{color:"E2E8F0",width:1},rectRadius:0.08,shadow:shadow()});
    s.addText(c[0],{x:7.3,y,w:2.4,h:1.15,fontFace:HEAD,fontSize:34,bold:true,color:c[2],valign:"middle",margin:0});
    s.addText(c[1],{x:9.7,y,w:2.9,h:1.15,fontFace:BODY,fontSize:16,color:INK,valign:"middle",margin:0});});
  s.addNotes("Dados: coleta própria via whatsapp-web.js, 21.378 mensagens, 72 grupos, 814 usuários, recortados na janela densa de ~33 dias. Conteúdo real de saúde mais spam.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Metodologia — construção da rede");
  circleIcon(s,icNet,0.6,1.55,0.9,H1C);
  s.addText([
    {text:"Nós",options:{bold:true,color:INK}},{text:" = usuários.  ",options:{}},
    {text:"Arestas",options:{bold:true,color:INK}},{text:" = proximidade conversacional: no mesmo grupo, em ordem temporal, cada mensagem liga o autor ao autor distinto imediatamente anterior (janela de 10 min). Rede dirigida e ponderada.",options:{}},
  ],{x:1.75,y:1.55,w:10.9,h:1.6,fontFace:BODY,fontSize:15.5,color:"374151",margin:0,lineSpacingMultiple:1.05});
  s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:0.6,y:3.5,w:12.1,h:1.55,fill:{color:SLATE},rectRadius:0.08});
  s.addText([
    {text:"Por que proximidade, e não \u201cresposta/menção\u201d?  ",options:{bold:true,color:H2C}},
    {text:"A proposta previa arestas de resposta/menção, mas o WhatsApp Web não expõe esses metadados na coleta (e menções explícitas são raras). A proximidade temporal é a melhor aproximação disponível de \u201cinteração direta\u201d — uma escolha honesta, forçada pelo dado, que declaramos explicitamente.",options:{color:"374151"}},
  ],{x:0.85,y:3.62,w:11.6,h:1.35,fontFace:BODY,fontSize:14,margin:0,valign:"middle",lineSpacingMultiple:1.05});
  s.addText("Robustez: os achados se mantêm ao variar a janela (1, 5, 10, 30 min).",
    {x:0.6,y:5.25,w:12,h:0.5,fontFace:BODY,fontSize:13,italic:true,color:MUTED,margin:0});
  s.addNotes("Ponto metodológico central e honesto: a proposta dizia resposta/menção, mas o dado não tem esses metadados. Então operacionalizamos a interação como proximidade temporal no mesmo grupo. Declaramos isso abertamente; os resultados são robustos à janela.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Metodologia — rotulagem de conteúdo");
  circleIcon(s,icWarn,0.6,1.55,0.9,RED);
  s.addText([
    {text:"Definição concreta de \u201cconteúdo problemático\u201d",options:{bold:true,color:INK}},
    {text:" (taxonomia operacional):",options:{}},
  ],{x:1.75,y:1.6,w:10.9,h:0.5,fontFace:BODY,fontSize:15.5,color:"374151",margin:0});
  const tax=[
    [RED,"Substâncias/práticas perigosas","anabolizantes, SARMs, emagrecedores sem prescrição (tirzepatida, sibutramina), jejum/restrição extrema, indução de vômito"],
    ["B45309","Desinformação em saúde","curas milagrosas, \u201cdetox\u201d, \u201cemagreça X kg em Y dias\u201d, alegações sem evidência"],
    [MUTED,"Spam/golpe comercial","pix, esquemas de renda, divulgação de produtos — mantido na rede (eixo à parte)"],
  ];
  tax.forEach((t,i)=>{const y=2.25+i*0.92;
    s.addShape(p.shapes.RECTANGLE,{x:0.6,y,w:0.11,h:0.8,fill:{color:t[0]}});
    s.addText(t[1],{x:0.85,y,w:3.7,h:0.8,fontFace:BODY,fontSize:13.5,bold:true,color:t[0]==="MUTED"?INK:t[0],valign:"middle",margin:0});
    s.addText(t[2],{x:4.65,y,w:7.9,h:0.8,fontFace:BODY,fontSize:12,color:"374151",valign:"middle",margin:0,lineSpacingMultiple:1.0});});
  s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:0.6,y:5.15,w:12.1,h:1.45,fill:{color:SLATE},rectRadius:0.08});
  s.addText([
    {text:"Como rotulamos:  ",options:{bold:true,color:TEAL}},
    {text:"léxico de alta precisão (termos curados) para escala + validação por LLM em amostra. Resultado: ",options:{color:"374151"}},
    {text:"11% das mensagens são conteúdo problemático de saúde",options:{bold:true,color:RED}},
    {text:" e 12,6% spam/golpe.",options:{color:"374151"}},
  ],{x:0.85,y:5.27,w:11.6,h:1.2,fontFace:BODY,fontSize:13.5,margin:0,valign:"middle",lineSpacingMultiple:1.04});
  s.addNotes("Resolve o feedback 1 (definição vaga): taxonomia operacional concreta de conteúdo problemático, rotulada por léxico + validação por LLM. 11% problemático, 12,6% spam (mantido na rede).");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"H1 — A rede é um \u201cmundo pequeno\u201d",H1C);
  await fitImage(s,"rc_fig/h1_smallworld.png",0.5,1.55,6.5,4.7);
  whyFixRight(s,7.3,1.55,5.45,"CONFIRMADO  (σ = 10,2)","CONF",
    "Clustering 18× maior que o aleatório porque pessoas do mesmo grupo conversam entre si (triângulos densos). Caminhos curtos porque as pontes multigrupo funcionam como atalhos entre grupos. É a receita clássica de mundo pequeno: clusters densos + poucos atalhos.",
    "Achado robusto e estável à janela temporal; mais dados apenas o reforçam.");
  s.addNotes("H1a confirmado. Clustering alto vem da conversa intra-grupo; caminhos curtos vêm das pontes. Robusto.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"H1 — Cauda pesada, mas \u201clivre de escala\u201d?",H1C);
  await fitImage(s,"rc_fig/h1b_degree.png",0.5,1.55,6.5,4.7);
  whyFixRight(s,7.3,1.55,5.45,"PARCIAL","PARC",
    "Há hubs claros (top 10% = 49,5% do grau, α ≈ 2,2, mais pesada que exponencial). Mas a lei de potência é estatisticamente indistinguível de uma lognormal (p = 0,22). A causa é poder estatístico: a rede é pequena (302 nós), então a cauda tem poucos nós de grau alto — e separar power-law de lognormal exige muitas ordens de grandeza na cauda.",
    "Entrar em mais grupos e coletar mais mensagens → rede maior → cauda mais longa, com nós de grau alto suficientes para distinguir as duas distribuições.");
  s.addNotes("H1b parcial: cauda pesada e hubs sim, mas power-law não distinguível de lognormal — por falta de poder estatístico (rede pequena). Mais dados resolveria.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"H2 — Pontes conectam os grupos",H2C);
  await fitImage(s,"rc_fig/h2_network.png",0.4,1.45,7.0,3.4);
  await fitImage(s,"rc_fig/h2_multigroup.png",7.6,1.45,5.3,3.4);
  whyFixBand(s,"CONFIRMADO","CONF",
    "77% do top-30 em intermediação são multigrupo (vs 15% de base). Faz sentido estrutural: usuários multigrupo são os únicos que ligam clusters de grupos diferentes, então caem nos caminhos mais curtos entre eles → alta intermediação.",
    "Achado estrutural robusto.");
  s.addNotes("H2 estrutural confirmado: pontes = nós multigrupo, que conectam clusters e por isso têm alta betweenness.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"H2 — As pontes disseminam conteúdo problemático",H2C);
  await fitImage(s,"rc_fig/h2_content_share.png",0.5,1.45,5.9,3.35);
  await fitImage(s,"rc_fig/h2_content_groups.png",6.7,1.45,5.9,3.35);
  whyFixBand(s,"APOIADO  (modesto)","APOIO",
    "6% dos usuários (maiores pontes) geram 20% do conteúdo problemático; correlações positivas (grupos +0,27). Entre os multigrupo estão divulgadores que repostam o mesmo conteúdo (muitas vezes problemático/comercial) em vários grupos — o que os torna pontes E disseminadores. O efeito é modesto porque nem toda ponte é divulgador.",
    "Mais mensagens por usuário e rotulagem por LLM em escala → taxa por usuário menos ruidosa e sinal mais nítido.");
  s.addNotes("H2 conteúdo apoiado (modesto): pontes concentram a disseminação (6%->20%). Mecanismo: cross-posters/divulgadores. Mais dados e rotulagem em escala afiariam o sinal.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"H3 — Não há homofilia de conteúdo",H3C);
  await fitImage(s,"rc_fig/h3_assortativity.png",0.5,1.55,6.3,4.7);
  whyFixRight(s,7.3,1.55,5.45,"NÃO SE SUSTENTA","NAO",
    "Assortatividade por conteúdo ≈ 0 (−0,04): usuários de conteúdo similar não interagem mais que o acaso. Já a assortatividade por grupo é altíssima (+0,71). A causa é a própria construção: as arestas são proximidade DENTRO do grupo, então a interação é determinada pela co-participação no grupo, não pelo conteúdo — e a estrutura de grupos \u201clava\u201d qualquer homofilia.",
    "Metadados de resposta/menção permitiriam testar a ESCOLHA (responder a quem tem conteúdo similar) — o verdadeiro teste de homofilia, que a proximidade não captura. Rótulos de conteúdo mais finos (tópicos) também ajudariam.");
  s.addNotes("H3 não se sustenta. A interação é estruturada pelo grupo (assort. 0,71), não pelo conteúdo (~0). A proximidade não captura escolha; faltam metadados de resposta para o teste real de homofilia.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"H4 — Não há preferential attachment",H4C);
  await fitImage(s,"rc_fig/h4_activity.png",0.5,1.55,6.3,4.7);
  whyFixRight(s,7.3,1.55,5.45,"NÃO SE SUSTENTA","NAO",
    "A correlação bruta entre grau prévio e crescimento é positiva (+0,31), mas é artefato de atividade: quem tem grau alto posta muito e acumula laços por isso. Ao controlar pela atividade do nó, o sinal inverte para −0,35 — bem-conectados não atraem novos laços a mais. Além disso, preferential attachment é um processo de crescimento, e a janela (~33 dias) é curta para acumular vantagem.",
    "Coletar por mais tempo → observar o crescimento real da rede, onde a vantagem cumulativa se manifestaria. Metadados de resposta permitiriam medir se novos usuários escolhem se ligar aos mais populares.");
  s.addNotes("H4 não se sustenta: o +0,31 bruto é artefato de atividade; controlando, vira -0,35. E a janela é curta para um processo de crescimento. Coletar por mais tempo e ter metadados de resposta ajudaria.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Síntese dos achados");
  const hd=(t,c)=>({text:t,options:{fill:{color:c},color:WHITE,bold:true,align:"center",valign:"middle",fontSize:12.5}});
  const cell=(t,c)=>({text:t,options:{valign:"middle",fontSize:11,color:c||"374151"}});
  const rows=[
    [hd("Hipótese","334155"),hd("Veredito","334155"),hd("Por quê (resumo)","334155"),hd("O que ajudaria","334155")],
    [{text:"H1 mundo pequeno",options:{bold:true,fontSize:11.5,color:H1C,valign:"middle"}},cell("Confirmado","047857"),cell("clusters de grupo + pontes como atalhos"),cell("robusto")],
    [{text:"H1 livre de escala",options:{bold:true,fontSize:11.5,color:H1C,valign:"middle"}},cell("Parcial","92400E"),cell("hubs sim, mas power-law ≈ lognormal (rede pequena)"),cell("mais grupos e mensagens")],
    [{text:"H2 pontes",options:{bold:true,fontSize:11.5,color:H2C,valign:"middle"}},cell("Confirmado / Apoiado","047857"),cell("multigrupo = atalhos; divulgadores repostam em vários grupos"),cell("mais msgs/usuário; LLM em escala")],
    [{text:"H3 homofilia",options:{bold:true,fontSize:11.5,color:H3C,valign:"middle"}},cell("Não se sustenta","B91C1C"),cell("interação é definida pelo grupo, não pelo conteúdo"),cell("metadados de resposta; tópicos finos")],
    [{text:"H4 pref. attachment",options:{bold:true,fontSize:11.5,color:H4C,valign:"middle"}},cell("Não se sustenta","B91C1C"),cell("correlação é artefato de atividade; janela curta"),cell("coletar por mais tempo")],
  ];
  s.addTable(rows,{x:0.5,y:1.6,w:12.3,colW:[2.3,2.3,4.6,3.1],rowH:[0.5,0.9,0.9,0.95,0.85,0.9],
    border:{pt:1,color:"E2E8F0"},valign:"middle",fontFace:BODY,fill:{color:WHITE}});
  s.addNotes("Síntese: 2 confirmadas (mundo pequeno, pontes), 1 parcial (livre de escala), 2 refutadas (homofilia, PA). Cada uma com a razão e o que melhoraria. O fio condutor das melhorias: mais dados, mais tempo, e metadados de resposta.");

  
  s=p.addSlide(); s.background={color:WHITE}; titleBar(s,"Considerações éticas e modelos generativos");
  circleIcon(s,icScale,0.6,1.55,0.9,TEAL);
  s.addText("Ética",{x:1.75,y:1.55,w:10,h:0.4,fontFace:BODY,fontSize:16,bold:true,color:TEAL,margin:0});
  s.addText([
    {text:"Dados de grupos públicos, mas de pessoas reais discutindo saúde — público potencialmente vulnerável (imagem corporal, transtornos alimentares).",options:{bullet:{code:"2022"},breakLine:true,color:"374151"}},
    {text:"Anonimização: identificadores → u0, u1…; sem telefones; conteúdo nunca vinculado a identidade nos resultados.",options:{bullet:{code:"2022"},breakLine:true,color:"374151"}},
    {text:"LGPD e termos do WhatsApp: compartilhamos apenas dados derivados anonimizados (rede/arestas) e o código — nunca as mensagens cruas.",options:{bullet:{code:"2022"},breakLine:true,color:"374151"}},
    {text:"Finalidade de bem público (entender a disseminação), sem amplificar ou expor o conteúdo problemático.",options:{bullet:{code:"2022"},color:"374151"}},
  ],{x:1.75,y:2.0,w:10.9,h:2.3,fontFace:BODY,fontSize:13,margin:0,paraSpaceAfter:5,lineSpacingMultiple:1.03});
  s.addShape(p.shapes.ROUNDED_RECTANGLE,{x:0.6,y:5.0,w:12.1,h:1.6,fill:{color:SLATE},rectRadius:0.08});
  s.addText("Modelos generativos",{x:0.85,y:5.12,w:10,h:0.4,fontFace:BODY,fontSize:15,bold:true,color:INK,margin:0});
  s.addText("Um assistente de IA foi usado como apoio à implementação (coleta e análise), à rotulagem de conteúdo (validada manualmente em amostra) e à redação. Todo o código e os resultados foram revisados e executados pelo autor.",
    {x:0.85,y:5.5,w:11.6,h:1.0,fontFace:BODY,fontSize:13,color:"374151",margin:0,valign:"top",lineSpacingMultiple:1.04});
  s.addNotes("Resolve o feedback 2 (ética não abordada). Pontos: público vulnerável, anonimização, LGPD/ToS, compartilhar só dados derivados + código, finalidade de bem público. E a divulgação do uso de modelos generativos.");

  
  s=p.addSlide(); s.background={color:NAVY};
  s.addText("Conclusão e trabalhos futuros",{x:0.7,y:0.5,w:12,h:0.8,fontFace:HEAD,fontSize:30,bold:true,color:WHITE,margin:0});
  s.addText([
    {text:"A rede é um mundo pequeno dominado por hubs",options:{bold:true,color:WHITE,breakLine:true}},
    {text:"As pontes multigrupo concentram a disseminação de conteúdo problemático (6% dos usuários → 20% do conteúdo).",options:{color:"CADCFC",breakLine:true}},
    {text:"Mas não há homofilia de conteúdo nem preferential attachment: a interação é estruturada pelo grupo e pela atividade — não por escolha de conteúdo nem por status acumulado.",options:{color:"CADCFC"}},
  ],{x:0.8,y:1.5,w:11.7,h:2.0,fontFace:BODY,fontSize:16,margin:0,lineSpacingMultiple:1.1});
  s.addText("Trabalhos futuros",{x:0.8,y:3.7,w:10,h:0.4,fontFace:BODY,fontSize:16,bold:true,color:WHITE,margin:0});
  const fut=[
    "Entrar em mais grupos e coletar por mais tempo → mais poder estatístico (H1b) e captura do crescimento real (H4).",
    "Obter metadados de resposta/menção → testar escolha: homofilia e preferential attachment reais (H3, H4).",
    "Rotulagem por LLM em escala e por tópicos → sinal de conteúdo mais nítido (H2).",
  ];
  s.addText(fut.map((t,i)=>({text:t,options:{bullet:{code:"2022"},breakLine:i<fut.length-1,color:"CADCFC"}})),
    {x:0.8,y:4.15,w:11.7,h:2.2,fontFace:BODY,fontSize:14.5,margin:0,paraSpaceAfter:8,lineSpacingMultiple:1.04});
  s.addNotes("Conclusão: mundo pequeno + hubs; pontes disseminam conteúdo problemático; sem homofilia nem PA (interação definida por grupo e atividade). Futuros: mais dados/tempo, metadados de resposta, rotulagem em escala — exatamente o que destravaria os resultados parciais/negativos.");

  await p.writeFile({fileName:"Apresentacao_RedesComplexas.pptx"});
  console.log("Deck RC gerado: Apresentacao_RedesComplexas.pptx ("+ (s?16:0) +" slides montados)");
})();
