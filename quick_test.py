import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula
from propositions.semantics import evaluate

# Тест из ошибки
formula = Formula.parse('~(p&q7)')
model = {'p': True, 'q7': False}
print(f"Формула: {formula}")
print(f"Модель: {model}")
print(f"Результат: {evaluate(formula, model)}")
print(f"Ожидается: True (not (True and False) = not False = True)")
