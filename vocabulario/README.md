# Vocabulario controlado de entidades del franquismo

`vocabulario_gresel_completo.json` es la versión estructurada del **Glosario NER del Franquismo** elaborado en el proyecto GRESEL-UNED (PID2023-151280OB-C22). Contiene **1.105 entradas**.

## Fuentes

El glosario se construyó procesando íntegramente, página a página, cuatro obras de referencia:

| Etiqueta | Obra |
|---|---|
| [Zira Box] | Zira Box, *España, Año Cero. La construcción simbólica del franquismo*, Madrid, Alianza Editorial, 2010. Fuente principal (pp. 1-588, procesada en 44 bloques). |
| [Rodao] | Florentino Rodao, *Franquistas sin Franco. Una historia alternativa de la Guerra Civil española desde Filipinas*, Granada, Comares, 2012. |
| [González Calleja] | Eduardo González Calleja, «Fascismo para la exportación: la delegación española del CAUR y el proyecto de una Internacional Fascista, 1933-1936», *Hispania*, LXXIV/246 (2014), pp. 205-236. |
| [Orive de la Rosa] | Carmen Orive de la Rosa, «Arremangando las camisas negras: una historia transnacional del fascismo desde el feminismo», 2023. |

## Categorías

| Categoría | Entradas | % |
|---|---|---|
| TÉRMINOS | 201 | 18,2 % |
| EVENTOS | 165 | 14,9 % |
| PERSONAS | 452 | 40,9 % |
| LUGARES / PUBLICACIONES | 287 | 26,0 % |
| **Total** | **1.105** | **100 %** |

En el JSON, la categoría LUGARES/PUBLICACIONES aparece con el valor `"LUGARES"`.

## Estructura de cada entrada

Entrada real del archivo:

```json
{
  "id": "cruzada",
  "lema": "Cruzada",
  "categoria": "TÉRMINOS",
  "definicion": "Denominación oficial con la que el régimen y la Iglesia católica definieron la guerra civil española (1936–1939). Al presentar el conflicto como una cruzada religiosa contra el «marxismo ateo», se confería al alzamiento una dimensión sacra que legitimaba la violencia bélica.",
  "fuentes": [],
  "variantes": ["una cruzada"],
  "relaciones": [
    {"lema": "Nacional-catolicismo", "categoria": "TÉRMINO"},
    {"lema": "Alzamiento Nacional", "categoria": "EVENTO"},
    {"lema": "Religión política", "categoria": "TÉRMINO"}
  ]
}
```

- `lema`: forma normalizada (en personas, «Apellidos, Nombre»).
- `definicion`: definición contextualizada con referencias de página a las fuentes.
- `fuentes`: obras de las que procede la información. En la exportación actual el campo está relleno en 1.022 entradas (951 con [Zira Box] y 71 con [Rodao]) y vacío en 83; las atribuciones a González Calleja y Orive de la Rosa constan en la versión PDF/Word del glosario, pero no se trasladaron al JSON. Queda pendiente completar este campo.
- `variantes`: formas alternativas de denominación.
- `relaciones`: referencias cruzadas («Ver también») a otras entradas.

## Metodología resumida

La extracción se hizo manualmente con asistencia de IA, leyendo cada fuente en bloques de unas 20 páginas. Para cada bloque se identificaban entidades candidatas, se comprobaba que no estuvieran ya registradas, se redactaba la definición con referencia a las páginas y se añadían referencias cruzadas. El detalle completo está en [`../documentacion/informe_tecnico_GRESEL.md`](../documentacion/informe_tecnico_GRESEL.md).

## Alcance

- El vocabulario se diseñó para la **prensa franquista**. No es adecuado para corpus anteriores al franquismo, como *Excelsior* (Manila, 1929-1932).
- Prioriza la dimensión estatal y nacional del franquismo; el vocabulario regional y local está subrepresentado y queda como línea de trabajo futura.
- Refleja la perspectiva de las cuatro fuentes procesadas.
