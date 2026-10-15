# Informe técnico: vocabulario controlado del franquismo y prototipo RAG

**Proyecto:** PID2023-151280OB-C22 · GRESEL-UNED · Departamento de Literatura Española, UNED
**Autor:** Fernando Obispo Permuy (técnico informático)
**Supervisión:** Rocío Ortuño Casanova
**Fecha:** octubre de 2026

---

## 1. Objeto

Este informe documenta cómo se han elaborado los dos recursos publicados en este repositorio:

1. El **vocabulario controlado de entidades del franquismo** (Glosario NER), carpeta `vocabulario/`.
2. El **prototipo RAG** de recuperación sobre la prensa del repositorio, carpeta `rag/`.

---

## 2. Glosario NER del franquismo

### 2.1 Objetivo

Disponer de un inventario controlado de las entidades más relevantes del discurso y la simbología franquista, que sirva de base para la anotación semántica, la recuperación de información y el análisis del discurso sobre el corpus de prensa del grupo.

### 2.2 Fuentes procesadas

Cuatro obras procesadas íntegramente, de la introducción a las conclusiones (sin la bibliografía final):

| Fuente | Aportación |
|---|---|
| Zira Box, *España, Año Cero. La construcción simbólica del franquismo* (Alianza, 2010) | Fuente principal: liturgia política, simbolismo y rituales del régimen. 44 bloques, pp. 1-588 |
| Florentino Rodao, *Franquistas sin Franco* (Comares, 2012) | Contexto internacional y redes franquistas en el ámbito hispanofilipino |
| Eduardo González Calleja, «Fascismo para la exportación…», *Hispania* (2014) | Fascismo internacional y organismos de coordinación fascista |
| Carmen Orive de la Rosa, «Arremangando las camisas negras…» (2023) | Género, fascismo femenino y redes transnacionales |

### 2.3 Procedimiento

La extracción se hizo de forma manual con asistencia de IA (Claude, de Anthropic):

1. Lectura de cada fuente en PDF, en bloques de unas 20 páginas.
2. Identificación de entidades candidatas a partir de cuatro preguntas: ¿es un concepto clave del discurso franquista?, ¿un evento datable?, ¿una persona con papel en el período?, ¿un lugar o publicación citado como referencia?
3. Comprobación de que la entidad no estaba ya registrada.
4. Redacción de una definición contextualizada con referencia a las páginas de la fuente.
5. Registro con etiqueta de fuente y referencias cruzadas («Ver también»).
6. Actualización de entradas existentes cuando un bloque aportaba información nueva.
7. Regeneración del PDF al cerrar cada bloque para verificar la integridad y el recuento.

El glosario se mantiene en un script Python (`glosario_ner_franquismo.py`) que genera el PDF con ReportLab y el Word con python-docx. Para su uso en herramientas se exportó a JSON (`vocabulario_gresel_completo.json`) con los campos `id`, `lema`, `categoria`, `definicion`, `fuentes`, `variantes` y `relaciones`.

### 2.4 Resultado

| Categoría | Entradas | % |
|---|---|---|
| TÉRMINOS | 201 | 18,2 % |
| EVENTOS | 165 | 14,9 % |
| PERSONAS | 452 | 40,9 % |
| LUGARES / PUBLICACIONES | 287 | 26,0 % |
| **Total** | **1.105** | **100 %** |

### 2.5 Criterios y limitaciones

- Se excluyeron las entidades de alcance exclusivamente regional o local, las menciones anecdóticas y los topónimos genéricos sin significado simbólico propio. La incorporación de vocabulario regional queda como línea futura.
- El glosario refleja la perspectiva de las cuatro fuentes; puede haber entidades relevantes ausentes.
- Está diseñado para la prensa franquista y **no debe aplicarse a corpus anteriores al franquismo**, como *Excelsior* (Manila, 1929-1932).
- En el JSON, el campo `fuentes` está incompleto (vacío en 83 entradas y sin las atribuciones a González Calleja y Orive de la Rosa, que sí constan en la versión Word/PDF).

---

## 3. Prototipo RAG

### 3.1 Antecedentes

Una primera exploración comparó frameworks RAG (LlamaIndex, LangChain, Haystack), bases vectoriales (ChromaDB, FAISS, Weaviate, Pinecone) y modelos de embeddings, y construyó un prototipo de recuperación solo sobre el glosario. Tras la revisión de la investigadora principal, que indicó que el RAG debía operar sobre los propios periódicos con el glosario como capa adicional, se desarrolló el prototipo actual.

### 3.2 Arquitectura

```
Consulta
   │
   ├─► Índice del corpus de prensa ──► páginas más similares (publicación, fecha, nº, página)
   │       TF-IDF (1-2 gramas) + SVD 512 dim + coseno
   │
   └─► Índice del vocabulario ───────► entradas relacionadas (capa experta)
           TF-IDF (1-2 gramas) + SVD 512 dim + coseno
   │
   └─► (opcional) Ollama: respuesta generada a partir de los pasajes recuperados
```

- Interfaz: Streamlit, ejecución local (`localhost:8501`).
- Sin dependencia de red ni de GPU.
- Corpus: páginas `.txt` de *Excelsior*, *Hispanidad*, *Yugo*, *Avance* y *Los Quijotes*. En la versión enviada a la investigadora principal se indexaron 1.925 páginas.
- Los metadatos (fecha, número, página) se extraen del nombre de cada fichero.

### 3.3 Prueba funcional

Consultas ejecutadas sobre el prototipo y resultado principal devuelto:

| Consulta | Relevancia máx. | Primer resultado |
|---|---|---|
| «Falange española en Filipinas» | 39 % | *Yugo* (1938-01-25), artículo sobre el Día de los Caídos |
| «José Antonio Primo de Rivera» | 52 % | Sumario de *Yugo* (1938-01-25) con artículos dedicados al fundador |
| «Hispanidad y misión de España en América» | 40 % | Artículos de *Los Quijotes* y *Avance* sobre la Hispanidad |
| «Prensa y propaganda del régimen franquista» | 56 % | Portada de *Yugo*: Delegación Territorial de Prensa y Propaganda de FET de las JONS en Filipinas |
| «República española comunismo» (filtro *Excelsior*) | 24 % | Artículos de *Excelsior* de 1938 sobre la amenaza comunista |

Se trata de una prueba cualitativa; no se ha realizado todavía una evaluación sistemática con métricas.

### 3.4 Limitaciones

- Recuperación léxico-semántica (TF-IDF + SVD); no se usan embeddings neuronales.
- Calidad dependiente del OCR; parte del corpus no tiene revisión humana.
- Sin evaluación cuantitativa todavía.

---

## 4. Próximos pasos

1. Diseñar un conjunto de preguntas de evaluación con el equipo investigador y comparar la recuperación con y sin capa experta.
2. Sustituir TF-IDF + SVD por embeddings neuronales multilingües cuando se disponga del entorno adecuado.
3. Completar el campo `fuentes` del JSON y añadir las entradas sobre Falange Exterior que prepare el equipo.
4. Elaborar un vocabulario específico de naturaleza para *Excelsior* (1929-1932), siguiendo la misma metodología.
