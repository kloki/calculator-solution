class InvalidCalculation(Exception):

    pass


class InvalidOperator(InvalidCalculation):
    pass


class InvalidNumber(InvalidCalculation):
    pass


def solve(calculation):
    # Make it a list and reverse it for better popping

    try:
        calculation_precheck(calculation)
        symbols = list(calculation)
        symbols.reverse()
        return (True, parse(symbols).value())
    except InvalidCalculation:
        return (False, 0)


numbers = "0123456789."
operators = "-+*/"
operator_level = {"-": 1, "+": 1, "*": 2, "/": 2}


def calculation_precheck(calculation):
    if calculation.count(")") != calculation.count("("):
        raise InvalidCalculation("paranthesis mismatch")


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
        node = self
        while node.right:
            node = node.right

        node.right = right_most
        return self

    def add_above(self, operator, sub_node):
        """add new node a top the tree, implies lower priority of operator"""
        self.append(sub_node)
        return Node(left=self, operator=operator)

    def add_below(self, operator, sub_node):
        """add note to right most open node, implies higher priority of operator"""
        self.append(Node(left=sub_node, operator=operator))
        return self


def parse(symbols, open_node=None, level=0):
    current_symbols = symbols.pop()
    sub_node = None
    if current_symbols == "(":
        sub_node = parse(symbols)
        print(sub_node)

    elif current_symbols not in numbers and current_symbols != "-":
        raise InvalidNumber(current_symbols)
    else:
        while symbols and symbols[-1] in numbers:
            current_symbols += symbols.pop()
        sub_node = Number(current_symbols)
    # Where at the end of the calculation
    if not symbols:
        # Handle the case when its the calculation a sole number
        if not open_node:
            return sub_node
        return open_node.append(sub_node)
    # and of sub_node
    if symbols[-1] == ")":
        symbols.pop()
        # Handle the case when its the calculation a sole number
        if not open_node:
            return sub_node
        return open_node.append(sub_node)

    operator = parse_operator(symbols.pop())
    new_level = operator_level[operator]

    if not open_node:
        open_node = Node(left=sub_node, operator=operator)
    else:
        if new_level <= level:
            open_node = open_node.add_above(operator, sub_node)
        else:
            open_node = open_node.add_below(operator, sub_node)

    return parse(
        symbols,
        open_node,
        level=new_level,
    )
