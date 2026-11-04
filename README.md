# Minecraftpédia

Wiki navegável do banco de dados de Minecraft criado em Banco de Dados I.
Cada artigo (mob, item, bloco, bioma, dimensão, jogador, efeito, receita) é montado em tempo real
com consultas que juntam várias tabelas (JOIN, GROUP BY, subconsultas). Há busca global que ignora
acentos, filtros, links entre artigos, receitas com grade de crafting e uma página de estatísticas.

**Tecnologias:** Streamlit (Community Cloud), Python, PostgreSQL no Neon, psycopg2, pandas.

- **Aplicação:** _cole aqui o link do Streamlit_
- **Código:** _cole aqui o link do GitHub_
- **Grupo:** _nomes_

## Arquitetura
```
Navegador  →  Streamlit Community Cloud (app.py)  →  Neon (PostgreSQL)
```
O app se conecta direto ao banco usando a `DATABASE_URL`, guardada nos *Secrets* do Streamlit
(nunca no código nem no GitHub).

## Banco de dados (rodar uma vez, no seu computador)
1. Crie um projeto no [Neon](https://neon.tech) e copie a connection string (botão **Connect**).
2. No terminal, dentro desta pasta:
   ```bash
   pip install -r requirements.txt
   # PowerShell:  $env:DATABASE_URL="postgresql://...?sslmode=require"
   # Mac/Linux:   export DATABASE_URL="postgresql://...?sslmode=require"
   python setup_db.py
   ```
   O script recria e popula as 27 tabelas. Pode rodar de novo quando quiser (apaga e recria).

## Rodar localmente
```bash
# com a DATABASE_URL definida, ou em .streamlit/secrets.toml (copie o .example)
streamlit run app.py
```

## Deploy no Streamlit Community Cloud
1. Suba a pasta para um repositório **público** no GitHub (o `.gitignore` já protege o `secrets.toml`).
2. Em https://share.streamlit.io entre com o GitHub e clique em **Create app**.
3. Escolha o repositório, a branch `main` e o arquivo principal `app.py`.
4. Em **Advanced settings**, cole nos *Secrets*:
   ```toml
   DATABASE_URL = "postgresql://usuario:senha@host/banco?sslmode=require"
   ```
5. Clique em **Deploy**. Em alguns minutos o link público fica pronto.

Observações:
- Apps parados por um tempo "dormem" no Community Cloud. Abra o link antes da apresentação; se aparecer o
  botão de acordar, clique nele. O Neon também suspende quando fica ocioso, então o primeiro acesso pode
  demorar alguns segundos (o app reconecta sozinho).
- Se mudar os dados no banco, a wiki pode levar até 5 minutos para refletir (cache). Use *Clear cache* (tecla `C`).
- Para alterar os Secrets depois: painel do app → **Settings → Secrets**.

## Estrutura
```
app.py                     aplicação Streamlit
setup_db.py                cria e popula o banco (rodar localmente)
requirements.txt           dependências
.streamlit/config.toml     tema
sql/SQL_MINECRAFT.sql      DDL (modelo relacional de BD I, já com resultado, tempo opcional e combustível nas receitas)
sql/POPULATE_MINECRAFT.sql dados de exemplo (inclui o catálogo de itens e as 34 receitas por estação)
```
`setup_db.py` converte nomes de tabelas e colunas para minúsculas sem acento (`INVENTÁRIO` → `inventario`),
porque o PostgreSQL trata identificadores acentuados sem aspas de forma inconsistente. Os dados não mudam.
O DDL e o POPULATE também podem ser executados diretamente no pgAdmin ou no editor SQL do Neon, mas nesse caso é preciso
remover os acentos dos nomes de tabelas e colunas. Por isso o caminho recomendado é o `setup_db.py`.
