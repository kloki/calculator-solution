from calculator.solver import solve


class TestSolver:
    def test_simple(self):
        assert solve("12-8")[1] == 2
        assert solve("3-4-8+12-3+7")[1] == 2
