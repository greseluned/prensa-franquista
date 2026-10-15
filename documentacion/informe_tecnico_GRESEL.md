# Informe Técnico — Vocabulario NER y Sistema RAG para la Prensa Franquista

**Proyecto**: PID2023-151280OB-C22  
**Grupo**: GRESEL-UNED  
**Elaborado por**: Fernando Obispo Permuy (Técnico TIC, UNED)  
**Supervisión científica**: Rocío Ortuño Casanova (IP, UNED)  
**Fecha**: Octubre 2026  

---

## 1. Introducción

Este informe describe el proceso de elaboración del **vocabulario controlado GRESEL** para el análisis de Named Entities (NER) en la prensa franquista de circulación en Filipinas y Puerto Rico, así como el desarrollo del **sistema RAG** (Retrieval-Augmented Generation) para la explotación de estos corpus.

El trabajo se enmarca en el proyecto de investigación PID2023-151280OB-C22, financiado por el Ministerio de Ciencia, Innovación y Universidades (MICIU/AEI), y forma parte de la línea de **Humanidades Digitales** del grupo GRESEL-UNED.

---

## 2. Vocabulario Controlado NER

### 2.1 Objetivo

Construir un léxico de entidades nombradas representativas del **discurso franquista** en prensa de circulación hispanofilipina e hispanoboricua, que permita:

- Etiquetar automáticamente documentos del corpus
- Enriquecer búsquedas semánticas con contexto histórico
- Cuantificar la presencia de entidades clave en el corpus

### 2.2 Categorías

El vocabulario se organiza en cuatro categorías NER:

| Categoría | N.º entidades (aprox.) | Descripción |
|---|---|---|
| `TÉRMINOS` | ~350 | Conceptos del discurso franquista (Hispanidad, Cruzada, Caudillo…) |
| `PERSONAS` | ~300 | Figuras históricas relevantes (políticos, militares, religiosos…) |
| `EVENTOS` | ~200 | Sucesos históricos del período (Guerra Civil, proclamaciones…) |
| `LUGARES` | ~255 | Topónimos de relevancia (ciudades, regiones, países…) |
| **TOTAL** | **~1.105** | |

### 2.3 Fuentes

El vocabulario se ha elaborado principalmente a partir de:

1. **Rodao, Florentino** (2002). *Franco y el Imperio Japonés: Imágenes y propaganda en tiempos de guerra*. Plaza & Janés. — Principal fuente historiográfica sobre el franquismo en Asia.
2. **Análisis exploratorio del corpus**: lectura y análisis manual de ejemplares de *Excelsior* (Manila), *Hispanidad*, *Yugo*, *Avance* (Puerto Rico) y *Los Quijotes*.
3. **Bibliografía secundaria** sobre propaganda franquista exterior, hispanismo y relaciones con Filipinas y Puerto Rico.

### 2.4 Proceso de elaboración

1. **Revisión bibliográfica**: Extracción de entidades nombradas relevantes de la bibliografía historiográfica.
2. **Análisis de corpus**: Lectura exploratoria de fragmentos representativos de las publicaciones del corpus.
3. **Codificación manual**: Clasificación de cada entidad en su categoría NER correspondiente.
4. **Validación**: Revisión y validación por parte del equipo investigador GRESEL.
5. **Serialización**: Exportación a formato JSON (`vocabulario_gresel_completo.json`) para su uso en sistemas informáticos.

### 2.5 Formato de salida

El vocabulario se distribuye en formato JSON:

```json
{
  "TÉRMINOS": ["Hispanidad", "Cruzada", "Caudillo", ...],
  "PERSONAS": ["Francisco Franco", "José Antonio Primo de Rivera", ...],
  "EVENTOS": ["Guerra Civil Española", "Alzamiento Nacional", ...],
  "LUGARES": ["Manila", "Filipinas", "Madrid", "Puerto Rico", ...]
}
```

### 2.6 Limitaciones y alcance

> El vocabulario GRESEL está diseñado **exclusivamente para la prensa franquista** (ca. 1936–1975). No es adecuado para corpus anteriores al período franquista, como la revista *Excelsior* de Manila (1929–1932), cuyo contenido es predominantemente colonial filipino, pre-franquista y de temática distinta.

Para el corpus *Excelsior* (1929–1932) se está elaborando un vocabulario específico de temática naturaleza/patrimonio natural filipino, a cargo de Diana Villanueva Romero (Universidad de Extremadura), en el marco del grupo de trabajo PHASSES (EUGreen Alliance).

---

## 3. Sistema RAG (Retrieval-Augmented Generation)

### 3.1 Objetivo

Desarrollar una herramienta de consulta semántica del corpus de prensa franquista que permita:

- Buscar fragmentos relevantes del corpus mediante lenguaje natural
- Enriquecer los resultados con el vocabulario GRESEL
- (Opcionalmente) Generar respuestas en lenguaje natural con modelos locales

