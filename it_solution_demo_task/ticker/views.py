from django.shortcuts import render
from django.http import HttpResponse
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
    return HttpResponse(create_ticker_video_opencv(text))

def create_ticker_video_opencv(ticker_text):
    # Текст из адресной строки
    ticker_message = ticker_text

    # Размеры видео (ширина x высота)
    width, height = 100,100

    # Задаём параметры - видеопоток с частотой 24 кадра в секунду
    out = cv2.VideoWriter(f"{ticker_text}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

    # Создаем кадр с черным фоном
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Начальные координаты для бегущей строки
    x, y = width, height // 2

    # Установим параметры шрифта
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)  # Белый цвет текста

    # Пройдемся по каждому кадру
    for t in range(72):  # 3 секунды с частотой 24 кадра/сек
        # Очистка кадра
        frame.fill(0)

        # Новые координаты для бегущей строки
        x -= 10  # Скорость бегущей строки

        # Вот тут добавим текст
        cv2.putText(frame, ticker_message, (x, y), font, font_scale, font_color, font_thickness)

        # Тут запишем кадр
        out.write(frame)

    # Закроем тут видеопоток
    out.release()
    asyncio.run(acreate_log(ticker_message))





