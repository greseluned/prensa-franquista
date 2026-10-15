#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Prensa Franquista — Interfaz de recuperación dual
GRESEL-UNED · PID2023-151280OB-C22

Corpus principal : Periódicos franquistas (Filipinas + Puerto Rico)
Capa experta     : Glosario NER del Franquismo (1.105 entradas)
Motor            : TF-IDF + SVD + similitud coseno (scikit-learn)
Generación local : Ollama (opcional — modelos: qwen2.5:3b, llama3.2:3b, mistral)

Ejecutar con:
    streamlit run app_rag_prensa_franquista.py

Estructura esperada en el mismo directorio:
    corpus/                           ← carpeta con los .txt del repositorio
        Filipinas/Excelsior/txt/*.txt
        Filipinas/Hispanidad/txt/*.txt
        Filipinas/Yugo/txt/*.txt
        Puerto-Rico/Avance/txt/*.txt
        Puerto-Rico/Los-Quijotes/txt/*.txt
    glosario_ner_franquismo.py        ← capa experta
"""

import os
import re
import sys
import types
import json
from pathlib import Path

import numpy as np
import streamlit as st
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── Configuración de página ─────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Prensa Franquista · GRESEL-UNED",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body,
[data-testid="stAppViewContainer"] > .main {
    background-color: #F5F4F0;
    font-family: 'Segoe UI', Calibri, Arial, sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%);
}
[data-testid="stSidebar"] * { color: #D8D8EE !important; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #FFF !important; }
[data-testid="stSidebar"] label {
    color: #9090B8 !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 600;
}

.rag-header {
    background: linear-gradient(135deg, #1A1A2E 0%, #2D2D4E 100%);
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.4rem;
}
.rag-title { color: #FFF; font-size: 1.5rem; font-weight: 700; margin: 0; }
.rag-sub   { color: #9898C0; font-size: 0.87rem; margin: 0.2rem 0 0; }

/* Tarjeta de pasaje */
.passage-card {
    background: #FFF;
    border-radius: 12px;
    border-left: 5px solid #8B0000;
    padding: 1rem 1.3rem 1.1rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.passage-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
.passage-meta {
    font-size: 0.78rem;
    color: #666;
    margin-bottom: 0.4rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.passage-text {
    color: #222;
    font-size: 0.92rem;
    line-height: 1.65;
}
.pub-chip {
    display: inline-block;
    padding: 0.1rem 0.55rem;
    border-radius: 6px;
    font-size: 0.73rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.pub-Excelsior       { background: #E3F2FD; color: #0D47A1; }
.pub-Hispanidad      { background: #FCE4EC; color: #880E4F; }
.pub-Yugo            { background: #FFF9C4; color: #5D4037; }
.pub-Avance          { background: #E8F5E9; color: #1B5E20; }
.pub-Los-Quijotes    { background: #F3E5F5; color: #4A148C; }

/* Tarjeta de glosario */
.gloss-card {
    background: #FAFAFA;
    border-radius: 10px;
    border-left: 4px solid #1A1A2E;
    padding: 0.8rem 1.1rem;
    margin-bottom: 0.7rem;
    font-size: 0.88rem;
}
.gloss-term { color: #8B0000; font-weight: 700; margin-bottom: 0.25rem; }
.gloss-def  { color: #444; line-height: 1.55; }

/* Badges */
.badge {
    display: inline-block;
    padding: 0.12rem 0.55rem;
    border-radius: 20px;
    font-size: 0.73rem;
    font-weight: 700;
}
.badge-high   { background: #D4EDDA; color: #155724; }
.badge-medium { background: #FFF3CD; color: #856404; }
.badge-low    { background: #F8D7DA; color: #721C24; }

/* Botones */
div[data-testid="stButton"] > button {
    background: #1A1A2E; color: #FFF;
    border: none; border-radius: 10px;
    font-weight: 600; padding: 0.6rem 1.5rem;
    transition: background 0.2s;
}
div[data-testid="stButton"] > button:hover { background: #8B0000; }

[data-testid="stTextInput"] input {
    font-size: 1rem; border-radius: 10px;
    border: 2px solid #D0D0E0; padding: 0.7rem 1rem;
}
[data-testid="stTextInput"] input:focus {
    border-color: #8B0000 !important;
    box-shadow: 0 0 0 3px rgba(139,0,0,0.12) !important;
}

/* Separadores */
.sep      { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 0.8rem 0; }
.sep-main { border: none; border-top: 1px solid #E0DFD8; margin: 1rem 0 1.2rem; }

/* Sidebar stat rows */
.srow {
    display: flex; justify-content: space-between;
    font-size: 0.82rem; padding: 0.22rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.srow .val { font-weight: 700; color: #FFF !important; }

.sidebar-footer {
    font-size: 0.75rem; color: #6868A0 !important; line-height: 1.6;
}

/* Ollama banner */
.ollama-ok  { background:#D4EDDA; border-radius:8px; padding:0.5rem 0.9rem; font-size:0.85rem; color:#155724; }
.ollama-off { background:#F8D7DA; border-radius:8px; padding:0.5rem 0.9rem; font-size:0.85rem; color:#721C24; }

/* Generation box */
.gen-box {
    background: #1A1A2E; color: #E8E8F8;
    border-radius: 12px; padding: 1.2rem 1.5rem;
    font-size: 0.95rem; line-height: 1.7;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Localización de ficheros ────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()

# Corpus: buscar carpeta "corpus" junto al script
CORPUS_CANDIDATES = [
    SCRIPT_DIR / "corpus",
    SCRIPT_DIR / "prensa-repo",
    Path("/tmp/claude-0/-home-claude/41636698-c6df-5db3-9686-4ea683148a07/scratchpad/prensa-repo"),
]
CORPUS_ROOT = next((p for p in CORPUS_CANDIDATES if p.exists()), None)

# Glosario NER
GLOSARIO_CANDIDATES = [
    SCRIPT_DIR / "glosario_ner_franquismo.py",
    Path.home() / "glosario_ner_franquismo.py",
    Path("/home/claude/glosario_ner_franquismo.py"),
]
GLOSARIO_PATH = next((p for p in GLOSARIO_CANDIDATES if p.exists()), None)

# Publicaciones y sus carpetas
PUBLICACIONES = {
    "Excelsior":    "Filipinas/Excelsior/txt",
    "Hispanidad":   "Filipinas/Hispanidad/txt",
    "Yugo":         "Filipinas/Yugo/txt",
    "Avance":       "Puerto-Rico/Avance/txt",
    "Los-Quijotes": "Puerto-Rico/Los-Quijotes/txt",
}

PAIS = {
    "Excelsior": "Filipinas", "Hispanidad": "Filipinas", "Yugo": "Filipinas",
    "Avance": "Puerto Rico", "Los-Quijotes": "Puerto Rico",
}


# ─── Parser de metadatos desde nombre de fichero ──────────────────────────────
def parse_filename(fname: str) -> dict:
    """
    Extrae publicación, fecha, número de ejemplar y página
    desde nombres como: Excelsior-1937-10-01-N1053_p003.txt
    """
    stem = Path(fname).stem
    meta = {"publicacion": "Desconocida", "fecha": "", "numero": "", "pagina": ""}

    # Publicación (primera parte antes del primer guión-fecha)
    for pub in PUBLICACIONES:
        if stem.startswith(pub) or stem.startswith(pub.replace("-", " ")):
            meta["publicacion"] = pub
            break

    # Fecha YYYY-MM-DD
    m = re.search(r'(\d{4}-\d{2}-\d{2})', stem)
    if m:
        meta["fecha"] = m.group(1)

    # Número de ejemplar N####
    m = re.search(r'[Nn](\d+)', stem)
    if m:
        meta["numero"] = f"N.º {m.group(1)}"

    # Página
    m = re.search(r'[_-]p(\d+)', stem)
    if m:
        meta["pagina"] = f"p. {int(m.group(1))}"

    return meta


# ─── Carga y caché del sistema RAG ──────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def build_rag_system(corpus_root_str: str, glosario_path_str: str):
    """
    Construye dos índices independientes en memoria:
      1. Corpus de prensa (1.985 páginas)
      2. Glosario NER (1.105 entradas — capa experta)
    """
    corpus_root = Path(corpus_root_str)

    # ── 1. CORPUS DE PRENSA ────────────────────────────────────────────────
    press_docs, press_meta = [], []

    for pub, rel_path in PUBLICACIONES.items():
        folder = corpus_root / rel_path
        if not folder.exists():
            continue
        for txt_file in sorted(folder.glob("*.txt")):
            try:
                text = txt_file.read_text(encoding="utf-8", errors="ignore").strip()
            except Exception:
                continue
            if len(text) < 20:          # ignorar páginas casi vacías
                continue
            meta = parse_filename(txt_file.name)
            press_docs.append(text)
            press_meta.append({
                "publicacion": pub,
                "pais":        PAIS.get(pub, ""),
                "fecha":       meta["fecha"],
                "numero":      meta["numero"],
                "pagina":      meta["pagina"],
                "fichero":     txt_file.name,
            })

    # Vectorizar corpus de prensa
    press_vec = TfidfVectorizer(
        analyzer="word", ngram_range=(1, 2),
        min_df=2, max_df=0.90,
        sublinear_tf=True, strip_accents=None,
        max_features=60000,
    )
    press_tfidf = press_vec.fit_transform(press_docs)
    press_svd   = TruncatedSVD(n_components=min(512, press_tfidf.shape[1]-1), random_state=42)
    press_dense = press_svd.fit_transform(press_tfidf)
    norms = np.linalg.norm(press_dense, axis=1, keepdims=True)
    norms[norms == 0] = 1
    press_norm = press_dense / norms

    # ── 2. GLOSARIO NER (capa experta) ───────────────────────────────────
    # Stub ReportLab
    for mod in ["reportlab","reportlab.lib","reportlab.lib.pagesizes",
                "reportlab.lib.styles","reportlab.lib.colors","reportlab.lib.units",
                "reportlab.platypus","reportlab.lib.enums",
                "reportlab.pdfgen","reportlab.pdfgen.canvas"]:
        if mod not in sys.modules:
            sys.modules[mod] = types.ModuleType(mod)
    sys.modules["reportlab.lib.pagesizes"].A4 = (595.28, 841.89)
    for a in ("getSampleStyleSheet","ParagraphStyle"):
        setattr(sys.modules["reportlab.lib.styles"], a, lambda *x, **k: None)
    for a in ("HexColor","black","white"):
        setattr(sys.modules["reportlab.lib.colors"], a, lambda *x, **k: None)
    sys.modules["reportlab.lib.units"].cm = 28.35
    for a in ("SimpleDocTemplate","Paragraph","Spacer","Table","TableStyle",
               "PageBreak","HRFlowable","KeepTogether"):
        setattr(sys.modules["reportlab.platypus"], a, lambda *x, **k: None)
    for a in ("TA_LEFT","TA_CENTER","TA_JUSTIFY"):
        setattr(sys.modules["reportlab.lib.enums"], a, 0)
    sys.modules["reportlab.pdfgen.canvas"].Canvas = lambda *x, **k: None

    with open(glosario_path_str, "r", encoding="utf-8") as f:
        src = f.read()
    cut = re.search(r"^def [a-z_]+\(", src, re.MULTILINE)
    ns  = {}
    exec(compile(src[: cut.start()] if cut else src, "glosario.py", "exec"), ns)

    GLOSS_MAP = {
        "TÉRMINOS":              ns.get("TERMINOS", []),
        "EVENTOS":               ns.get("EVENTOS",  []),
        "PERSONAS":              ns.get("PERSONAS", []),
        "LUGARES/PUBLICACIONES": ns.get("LUGARES",  []),
    }
    gloss_docs, gloss_meta = [], []
    for cat, entries in GLOSS_MAP.items():
        for term, defn in entries:
            gloss_docs.append(f"{cat.split('/')[0]}: {term}\n{defn}")
            gloss_meta.append({"category": cat, "term": term, "definition": defn})

    gloss_vec = TfidfVectorizer(
        analyzer="word", ngram_range=(1, 2),
        min_df=1, max_df=0.95,
        sublinear_tf=True, strip_accents=None,
    )
    gloss_tfidf = gloss_vec.fit_transform(gloss_docs)
    gloss_svd   = TruncatedSVD(n_components=512, random_state=42)
    gloss_dense = gloss_svd.fit_transform(gloss_tfidf)
    norms2 = np.linalg.norm(gloss_dense, axis=1, keepdims=True)
    norms2[norms2 == 0] = 1
    gloss_norm = gloss_dense / norms2

    stats = {
        "press_docs":  len(press_docs),
        "press_vocab": press_tfidf.shape[1],
        "gloss_total": len(gloss_docs),
        "by_pub": {pub: sum(1 for m in press_meta if m["publicacion"] == pub)
                   for pub in PUBLICACIONES},
    }

    return (press_vec, press_svd, press_norm, press_meta,
            gloss_vec,  gloss_svd,  gloss_norm,  gloss_meta,
            stats)


def query_press(query, vec, svd, norm, meta, n=5, pub_filter=None):
    """Recupera pasajes del corpus de prensa."""
    q = vec.transform([query])
    q = svd.transform(q)
    q = q / (np.linalg.norm(q) + 1e-10)
    scores = cosine_similarity(q, norm)[0]

    if pub_filter:
        mask = np.array([m["publicacion"] == pub_filter for m in meta])
        scores = np.where(mask, scores, -1.0)

    top = np.argsort(scores)[::-1][:n]
    return [
        {**meta[i], "score": round(float(scores[i]) * 100, 1),
         "snippet": _snippet(i, norm, meta)}
        for i in top if scores[i] > 0
    ]


def _snippet(idx, norm, meta):
    """Recupera el texto del fichero dado el índice."""
    # El texto no se almacena en memoria para ahorrar RAM;
    # se lee desde el fichero cuando se necesita mostrar.
    return ""   # se completa en la búsqueda


@st.cache_resource(show_spinner=False)
def load_press_texts(corpus_root_str: str) -> dict:
    """Carga todos los textos del corpus en un diccionario {fichero: texto}."""
    root  = Path(corpus_root_str)
    texts = {}
    for pub, rel in PUBLICACIONES.items():
        folder = root / rel
        if not folder.exists():
            continue
        for txt in folder.glob("*.txt"):
            try:
                content = txt.read_text(encoding="utf-8", errors="ignore").strip()
                if len(content) >= 20:
                    texts[txt.name] = content
            except Exception:
                pass
    return texts


def query_press_full(query, vec, svd, norm, meta, texts, n=5, pub_filter=None):
    """Recupera pasajes con texto incluido."""
    q = vec.transform([query])
    q = svd.transform(q)
    q = q / (np.linalg.norm(q) + 1e-10)
    scores = cosine_similarity(q, norm)[0]

    if pub_filter and pub_filter != "Todas":
        mask = np.array([m["publicacion"] == pub_filter for m in meta])
        scores = np.where(mask, scores, -1.0)

    top = np.argsort(scores)[::-1][:n]
    results = []
    for i in top:
        if scores[i] <= 0:
            continue
        m = meta[i]
        texto = texts.get(m["fichero"], "")
        snippet = texto[:500].replace("\n", " ").strip() + ("…" if len(texto) > 500 else "")
        results.append({**m, "score": round(float(scores[i]) * 100, 1), "snippet": snippet})
    return results


def query_gloss(query, vec, svd, norm, meta, n=4):
    """Recupera entidades del glosario NER relacionadas con la consulta."""
    q = vec.transform([query])
    q = svd.transform(q)
    q = q / (np.linalg.norm(q) + 1e-10)
    scores = cosine_similarity(q, norm)[0]
    top = np.argsort(scores)[::-1][:n]
    return [
        {**meta[i], "score": round(float(scores[i]) * 100, 1)}
        for i in top if scores[i] > 0
    ]


def badge(s):
    if s >= 35: return "badge-high"
    if s >= 18: return "badge-medium"
    return "badge-low"


CAT_CHIP = {
    "TÉRMINOS":              ("T", "#1A237E", "#E8EAF6"),
    "EVENTOS":               ("E", "#880E4F", "#FCE4EC"),
    "PERSONAS":              ("P", "#1B5E20", "#E8F5E9"),
    "LUGARES/PUBLICACIONES": ("L", "#0D47A1", "#E3F2FD"),
}

EXAMPLE_QUERIES = [
    "Falange española en Filipinas",
    "José Antonio Primo de Rivera",
    "Guerra Civil española y propaganda",
    "Franco y el Nuevo Estado",
    "Hispanidad y misión de España en América",
    "Prensa y control de la información",
    "Misioneros y labor cultural española",
    "Comunismo y amenaza roja",
]

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODELS = ["qwen2.5:3b", "llama3.2:3b", "mistral:7b", "phi3:mini"]


def check_ollama():
    try:
        import urllib.request
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=2) as r:
            data = json.loads(r.read())
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return None


def generate_ollama(model, query, passages, glossary_terms):
    """Genera respuesta con Ollama usando los pasajes y entidades recuperados."""
    try:
        import urllib.request, urllib.error

        # Construir contexto
        ctx_parts = ["=== PASAJES DE PRENSA ==="]
        for p in passages[:3]:
            ctx_parts.append(
                f"[{p['publicacion']} · {p['fecha']} · {p['pagina']}]\n{p['snippet']}"
            )
        ctx_parts.append("\n=== ENTIDADES DEL GLOSARIO NER ===")
        for g in glossary_terms[:3]:
            ctx_parts.append(f"[{g['term']} — {g['category']}]\n{g['definition'][:200]}")
        context = "\n\n".join(ctx_parts)

        prompt = (
            f"Eres un asistente especializado en historia del franquismo y prensa española "
            f"de los años 30-50 del siglo XX. Responde en español, de forma precisa y académica.\n\n"
            f"CONTEXTO RECUPERADO:\n{context}\n\n"
            f"PREGUNTA: {query}\n\n"
            f"RESPUESTA (basada exclusivamente en el contexto anterior):"
        )

        payload = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 400},
        }).encode()

        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.loads(r.read())
            return resp.get("response", "").strip()
    except Exception as e:
        return f"Error al conectar con Ollama: {e}"


# ─── Estado de sesión ────────────────────────────────────────────────────────
for key, default in [
    ("query_text", ""),
    ("trigger_search", False),
    ("last_results", None),
    ("last_gloss", None),
    ("last_query", ""),
    ("last_gen", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def use_example(q):
    st.session_state.query_text     = q
    st.session_state.trigger_search = True


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📰 RAG Prensa Franquista")
    st.markdown("**GRESEL-UNED**  \n`PID2023-151280OB-C22`")
    st.markdown('<hr class="sep"/>', unsafe_allow_html=True)

    ready = CORPUS_ROOT is not None and GLOSARIO_PATH is not None
    if not ready:
        if CORPUS_ROOT is None:
            st.error("No se encontró la carpeta `corpus/`.\nColócala junto al script.")
        if GLOSARIO_PATH is None:
            st.error("No se encontró `glosario_ner_franquismo.py`.")

    rag_ready = False
    if ready:
        with st.spinner("Indexando corpus y glosario…"):
            try:
                (press_vec, press_svd, press_norm, press_meta,
                 gloss_vec,  gloss_svd,  gloss_norm,  gloss_meta,
                 stats) = build_rag_system(str(CORPUS_ROOT), str(GLOSARIO_PATH))
                texts = load_press_texts(str(CORPUS_ROOT))
                rag_ready = True
            except Exception as e:
                st.error(f"Error al indexar: {e}")

        if rag_ready:
            st.success(f"✓ {stats['press_docs']} páginas indexadas")
            st.success(f"✓ {stats['gloss_total']} entradas NER")

    st.markdown('<hr class="sep"/>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;color:#9090B8;font-weight:600;margin:0 0 0.5rem">Filtros</p>', unsafe_allow_html=True)

    pub_options = ["Todas"] + list(PUBLICACIONES.keys())
    pub_filter  = st.selectbox("Publicación", pub_options, label_visibility="collapsed")
    n_press     = st.slider("Pasajes de prensa",  1, 10, 5)
    n_gloss     = st.slider("Entidades del glosario", 1, 8, 4)

    st.markdown('<hr class="sep"/>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;color:#9090B8;font-weight:600;margin:0 0 0.5rem">Corpus</p>', unsafe_allow_html=True)

    if rag_ready:
        for pub, cnt in stats["by_pub"].items():
            pais = PAIS.get(pub, "")
            st.markdown(
                f'<div class="srow"><span>{pub} <small style="opacity:0.5">({pais})</small></span>'
                f'<span class="val">{cnt}</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            f'<div class="srow"><span>Vocabulario</span><span class="val">{stats["press_vocab"]:,}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="sep"/>', unsafe_allow_html=True)

    # ── Ollama ──
    st.markdown('<p style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.07em;color:#9090B8;font-weight:600;margin:0 0 0.5rem">Generación local (Ollama)</p>', unsafe_allow_html=True)
    ollama_models = check_ollama()
    use_ollama    = False
    selected_model = None

    if ollama_models:
        st.markdown('<div class="ollama-ok">✓ Ollama conectado</div>', unsafe_allow_html=True)
        available = [m for m in OLLAMA_MODELS if any(m in om for om in ollama_models)]
        if not available:
            available = ollama_models[:3]
        selected_model = st.selectbox("Modelo", available, label_visibility="collapsed")
        use_ollama = st.checkbox("Activar generación de respuesta", value=False)
    else:
        st.markdown(
            '<div class="ollama-off">Ollama no detectado — modo recuperación</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:0.75rem;color:#9090B8;margin-top:0.4rem">'
            'Instala <a href="https://ollama.com" style="color:#A0A0D0">ollama.com</a> '
            'y ejecuta:<br><code>ollama pull qwen2.5:3b</code>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="sep"/>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-footer">'
        "Motor: TF-IDF (1-2-gramas) + SVD + coseno<br>"
        "Corpus: Filipinas · Puerto Rico<br>"
        "Capa experta: Glosario NER (1.105 entradas)<br><br>"
        "© 2025 GRESEL-UNED · Fernando Obispo Permuy"
        "</div>",
        unsafe_allow_html=True,
    )


# ─── Área principal ───────────────────────────────────────────────────────────
st.markdown("""
<div class="rag-header">
    <div class="rag-title">📰 RAG Prensa Franquista</div>
    <div class="rag-sub">
        Recuperación dual sobre periódicos históricos (Filipinas · Puerto Rico) + Glosario NER del Franquismo
    </div>
</div>
""", unsafe_allow_html=True)

query_val = st.text_input(
    "Consulta",
    value=st.session_state.query_text,
    placeholder="Escribe una pregunta o tema sobre la prensa franquista…",
    label_visibility="collapsed",
    key="query_text",
)
col_btn, _ = st.columns([1, 7])
with col_btn:
    search_clicked = st.button("🔍  Buscar", use_container_width=True)

with st.expander("💡  Consultas de ejemplo"):
    ca, cb = st.columns(2)
    for i, ex in enumerate(EXAMPLE_QUERIES):
        with (ca if i % 2 == 0 else cb):
            st.button(
                f"→ {ex}",
                key=f"ex_{i}",
                on_click=use_example,
                args=(ex,),
                use_container_width=True,
            )

st.markdown('<hr class="sep-main"/>', unsafe_allow_html=True)

# ─── Búsqueda ────────────────────────────────────────────────────────────────
run_search = search_clicked or st.session_state.trigger_search
if st.session_state.trigger_search:
    st.session_state.trigger_search = False

query = st.session_state.query_text.strip()

if run_search and query:
    if not rag_ready:
        st.error("El sistema RAG no está disponible.")
    else:
        with st.spinner("Buscando en corpus y glosario…"):
            pf = None if pub_filter == "Todas" else pub_filter
            press_res = query_press_full(
                query, press_vec, press_svd, press_norm, press_meta,
                texts, n=n_press, pub_filter=pf,
            )
            gloss_res = query_gloss(
                query, gloss_vec, gloss_svd, gloss_norm, gloss_meta, n=n_gloss,
            )
            gen_text = ""
            if use_ollama and selected_model and (press_res or gloss_res):
                with st.spinner(f"Generando respuesta con {selected_model}…"):
                    gen_text = generate_ollama(selected_model, query, press_res, gloss_res)

        st.session_state.last_results = press_res
        st.session_state.last_gloss   = gloss_res
        st.session_state.last_query   = query
        st.session_state.last_gen     = gen_text

# ─── Mostrar resultados ───────────────────────────────────────────────────────
if st.session_state.last_results is not None:
    lq    = st.session_state.last_query
    press = st.session_state.last_results
    gloss = st.session_state.last_gloss
    gen   = st.session_state.last_gen

    st.markdown(f"Resultados para **«{lq}»**")

    # Respuesta generada (si existe)
    if gen:
        st.markdown("#### 🤖 Respuesta generada")
        st.markdown(f'<div class="gen-box">{gen}</div>', unsafe_allow_html=True)
        st.markdown("---")

    # Dos columnas: prensa (izq) | glosario (der)
    col_press, col_gloss = st.columns([3, 2])

    with col_press:
        st.markdown(f"#### 📰 Pasajes de prensa ({len(press)} resultados)")
        if not press:
            st.info("No se encontraron pasajes relevantes.")
        for r in press:
            pub = r["publicacion"]
            cls = f"pub-{pub}"
            b   = badge(r["score"])
            st.markdown(f"""
<div class="passage-card">
  <div class="passage-meta">
    <span class="badge {b}">Relevancia: {r['score']}%</span>
    <span class="pub-chip {cls}">{pub}</span>
    <span>📅 {r['fecha']}</span>
    <span>{r['numero']}</span>
    <span>{r['pagina']}</span>
    <span style="opacity:0.6">{r['pais']}</span>
  </div>
  <div class="passage-text">{r['snippet']}</div>
</div>""", unsafe_allow_html=True)

    with col_gloss:
        st.markdown(f"#### 🗂 Capa experta — Glosario NER ({len(gloss)} entidades)")
        if not gloss:
            st.info("No se encontraron entidades relacionadas.")
        for g in gloss:
            cat = g["category"]
            chip_lbl, chip_fg, chip_bg = CAT_CHIP.get(cat, ("?", "#333", "#EEE"))
            b = badge(g["score"])
            defn = g["definition"][:280] + ("…" if len(g["definition"]) > 280 else "")
            st.markdown(f"""
<div class="gloss-card">
  <div style="margin-bottom:0.3rem">
    <span class="badge {b}">{g['score']}%</span>
    <span style="display:inline-block;padding:0.1rem 0.5rem;border-radius:6px;
          font-size:0.7rem;font-weight:700;background:{chip_bg};color:{chip_fg};
          margin-left:0.4rem">{chip_lbl} {cat}</span>
  </div>
  <div class="gloss-term">{g['term']}</div>
  <div class="gloss-def">{defn}</div>
</div>""", unsafe_allow_html=True)

else:
    # Pantalla de inicio
    if rag_ready:
        pubs_list = list(stats["by_pub"].items())
        colors = ["#0D47A1","#880E4F","#5D4037","#1B5E20","#4A148C"]
        cols   = st.columns(5)
        for i, (col, (pub, cnt)) in enumerate(zip(cols, pubs_list)):
            with col:
                pais = PAIS.get(pub, "")
                st.markdown(
                    f'<div style="background:{colors[i]};color:white;border-radius:10px;'
                    f'padding:1rem 0.5rem;text-align:center;">'
                    f'<div style="font-size:1.6rem;font-weight:800">{cnt}</div>'
                    f'<div style="font-size:0.78rem;opacity:0.85">{pub}</div>'
                    f'<div style="font-size:0.7rem;opacity:0.6">{pais}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown(
            "<br><p style='text-align:center;color:#888;font-size:0.94rem'>"
            "Introduce una consulta para recuperar pasajes de los periódicos franquistas<br>"
            "y entidades relacionadas del Glosario NER."
            "</p>",
            unsafe_allow_html=True,
        )
