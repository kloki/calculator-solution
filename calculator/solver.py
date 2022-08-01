def solve(calculation):
    try:
        return (True, float(calculation))
    except ValueError:
        return (False, 0)