### 3.2 Arquitectura del sistema

```
CONSULTA DEL USUARIO
        │
        ▼
┌───────────────────┐
│   Vectorización   │  TF-IDF + TruncatedSVD (LSA, 300 dims)
│   de la consulta  │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Búsqueda por     │  Cosine similarity sobre índice TF-IDF
│  similitud        │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Fragmentos       │  Top-K fragmentos más relevantes
│  recuperados      │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Capa de experto  │  Identificación de entidades GRESEL
│  (vocabulario)    │  en los fragmentos recuperados
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Generación       │  Ollama local (opcional)
│  (opcional)       │  qwen2.5:3b / llama3.2:3b / mistral
└───────────────────┘
        │
        ▼
   RESULTADO EN PANTALLA (Streamlit)
```

### 3.3 Componentes técnicos

#### Indexación del corpus

La indexación se realiza una sola vez al arrancar la aplicación:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline

# Pipeline de vectorización semántica
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ('svd', TruncatedSVD(n_components=300))
])

corpus_vectors = pipeline.fit_transform(documentos)
```

#### Recuperación

```python
from sklearn.metrics.pairwise import cosine_similarity

query_vector = pipeline.transform([consulta])
scores = cosine_similarity(query_vector, corpus_vectors)[0]
top_k_idx = scores.argsort()[::-1][:10]
fragmentos = [documentos[i] for i in top_k_idx]
```

#### Generación con Ollama (opcional)

```python
import requests

prompt = f"""Contexto: {fragmentos_recuperados}
Pregunta: {consulta}
Responde en español basándote únicamente en el contexto proporcionado."""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "qwen2.5:3b", "prompt": prompt, "stream": False}
)
```

### 3.4 Corpus cubierto

| Publicación | Territorio | Período | Estado |
|---|---|---|---|
| *Excelsior* | Filipinas | 1929–1932 | ✅ Indexado |
| *Hispanidad* | Filipinas | Por confirmar | 🔄 Pendiente de corpus |
| *Yugo* | Filipinas | Por confirmar | 🔄 Pendiente de corpus |
| *Avance* | Puerto Rico | Por confirmar | 🔄 Pendiente de corpus |
| *Los Quijotes* | Puerto Rico | Por confirmar | 🔄 Pendiente de corpus |

### 3.5 Interfaz

La aplicación utiliza **Streamlit** como framework de interfaz web:

- Panel lateral: selección de corpus, modelo de generación, número de resultados
- Área principal: campo de búsqueda, resultados con puntuación de relevancia
- Resaltado de entidades GRESEL en los fragmentos recuperados

### 3.6 Ejecución

```bash
streamlit run app_rag_prensa_franquista.py
```

Acceso en: `http://localhost:8501`

---

## 4. Etiquetado semántico y estructural

*(Sección en desarrollo — ver repositorio `greseluned/Etiquetado`)*

En paralelo al vocabulario NER y al sistema RAG, se ha desarrollado una herramienta de **etiquetado semántico y estructural** del corpus:

- **`app_etiquetado_semantico.py`**: Aplicación Streamlit para etiquetar fragmentos manualmente con las categorías GRESEL
- **`etiquetado_semantico_gresel.csv`**: Resultados del etiquetado realizado hasta la fecha

El etiquetado estructural (identificación de secciones, titulares, artículos, anuncios…) está en curso.

---

## 5. Próximos pasos

1. **Ampliar el corpus**: Incorporar los textos de *Hispanidad*, *Yugo*, *Avance* y *Los Quijotes* cuando estén disponibles en formato digital.
2. **Vocabulario Excelsior**: Integrar el vocabulario de naturaleza/patrimonio natural de Diana Villanueva Romero (UEx) cuando esté disponible, como nueva categoría `NATURALEZA` en el JSON.
3. **Evaluación del RAG**: Diseñar un conjunto de preguntas de evaluación para medir la precisión y recall del sistema de recuperación.
4. **Integración con etiquetado**: Conectar el sistema RAG con los resultados del etiquetado semántico para búsquedas más precisas.

---

## 6. Referencias

- Rodao, F. (2002). *Franco y el Imperio Japonés: Imágenes y propaganda en tiempos de guerra*. Plaza & Janés.
- Ortuño Casanova, R. (coord.). Proyecto PID2023-151280OB-C22. GRESEL-UNED.
- Villanueva Romero, D. (2026). "Unearthing Nature in the Digitized Historical Press: The Case of the Hispanophone Magazine *Excelsior*". Ponencia presentada en el workshop *Memory and Expectations: Rethinking Heritage*, 16 de septiembre de 2026, EUGreen Alliance / PHASSES.

---

*Documento elaborado por Fernando Obispo Permuy, técnico TIC UNED, en el marco del proyecto PID2023-151280OB-C22. Octubre 2026.*
