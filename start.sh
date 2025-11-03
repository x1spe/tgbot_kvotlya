#!/bin/bash

# Обновляем pip, setuptools и wheel
pip install --upgrade pip setuptools wheel

# Устанавливаем зависимости, используя готовые бинарные колёса для Pillow
pip install --only-binary=:all: Pillow==10.1.1
pip install python-telegram-bot==13.15

# Запуск бота
python3 main.py

chmod +x start.sh
