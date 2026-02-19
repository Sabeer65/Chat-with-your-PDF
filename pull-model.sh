#!/bin/bash

ollama serve &

sleep 5

echo "Pulling llama3.2 model..."
ollama pull llama3.2

wait