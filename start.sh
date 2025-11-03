#!/bin/bash

# Обновляем pip, setuptools и wheel
pip install --upgrade pip setuptools wheel

# Устанавливаем зависимости
pip install -r requirements.txt

# Запуск бота
python3 main.py

chmod +x start.sh
