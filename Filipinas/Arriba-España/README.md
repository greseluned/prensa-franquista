# Arriba España Manila

## Descripción

Esta carpeta contiene la digitalización y transcripción del periódico **Arriba España Manila**, publicación de la Falange Española en Filipinas durante la década de 1930-1940.

## Contenido

- `jpg/` — Imágenes de las páginas digitalizadas (208 páginas)
- `page_xml/` — Transcripciones en formato PAGE-XML
- `txt/` — Transcripciones en formato de texto plano

## Proceso de transcripción

### Primera fase — Transcripción automática en Transkribus

Las 208 páginas fueron transcritas inicialmente mediante el modelo general de reconocimiento de texto manuscrito e impreso de Transkribus. Al tratarse de un modelo de carácter general entrenado sobre prensa y revistas históricas de distintas procedencias, las transcripciones resultantes presentaban errores de OCR propios de este tipo de procesamiento automático sin especialización: letras mal reconocidas, espacios incorrectos y confusiones entre caracteres similares. Las transcripciones se encontraban en estado "naranja" en Transkribus, es decir, transcritas automáticamente pero sin revisión humana.

### Segunda fase — Corrección post-OCR con Llama 3.2

Con el objetivo de mejorar la calidad de las transcripciones sin necesidad de revisión manual página por página, se aplicó un proceso de corrección post-OCR automática sobre los PAGE-XML exportados desde Transkribus. El proceso utilizó el modelo de lenguaje **Llama 3.2** ejecutado en local mediante **Ollama**, sin coste de créditos ni envío de datos a servicios externos.

El script de corrección procesó el texto de cada `TextLine` del PAGE-XML, pasándolo por el modelo para corregir errores tipográficos de OCR, y escribió el texto corregido de vuelta en el propio XML. A partir de los XML corregidos se generaron también los ficheros TXT correspondientes. De este modo, los PAGE-XML y los TXT son consistentes entre sí y reflejan la transcripción corregida.

El proceso de corrección fue aplicado sobre las 208 páginas disponibles. El script utilizado (`post_ocr_arriba_espana.py`) y el log con el número de líneas procesadas y corregidas por página (`post_ocr_log.txt`) se incluyen en esta carpeta para documentar y reproducir el proceso.

## Limitaciones

Al tratarse de una corrección automática sin revisión humana, pueden persistir errores puntuales de OCR, especialmente en palabras poco frecuentes, nombres propios, términos en tagalo o inglés, y texto muy degradado por el estado físico del original. Se recomienda tener esto en cuenta al utilizar las transcripciones para análisis lingüístico o de contenido.

## Referencias

- Modelo de transcripción: Transkribus (modelo general de prensa y revistas)
- Modelo de corrección post-OCR: Llama 3.2 (Meta), ejecutado en local con Ollama
- Proyecto: GRESEL-UNED (PID2023-151280OB-C22)
