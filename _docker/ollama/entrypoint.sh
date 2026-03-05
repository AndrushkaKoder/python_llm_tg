#!/bin/bash

MODEL_NAME="qwen2.5:7b"

ollama serve &

echo "⏳ Ожидание запуска Ollama..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done

if ollama list | grep -q "$MODEL_NAME"; then
  echo "✅ Модель $MODEL_NAME уже установлена."
else
  echo "📥 Модель $MODEL_NAME не найдена. Начинаю загрузку..."
  ollama pull $MODEL_NAME
  echo "✅ Загрузка завершена!"
fi

wait
