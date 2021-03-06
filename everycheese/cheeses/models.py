from django.conf import settings
from django.db import models
from django.urls import reverse

from django_countries.fields import CountryField
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel


class Cheese(TimeStampedModel):
    name = models.CharField('Name of Cheese', max_length=255)
    slug = AutoSlugField('Cheese Address', unique=True, always_update=False, populate_from='name')
    description = models.TextField('Description', blank=True)
    country_of_origin = CountryField('Country of Origin', blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    class Firmness(models.TextChoices):
        """
        Обратите внимание, что мы определили константы твердости как переменные в рамках
        модели Cheese. Это позволяет нам делать такие вещи, как это сравнение:
        if cheese.firmness == Cheese.Firmness.SOFT:
            ...Do Something
        """
        UNSPECIFIED = 'unspecified', 'Unspecifid'
        SOFT = 'soft', 'Soft'
        SEMI_SOFT = 'semi-soft', 'Semi-Soft'
        SEMI_HARD = 'semi-hard', 'Semi-Hard'
        HARD = 'hard', 'Hard'
    firmness = models.CharField("Firmness", max_length=20,
                                choices=Firmness.choices, default=Firmness.UNSPECIFIED)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Вернуть абсолютный URL на страницу сведений о сыре. """
        return reverse('cheeses:detail', kwargs={'slug': self.slug})
