# Redes de interação em grupos de WhatsApp sobre saúde e emagrecimento

Análise de redes complexas da interação entre usuários de grupos públicos de WhatsApp voltados a saúde e emagrecimento, com foco na disseminação de conteúdo problemático. Projeto da disciplina INF 791 (Redes Complexas) - UFV.

Autor: Marcos Biscotto de Oliveira

## Visão geral

A partir das mensagens coletadas, constrói-se uma rede dirigida e ponderada em que os nós são usuários e as arestas representam proximidade conversacional temporal. Sobre essa rede, testam-se quatro hipóteses: estrutura de mundo pequeno e distribuição de grau (H1), papel das pontes na disseminação de conteúdo problemático (H2), homofilia de conteúdo (H3) e anexação preferencial (H4). O conteúdo das mensagens é rotulado por um léxico validado por amostragem.

## Arquivos

- `wazap_network.py` - construção da rede de proximidade a partir do banco `coleta.db`; expõe `load_network` e `proximity_events`.
- `analise_estrutura.py` - H1 (mundo pequeno e distribuição de grau), H2 estrutural e H4.
- `teste_h4.py` - teste de anexação preferencial com controle de atividade.
- `lexico.py` - medição de prevalência de termos para o léxico de conteúdo.
- `analise_conteudo.py` - rotulagem de conteúdo e perfis por usuário.
- `h2_e_h3.py` - H2 de conteúdo e H3.
- `fazedor_de_figuras.py`, `conteudo_para_figuras.py` - geração das figuras.
- `build_deck_rc.js` - geração da apresentação (Node.js).

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

Coloque o banco `coleta.db` no diretório do projeto e execute:

```
python wa_network.py
python analyze_structure.py
python content_analysis.py
python h2h3.py
python make_figures_rc.py
python make_content_figures.py
```

## Dados

O banco `coleta.db` não é distribuído neste repositório: contém mensagens reais de grupos públicos, e os Termos de Serviço do WhatsApp, assim como a LGPD, restringem a redistribuição de dados de usuários. São compartilhados apenas artefatos derivados e anonimizados.
