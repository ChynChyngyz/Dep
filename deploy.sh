#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Пожалуйста, запустите скрипт с правами суперпользователя"
   exit 1
fi

echo "Обновляем систему..."
apt update && apt upgrade -y

echo "Устанавливаем Docker, Docker Compose и другие зависимости..."
apt install -y docker.io docker-compose git

docker --version
docker-compose --version

if [ ! -d "/home/ubuntu/django" ]; then
  echo "Клонируем проект..."
  git clone https://your-repository-url.git /home/ubuntu/django
else
  echo "Проект уже существует, выполняем git pull..."
  cd /home/ubuntu/django
  git pull
fi

cd /home/ubuntu/django

echo "Запускаем Docker Compose..."
docker-compose up --build -d

# Запуск Nginx (если он не запускается через docker-compose, можно запустить его вручную)
echo "Перезапускаем Nginx..."
systemctl restart nginx

docker ps

clear