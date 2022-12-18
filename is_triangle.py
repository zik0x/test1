import pytest

def is_triangle(a, b, c):
    if (a**2 == b**2 + c**2 or b**2 == c**2 + a**2 or c**2 == b**2 + a**2) and (a > 0 or b > 0 or c > 0):
        return True
    else:
        return False

@pytest.fixture(scope="function", params=[
   ((3, 4, 5), True),
   ((1, 4, 5), False), ((0, 0, 0), False), ((-1, 2, 3), False)], ids=["True", "False", "0", "<0"])
def param_fun(request):
   return request.param


def test_triangle(param_fun):
   (input, expected_output) = param_fun
   result = is_triangle(*input)
   print ("Стороны треугольника: {0}\nВыходное значение: {1}\nЗначение функции: {2}".format(input, result, expected_output))
   assert result == expected_output