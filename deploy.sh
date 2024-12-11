#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Пожалуйста, запустите скрипт с правами суперпользователя"
   exit 1
fi

echo "Обновляем систему..."
apt update && apt upgrade -y

echo "Устанавливаем Docker, Docker Compose и другие зависимости..."
apt install -y docker.io git

curl -L https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r .tag_name)/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

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

echo "Перезапускаем Nginx..."
docker-compose restart nginx

docker ps
