# Prensa Franquista — GRESEL (UNED)

Repositorio de recursos digitales del grupo **GRESEL** (Grupo de Investigación en Estudios de Literatura Española) de la UNED, proyecto **PID2023-151280OB-C22**.

Contiene el vocabulario controlado, el sistema RAG y la documentación técnica para el análisis de la prensa franquista de circulación en Filipinas y Puerto Rico.

---

## Estructura del repositorio

```
prensa-franquista/
│
├── vocabulario/               # Vocabulario controlado GRESEL
│   ├── vocabulario_gresel_completo.json   # 1.105 entidades etiquetadas
│   └── README.md              # Descripción del vocabulario y categorías
│
├── rag/                       # Sistema RAG (Retrieval-Augmented Generation)
│   ├── app_rag_prensa_franquista.py       # Aplicación Streamlit principal
│   ├── requirements.txt       # Dependencias Python
│   └── README.md              # Instrucciones de instalación y uso
│
├── documentacion/             # Informes y metodología
│   └── informe_tecnico_GRESEL.md          # Informe técnico completo
│
└── README.md                  # Este archivo
```

---

## Corpus cubierto

| Territorio | Publicación | Período |
|---|---|---|
| Filipinas | *Excelsior* | 1929–1932 |
| Filipinas | *Hispanidad* | Por confirmar |
| Filipinas | *Yugo* | Por confirmar |
| Puerto Rico | *Avance* | Por confirmar |
| Puerto Rico | *Los Quijotes* | Por confirmar |

---

## Vocabulario GRESEL

El vocabulario controlado (`vocabulario/`) contiene **1.105 entidades** organizadas en cuatro categorías:

- `TÉRMINOS` — conceptos temáticos relevantes para la prensa franquista
- `PERSONAS` — figuras históricas y políticas
- `EVENTOS` — sucesos históricos y coyunturales
- `LUGARES` — topónimos geográficos relevantes

Basado en la obra de Florentino Rodao sobre la propaganda franquista en Asia y el Pacífico.

---

## Sistema RAG

La aplicación RAG (`rag/`) permite buscar y recuperar fragmentos del corpus usando:

- **TF-IDF + SVD** (recuperación semántica por similitud de coseno)
- **Vocabulario GRESEL** como capa de experto para enriquecimiento contextual
- **Generación opcional** con modelos Ollama locales (`qwen2.5:3b`, `llama3.2:3b`, `mistral`)

---

## Equipo

- **IP del proyecto**: Rocío Ortuño Casanova (UNED)
- **Desarrollo técnico**: Fernando Obispo Permuy (UNED)
- **Proyecto**: PID2023-151280OB-C22
- **Grupo**: GRESEL-UNED — [gresel-uned.hypotheses.org](https://gresel-uned.hypotheses.org)

---

## Licencia

Este recurso es de uso académico e investigador. Para otros usos, contactar con el grupo GRESEL.
