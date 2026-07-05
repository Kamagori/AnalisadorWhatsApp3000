# Redes de interação em grupos de WhatsApp sobre saúde e emagrecimento

Análise de redes complexas da interação entre usuários de grupos públicos de WhatsApp voltados a saúde e emagrecimento, com foco na disseminação de conteúdo problemático. Projeto da disciplina INF 791 (Redes Complexas) - UFV.

Autor: Marcos Biscotto de Oliveira

## Visão geral

A partir das mensagens coletadas, constrói-se uma rede dirigida e ponderada em que os nós são usuários e as arestas representam proximidade conversacional temporal. Sobre essa rede, testam-se quatro hipóteses: estrutura de mundo pequeno e distribuição de grau (H1), papel das pontes na disseminação de conteúdo problemático (H2), homofilia de conteúdo (H3) e anexação preferencial (H4). O conteúdo das mensagens é rotulado por um léxico validado por amostragem.

## Arquivos

- `wazap_network.py` - módulo base: constrói a rede de proximidade a partir de `coleta.db`; expõe `load_network` e `proximity_events`. É importado pelos demais scripts.
- `lexico.py` - mede a prevalência de termos candidatos no corpus; usado para definir o léxico de conteúdo (o resultado já está embutido em `analise_conteudo.py`).
- `analise_estrutura.py` - H1 (mundo pequeno e distribuição de grau), H2 estrutural e H4; gera `coleta_network.graphml`.
- `teste_h4.py` - teste detalhado de anexação preferencial, separando atividade de atração de novos laços.
- `analise_conteudo.py` - rotulagem de conteúdo e perfis por usuário; gera `content_profiles.json`.
- `h2_e_h3.py` - H2 de conteúdo e H3; consome `content_profiles.json`.
- `fazer_figuras_estruturais.py`, `fazer_figuras_apresentacao.py` - geração das figuras (salvas em `rc_fig/`); `fazer_figuras_apresentacao.py` consome `content_profiles.json`.
- `build_deck_rc.js` - geração da apresentação (Node.js); consome as figuras de `rc_fig/`.

## Dependências

Python (análise e figuras):

```
pip install -r requirements.txt
```

Node.js (apresentação, opcional):

```
npm install pptxgenjs react-icons react react-dom sharp
```

## Uso

Coloque o banco `coleta.db` no diretório do projeto. Os scripts compartilham o módulo `wazap_network.py` e trocam dados por dois arquivos intermediários (`content_profiles.json` e as figuras em `rc_fig/`), então a ordem abaixo respeita essas dependências.

Preparação do léxico (opcional - o léxico já está embutido em `analise_conteudo.py`):

```
python build_lexicon.py
```

Análise:

```
python analise_estrutura.py     # H1, H2 estrutural, H4
python teste_h4.py              # H4 detalhado, com controle de atividade
python analise_conteudo.py      # rotulagem -> content_profiles.json
python h2_e_h3.py               # H2 de conteúdo e H3 (requer content_profiles.json)
```

Figuras:

```
python fazer_figuras_estruturais.py       # figuras estruturais -> rc_fig/
python fazer_figuras_apresentacao.py      # figuras de conteúdo (requer content_profiles.json)
```

Apresentação (opcional, requer as figuras já geradas):

```
node build_deck_rc.js
```

## Dados

O banco `coleta.db` não é distribuído neste repositório: contém mensagens reais de grupos públicos, e os Termos de Serviço do WhatsApp, assim como a LGPD, restringem a redistribuição de dados de usuários. São compartilhados apenas artefatos derivados e anonimizados.
