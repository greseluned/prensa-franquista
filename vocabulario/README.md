# Vocabulario Controlado GRESEL — Prensa Franquista

## Descripción

`vocabulario_gresel_completo.json` es el vocabulario controlado del grupo GRESEL para el análisis de la **prensa franquista de circulación en Filipinas y Puerto Rico** (décadas de 1930–1960).

Contiene **1.105 entidades** nombradas, organizadas en cuatro categorías de etiquetado NER (Named Entity Recognition).

---

## Categorías

| Categoría | Descripción |
|---|---|
| `TÉRMINOS` | Conceptos temáticos del discurso franquista: hispanidad, catolicismo, anticomunismo, etc. |
| `PERSONAS` | Figuras históricas: políticos, militares, religiosos, periodistas relevantes |
| `EVENTOS` | Sucesos históricos: Guerra Civil, proclamaciones, actos oficiales, etc. |
| `LUGARES` | Topónimos: ciudades, regiones, países mencionados en la prensa |

---

## Estructura del JSON

```json
{
  "TÉRMINOS": [
    "Hispanidad",
    "Cruzada",
    ...
  ],
  "PERSONAS": [
    "Francisco Franco",
    "José Antonio Primo de Rivera",
    ...
  ],
  "EVENTOS": [
    "Guerra Civil Española",
    "Alzamiento Nacional",
    ...
  ],
  "LUGARES": [
    "Manila",
    "Filipinas",
    "Madrid",
    ...
  ]
}
```

---

## Fuentes y metodología

El vocabulario está basado principalmente en la obra de **Florentino Rodao** sobre la proyección del franquismo en Asia y el Pacífico, especialmente:

- Rodao, F. (2002). *Franco y el Imperio Japonés: Imágenes y propaganda en tiempos de guerra*. Plaza & Janés.
- Análisis del discurso franquista en publicaciones periódicas filipinas y puertorriqueñas.

El proceso de elaboración incluyó:
1. Revisión bibliográfica de la historiografía sobre el franquismo exterior
2. Análisis de los corpus textuales disponibles (Excelsior, Hispanidad, Yugo, Avance, Los Quijotes)
3. Validación terminológica por parte del equipo investigador GRESEL
4. Codificación manual por Fernando Obispo Permuy (técnico TIC, UNED)

---

## Alcance y limitaciones

> **IMPORTANTE**: Este vocabulario está diseñado específicamente para la **prensa franquista** (ca. 1936–1975). NO es adecuado para corpus anteriores al franquismo, como la revista *Excelsior* de Manila (1929–1932), que requiere un vocabulario propio adaptado a su contexto histórico pre-franquista.

Para el corpus *Excelsior* (1929–1932) se está elaborando un vocabulario específico de temática naturaleza/patrimonio (trabajo en curso, Diana Villanueva Romero, UEx).

---

## Uso en el sistema RAG

Este vocabulario se usa como **capa de experto** en la aplicación `../rag/app_rag_prensa_franquista.py`:

```python
from glosario_ner_franquismo import VOCABULARIO_GRESEL
# Enriquece los resultados de búsqueda con contexto histórico
```

---

## Contacto

- Proyecto: PID2023-151280OB-C22
- Grupo: GRESEL-UNED
- Web: [gresel-uned.hypotheses.org](https://gresel-uned.hypotheses.org)
