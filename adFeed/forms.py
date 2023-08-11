from django.forms import ModelForm, Textarea, TextInput, Select
from .models import Advertisement, Reaction
from django.utils.translation import gettext_lazy as gl
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_ckeditor_5.widgets import CKEditor5Widget


# Создаём модельную форму для создания новых объявлений
class AdForm(ModelForm):

    class Meta:
        model = Advertisement
        fields = ['head', 'text', 'category']
        labels = {
            'category': gl("Категория"),
            'head': gl("Заголовок статьи"),
            'text': gl("Текст статьи"),

        }
        widgets = {
            'head': TextInput(attrs={"class": "comment-name", "required": "true"}),
            'text': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              ),
            # TextInput(attrs={"class": "comment-name", "required": "true"}),
            # CKEditorUploadingWidget(attrs={"required": "true"}),
            'category': Select(attrs={"class": "comment-name", "required": "true"}),
        }


# Создаём модельную форму для комментариев/реакций
class ReactionForm(ModelForm):

    class Meta:
        model = Reaction
        fields = ['text']
        labels = {
            'text': gl("Отклик"),
        }
        widgets = {
            'text': Textarea(attrs={"class": "comment-text-area", "placeholder": "Введите сообщение"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

