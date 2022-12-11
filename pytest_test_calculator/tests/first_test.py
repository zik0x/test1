from app.calculator import Calculator
import pytest

class TestCalc:
    def setup(self): #определяем подготоительный метод
        self.calc = Calculator #создаем обьект калькултора из импортированного класса

    def tests_multiply_calc_correctly(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def tests_division_calc_correctly(self):
        assert self.calc.division(self, 2, 2) == 1

    def tests_subtraction_calc_correctly(self):
        assert self.calc.subtraction(self, 2, 2) == 0

    def tests_adding_calc_correctly(self):
        assert self.calc.adding(self, 2, 2) == 4