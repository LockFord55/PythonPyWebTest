from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count


class TrainView(View):
    def get(self, request):
        # Создайте здесь запросы к БД
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        # Какие авторы имеют самый высокий уровень самооценки(self_esteem)?
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])

        # Какой автор имеет наибольшее количество опубликованных статей?
        # TODO Нет результата
        # answer_2 = Entry.objects.values('author', 'text').annotate(Count('text'))
        self.answer2 = None

        # Какие статьи содержат тег 'Кино' или 'Музыка'? TODO Нет результата
        # answer_3 = Entry.objects.filter(Q(tags__icontains='Кино')|Q(tags__icontains='Музыка'))
        self.answer3 = None

        # Сколько авторов женского пола зарегистрировано в системе?
        gender = Author.objects.filter(gender__contains='ж').count()
        self.answer4 = gender

        # Какой процент авторов согласился с правилами при регистрации?
        agreed = Author.objects.filter(status_rule=True)
        all = Author.objects.all()
        self.answer5 = f"{(agreed.count() * 100 / all.count()):.1f}%"

        # Какие авторы имеют стаж от 1 до 5 лет? TODO Что-то не так
        answer_6 = AuthorProfile.objects.filter(
            Q(stage__gte=1) & Q(stage__lte=5)
        )
        self.answer6 = answer_6

        # Какой автор имеет наибольший возраст?
        max_age = Author.objects.aggregate(Max('age'))
        self.answer7 = Author.objects.get(age=max_age['age__max'])

        # Сколько авторов указали свой номер телефона?
        phone_none = Author.objects.exclude(phone_number=None)
        self.answer8 = phone_none.count()

        # Какие авторы имеют возраст младше 25 лет?
        self.answer9 = Author.objects.filter(age__lt=25)

        # Сколько статей написано каждым автором? TODO Что-то не так
        self.answer10 = Entry.objects.values('author').annotate(Count('id'))

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}  # Создайте здесь запросы к БД

        return render(request, 'train_db/training_db.html', context=context)

