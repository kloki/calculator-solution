from calculator.solver import solve


class TestSolver:
    def test_simple(self):
        # assert solve("23+(9-9)")[1] == 23
        # assert solve("23+(9-9)*9")[1] == 23
        assert solve("3-4-8+12-3+7")[1] == 7
        assert solve("3+2+1")[1] == 6
        assert solve("9*3*3")[1] == 81
        assert solve("1+9*3*3")[1] == 82
        assert solve("9-9*3*3")[1] == -72
        assert solve("23+(9-9*3*3)")[1] == -49
        assert solve("23+(9-9)*3*3")[1] == 23
        assert solve("23+(9-9)*9*(35-21)")[1] == 23
