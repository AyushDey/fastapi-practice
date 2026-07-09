import pytest

def test_comparison():
    assert 3 == 3
    assert 4 > 2
    assert 2 < 10

def test_is_instance():
    assert isinstance("This is a string", str)
    assert not isinstance("10", int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('hello' is str)
    assert type('hello' is not int)

def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False, True]
    assert 1 in num_list
    assert 10 not in num_list
    assert all(num_list)
    assert any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'CS', 4)

def test_person_init(default_employee):
    assert default_employee.first_name == 'John', 'First name should be John'
    assert default_employee.last_name == 'Doe', 'Last name should be Doe'
    assert default_employee.major == 'CS', 'Major should be CS'
    assert default_employee.years == 4, 'Years should be 4'