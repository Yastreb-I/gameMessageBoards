from django_filters import FilterSet, DateFilter, ModelChoiceFilter, \
    CharFilter, BooleanFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики

from django import forms
from adFeed.models import *


def user_ads(request):
    print(request)
    if request is None:
        return Advertisement.objects.none()

    user = request.user
    return Advertisement.objects.filter(author_id=user.id)


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


# создаём фильтр
class ReactionFilter(FilterSet):


    def user_ads(self, request):
        return print(request)

    text = CharFilter(
        label='Текст сообщения ',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите часть текста',
            'class': 'filter_form_head',
        }))
    dateCreation = DateFilter(label='Поиск с ',
                              lookup_expr='gte',
                              widget=MyDateInput({
                                  'class': 'filter_form_date',
                                  # 'value': "2023-06-01",
                              }))
    status = BooleanFilter()

    class Meta:
        model = Reaction
        fields = ('ads',
                  'text',
                  'dateCreation',
                  'status',
                  )  # поля, которые мы будем фильтровать
        # (т.е. отбирать по каким-то критериям, имена берутся из моделей)

