# prensa-franquista

Ejemplares de periódicos pro-franquistas y falangistas de Filipinas y Puerto Rico relacionados con el estudio de caso del proyecto **GRESEL-UNED** (PID2023-151280OB-C22), junto con los recursos derivados: el vocabulario controlado de entidades del franquismo y un prototipo de recuperación semántica (RAG) sobre el corpus.

Estudio de caso: [gresel-uned.hypotheses.org](https://gresel-uned.hypotheses.org)

---

## Estructura del repositorio

```
prensa-franquista/
├── Filipinas/          Transcripciones de las cabeceras filipinas
├── Puerto-Rico/        Transcripciones de Avance y Los Quijotes
├── vocabulario/        Vocabulario controlado de entidades del franquismo (1.105 entradas, JSON)
├── rag/                Prototipo RAG en Streamlit e instrucciones de instalación
└── documentacion/      Informe técnico del vocabulario y del prototipo RAG
```

De acuerdo con los criterios del proyecto, en este repositorio solo se publican transcripciones y archivos XML; los PDF originales no se comparten.

---

## Vocabulario controlado

`vocabulario/vocabulario_gresel_completo.json` contiene **1.105 entradas** extraídas de cuatro obras historiográficas sobre el franquismo (Zira Box, Rodao, González Calleja y Orive de la Rosa):

| Categoría | Entradas |
|---|---|
| TÉRMINOS | 201 |
| EVENTOS | 165 |
| PERSONAS | 452 |
| LUGARES / PUBLICACIONES | 287 |
| **Total** | **1.105** |

Este vocabulario está pensado para la prensa franquista. No debe aplicarse a corpus anteriores al franquismo, como *Excelsior* (1929-1932).

Más información en [`vocabulario/README.md`](vocabulario/README.md).

---

## Prototipo RAG

Aplicación local en Streamlit que recupera páginas del corpus mediante TF-IDF + SVD y similitud coseno, y muestra junto a cada resultado las entradas del vocabulario relacionadas. La generación de respuestas con Ollama es opcional.

Instrucciones en [`rag/README.md`](rag/README.md).

---

## Créditos

- Investigadora principal: Rocío Ortuño Casanova (UNED)
- Colaborador técnico: Fernando Obispo Permuy (UNED)
- Financiación: Ministerio de Ciencia, Innovación y Universidades / AEI, proyecto PID2023-151280OB-C22
