# Восстановим правильный порядок
import sys

# Читаем файл
with open('propositions/semantics.py', 'r') as f:
    lines = f.readlines()

# Находим и перемещаем __future__ импорт на первую строку
new_lines = []
future_import = None

for line in lines:
    if 'from __future__ import annotations' in line:
        future_import = line
    else:
        new_lines.append(line)

# Записываем обратно с __future__ на первом месте
with open('propositions/semantics.py', 'w') as f:
    if future_import:
        f.write(future_import)
    for line in new_lines:
        f.write(line)

print("Файл исправлен!")
