from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives

from .models import *


# Отклик на объявление
def send_email_reaction(reaction_id):
    reaction = Reaction.objects.get(id=reaction_id)
    send_mail(
        subject='На Ваше объявление в MMORPG откликнулись!',
        message=f'Здравствуйте, {reaction.ads.author.username}, !\n'
                f'На ваше объявление - http://127.0.0.1:8000/adFeed/{reaction.ads.id}, есть новый отклик!\n'
                f' Содержание отклика: \n'
                f'  {reaction.text}.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reaction.ads.author.email, ],
    )


# Ответ на отклик
def answer_to_reaction(reaction_id, answer=False):
    reaction = Reaction.objects.get(id=reaction_id)
    answers = "положительный" if answer else "отрицательный"
    send_mail(
        subject=f'На Ваш сообщение в MMORPG получен ответ!',
        message=f'Здравствуйте, {reaction.user.username}, !\n'
                f'На Ваше сообщение:'
                f' {reaction.text}'
                f' в объявлении - http://127.0.0.1:8000/adFeed/{reaction.ads.id}, получен {answers} ответ!\n'
                ,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reaction.user.email, ],
    )


# Еженедельная рассылка подписчикам
def weekly_ads_letter():
    print("Запущена-weekly_newsletter")
    start_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date_of_week = start_day
    start_date_of_week = start_day - timedelta(weeks=1)
    weekly_ads = Advertisement.objects.filter(dateCreation__gte=start_date_of_week, dateCreation__lt=end_date_of_week)
    template = 'mailing/weekly_newsletter.html'
    subject = 'Объявления за неделю'
    url_site = 'http://127.0.0.1:8000/adFeed/'

    for user in User.objects.all():
        email_user = user.email
        context = {
            'user': user.username,
            'ads': weekly_ads,
            'url_site': url_site,
        }
        html = render_to_string(
            template_name=template,
            context=context,
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_user, ],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
