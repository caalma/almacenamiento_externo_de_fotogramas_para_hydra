#!/bin/bash

# Parámetros del usuario
INPUT_DIR="$1"        # Carpeta con las imágenes
FRAMERATE="$2"        # Fotogramas por segundo (ej: 30)
OUTPUT_VIDEO="$3"     # Ruta de salida del video (ej: output.mp4)

# Validar parámetros
if [ -z "$INPUT_DIR" ] || [ -z "$FRAMERATE" ] || [ -z "$OUTPUT_VIDEO" ]; then
    echo "Uso: $0 <directorio_imagenes> <frame_rate> <video_salida>"
    exit 1
fi

# Detectar automáticamente la extensión de las imágenes
IMAGE_EXT=""
if [ "$(ls -1 "$INPUT_DIR"/*.jpeg 2>/dev/null)" ]; then
    IMAGE_EXT="jpeg"
elif [ "$(ls -1 "$INPUT_DIR"/*.png 2>/dev/null)" ]; then
    IMAGE_EXT="png"
else
    echo "Error: No se encontraron imágenes JPG o PNG en $INPUT_DIR"
    exit 1
fi

# Patrón de nombres de imágenes (ajustar según tus archivos, ej: img%03d.jpg)
IMAGE_PATTERN="$INPUT_DIR/frame_%05d.$IMAGE_EXT"

# Comando FFmpeg para generar el video
ffmpeg -framerate "$FRAMERATE" -i "$IMAGE_PATTERN" \
       -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p \
       "$OUTPUT_VIDEO"

# Confirmación
if [ $? -eq 0 ]; then
    echo "Video generado exitosamente: $OUTPUT_VIDEO"
else
    echo "!! Error al generar el video."
    exit 1
fi
