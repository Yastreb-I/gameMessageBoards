from django.db import models
from django.contrib.auth.models import User


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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=CATEGORIES, default=tanks)
    head = models.CharField(max_length=192)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ads = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
