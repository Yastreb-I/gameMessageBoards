from django.db import models
from django.contrib.auth.models import User
# from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field
from django.core.cache import cache


class Advertisement(models.Model):

    tanks = "Ta"
    healers = "He"
    dd = "DD"
    merchants = "Me"
    guild_masters = "GM"
    quest_givers = "QG"
    blacksmiths = "Bs"
    tanners = "Tn"
    potion_makers = "PM"
    spell_masters = "SM"
    CATEGORIES = [
        (tanks, 'Танки'),
        (healers, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guild_masters, 'Гилдмастеры'),
        (quest_givers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Изготовители зелий'),
        (spell_masters, 'Мастера заклинаний'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор",)
    category = models.CharField(max_length=2, choices=CATEGORIES, default=tanks, verbose_name="Категория",)
    head = models.CharField(max_length=192, verbose_name="Заголовок",)
    text = CKEditor5Field('Text', config_name='extends')  # models.TextField()#  RichTextUploadingField(blank=True, null=True, verbose_name="Содержание",)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания",)

    # class Meta:
    #     verbose_name = "Объявления",

    def __str__(self):
        return self.head

    # добавим абсолютный путь,
    # чтобы после создания нас перебрасывало на страницу с новостью
    def get_absolute_url(self):
        return f'/blog/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    # Предварительный просмотр поста
    def preview(self):
        return self.text[0:256] + "..."


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ads = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                            related_name='reaction_advertisement',
                            verbose_name="Объявление",)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
