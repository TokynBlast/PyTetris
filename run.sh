if !command -v import pygame &> /dev/null; then
  echo "You need to install pygame!"
elif !command -v import memory_profiler &> /dev/null; then
  echo "You need to install memory profiler!"
fi

python3 main.py
