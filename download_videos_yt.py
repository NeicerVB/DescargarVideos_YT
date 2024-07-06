from pytube import YouTube
import subprocess
import re
import os

def Descargar_Video_YT(URL):
    yt = YouTube(URL)

    # Descargar el audio y video con mejor calidad
    video_stream = yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first()
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Descargar el audio y video
    video_stream.download(output_path="./Videos", filename="video.mp4")
    audio_stream.download(output_path="./Videos", filename="audio.mp3")

    # Limpiar el título del video para evitar caracteres especiales
    titulo = re.sub(r"[-|,\.\\/<>\"?¿:*]", "" , yt.title)

    # Combinar el audio y video con ffmpeg
    fileName = f"./Videos/{titulo}.mp4"
    subprocess.run(
        [
            "N:/FFmpeg/FFmpeg/bin/ffmpeg.exe",
            "-i", "Videos/video.mp4",
            "-i", "Videos/audio.mp3",
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            fileName
        ]
    )

    # Eliminamos los archivos de audio y video para liberar espacio
    os.remove("./Videos/video.mp4")
    os.remove("./Videos/audio.mp3")

    # Devolvemos el video descargado
    return fileName