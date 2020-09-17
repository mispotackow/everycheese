import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse

from .factories import CheeseFactory, cheese
from ..models import Cheese
from ..views import (
    CheeseListView,
    CheeseDetailView,
    CheeseCreateView,
    CheeseUpdateView
)

pytestmark = pytest.mark.django_db


# def test_good_cheese_list_view_expanded(rf):
#     # Определите URL-адрес
#     url = reverse('cheeses:list')
#     # rf - это быстрый путь pytest для django.test.RequestFactory
#     # Мы генерируем запрос, как будто от пользователя,
#     # получающего доступ к представлению списка сыров
#     request = rf.get(url)
#     # Вызовите функцию as_view (), чтобы создать вызываемый объект
#     # callable_obj аналогичен представлению на основе функций
#     callable_obj = CheeseListView.as_view()
#     # Передайте запрос в callable_obj, чтобы получить
#     # HTTP-ответ, обслуживаемый Django
#     response = callable_obj(request)
#     # Убедитесь, что в ответе HTTP есть "Cheese List" в
#     # HTML и имеет код ответа 200
#     assertContains(response, 'Cheese List')


def test_good_cheese_list_view(rf):
    """ Короткая версия теста выше. """
    # Получить reauest
    request = rf.get(reverse("cheeses:list"))
    # Используйте запрос, чтобы получить ответ
    response = CheeseListView.as_view()(request)
    # Проверьте правильность ответа
    assertContains(response, 'Cheese List')


def test_good_cheese_detail_view(rf, cheese):
    # Закажите сыр на CheeseFactory
    # Отправте запрос на наш новый сыр
    url = reverse("cheeses:detail",
                  kwargs={'slug': cheese.slug})
    request = rf.get(url)

    # Используйте запрос, чтобы получить ответ
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Проверьте валидность ответа
    assertContains(response, cheese.name)


# В тесте класс admin_user предоставляет уже аутентифицированного пользователя.
def test_good_cheese_create_view(rf, admin_user, cheese):
    # Закажите сыр на CheeseFactory
    # Сделайте запрос на наш новый сыр
    request = rf.get(reverse('cheeses:add'))
    # Добавить прошедших проверку подлинности пользователей
    request.user = admin_user
    # Используйте запрос, чтобы получить ответ
    response = CheeseCreateView.as_view()(request)
    # Проверьте правильность ответа
    assert response.status_code == 200


def test_cheese_list_contains_2_cheeses(rf):
    # Давайте создадим пару сыров
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    # Создайте запрос, а затем ответ для списка сыров
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    # Проверьте, что ответ содержит оба названия сыра в шаблоне.
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_detail_contains_cheese_data(rf, cheese):
    # Сделайте запрос на наш новый сыр
    url = reverse('cheeses:detail',
                  kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # Используйте запрос, чтобы получить ответ
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Давайте проверим наши «Cheesy» детали!
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_cheese_create_form_valid(rf, admin_user):
    # Отправить форму добавления сыра
    form_data = {
        'name': 'Paski Sir',
        'description': 'A salty hard cheese',
        'firmness': Cheese.Firmness.HARD
    }
    request = rf.post(reverse('cheeses:add'), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    # Получите сыр по названию
    cheese = Cheese.objects.get(name="Paski Sir")

    # Проверьте, чтобы сыр соответствовал нашей форме
    assert cheese.description == 'A salty hard cheese'
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user


def test_cheese_create_correct_title(rf, admin_user):
    """Заголовок страницы для CheeseCreateView должен быть «Add Cheese»."""
    request = rf.get(reverse('cheeses:add'))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assertContains(response, 'Add Cheese')


def test_good_cheese_update_view(rf, admin_user, cheese):
    url = reverse('cheeses:update', kwargs={'slug': cheese.slug})
    # Сделайте запрос на наш новый сыр
    request = rf.get(url)
    # Добавить аутентифицированного пользователя
    request.user = admin_user
    # Используйте запрос, чтобы получить ответ
    callable_obj = CheeseUpdateView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Проверьте правильность ответа
    assertContains(response, 'Update Cheese')


def test_cheese_update(rf, admin_user, cheese):
    """Запрос POST к CheeseUpdateView обновляет сыр и перенаправляет."""
    # Сделайте запрос на наш новый сыр
    form_data = {
        'name': cheese.name,
        'description': 'Something new',
        'firmness': cheese.firmness
    }
    url = reverse('cheeses:update', kwargs={'slug': cheese.slug})
    request = rf.post(url, form_data)
    request.user = admin_user
    callable_obj = CheeseUpdateView.as_view()
    response = callable_obj(request, slug=cheese.slug)

    # Проверьте, что сыр был изменен
    cheese.refresh_from_db()
    assert cheese.description == 'Something new'
