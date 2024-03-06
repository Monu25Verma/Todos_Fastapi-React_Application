import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 2

def test_instance():
    assert isinstance('hello' , str)
    assert not isinstance('hello' , int)

def test_boolean():
    validation = True
    assert validation is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('hello' is str)
    assert type(10 is int)


def test_list():
    lst_data = [1,4,5,6,3,8]
    any_list = [False, True]
    assert 1 is not lst_data
    assert lst_data is not list



class Student:
    def __init__(self,first_name: str, last_name: str, major : str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():         #mock ->
    return Student('monu', 'verma' , 'computer scinece', 3)

def test_person_initialisation(default_employee):
    assert default_employee.first_name == 'monu'
    assert default_employee.last_name == 'verma'
    assert default_employee.major == 'computer scinece'
    assert default_employee.years == 3