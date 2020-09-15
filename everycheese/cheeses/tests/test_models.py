import pytest
from ..models import Cheese
from .factories import CheeseFactory

# Связывает наши тесты с нашей базой данных
pytestmark = pytest.mark.django_db


def test___str__():
    cheese = CheeseFactory()
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name
