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
operator_level = {"-": 1, "+": 1, "*": 2, "/": 2}


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

    def append(self, right_most):
        """add to pending right most open node"""
        node = self.right
        while node is not None:
            node = node.right

        node.right = right_most
        return self

    def add_above(self, operator, number):
        """add new node a top the tree"""
        self.append(number)
        return Node(left=self, operator=operator)

    def add_below(self, operator, number):
        """add note to right most open node"""
        self.append(Node(left=number, operator=operator))
        return self


def parse(symbols, open_node=None, level=99):
    print(symbols, open_node)
    current_symbols = symbols.pop()
    if current_symbols not in numbers and current_symbols != "-":
        raise InvalidNumber(current_symbols)
    while symbols and symbols[-1] in numbers:
        current_symbols += symbols.pop()
    number = Number(current_symbols)
    # Where at the end of the calculation
    if not symbols:
        # Handle the case when its the calculation a sole number
        if not open_node:
            return number
        return open_node.append(number)

    operator = parse_operator(symbols.pop())
    new_level = operator_level[operator]

    if not open_node:
        open_node = Node(left=number, operator=operator)
    else:
        if new_level <= level:
            open_node.add_below(operator, number)
        else:
            open_node.add_above(operator, number)

    return parse(
        symbols,
        open_node,
        level=new_level,
    )
