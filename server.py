import asyncio
import websockets
import os
import cv2
import numpy as np
import json
from io import BytesIO

# Configuración
SAVE_DIR = './frames/'
SERVER_HOST = 'localhost'
SERVER_PORT = 9009
VIDEO_OUTPUT = ''
FRAME_RATE = ''
IMAGE_FORMAT = ''

DELETE_PREVIOUS_FRAMES = True
DELETE_LAST_FRAMES = False

async def handle_connection(websocket):
    global VIDEO_OUTPUT, FRAME_RATE, IMAGE_FORMAT
    os.makedirs(SAVE_DIR, exist_ok=True)
    frame_count = 0

    try:
        # Recibir configuración inicial
        config = await websocket.recv()
        config_data = json.loads(config)
        IMAGE_FORMAT = config_data.get('format', 'png')
        video_filename = config_data.get('filename', 'output')
        VIDEO_OUTPUT = f'{video_filename}.mp4'
        FRAME_RATE = config_data.get('fps', '30')

        print(f'{"-"*20} NUEVA CAPTURA')
        print(f'  Formato de imagen seleccionado: {IMAGE_FORMAT}')
        print(f'  Tasa de muestreo: {FRAME_RATE}')

        if DELETE_PREVIOUS_FRAMES:
            delete_frames()

        # Bucle principal
        while True:
            message = await websocket.recv()

            # Si es mensaje de finalización
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                    if data.get('action') == 'done':
                        print('  Finalizando transmisión...')
                        break
                except:
                    continue

            # Guardar frame
            frame_path = os.path.join(SAVE_DIR, f'frame_{frame_count:05d}.{IMAGE_FORMAT}')
            with open(frame_path, 'wb') as f:
                f.write(message)

            if (frame_count % 50) == 0:
                print(f'  ... registrando por el fotograma: {frame_count}')

            frame_count += 1

    except websockets.exceptions.ConnectionClosed:
        print('  Conexión cerrada.')

    # Crear video
    create_video(frame_count)


def delete_frames():
    for f in os.listdir(SAVE_DIR):
        os.remove(os.path.join(SAVE_DIR, f))


def create_video(frame_count):
    print(f'  Creando video con {frame_count} frames ({IMAGE_FORMAT})...')

    # Leer primer frame para obtener dimensiones
    first_frame = cv2.imread(os.path.join(SAVE_DIR, f'frame_00000.{IMAGE_FORMAT}'))
    if first_frame is None:
        print('  !! Error: No se pudo leer el primer frame.')
        return

    height, width, _ = first_frame.shape

    # Configurar VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(VIDEO_OUTPUT, fourcc, FRAME_RATE, (width, height))

    # Escribir frames
    for i in range(frame_count):
        frame_path = os.path.join(SAVE_DIR, f'frame_{i:05d}.{IMAGE_FORMAT}')
        frame = cv2.imread(frame_path)
        if frame is None:
            print(f'  !! Error leyendo frame {i}')
            continue
        out.write(frame)

    out.release()

    if DELETE_LAST_FRAMES:
        delete_frames()

    print(f'  Video guardado como: {VIDEO_OUTPUT}')
    print(f'{"-"*20}. \n\n')


async def main():
    async with websockets.serve(
        handle_connection,
        SERVER_HOST,
        SERVER_PORT,
        ping_interval=None
    ):
        print(f'-- Servidor iniciado en ws://{SERVER_HOST}:{SERVER_PORT}')
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
