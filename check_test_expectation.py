import sys
sys.path.insert(0, '.')
from propositions.semantics import all_models
from logic_utils import frozendict

# Что ожидает тест?
print("Проверяем, что ожидает тест...")
result = all_models(['p', 'q'])

# Преобразуем в frozendict
frozen_result = [frozendict(m) for m in result]
print(f"\nОбычный dict: {result[0]}, тип: {type(result[0])}")
print(f"Frozendict: {frozen_result[0]}, тип: {type(frozen_result[0])}")

# Посмотрим на тест из semantics_test.py
print("\n=== Проверяем семантику теста ===")
print("В тесте ожидается frozendict? Давайте проверим...")
