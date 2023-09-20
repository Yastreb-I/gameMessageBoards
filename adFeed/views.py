from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.views.generic.edit import FormMixin
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.utils.html import strip_tags
from django.core.cache import cache


from .models import Advertisement, Reaction, User
from adFeed.tasks import send_email_reaction
from .forms import AdForm, ReactionForm


# Список всех объявлений
class Advertisements(ListView):
    model = Advertisement  # указываем модель, объекты которой мы будем выводить
    template_name = 'ad_feed.html'  # указываем имя шаблона, в котором будет лежать HTML,
    # в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'ad_feed'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Advertisement.objects.order_by('-dateCreation')  # Вывод новых статей в начало страницы
    # paginate_by = 10  # поставим постраничный вывод в 10 элемента

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['count_comments'] = 0
        return context


# Создаём представление, в котором будут детали конкретного отдельного поста
class AdsDetailView(FormMixin, DetailView):

    model = Advertisement  # модель всё та же, но мы хотим получать детали конкретной отдельной новости
    template_name = 'blog.html'  # название шаблона
    context_object_name = 'ad_blog'  # название объекта
    form_class = ReactionForm  # Подключаем форму для комментариев/ реакций

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'{self.kwargs["pk"]}', obj)
        return obj

    def get_success_url(self):
        return reverse_lazy('ad_blog', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ads = self.get_object()
        self.object.user = self.request.user
        print(self.object.id)
        self.object.save()
        send_email_reaction(reaction_id=self.object.id)
        return super().form_valid(form)


# Создание объявления
class AdCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ad_create.html'
    form_class = AdForm
    # permission_required = ('adFeed.add_post',)
    success_url = '/adFeed/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, user)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый пост
            post = form.save(False)
            strip_tags(f"<pre>{request}</pre>")
            post.author = User.objects.get_or_create(username=user.username)[0]
            authors_group = Group.objects.get(name='authors')
            if not user.groups.filter(name='authors').exists():
                authors_group.user_set.add(user)
            form.save(True)
            return self.form_valid(form)

        return redirect("adFeed:adFeed")


# Дженерик для редактирования объекта
class AdUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'ad_create.html'
    form_class = AdForm
    # permission_required = ('adFeed.change_post',)
    success_url = '/adFeed/'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
    # который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertisement.objects.get(pk=id)


# дженерик для удаления товара
class AdDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'ad_delete.html'
    # permission_required = ('adFeed.delete_post',)
    queryset = Advertisement.objects.all()

    def get_success_url(self):
        return reverse("user_accounts")


