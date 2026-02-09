import sys
sys.path.insert(0, '.')
from propositions import operators_test
import inspect

# Получим исходный код всего файла
with open('propositions/operators_test.py', 'r') as f:
    content = f.read()
    
# Найдём импорты
import_lines = []
for line in content.split('\n'):
    if 'import' in line or 'from' in line:
        import_lines.append(line.strip())
        
print("Импорты в operators_test.py:")
for line in import_lines[:10]:
    print(f"  {line}")
