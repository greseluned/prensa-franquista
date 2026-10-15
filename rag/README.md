# Prototipo RAG — Prensa franquista

Aplicación local de recuperación semántica sobre las transcripciones de este repositorio, con el vocabulario controlado de entidades del franquismo como capa experta.

## Qué hace

- Indexa las páginas `.txt` de las cinco cabeceras del repositorio (*Excelsior*, *Hispanidad* y *Yugo* en Filipinas; *Avance* y *Los Quijotes* en Puerto Rico).
- Ante una consulta, recupera las páginas más próximas (TF-IDF de 1-2 gramas, SVD a 512 dimensiones y similitud coseno) y muestra publicación, fecha, número y página.
- Junto a cada resultado muestra las entradas del vocabulario relacionadas (1.105 entradas, carpeta `../vocabulario/`).
- Permite filtrar por publicación y ajustar el número de resultados.
- Si Ollama está instalado, puede generar una respuesta en lenguaje natural a partir de los pasajes recuperados (opcional).

Funciona sin conexión a internet y sin GPU.

## Requisitos

- Python 3.10 o superior
- Git
- (Opcional) [Ollama](https://ollama.com) con un modelo pequeño, por ejemplo `llama3.2:3b` o `qwen2.5:3b`

## Instalación

```bash
git clone https://github.com/greseluned/prensa-franquista.git
cd prensa-franquista/rag
pip install -r requirements.txt
```

El repositorio completo ocupa varios GB porque incluye las transcripciones.

## Ejecución

Desde la carpeta `rag/`:

```bash
streamlit run app_rag_prensa_franquista.py
```

La aplicación se abre en el navegador (`http://localhost:8501`). La primera vez tarda un poco en indexar el corpus.

La app localiza automáticamente:

- el corpus en la raíz del repositorio (`Filipinas/` y `Puerto-Rico/`);
- el vocabulario en `vocabulario/vocabulario_gresel_completo.json`.

## Generación opcional con Ollama

```bash
ollama pull llama3.2:3b
```

Con Ollama en marcha, la app detecta los modelos instalados y permite activar la generación desde el panel lateral.

## Limitaciones

- La recuperación es léxico-semántica (TF-IDF + SVD), no se usan embeddings neuronales.
- La calidad depende del OCR. Parte del corpus no tiene revisión humana.
- Es un prototipo para exploración interna y todavía no se ha evaluado de forma sistemática.
