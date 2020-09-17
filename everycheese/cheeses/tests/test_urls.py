import pytest

from django.urls import reverse, resolve

from .factories import CheeseFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def cheese():
    return CheeseFactory()


def test_list_reverse():
    """cheeses:list должен измениться на /cheeses/."""
    assert reverse('cheeses:list') == '/cheeses/'


def test_list_resolve():
    """/cheeses/ должен измениться на cheese:list."""
    assert resolve('/cheeses/').view_name == 'cheeses:list'


def test_add_reverse():
    """cheeses:add должен измениться на /cheeses/add/."""
    assert reverse('cheeses:add') == '/cheeses/add/'


def test_add_resolve():
    """/cheeses/add/ должен разрешить cheeses:add."""
    assert resolve('/cheeses/add/').view_name == 'cheeses:add'


def test_detail_reverse(cheese):
    """cheeses:detail должен измениться на /cheeses/cheeseslug/."""
    url = reverse('cheeses:detail', kwargs={'slug': cheese.slug})
    assert url == f'/cheeses/{cheese.slug}/'


def test_detail_resolve(cheese):
    """/cheeses/cheeseslug/ должен разрешить cheeses:detail."""
    url = f'/cheeses/{cheese.slug}/'
    assert resolve(url).view_name == 'cheeses:detail'
