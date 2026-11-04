import html
import os
import random
import unicodedata
from functools import partial

import pandas as pd
import psycopg2
import psycopg2.extras
import streamlit as st

st.set_page_config(page_title="Minecraftpédia", page_icon="⛏️", layout="wide")

# ──────────────────────────── Estilo ────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Silkscreen:wght@400;700&display=swap');
h1 { font-family:'Press Start 2P',monospace !important; font-size:1.45rem !important; line-height:1.6 !important;
     border-bottom:4px solid #4c7a2b; padding-bottom:.7rem !important; }
h2, h3 { font-family:'Silkscreen',monospace !important; border-bottom:2px solid #9aa59a; padding-bottom:.25rem; }
.stButton > button { border-radius:0; border:2px solid #1f2420; background:#f7f8f5; box-shadow:3px 3px 0 #1f2420;
     transition:transform .08s, box-shadow .08s; }
.stButton > button:hover { transform:translate(2px,2px); box-shadow:1px 1px 0 #1f2420; border-color:#1f2420; color:#1f2420; }
.ib { border:3px solid #1f2420; background:#f7f8f5; box-shadow:5px 5px 0 #1f2420; margin-bottom:1.2rem; }
.ib-t { background:#4c7a2b; color:#fff; font-family:'Silkscreen',monospace; font-size:1.2rem; text-align:center; padding:.55rem .4rem; }
.ib-s { background:#7a5233; color:#f7f8f5; text-align:center; padding:.25rem; font-size:.88rem; }
.ib table { width:100%; border-collapse:collapse; margin:0; }
.ib th { text-align:left; font-weight:600; padding:.3rem .6rem; width:46%; border-top:1px solid #c5ccc2; vertical-align:top; }
.ib td { padding:.3rem .6rem; border-top:1px solid #c5ccc2; }
.grade { display:grid; grid-template-columns:repeat(3,92px); gap:0; width:max-content; background:#c6c6c6; padding:6px;
         border:3px solid #1f2420; margin:.4rem 0 1rem; }
.slot { background:#8b8b8b; border:3px solid; border-color:#373737 #fff #fff #373737; height:92px; display:flex;
        flex-direction:column; align-items:center; justify-content:center; font-size:.72rem; text-align:center;
        color:#fff; text-shadow:1px 1px 0 #3f3f3f; line-height:1.15; padding:2px; }
.slot b { font-family:'Silkscreen',monospace; font-size:.9rem; }
.linha { display:flex; align-items:center; gap:14px; flex-wrap:wrap; margin:.4rem 0 1rem; }
.linha .grade { margin:0; }
.coluna { display:flex; flex-direction:column; gap:6px; }
.coluna .grade { margin:0; }
.slot.comb { background:#7a5233; }
.seta { font-family:'Silkscreen',monospace; font-size:1.6rem; }
.lead { font-size:1.08rem; line-height:1.65; max-width:70ch; }
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────── Banco de dados ────────────────────────────
def _dsn():
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        try:
            dsn = st.secrets["DATABASE_URL"]
        except Exception:
            dsn = None
    return dsn


@st.cache_resource(ttl=600, show_spinner=False)
def _conexao():
    """Uma conexão reaproveitada entre as consultas (o Neon "dorme" quando fica parado)."""
    conn = psycopg2.connect(_dsn(), connect_timeout=30, keepalives=1, keepalives_idle=30,
                            keepalives_interval=10, keepalives_count=5)
    conn.autocommit = True
    return conn


@st.cache_data(ttl=300, show_spinner=False)
def q(sql, params=()):
    """Executa uma consulta e devolve uma lista de dicionários (cache de 5 min).
    Se a conexão tiver caído (ex.: Neon suspenso), reconecta e tenta de novo uma vez."""
    for tentativa in (1, 2):
        try:
            with _conexao().cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, params)
                return [dict(r) for r in cur.fetchall()]
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            _conexao.clear()
            if tentativa == 2:
                raise


def one(sql, params=()):
    r = q(sql, params)
    return r[0] if r else None


# ──────────────────────────── Utilidades ────────────────────────────
LABELS = {
    "nome": "Nome", "vida": "Vida", "dano_base": "Dano base", "folego": "Fôlego", "velocidade": "Velocidade",
    "classe_mob": "Classe", "taxa_de_spawn": "Taxa de spawn", "taxa_de_geracao": "Taxa de geração",
    "bioma": "Bioma", "dimensao": "Dimensão", "mundo": "Mundo", "jogador": "Jogador", "mob": "Mob",
    "item": "Item", "bloco": "Bloco", "raridade": "Raridade", "quantidade": "Quantidade", "numero_slot": "Slot",
    "inventario": "Inventário", "classe_inventario": "Tipo de inventário", "numero_de_slots": "Slots",
    "expansivel": "Expansível", "coordenadas_bau": "Coordenadas", "coordenadas": "Coordenadas",
    "data_domesticacao": "Data de domesticação", "name_tag": "Name tag", "tipo_do_portal": "Tipo de portal",
    "receita": "Receita", "tipo_de_crafting": "Tipo de crafting", "tempo_para_o_crafting": "Tempo (s)",
    "posicao_slot": "Posição", "estrutura": "Estrutura", "variante": "Variante", "extensao": "Extensão",
    "temperatura": "Temperatura", "altitude_media": "Altitude média", "tipo_de_precipitacao": "Precipitação",
    "durabilidade": "Durabilidade", "condicao_de_quebra": "Condição de quebra", "experiencia": "Experiência",
    "nivel": "Nível", "tipo_de_efeito": "Tipo", "tempo_de_efeito": "Duração", "categoria": "Categoria",
    "classes": "Classes", "dificuldade": "Dificuldade", "modo": "Modo", "nome_mundo": "Mundo",
    "data_de_criacao": "Data de criação", "entidade": "Entidade", "quebravel": "Quebrável", "dropavel": "Dropável",
    "tipo": "Tipo", "detalhe": "Detalhe", "id_inventario": "Inventário", "pode_dormir": "Pode dormir",
    "ingredientes": "Ingredientes", "nickname": "Nickname", "armadura": "Armadura", "biomas": "Biomas",
    "hitbox": "Hitbox", "spawn_total": "Taxa de spawn total", "mobs": "Mobs", "vida_media": "Vida média",
    "mobs_domesticados": "Mobs domesticados", "mundos": "Mundos", "item_resultado": "Produz",
    "quantidade_resultado": "Qtd. produzida", "receitas": "Receitas", "combustivel": "Combustível",
}
KIND_LABEL = {"mob": "Mob", "item": "Item", "bloco": "Bloco", "bioma": "Bioma", "dimensao": "Dimensão",
              "jogador": "Jogador", "efeito": "Efeito", "receita": "Receita"}
SECAO = {"mob": "Mobs", "item": "Itens", "bloco": "Blocos", "bioma": "Biomas", "dimensao": "Mundos e dimensões",
         "jogador": "Jogadores", "efeito": "Efeitos", "receita": "Receitas"}
SECOES = ["Início", "Mobs", "Itens", "Blocos", "Biomas", "Mundos e dimensões", "Jogadores", "Efeitos",
          "Receitas", "Estruturas", "Estatísticas"]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").lower()


def esc(v):
    return html.escape(str(v))


def fmt(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "—"
    if isinstance(v, bool):
        return "Sim" if v else "Não"
    return esc(v)


def sim(v):
    return None if v is None else bool(v)


# ──────────────────────────── Navegação ────────────────────────────
def abrir(kind, nome):
    st.session_state.entidade = (kind, nome)
    st.session_state.nav = SECAO[kind]
    st.session_state.busca = ""


def fechar():
    st.session_state.entidade = None


def trocar_secao():
    st.session_state.entidade = None
    st.session_state.busca = ""


def ir(secao):
    st.session_state.nav = secao
    st.session_state.entidade = None
    st.session_state.busca = ""


def _pick(key, targets):
    sel = st.session_state[key].selection.rows
    if sel and targets[sel[0]] and targets[sel[0]][1] is not None:
        abrir(*targets[sel[0]])


def tabela(rows, name_col=None, kind=None, targets=None, key="tab"):
    """Mostra uma tabela. Se houver destino, clicar em uma linha abre o artigo."""
    if not rows:
        st.caption("Nenhum registro relacionado.")
        return
    d = pd.DataFrame(rows)
    if targets is None and kind and name_col:
        targets = [(kind, n if pd.notna(n) else None) for n in d[name_col]]
    d = d.rename(columns=lambda c: LABELS.get(c, c.replace("_", " ").capitalize()))
    if targets:
        st.dataframe(d, hide_index=True, width="stretch", key=key, selection_mode="single-row",
                     on_select=partial(_pick, key, targets))
    else:
        st.dataframe(d, hide_index=True, width="stretch")


def chips(kind, nomes, ctx):
    nomes = [n for n in nomes if n]
    if not nomes:
        return
    cols = st.columns(min(len(nomes), 5))
    for i, n in enumerate(nomes):
        cols[i % len(cols)].button(n, key=f"chip_{ctx}_{kind}_{n}", on_click=abrir, args=(kind, n))


def infobox(titulo, subtitulo, linhas):
    h = f"<div class='ib'><div class='ib-t'>{esc(titulo)}</div><div class='ib-s'>{esc(subtitulo)}</div><table>"
    for k, v in linhas:
        h += f"<tr><th>{esc(k)}</th><td>{fmt(v)}</td></tr>"
    st.markdown(h + "</table></div>", unsafe_allow_html=True)


def topo(kind):
    st.button(f"← Voltar para {SECAO[kind]}", on_click=fechar, key=f"voltar_{kind}")
    return st.columns([2.2, 1], gap="large")


def sub(titulo):
    st.markdown(f"### {titulo}")


def lead(texto):
    st.markdown(f"<p class='lead'>{texto}</p>", unsafe_allow_html=True)


def nao_encontrado(nome):
    st.warning(f"Não encontramos o artigo “{nome}”.")
    st.button("Voltar ao índice", on_click=fechar, key="nf_voltar")


# ──────────────────────────── Artigos ────────────────────────────
def art_mob(nome):
    m = one("""
        SELECT m.*,
               h.sensibilidade_ao_sol, h.spawn_no_escuro, h.barra_de_vida_visivel, h.e_boss,
               p.comportamento_de_fuga, p.montavel,
               COALESCE(p.domesticavel, n.domesticavel) AS domesticavel, n.sofreu_ataque
        FROM tipo_mob m
        LEFT JOIN tipo_mob_hostil h ON h.nome = m.nome
        LEFT JOIN tipo_mob_pacifico p ON p.nome = m.nome
        LEFT JOIN tipo_mob_neutro n ON n.nome = m.nome
        WHERE m.nome = %s""", (nome,))
    if not m:
        return nao_encontrado(nome)
    biomas = q("""SELECT g.bioma, b.dimensao, b.temperatura, g.taxa_de_spawn
                  FROM geracao_mob_bioma g JOIN tipo_bioma b ON b.nome = g.bioma
                  WHERE g.mob = %s ORDER BY g.taxa_de_spawn DESC""", (nome,))
    dims = q("""SELECT g.dimensao, mu.nome AS nome_mundo, g.taxa_de_spawn
                FROM geracao_mob_dimensao g
                JOIN dimensao d ON d.nome = g.dimensao JOIN mundo mu ON mu.save = d.mundo
                WHERE g.mob = %s ORDER BY g.taxa_de_spawn DESC""", (nome,))
    doms = q("""SELECT d.data_domesticacao, d.name_tag, d.coordenadas, d.jogador, mu.nome AS nome_mundo
                FROM domesticacao_mob d JOIN jogador j ON j.nickname = d.jogador
                LEFT JOIN mundo mu ON mu.jogador = j.nickname
                WHERE d.mob = %s ORDER BY d.data_domesticacao""", (nome,))
    esq, dir_ = topo("mob")
    extra = {
        "Hostil": [("Sensível ao sol", "sensibilidade_ao_sol"), ("Nasce no escuro", "spawn_no_escuro"),
                   ("Barra de vida visível", "barra_de_vida_visivel"), ("É chefe", "e_boss")],
        "Pacífico": [("Domesticável", "domesticavel"), ("Foge do jogador", "comportamento_de_fuga"),
                     ("Montável", "montavel")],
        "Neutro": [("Domesticável", "domesticavel"), ("Já sofreu ataque", "sofreu_ataque")],
    }
    with dir_:
        linhas = [("Classe", m["classe_mob"]), ("Vida", m["vida"]), ("Dano base", m["dano_base"]),
                  ("Armadura", m["armadura"]), ("Velocidade", m["velocidade"]), ("Pulo", m["pulo"]),
                  ("Hitbox", m["hitbox"]), ("Fôlego", m["folego"]), ("XP dropável", m["xp_dropavel"]),
                  ("Raio de detecção", m["raio_de_deteccao"]), ("Procurável", m["prociavel"]),
                  ("Carrega item", sim(m["item_carregavel"]))]
        linhas += [(r, m[c]) for r, c in extra.get(m["classe_mob"], [])]
        infobox(nome, f"Mob {m['classe_mob'].lower()}", linhas)
    with esq:
        st.title(nome)
        t = (f"<b>{esc(nome)}</b> é um mob <b>{esc(m['classe_mob'].lower())}</b> com <b>{m['vida']}</b> pontos "
             f"de vida e velocidade {m['velocidade']}. ")
        t += f"Causa {m['dano_base']} de dano base. " if m["dano_base"] else "Não causa dano direto. "
        if biomas:
            t += (f"Nasce em {len(biomas)} bioma(s), principalmente em <b>{esc(biomas[0]['bioma'])}</b> "
                  f"(taxa {biomas[0]['taxa_de_spawn']}). ")
        if doms:
            t += f"Já foi domesticado {len(doms)} vez(es) pelos jogadores."
        lead(t)
        sub("Onde aparece")
        st.markdown("**Biomas**")
        tabela(biomas, "bioma", "bioma", key=f"mob_{nome}_b")
        st.markdown("**Dimensões**")
        tabela(dims, "dimensao", "dimensao", key=f"mob_{nome}_d")
        sub("Domesticações")
        tabela(doms, "jogador", "jogador", key=f"mob_{nome}_j")


def art_item(nome):
    i = one("""
        SELECT i.*, e.tipo_de_efeito, e.tempo_de_efeito, c.lancavel, c.fome_recuperada,
               d.durabilidade, d.equipavel,
               CASE WHEN c.nome IS NOT NULL THEN 'Consumível'
                    WHEN d.nome IS NOT NULL THEN 'Desgastável' ELSE 'Item comum' END AS categoria
        FROM tipo_item i
        LEFT JOIN efeito e ON e.nome = i.efeito_nome AND e.nivel = i.nivel
        LEFT JOIN tipo_item_consumivel c ON c.nome = i.nome
        LEFT JOIN tipo_item_desgastavel d ON d.nome = i.nome
        WHERE i.nome = %s""", (nome,))
    if not i:
        return nao_encontrado(nome)
    classes = [r["classe_item"] for r in q("SELECT classe_item FROM item_classe WHERE nome = %s", (nome,))]
    feita_por = q("""SELECT receita, tipo_de_crafting, quantidade_resultado, tempo_para_o_crafting
                     FROM receita_crafting WHERE item_resultado = %s ORDER BY receita""", (nome,))
    receitas = q("""SELECT ci.receita, r.item_resultado, r.tipo_de_crafting, ci.quantidade, ci.combustivel
                    FROM crafting_item ci JOIN receita_crafting r ON r.receita = ci.receita
                    WHERE ci.item = %s ORDER BY ci.receita""", (nome,))
    slots = q("""SELECT s.inventario, inv.classe_inventario, s.numero_slot, s.quantidade, j.nickname AS jogador
                 FROM slot_inventario s JOIN inventario inv ON inv.id_inventario = s.inventario
                 LEFT JOIN jogador j ON j.inventario = s.inventario
                 WHERE s.item = %s ORDER BY s.inventario""", (nome,))
    drops = q("""SELECT nome AS entidade, data_de_criacao, quebravel, hitbox
                 FROM entidade_dinamica WHERE item = %s ORDER BY data_de_criacao""", (nome,))
    esq, dir_ = topo("item")
    with dir_:
        linhas = [("Raridade", i["raridade"]), ("Categoria", i["categoria"]), ("Dano base", i["dano_base"]),
                  ("Área de ataque", i["area_de_ataque"]), ("Repulsão", i["repulsao"]),
                  ("Pilha máxima", i["pilha_maxima"])]
        if i["efeito_nome"]:
            linhas += [("Efeito", f"{i['efeito_nome']} (nível {i['nivel']})"), ("Duração do efeito", i["tempo_de_efeito"])]
        if i["categoria"] == "Consumível":
            linhas += [("Lançável", i["lancavel"]), ("Fome recuperada", i["fome_recuperada"])]
        if i["categoria"] == "Desgastável":
            linhas += [("Durabilidade", i["durabilidade"]), ("Equipável", i["equipavel"])]
        infobox(nome, f"Item {i['raridade'].lower()}", linhas)
    with esq:
        st.title(nome)
        t = f"<b>{esc(nome)}</b> é um item <b>{esc(i['raridade'].lower())}</b> ({esc(i['categoria'].lower())}). "
        if classes:
            t += f"Pertence à classe {esc(', '.join(classes))}. "
        if i["categoria"] == "Consumível":
            t += (f"Recupera {i['fome_recuperada']} de fome. " if i["fome_recuperada"]
                  else ("Pode ser lançado. " if i["lancavel"] else ""))
        if i["categoria"] == "Desgastável":
            t += f"Aguenta {i['durabilidade']} usos. "
        if i["efeito_nome"]:
            t += f"Concede o efeito <b>{esc(i['efeito_nome'])}</b> por {i['tempo_de_efeito']} ticks."
        lead(t)
        sub("Como fabricar")
        tabela(feita_por, "receita", "receita", key=f"item_{nome}_f")
        sub("Receitas que usam este item")
        tabela(receitas, "receita", "receita", key=f"item_{nome}_r")
        sub("Inventários onde está guardado")
        tabela(slots, "jogador", "jogador", key=f"item_{nome}_s")
        sub("Entidades dropadas no mundo")
        tabela(drops, key=f"item_{nome}_d")
        if i["efeito_nome"]:
            sub("Veja também")
            st.caption("Efeito associado")
            chips("efeito", [i["efeito_nome"]], f"item_{nome}")


def art_bloco(nome):
    b = one("SELECT * FROM tipo_bloco WHERE nome = %s", (nome,))
    if not b:
        return nao_encontrado(nome)
    gen = q("""SELECT g.bioma, bi.dimensao, bi.temperatura, g.taxa_de_geracao
               FROM geracao_bloco_bioma g JOIN tipo_bioma bi ON bi.nome = g.bioma
               WHERE g.bloco = %s ORDER BY g.taxa_de_geracao DESC""", (nome,))
    slot = q("""SELECT s.inventario, inv.classe_inventario, s.numero_slot, s.item, s.quantidade
                FROM slot_inventario s JOIN inventario inv ON inv.id_inventario = s.inventario
                WHERE s.numero_slot = %s AND s.inventario = %s""", (b["numero_slot"], b["inventario"]))
    esq, dir_ = topo("bloco")
    with dir_:
        infobox(nome, "Bloco", [
            ("Durabilidade", b["durabilidade"]), ("Condição de quebra", b["condicao_de_quebra"]),
            ("Hitbox", b["hitbox"]), ("Dropável", b["dropavel"]), ("Interagível", b["interagivel"]),
            ("Quebrável", b["quebravel"]), ("Coletável", b["coletavel"]),
            ("Slot de referência", f"Slot {b['numero_slot']} do inventário {b['inventario']}")])
    with esq:
        st.title(nome)
        t = (f"<b>{esc(nome)}</b> é um bloco com durabilidade <b>{b['durabilidade']}</b>"
             f"{' e pode ser quebrado' if b['quebravel'] else ' e não pode ser quebrado'}"
             f"{', soltando item ao ser destruído' if b['dropavel'] else ''}. ")
        if gen:
            t += f"Gera-se naturalmente em <b>{esc(gen[0]['bioma'])}</b> (taxa {gen[0]['taxa_de_geracao']})."
        else:
            t += "Não é gerado naturalmente em nenhum bioma cadastrado."
        lead(t)
        sub("Onde é gerado")
        tabela(gen, "bioma", "bioma", key=f"bloco_{nome}_g")
        sub("Slot de inventário associado")
        tabela(slot, "item", "item", key=f"bloco_{nome}_s")


def art_bioma(nome):
    b = one("""SELECT b.*, d.aparencia_visual, d.pode_dormir, mu.nome AS nome_mundo, mu.dificuldade, mu.jogador
               FROM tipo_bioma b JOIN dimensao d ON d.nome = b.dimensao JOIN mundo mu ON mu.save = d.mundo
               WHERE b.nome = %s""", (nome,))
    if not b:
        return nao_encontrado(nome)
    est = q("SELECT nome AS estrutura, variante, extensao FROM tipo_estrutura WHERE bioma = %s ORDER BY nome", (nome,))
    mobs = q("""SELECT g.mob, m.classe_mob, m.vida, g.taxa_de_spawn
                FROM geracao_mob_bioma g JOIN tipo_mob m ON m.nome = g.mob
                WHERE g.bioma = %s ORDER BY g.taxa_de_spawn DESC""", (nome,))
    blocos = q("""SELECT g.bloco, t.durabilidade, g.taxa_de_geracao
                  FROM geracao_bloco_bioma g JOIN tipo_bloco t ON t.nome = g.bloco
                  WHERE g.bioma = %s ORDER BY g.taxa_de_geracao DESC""", (nome,))
    esq, dir_ = topo("bioma")
    with dir_:
        infobox(nome, f"Bioma de {b['dimensao']}", [
            ("Dimensão", b["dimensao"]), ("Mundo", b["nome_mundo"]), ("Jogador", b["jogador"]),
            ("Altitude média", b["altitude_media"]), ("Temperatura", b["temperatura"]),
            ("Precipitação", b["tipo_de_precipitacao"]), ("Cor da folhagem", b["cor_da_folhagem"]),
            ("Cor da água", b["cor_da_agua"]), ("Dificuldade do mundo", b["dificuldade"])])
    with esq:
        st.title(nome)
        t = (f"<b>{esc(nome)}</b> é um bioma de altitude média <b>{b['altitude_media']}</b> e temperatura "
             f"<b>{b['temperatura']}</b>, com precipitação do tipo {esc((b['tipo_de_precipitacao'] or 'nenhuma').lower())}. "
             f"Fica na dimensão <b>{esc(b['dimensao'])}</b>, do mundo “{esc(b['nome_mundo'])}”. ")
        if est:
            t += f"Abriga {len(est)} estrutura(s), como {esc(est[0]['estrutura'])}."
        lead(t)
        sub("Estruturas")
        tabela(est, key=f"bioma_{nome}_e")
        sub("Mobs que nascem aqui")
        tabela(mobs, "mob", "mob", key=f"bioma_{nome}_m")
        sub("Blocos gerados")
        tabela(blocos, "bloco", "bloco", key=f"bioma_{nome}_b")
        sub("Veja também")
        st.caption("Dimensão e jogador")
        chips("dimensao", [b["dimensao"]], f"bioma_{nome}")
        chips("jogador", [b["jogador"]], f"bioma_{nome}")


def art_dimensao(nome):
    d = one("""SELECT d.*, mu.seed, mu.nome AS nome_mundo, mu.dificuldade, mu.modo, mu.tipo AS tipo_mundo,
                      mu.permitir_comandos, mu.gerar_estruturas, mu.jogador
               FROM dimensao d JOIN mundo mu ON mu.save = d.mundo WHERE d.nome = %s""", (nome,))
    if not d:
        return nao_encontrado(nome)
    portais = q("SELECT tipo_do_portal, coordenadas FROM dimensao_portal WHERE dimensao = %s", (nome,))
    mobs = q("""SELECT g.mob, m.classe_mob, g.taxa_de_spawn FROM geracao_mob_dimensao g
                JOIN tipo_mob m ON m.nome = g.mob WHERE g.dimensao = %s ORDER BY g.taxa_de_spawn DESC""", (nome,))
    biomas = q("SELECT nome AS bioma, temperatura, altitude_media FROM tipo_bioma WHERE dimensao = %s", (nome,))
    baus = q("""SELECT b.tipo_bau AS id_inventario, i.classe_inventario, i.numero_de_slots, b.expansivel, b.coordenadas_bau
                FROM inventario_bau b JOIN inventario i ON i.id_inventario = b.tipo_bau
                WHERE b.nome = %s""", (nome,))
    esq, dir_ = topo("dimensao")
    with dir_:
        infobox(nome, f"Dimensão de “{d['nome_mundo']}”", [
            ("Mundo", d["nome_mundo"]), ("Jogador", d["jogador"]), ("Seed", d["seed"]),
            ("Dificuldade", d["dificuldade"]), ("Modo", d["modo"]), ("Tipo de mundo", d["tipo_mundo"]),
            ("Comandos permitidos", d["permitir_comandos"]), ("Gera estruturas", d["gerar_estruturas"]),
            ("Aparência", d["aparencia_visual"]), ("Pode dormir", d["pode_dormir"])])
    with esq:
        st.title(nome)
        lead(f"<b>{esc(nome)}</b> é a dimensão do mundo <b>{esc(d['nome_mundo'])}</b>, jogado por "
             f"<b>{esc(d['jogador'])}</b> em modo {esc(d['modo'].lower())} e dificuldade {esc(d['dificuldade'].lower())}. "
             f"Tem {len(biomas)} bioma(s), {len(portais)} portal(is) e {len(baus)} baú(s) cadastrado(s).")
        sub("Biomas")
        tabela(biomas, "bioma", "bioma", key=f"dim_{nome}_b")
        sub("Mobs que nascem na dimensão")
        tabela(mobs, "mob", "mob", key=f"dim_{nome}_m")
        sub("Portais")
        tabela(portais, key=f"dim_{nome}_p")
        sub("Baús")
        tabela(baus, key=f"dim_{nome}_c")
        sub("Veja também")
        st.caption("Jogador do mundo")
        chips("jogador", [d["jogador"]], f"dim_{nome}")


def art_jogador(nome):
    j = one("""SELECT j.*, e.tipo_de_efeito, e.tempo_de_efeito, inv.numero_de_slots, ij.slot_hotbar_selecionado,
                      mu.nome AS nome_mundo, mu.modo, mu.dificuldade, d.nome AS dimensao
               FROM jogador j
               LEFT JOIN efeito e ON e.nome = j.efeito AND e.nivel = j.nivel
               JOIN inventario inv ON inv.id_inventario = j.inventario
               LEFT JOIN inventario_jogador ij ON ij.id_inventario = j.inventario
               LEFT JOIN mundo mu ON mu.jogador = j.nickname
               LEFT JOIN dimensao d ON d.mundo = mu.save
               WHERE j.nickname = %s""", (nome,))
    if not j:
        return nao_encontrado(nome)
    itens = q("""SELECT s.numero_slot, s.item, ti.raridade, s.quantidade
                 FROM slot_inventario s JOIN tipo_item ti ON ti.nome = s.item
                 WHERE s.inventario = %s ORDER BY s.numero_slot""", (j["inventario"],))
    mobs = q("""SELECT d.mob, m.classe_mob, d.name_tag, d.data_domesticacao, d.coordenadas
                FROM domesticacao_mob d JOIN tipo_mob m ON m.nome = d.mob
                WHERE d.jogador = %s ORDER BY d.data_domesticacao""", (nome,))
    esq, dir_ = topo("jogador")
    with dir_:
        infobox(nome, "Jogador", [
            ("Vida", j["vida"]), ("Dano base", j["dano_base"]), ("Fome", j["fome"]),
            ("Experiência", j["experiencia"]), ("Fôlego", j["folego"]), ("Armadura", j["armadura"]),
            ("Velocidade", j["velocidade"]), ("Pulo", j["pulo"]),
            ("Efeito ativo", f"{j['efeito']} (nível {j['nivel']})" if j["efeito"] else None), ("Mundo", j["nome_mundo"]),
            ("Modo", j["modo"]), ("Slots do inventário", j["numero_de_slots"]),
            ("Hotbar selecionada", j["slot_hotbar_selecionado"])])
    with esq:
        st.title(nome)
        t = (f"<b>{esc(nome)}</b> tem <b>{j['vida']}</b> de vida, <b>{j['experiencia']}</b> de experiência e "
             f"armadura {j['armadura']}. ")
        if j["nome_mundo"]:
            t += f"Joga em “{esc(j['nome_mundo'])}” ({esc(j['modo'].lower())}, dificuldade {esc(j['dificuldade'].lower())}). "
        t += f"Já domesticou {len(mobs)} mob(s) e carrega {len(itens)} tipo(s) de item."
        lead(t)
        sub("Inventário")
        tabela(itens, "item", "item", key=f"jog_{nome}_i")
        sub("Mobs domesticados")
        tabela(mobs, "mob", "mob", key=f"jog_{nome}_m")
        sub("Veja também")
        st.caption("Efeito e dimensão")
        chips("efeito", [j["efeito"]], f"jog_{nome}")
        chips("dimensao", [j["dimensao"]], f"jog_{nome}")


def art_efeito(nome):
    e = one("SELECT * FROM efeito WHERE nome = %s", (nome,))
    if not e:
        return nao_encontrado(nome)
    jog = q("SELECT nickname AS jogador, vida, experiencia FROM jogador WHERE efeito = %s", (nome,))
    itens = q("SELECT nome AS item, raridade FROM tipo_item WHERE efeito_nome = %s", (nome,))
    esq, dir_ = topo("efeito")
    with dir_:
        infobox(nome, f"Efeito {e['tipo_de_efeito'].lower()}", [
            ("Nível", e["nivel"]), ("Tipo", e["tipo_de_efeito"]), ("Duração", e["tempo_de_efeito"])])
    with esq:
        st.title(nome)
        lead(f"<b>{esc(nome)}</b> é um efeito <b>{esc(e['tipo_de_efeito'].lower())}</b> de nível {e['nivel']} que dura "
             f"{e['tempo_de_efeito']} ticks. Está ligado a {len(jog)} jogador(es) e {len(itens)} item(ns).")
        sub("Jogadores")
        tabela(jog, "jogador", "jogador", key=f"ef_{nome}_j")
        sub("Itens")
        tabela(itens, "item", "item", key=f"ef_{nome}_i")


def art_receita(nome):
    r = one("SELECT * FROM receita_crafting WHERE receita = %s", (nome,))
    if not r:
        return nao_encontrado(nome)
    ing = q("""SELECT ci.posicao_slot, ci.item, ti.raridade, ci.quantidade, ci.combustivel
               FROM crafting_item ci JOIN tipo_item ti ON ti.nome = ci.item
               WHERE ci.receita = %s ORDER BY ci.combustivel, ci.posicao_slot""", (nome,))
    outras = q("""SELECT receita, tipo_de_crafting, tempo_para_o_crafting FROM receita_crafting
                  WHERE item_resultado = %s AND receita <> %s ORDER BY receita""", (r["item_resultado"], nome))
    esq, dir_ = topo("receita")
    titulo = nome.replace("_", " ")
    tempo = r["tempo_para_o_crafting"]
    comb = [x for x in ing if x["combustivel"]]
    entradas = [x for x in ing if not x["combustivel"]]
    with dir_:
        linhas = [("Estação", r["tipo_de_crafting"]), ("Produz", f"{r['quantidade_resultado']}× {r['item_resultado']}")]
        if tempo is not None:  # bancada e estações instantâneas não têm tempo
            linhas.append(("Tempo", f"{tempo} s"))
        linhas.append(("Ingredientes", len(entradas)))
        if comb:
            linhas.append(("Combustível", ", ".join(x["item"] for x in comb)))
        elif r["tipo_de_crafting"] in ("Fogueira",):
            linhas.append(("Combustível", "Não usa"))
        infobox(titulo, "Receita de crafting", linhas)
    with esq:
        st.title(titulo)
        t = (f"Receita feita na estação <b>{esc(r['tipo_de_crafting'].lower())}</b>: produz "
             f"<b>{r['quantidade_resultado']}× {esc(r['item_resultado'])}</b> usando {len(entradas)} ingrediente(s). ")
        if comb:
            t += f"Consome <b>{esc(comb[0]['item'])}</b> como combustível. "
        t += f"O processo leva {tempo} segundo(s)." if tempo is not None else "É instantânea, sem tempo de espera."
        lead(t)
        sub("Como fazer")
        def slot(x, extra=""):
            return f"<div class='slot{extra}'>{esc(x['item'])}<b>×{x['quantidade']}</b></div>"
        res = ("<div class='grade' style='grid-template-columns:92px'>"
               f"<div class='slot'>{esc(r['item_resultado'])}<b>×{r['quantidade_resultado']}</b></div></div>")
        if r["tipo_de_crafting"] == "Bancada":
            cel = {x["posicao_slot"]: x for x in entradas}
            entrada = "<div class='grade'>" + "".join(
                slot(cel[n]) if n in cel else "<div class='slot'></div>" for n in range(1, 10)) + "</div>"
        else:
            entrada = ("<div class='grade' style='grid-template-columns:repeat(%d,92px)'>" % max(len(entradas), 1)
                       + "".join(slot(x) for x in entradas) + "</div>")
            if comb:
                entrada = ("<div class='coluna'>" + entrada
                           + "<div class='grade' style='grid-template-columns:92px'>"
                           + "".join(slot({"item": "🔥 " + x["item"], "quantidade": x["quantidade"]}, " comb") for x in comb)
                           + "</div></div>")
        st.markdown(f"<div class='linha'>{entrada}<span class='seta'>=</span>{res}</div>", unsafe_allow_html=True)
        if comb:
            st.caption("O slot marrom com chama é o combustível.")
        sub("Ingredientes")
        tabela(ing, "item", "item", key=f"rec_{nome}_i")
        sub("Outras formas de obter o mesmo item")
        tabela(outras, "receita", "receita", key=f"rec_{nome}_o")
        sub("Veja também")
        st.caption("Item produzido")
        chips("item", [r["item_resultado"]], f"rec_{nome}")


ARTIGOS = {"mob": art_mob, "item": art_item, "bloco": art_bloco, "bioma": art_bioma,
           "dimensao": art_dimensao, "jogador": art_jogador, "efeito": art_efeito, "receita": art_receita}

# ──────────────────────────── Índices ────────────────────────────
INDICES = {
    "Mobs": ("mob", "nome", "classe_mob", "Todos os mobs cadastrados, agrupados por classe. Clique em uma linha para abrir o artigo.",
             """SELECT m.nome, m.classe_mob, m.vida, m.dano_base, m.velocidade, COUNT(g.bioma) AS biomas
                FROM tipo_mob m LEFT JOIN geracao_mob_bioma g ON g.mob = m.nome
                GROUP BY m.nome, m.classe_mob, m.vida, m.dano_base, m.velocidade
                ORDER BY m.classe_mob, m.nome"""),
    "Itens": ("item", "nome", "categoria", "Itens, poções, alimentos e ferramentas do jogo.",
              """SELECT i.nome, i.raridade,
                        CASE WHEN c.nome IS NOT NULL THEN 'Consumível' WHEN d.nome IS NOT NULL THEN 'Desgastável'
                             ELSE 'Item comum' END AS categoria,
                        COALESCE(STRING_AGG(DISTINCT ic.classe_item, ', '), '—') AS classes
                 FROM tipo_item i
                 LEFT JOIN tipo_item_consumivel c ON c.nome = i.nome
                 LEFT JOIN tipo_item_desgastavel d ON d.nome = i.nome
                 LEFT JOIN item_classe ic ON ic.nome = i.nome
                 GROUP BY i.nome, i.raridade, c.nome, d.nome ORDER BY i.nome"""),
    "Blocos": ("bloco", "nome", "quebravel", "Blocos e a quantidade de biomas em que aparecem.",
               """SELECT b.nome, b.durabilidade, b.condicao_de_quebra, b.quebravel, b.dropavel, COUNT(g.bioma) AS biomas
                  FROM tipo_bloco b LEFT JOIN geracao_bloco_bioma g ON g.bloco = b.nome
                  GROUP BY b.nome, b.durabilidade, b.condicao_de_quebra, b.quebravel, b.dropavel ORDER BY b.nome"""),
    "Biomas": ("bioma", "nome", "tipo_de_precipitacao", "Biomas, com a dimensão e o mundo a que pertencem.",
               """SELECT b.nome, b.temperatura, b.altitude_media, b.tipo_de_precipitacao, b.dimensao, mu.nome AS nome_mundo
                  FROM tipo_bioma b JOIN dimensao d ON d.nome = b.dimensao JOIN mundo mu ON mu.save = d.mundo
                  ORDER BY b.nome"""),
    "Mundos e dimensões": ("dimensao", "nome", "dificuldade", "Cada dimensão com o mundo e o jogador dono dela.",
                           """SELECT d.nome, mu.nome AS nome_mundo, mu.jogador, mu.modo, mu.dificuldade, d.pode_dormir
                              FROM dimensao d JOIN mundo mu ON mu.save = d.mundo ORDER BY d.nome"""),
    "Jogadores": ("jogador", "nickname", "modo", "Jogadores ordenados por experiência.",
                  """SELECT j.nickname, j.vida, j.experiencia, j.armadura, mu.nome AS nome_mundo, mu.modo
                     FROM jogador j LEFT JOIN mundo mu ON mu.jogador = j.nickname ORDER BY j.experiencia DESC"""),
    "Efeitos": ("efeito", "nome", "tipo_de_efeito", "Efeitos de status aplicados a jogadores e itens.",
                "SELECT nome, nivel, tipo_de_efeito, tempo_de_efeito FROM efeito ORDER BY nivel"),
    "Receitas": ("receita", "receita", "tipo_de_crafting", "Receitas por estação (bancada, fornalha, alto-forno e outras). Só as estações de cozimento têm tempo.",
                 """SELECT r.receita, r.item_resultado, r.tipo_de_crafting, r.tempo_para_o_crafting, COUNT(ci.item) FILTER (WHERE NOT ci.combustivel) AS ingredientes
                    FROM receita_crafting r LEFT JOIN crafting_item ci ON ci.receita = r.receita
                    GROUP BY r.receita, r.item_resultado, r.tipo_de_crafting, r.tempo_para_o_crafting
                    ORDER BY r.tipo_de_crafting, r.receita"""),
    "Estruturas": ("bioma", "bioma", None, "Estruturas e o bioma onde cada uma aparece. Clique para abrir o bioma.",
                   """SELECT s.nome AS estrutura, s.variante, s.extensao, s.bioma, b.dimensao, b.temperatura
                      FROM tipo_estrutura s JOIN tipo_bioma b ON b.nome = s.bioma ORDER BY s.nome, s.variante"""),
}


def pagina_indice(secao):
    kind, name_col, filtro, intro, sql = INDICES[secao]
    st.title(secao)
    st.caption(intro)
    d = pd.DataFrame(q(sql))
    c1, c2 = st.columns([2, 1])
    texto = c1.text_input("Filtrar por nome", key=f"f_{secao}", placeholder="Digite parte do nome")
    if texto:
        d = d[d[d.columns[0]].map(lambda v: sem_acento(texto) in sem_acento(v))]
    if filtro:
        opcoes = sorted(pd.DataFrame(q(sql))[filtro].dropna().unique(), key=str)
        sel = c2.multiselect(LABELS.get(filtro, filtro), opcoes, key=f"m_{secao}")
        if sel:
            d = d[d[filtro].isin(sel)]
    tabela(d.to_dict("records"), name_col, kind, key=f"idx_{secao}")


# ──────────────────────────── Busca, início e estatísticas ────────────────────────────
SQL_NOMES = """
    SELECT 'mob' AS tipo, nome, classe_mob AS detalhe FROM tipo_mob
    UNION ALL SELECT 'item', nome, raridade FROM tipo_item
    UNION ALL SELECT 'bloco', nome, CASE WHEN quebravel THEN 'Quebrável' ELSE 'Inquebrável' END FROM tipo_bloco
    UNION ALL SELECT 'bioma', nome, dimensao FROM tipo_bioma
    UNION ALL SELECT 'dimensao', d.nome, mu.nome FROM dimensao d JOIN mundo mu ON mu.save = d.mundo
    UNION ALL SELECT 'jogador', j.nickname, COALESCE(mu.nome, 'Jogador')
              FROM jogador j LEFT JOIN mundo mu ON mu.jogador = j.nickname
    UNION ALL SELECT 'efeito', nome, tipo_de_efeito FROM efeito
    UNION ALL SELECT 'receita', receita, tipo_de_crafting FROM receita_crafting"""


def pagina_busca(termo):
    st.title(f"Busca: {termo}")
    t = sem_acento(termo)
    achados = [r for r in q(SQL_NOMES) if t in sem_acento(r["nome"]) or t in sem_acento(r["detalhe"])]
    if not achados:
        st.info("Nada encontrado. Tente outra palavra, como o nome de um mob, item, bioma ou jogador.")
        return
    st.caption(f"{len(achados)} artigo(s) encontrado(s). Clique em uma linha para abrir.")
    rows = [{"tipo": KIND_LABEL[r["tipo"]], "nome": r["nome"], "detalhe": r["detalhe"]} for r in achados]
    tabela(rows, targets=[(r["tipo"], r["nome"]) for r in achados], key="busca_res")


def pagina_inicio():
    st.title("Minecraftpédia")
    lead("A enciclopédia do nosso banco de dados de Minecraft. Cada artigo é montado em tempo real com consultas "
         "que cruzam mobs, biomas, dimensões, jogadores, itens e receitas. Use a busca ao lado ou escolha uma categoria.")
    n = one("""SELECT (SELECT COUNT(*) FROM tipo_mob) AS mobs, (SELECT COUNT(*) FROM tipo_item) AS itens,
                      (SELECT COUNT(*) FROM tipo_bloco) AS blocos, (SELECT COUNT(*) FROM tipo_bioma) AS biomas,
                      (SELECT COUNT(*) FROM mundo) AS mundos, (SELECT COUNT(*) FROM jogador) AS jogadores,
                      (SELECT COUNT(*) FROM receita_crafting) AS receitas""")
    cols = st.columns(7)
    for c, (k, v) in zip(cols, n.items()):
        c.metric(k.capitalize(), v)

    sub("Você sabia?")
    f1 = one("""SELECT g.mob, SUM(g.taxa) AS total FROM (
                   SELECT mob, taxa_de_spawn AS taxa FROM geracao_mob_bioma
                   UNION ALL SELECT mob, taxa_de_spawn FROM geracao_mob_dimensao) g
                GROUP BY g.mob ORDER BY total DESC LIMIT 1""")
    f2 = one("""SELECT j.nickname, j.experiencia, mu.nome AS nome_mundo FROM jogador j
                JOIN mundo mu ON mu.jogador = j.nickname ORDER BY j.experiencia DESC LIMIT 1""")
    f3 = one("""SELECT d.jogador, COUNT(*) AS n FROM domesticacao_mob d GROUP BY d.jogador ORDER BY n DESC LIMIT 1""")
    f4 = one("SELECT nome, temperatura, dimensao FROM tipo_bioma ORDER BY temperatura DESC LIMIT 1")
    a, b = st.columns(2)
    with a:
        if f1:
            st.markdown(f"- O mob que mais aparece é o **{f1['mob']}**, com taxa de spawn somada de {f1['total']}.")
        if f2:
            st.markdown(f"- **{f2['nickname']}** é quem mais tem experiência ({f2['experiencia']}), no mundo “{f2['nome_mundo']}”.")
    with b:
        if f3:
            st.markdown(f"- **{f3['jogador']}** é o maior domesticador, com {f3['n']} mob(s).")
        if f4:
            st.markdown(f"- O bioma mais quente é **{f4['nome']}** ({f4['temperatura']} graus), na dimensão {f4['dimensao']}.")
    ca, cb, cc, cd = st.columns(4)
    if f1:
        ca.button(f1["mob"], key="d1", on_click=abrir, args=("mob", f1["mob"]))
    if f2:
        cb.button(f2["nickname"], key="d2", on_click=abrir, args=("jogador", f2["nickname"]))
    if f3:
        cc.button(f3["jogador"], key="d3", on_click=abrir, args=("jogador", f3["jogador"]))
    if f4:
        cd.button(f4["nome"], key="d4", on_click=abrir, args=("bioma", f4["nome"]))

    sub("Explorar")
    cats = SECOES[1:]
    for linha in range(0, len(cats), 5):
        cs = st.columns(5)
        for c, s in zip(cs, cats[linha:linha + 5]):
            c.button(s, key=f"cat_{s}", on_click=ir, args=(s,))
    st.button("Artigo aleatório", key="aleatorio", on_click=lambda: abrir(
        *(lambda r: (r["tipo"], r["nome"]))(random.choice(q(SQL_NOMES)))))


def pagina_estatisticas():
    st.title("Estatísticas")
    st.caption("Resumos calculados com agrupamentos e junções sobre o banco.")

    def grafico(titulo, sql, indice, valor):
        st.markdown(f"**{titulo}**")
        d = pd.DataFrame(q(sql))
        d = d.rename(columns=lambda c: LABELS.get(c, c))
        st.bar_chart(d.set_index(LABELS.get(indice, indice))[LABELS.get(valor, valor)])

    c1, c2 = st.columns(2)
    with c1:
        grafico("Taxa de spawn de mobs por bioma",
                "SELECT bioma, SUM(taxa_de_spawn) AS spawn_total FROM geracao_mob_bioma GROUP BY bioma ORDER BY 2 DESC",
                "bioma", "spawn_total")
        grafico("Experiência por jogador", "SELECT nickname, experiencia FROM jogador ORDER BY experiencia DESC",
                "nickname", "experiencia")
        grafico("Vida média por classe de mob",
                "SELECT classe_mob, ROUND(AVG(vida), 1)::float AS vida_media FROM tipo_mob GROUP BY classe_mob",
                "classe_mob", "vida_media")
    with c2:
        grafico("Mobs domesticados por jogador",
                """SELECT j.nickname, COUNT(d.mob) AS mobs_domesticados FROM jogador j
                   LEFT JOIN domesticacao_mob d ON d.jogador = j.nickname GROUP BY j.nickname ORDER BY 2 DESC""",
                "nickname", "mobs_domesticados")
        grafico("Temperatura por bioma", "SELECT nome, temperatura FROM tipo_bioma ORDER BY temperatura",
                "nome", "temperatura")
        grafico("Receitas por estação de crafting",
                "SELECT tipo_de_crafting, COUNT(*) AS receitas FROM receita_crafting GROUP BY tipo_de_crafting ORDER BY 2 DESC",
                "tipo_de_crafting", "receitas")
        grafico("Mundos por dificuldade",
                "SELECT dificuldade, COUNT(*) AS mundos FROM mundo GROUP BY dificuldade ORDER BY 2 DESC",
                "dificuldade", "mundos")


# ──────────────────────────── Programa principal ────────────────────────────
if not _dsn():
    st.error("A variável DATABASE_URL não foi encontrada.")
    st.markdown("Defina a conexão do Neon como variável de ambiente ou em `.streamlit/secrets.toml`:")
    st.code('DATABASE_URL = "postgresql://usuario:senha@host/banco?sslmode=require"', language="toml")
    st.stop()

st.session_state.setdefault("nav", "Início")
st.session_state.setdefault("entidade", None)
st.session_state.setdefault("busca", "")

with st.sidebar:
    st.markdown("## ⛏️ Minecraftpédia")
    st.text_input("Buscar na wiki", key="busca", placeholder="Zumbi, picareta, deserto")
    st.radio("Seções", SECOES, key="nav", on_change=trocar_secao, label_visibility="collapsed")

try:
    termo = st.session_state.busca.strip()
    if termo:
        pagina_busca(termo)
    elif st.session_state.entidade:
        kind, nome = st.session_state.entidade
        ARTIGOS[kind](nome)
    elif st.session_state.nav == "Início":
        pagina_inicio()
    elif st.session_state.nav == "Estatísticas":
        pagina_estatisticas()
    else:
        pagina_indice(st.session_state.nav)
except psycopg2.Error as erro:
    st.error("Não foi possível consultar o banco de dados.")
    st.caption("Confira se `python setup_db.py` já foi executado no Neon e se a DATABASE_URL está correta.")
    with st.expander("Detalhes do erro"):
        st.code(str(erro))
