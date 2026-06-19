from app import add

def test_add_case1():
    assert add(10, 20) == 30

def test_add_case2():
    assert add(5, 5) == 10

def test_add_case3():
    assert add(0, 0) == 0

def test_add_case4():
    assert add(100, 200) == 300

def test_add_case5():
    assert add(-10, -20) == -30

def test_add_case6():
    assert add(-10, 20) == 10

def test_add_case7():
    assert add(20, -10) == 10

def test_add_case8():
    assert add(1000, 2000) == 3000

def test_add_case9():
    assert add(1, 999) == 1000

def test_add_case10():
    assert add(-50, 50) == 0