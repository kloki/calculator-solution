from calculator.solver import solve


class TestSolver:
    def test_simple(self):
        assert solve("23+(9-9)")[1] == 23
        assert solve("23+(9-9)*9")[1] == 23
        assert solve("9-9*3*3")[1] == -72
        assert solve("23+(9-9*3*3)")[1] == -49
        assert solve("23+(9-9)*3*3")[1] == 23
        assert solve("23+(9-9)*9*(35-21)")[1] == 23
