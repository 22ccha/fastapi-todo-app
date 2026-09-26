#!/bin/bash

domains=(22ccha.duckdns.org)
rsa_key_size=4096
data_path="./certbot"
email="hjmcos1204@gmail.com"

if [ ! -e "$data_path/conf/live/$domains/fullchain.pem" ]; then
  echo "### 임시 더미 인증서 생성 중..."
  mkdir -p "$data_path/conf/live/$domains"
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1 \
    -keyout "$data_path/conf/live/$domains/privkey.pem" \
    -out "$data_path/conf/live/$domains/fullchain.pem" \
    -subj "/CN=localhost"
fi

echo "### Nginx 및 서비스 실행 중..."
docker compose up -d nginx

echo "### 진짜 Let's Encrypt 인증서 발급 중..."
docker compose run --rm certbot certonly --webroot -w /var/www/certbot \
  -d $domains --email $email --rsa-key-size $rsa_key_size --agree-tos --force-renewal

echo "### Nginx 재로드..."
docker compose exec nginx nginx -s reload