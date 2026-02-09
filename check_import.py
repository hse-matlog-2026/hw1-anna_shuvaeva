import sys
sys.path.insert(0, '.')
import propositions.operators_test

# Посмотрим что импортируется в тесте
print("Импорты в operators_test.py:")
import inspect
source = inspect.getsource(propositions.operators_test.test_to_not_and_or)
lines = source.split('\n')
for line in lines:
    if 'to_not_and_or' in line:
        print(f"  {line.strip()}")
