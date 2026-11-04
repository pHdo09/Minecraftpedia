----Minecraftpédia

Wiki navegável do banco de dados de Minecraft criado em Banco de Dados I.
Cada artigo (mob, item, bloco, etc.) é montado em tempo real
com consultas que juntam várias tabelas (JOIN, GROUP BY, subconsultas). Há busca global que ignora
acentos, filtros, links entre artigos, receitas com grade de crafting e uma página de estatísticas.

**Tecnologias:** Streamlit (Community Cloud), Python, PostgreSQL no Neon, psycopg2, pandas.

- **Grupo:** Pedro Henrique Ito Rocha, Felipe Tatsuyuki Matsuo, Gustavo Henrique de Oliveira Magalhães, Guilherme Bisse.

----Arquitetura
```
Navegador  →  Streamlit Community Cloud (app.py)  →  Neon (PostgreSQL)
```
O app se conecta direto ao banco usando a `DATABASE_URL`, guardada nos *Secrets* do Streamlit.
----Banco de dados (rodar uma vez, no seu computador)
1. Crie um projeto no [Neon](https://neon.tech) e copie a connection string (botão **Connect**).
2. No terminal, dentro desta pasta:
   ```bash
   pip install -r requirements.txt
   # PowerShell:  $env:DATABASE_URL="postgresql://...?sslmode=require"
   # Mac/Linux:   export DATABASE_URL="postgresql://...?sslmode=require"
   python setup_db.py
   ```
----Rodar localmente
```bash
# com a DATABASE_URL definida, ou em .streamlit/secrets.toml (copie o .example)
streamlit run app.py
```
----Estrutura
```
app.py                     aplicação Streamlit
setup_db.py                cria e popula o banco (rodar localmente)
requirements.txt           dependências
.streamlit/config.toml     tema
sql/SQL_MINECRAFT.sql      DDL (modelo relacional de BD I, já com resultado, tempo opcional e combustível nas receitas)
sql/POPULATE_MINECRAFT.sql dados de exemplo (inclui o catálogo de itens e as 34 receitas por estação)
```
