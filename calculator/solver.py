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
        answer = parse(symbols)
        print(answer)
        return (True, answer.value())
    except InvalidCalculation:
        return (False, 0)


class Operator:
    def __init__(self, symbol, level):
        self.symbol = symbol
        self.level = level

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.__str__()


numbers = "0123456789."

operators = [
    Operator("-", 1),
    Operator("+", 1),
    Operator("*", 2),
    Operator("/", 2),
]


def calculation_precheck(calculation):
    if calculation.count(")") != calculation.count("("):
        raise InvalidCalculation("paranthesis mismatch")


def parse_operator(symbol):
    for operator in operators:
        if operator.symbol == symbol:
            return operator

    raise InvalidOperator(operator)


class Number:
    def __init__(self, number, parent=None):
        try:
            self.number = float(number)
        except ValueError:
            raise InvalidNumber(number)
        self.parent = parent
        self.right = None
        self.operator = Operator("", 0)

    def value(self):
        return self.number

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return self.__str__()


class Node:
    def __init__(self, left=None, right=None, operator=None, parent=None):
        self.left = left
        self.right = right
        self.operator = operator
        self.parent = parent

    def value(self):
        left = self.left.value()
        right = self.right.value()
        if self.operator.symbol == "+":
            return left + right
        if self.operator.symbol == "-":
            return left - right
        if self.operator.symbol == "*":
            return left * right
        if self.operator.symbol == "/":
            try:
                return left / right
            except ZeroDivisionError:
                raise InvalidNumber("divide by zero")

    def __str__(self):
        return f"({self.left}){self.operator.symbol}({self.right})"

    def __repr__(self):
        return self.__str__()

    def append(self, right_most):
        """add to pending right most open node"""
        node = self
        while node.right:
            node = node.right

        node.right = right_most
        right_most.parent = node
        return self

    def add_above(self, operator, sub_node):
        """add to the highest node with similar equal or higher, implies lower priority of operator"""
        node = self
        while node.right:
            node = node.right
        node.right = sub_node

        while node.parent and operator.level >= node.parent.operator.level:
            node = node.parent

        new_node = Node(left=node, operator=operator, parent=node.parent)
        node.parent = new_node

        if not new_node.parent:
            # new node is the new top.
            return new_node
        return self

    def add_below(self, operator, sub_node):
        """add note to right most open node, implies higher priority of operator"""
        self.append(Node(left=sub_node, operator=operator))
        return self


def parse(symbols, open_node=None, level=0):
    print(symbols, open_node, level)
    current_symbols = symbols.pop()
    sub_node = None
    if current_symbols == "(":
        sub_node = parse(symbols)

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

    if not open_node:
        open_node = Node(left=sub_node, operator=operator)
    else:
        if operator.level <= level:

            open_node = open_node.add_above(operator, sub_node)
        else:
            open_node = open_node.add_below(operator, sub_node)

    return parse(
        symbols,
        open_node,
        level=operator.level,
    )
