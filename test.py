from calculator.solver import solve


class TestSolver:
    def test_simple(self):
        assert solve("7*2-4")[1] == 0
