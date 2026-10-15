# Sistema RAG — Prensa Franquista (GRESEL-UNED)

Aplicación de búsqueda semántica y generación aumentada por recuperación (RAG) para los corpus de prensa franquista de circulación en **Filipinas** y **Puerto Rico**.

---

## Requisitos previos

- Python 3.9 o superior
- [Streamlit](https://streamlit.io/)
- (Opcional) [Ollama](https://ollama.com/) con un modelo local para generación de texto

---

## Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/greseluned/prensa-franquista.git
cd prensa-franquista/rag

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. (Opcional) Instala Ollama y descarga un modelo
#    https://ollama.com/download
ollama pull qwen2.5:3b
```

---

## Estructura del corpus

Coloca los textos del corpus en una carpeta `corpus/` en el mismo directorio que la app:

```
rag/
├── app_rag_prensa_franquista.py
├── requirements.txt
├── glosario_ner_franquismo.py          ← vocabulario GRESEL como módulo Python
└── corpus/
    ├── Filipinas/
    │   ├── Excelsior/
    │   │   └── txt/
    │   │       ├── pagina_001.txt
    │   │       └── ...
    │   ├── Hispanidad/
    │   │   └── txt/
    │   └── Yugo/
    │       └── txt/
    └── Puerto-Rico/
        ├── Avance/
        │   └── txt/
        └── Los-Quijotes/
            └── txt/
```

Cada archivo `.txt` contiene el texto de una página o artículo del corpus.

---

## Glosario NER como módulo Python

El archivo `glosario_ner_franquismo.py` debe contener el vocabulario GRESEL en formato de diccionario Python:

```python
# glosario_ner_franquismo.py
VOCABULARIO_GRESEL = {
    "TÉRMINOS": ["Hispanidad", "Cruzada", ...],
    "PERSONAS": ["Francisco Franco", ...],
    "EVENTOS": ["Guerra Civil Española", ...],
    "LUGARES": ["Manila", "Filipinas", ...]
}
```

Puedes generarlo automáticamente a partir de `../vocabulario/vocabulario_gresel_completo.json`.

---

## Ejecución

```bash
streamlit run app_rag_prensa_franquista.py
```

La aplicación se abrirá en el navegador en `http://localhost:8501`.

---

## Funcionalidades

### Búsqueda semántica
- Indexación del corpus con **TF-IDF** y reducción dimensional **TruncatedSVD** (LSA)
- Recuperación por **similitud de coseno** entre la consulta y los fragmentos del corpus
- Filtrado opcional por publicación o territorio

### Capa de experto (Vocabulario GRESEL)
- Identifica automáticamente entidades del vocabulario GRESEL en los resultados
- Enriquece la presentación con contexto histórico

### Generación de respuestas (opcional, requiere Ollama)
- Genera respuestas en lenguaje natural a partir de los fragmentos recuperados
- Modelos compatibles: `qwen2.5:3b`, `llama3.2:3b`, `mistral`

---

## Tecnología

| Componente | Tecnología |
|---|---|
| Interfaz | Streamlit |
| Indexación | scikit-learn TF-IDF + TruncatedSVD |
| Recuperación | Cosine similarity |
| Generación | Ollama (local, opcional) |

---

## Proyecto

- **Grupo**: GRESEL-UNED
- **Proyecto**: PID2023-151280OB-C22
- **IP**: Rocío Ortuño Casanova
- **Desarrollo**: Fernando Obispo Permuy
- **Web**: [gresel-uned.hypotheses.org](https://gresel-uned.hypotheses.org)
