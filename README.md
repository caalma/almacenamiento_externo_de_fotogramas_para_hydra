# Almacenamiento externo de fotogramas para Hydra

Este proyecto es una exploración para encontrar una técnica que permita almacenar en disco los imágenes dinámicamente generadas en un canvas de html.

Particularmente está configurado para que la generación de imágenes se realiza mediante hydra. Aunque, con los ajustes necesarios, podría utilizarse para cualquier canvas.

Requiere del uso de python para establecer un servidor que reciba las imágenes y las almacene. Además de algunas librerías própias indicadas en `requirements.txt`.


## Modo de uso

Es necesario ejecutar el servidor disponible en `server.py`. Luego abrir el `webclient/index.html` desde cualquier browser. Y ejecutar los comandos necesarios, indicados en la misma página, desde la consola de desarrolador.

También están disponibles algunos scripts en bash para automatizar ciertos pasos comunes.


## Pendiente

+ Mejoras de rendimiento cuando el framerate crece o las dimensiones de la imagen. En este intento inicial estoy usando websocket.
+ Hacer más amigable la interfaz web.
+ Probarlo en otros sistemas operativos. Solamente probado en GNU/Linux.
+ Crear alguna extensión para Hydra que permita disponer de la funcionalidad. En esta prueba inicial, simplemente modifique algunos puntos específicos del código de hydra-synth.js para poder agregar algunas características que creí necesitar para este proyecto.

Cualquier sugerencia será tenida en cuenta.
