class InvalidCalculation(Exception):
    pass


class InvalidOperator(InvalidCalculation):
    pass


class InvalidNumber(InvalidCalculation):
    pass


def solve(calculation):
    # Make it a list and reverse it for better popping
    symbols = list(calculation)
    symbols.reverse()

    try:
        return (True, parse(symbols).value())
    except InvalidCalculation:
        return (False, 0)


numbers = "0123456789."
operators = "-+*/"


def parse_operator(operator):
    if operator not in operators:
        raise InvalidOperator(operator)
    return operator


class Number:
    def __init__(self, number):
        try:
            self.number = float(number)
        except ValueError:
            raise InvalidNumber(number)

    def value(self):
        return self.number

    def __str__(self):
        return str(self.number)


class Node:
    def __init__(self, left=None, right=None, operator=None):
        self.left = left
        self.right = right
        self.operator = operator

    def value(self):
        left = self.left.value()
        right = self.right.value()
        if self.operator == "+":
            return left + right
        if self.operator == "-":
            return left - right
        if self.operator == "*":
            return left * right
        if self.operator == "/":
            try:
                return left / right
            except ZeroDivisionError:
                raise InvalidNumber("divide by zero")

    def __str__(self):
        return f"({self.left}){self.operator}({self.right})"


def parse(symbols, open_node=None):
    print(symbols, open_node)
    current_symbols = symbols.pop()
    if current_symbols not in numbers and current_symbols != "-":
        raise InvalidNumber(current_symbols)
    while symbols and symbols[-1] in numbers:
        current_symbols += symbols.pop()
    left = Number(current_symbols)
    # Where at the end of the calculation
    if not symbols:
        # Handle the case when its the calculation a sole number
        if not open_node:
            return left
        open_node.right = left
        return open_node
    operator = parse_operator(symbols.pop())
    if open_node:
        open_node.right = left
        left = open_node
    return parse(symbols, open_node=Node(left=left, operator=operator))
