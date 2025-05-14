#!/bin/bash

# Redis 서버 시작
echo "Starting Redis..."
redis-server --daemonize yes

# Redis가 시작될 때까지 대기
echo "Waiting for Redis to start..."
until redis-cli ping | grep -q "PONG"; do
  sleep 1
done
echo "Redis is running"

# 마이그레이션 실행
echo "Running migrations..."
python manage.py migrate

# 서비스 시작
echo "Starting services..."
gunicorn --bind 0.0.0.0:8001 conf.wsgi:application &
GUNICORN_PID=$!

celery -A conf worker --loglevel=info &
WORKER_PID=$!

celery -A conf beat --loglevel=info &
BEAT_PID=$!

# 종료 처리
trap 'kill $GUNICORN_PID $WORKER_PID $BEAT_PID; redis-cli shutdown; exit 0' SIGTERM

# 대기
wait $GUNICORN_PID $WORKER_PID $BEAT_PID