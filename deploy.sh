#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Пожалуйста, запустите скрипт с правами суперпользователя"
   exit 1
fi

echo "Обновляем систему..."
apt update && apt upgrade -y

echo "Устанавливаем Docker, Docker Compose и другие зависимости..."
apt install -y docker.io git docker-compose

chmod +x /usr/local/bin/docker-compose

docker --version
docker-compose --version

cd /var/www

if [ -d "Dep" ]; then
  echo "Проект уже существует, выполняем git pull..."
  cd Dep
  git pull
else
  echo "Клонируем проект..."
  git clone https://github.com/ChynChyngyz/Dep.git .
  cd Dep
fi

echo "Запускаем Docker Compose..."
docker-compose up --build -d

echo "Перезапускаем Nginx..."
docker-compose restart nginx

docker ps
