import re

with open('propositions/syntax.py', 'r') as f:
    content = f.read()

old_polish = '''    def polish(self) -> str:
        """Computes the polish notation representation of the current formula.

        Returns:
            The polish notation representation of the current formula.
        """
        # Optional Task 1.7'''

new_polish = '''    def polish(self) -> str:
        """Computes the polish notation representation of the current formula.

        Returns:
            The polish notation representation of the current formula.
        """
        # Optional Task 1.7
        if is_variable(self.root):
            return self.root
        elif is_constant(self.root):
            return self.root
        elif is_unary(self.root):
            return self.root + self.first.polish()
        else:  # binary operation
            return self.root + self.first.polish() + self.second.polish()'''

content = content.replace(old_polish, new_polish)

with open('propositions/syntax.py', 'w') as f:
    f.write(content)

print("polish() method updated")
