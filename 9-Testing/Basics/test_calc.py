import pytest

def square(n):
    return n*n

def test_square_1():
    assert square(5) == 25

#The below test fails
'''def test_square_2():
    assert square(5) == 30'''

@pytest.mark.parametrize("num, expected", [
    (3, 9),
    (4, 16),
    (6, 36),
    (7, 49)
])
def test_square_3(num, expected):
    assert square(num) == expected
