from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from .models import Logger
from datetime import datetime
import asyncio
import cv2
import numpy as np
import os

def index(request):
    logs = Logger.objects.all()
    return render(request, "index.html", {"logs": logs})


async def acreate_log(ticker_message):
    log = await Logger.objects.acreate(log_text=ticker_message, datetime=datetime.now())


def getText(request, text):
    create_ticker_video_opencv(text)
    file_path = f"downloading_media//{text}.mp4"
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"{text}.mp4")


def create_ticker_video_opencv(ticker_text):
    # Текст из адресной строки
    ticker_message = ticker_text

    # Размеры видео (ширина x высота)
    width, height = 100, 100

    # Задаём параметры - видеопоток с частотой 24 кадра в секунду
    out = cv2.VideoWriter(f"downloading_media//{ticker_text}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

    # Создаем кадр с черным фоном
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Начальные координаты для бегущей строки
    x, y = width, height // 2

    # Установим параметры шрифта
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)  # Белый цвет текста

    # Общая продолжительность видео в кадрах
    total_frames = 72  # 3 секунды с частотой 24 кадра/сек
    # Вычисляем длину текста
    text_size = cv2.getTextSize(ticker_message, font, font_scale, font_thickness)[0]
    text_width = text_size[0]
     # Скорость движения текста
    speed = (text_width + width) / total_frames


    # Пройдемся по каждому кадру
    for t in range(total_frames):  # 3 секунды с частотой 24 кадра/сек
        # Очистка кадра
        frame.fill(0)

        # Новые координаты для бегущей строки
        x = width - int(speed * t)

        # Вот тут добавим текст
        cv2.putText(frame, ticker_message, (x, y), font, font_scale, font_color, font_thickness)

        # Тут запишем кадр
        out.write(frame)

    # Закроем тут видеопоток
    out.release()
    asyncio.run(acreate_log(ticker_message))
    # download_file(ticker_text)
