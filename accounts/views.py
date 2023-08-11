from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from adFeed.models import Advertisement, Reaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .filters import ReactionFilter
from adFeed.tasks import answer_to_reaction


class UserAccountView(LoginRequiredMixin,  ListView):

    template_name = 'user_account.html'
    queryset = Reaction.objects.order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        groups_authors = user.groups.filter(name='authors').exists()
        if user.is_authenticated:
            advertisements = Advertisement.objects.filter(author=user).order_by('-dateCreation')
            reactions = Reaction.objects.filter(ads__author=user).order_by('-dateCreation')
            my_reactions = Reaction.objects.filter(user=user).order_by('-dateCreation')
            reaction_filter_qs = ReactionFilter(self.request.GET, queryset=reactions).qs
            paginator_ad = Paginator(advertisements, 3)
            paginator_react = Paginator(reaction_filter_qs, 5)
            paginator_my_react = Paginator(my_reactions, 6)
            page_ad = self.request.GET.get('page_ad')
            page_react = self.request.GET.get('page_re')
            page_my_react = self.request.GET.get('page_mr')
            page_obj_ad = paginator_ad.get_page(page_ad)
            page_obj_react = paginator_react.get_page(page_react)
            page_obj_my_react = paginator_my_react.get_page(page_my_react)

            context['reaction_filter'] = ReactionFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр
            context['paginator_ad'] = paginator_ad
            context['paginator_react'] = paginator_react
            context['paginator_my_react'] = paginator_my_react
            context['page_obj_ad'] = page_obj_ad
            context['page_obj_react'] = page_obj_react
            context['page_obj_my_react'] = page_obj_my_react
            context['is_authors'] = advertisements.exists()
        return context


# Ответ на отклик
@login_required
def accept_reaction(request, pk):
    reaction = Reaction.objects.get(id=pk)
    reaction.status = True
    reaction.save()
    answer_to_reaction(reaction_id=reaction.id, answer=True)
    return redirect("user_accounts")


# Удаление отклика
@login_required
def delete_reaction(request, pk):
    reaction = Reaction.objects.get(id=pk)
    if request.user.username == reaction.user.username or request.user.username == reaction.ads.author.username:
        answer_to_reaction(reaction_id=reaction.id)
        reaction.delete()
    return redirect("user_accounts")

