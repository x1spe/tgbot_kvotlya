#!/bin/bash

# Обновляем pip, setuptools и wheel
pip install --upgrade pip setuptools wheel

# Устанавливаем зависимости
pip install python-telegram-bot==13.15
pip install Pillow==12.0.0
pip install requests==2.31.0

# Запуск бота
python3 main.py


chmod +x start.sh
