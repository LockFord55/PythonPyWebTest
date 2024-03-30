import django
import os
import datetime
from django.db.models import Count, Avg, Q, Max, Min, StdDev, Variance, F, Case, When, BooleanField, CharField, Subquery, Window
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train_alternative.models import Blog, Author, AuthorProfile, Entry, Tag

    # Выводит все записи блогов, где у автора в имени содержится 'author'
    # obj = Entry.objects.filter(author__name__contains='author')
    # print(obj)

    # Выводит записи, где у автора не указан город
    # obj = Entry.objects.filter(author__authorprofile__city=None)
    # print(obj)

    # exact, iexact позволяют получить точное совпадение
    # print(Entry.objects.get(id__exact=4))  # с учётом регистра
    # print(Entry.objects.get(id=4))  # exact можно и опустить
    # без учета регистра:
    # print(Blog.objects.get(name__iexact='Путешествия по миру'))

    # contains, icontains поиск (не)чувствительный к регистру
    # print(Entry.objects.filter(headline__contains='мод'))

    # Проверка вхождения - in
    # print(Entry.objects.filter(id__in=[1, 3, 4]))
    # Число комментариев равно 1 или 2 или 3:
    # print(Entry.objects.filter(number_of_comments__in='123'))

    # Можно использовать динамический поиск
    # inner_qs = Blog.objects.filter(name__contains='Путешествия')
    # entries = Entry.objects.filter(blog__in=inner_qs)
    # print(entries)

    # 'gt' == '>'; 'gte' == '>='; 'lt' == '<'; 'lte' == '<='
    # Выводим записи, где число комментариев больше 10
    # print(Entry.objects.filter(number_of_comments__gt=10))
    # Выводим записи, где дата публикации позже или равна заданной
    # print(Entry.objects.filter(pub_date__gte=datetime.date(2023, 6, 1)))
    # Выводим записи, у которых число комментариев > 10 и рейтинг < 4
    # print(Entry.objects.filter(number_of_comments__gt=10).filter(rating__lt=4))
    # Выводим записи, где заголовок <= 'Зя'
    # print(Entry.objects.filter(headline__lte='Зя'))

    # (i)startswith, (i)endswith
    # Начинается с...:
    # print(Entry.objects.filter(headline__startswith='Как'))
    # Заканчивается на...:
    # print(Entry.objects.filter(headline__endswith='ния'))

    # range Диапазон проверки (Включительно)
    # Выводим записи за указанный период
    # start_date = datetime.date(2023, 1, 1)
    # end_date = datetime.date(2023, 12, 31)
    # print(Entry.objects.filter(pub_date__range=(start_date, end_date)))
    # Хотя в данной задаче будет проще вывести целый год

    # year, month, day, week, week_day, quarter, hour, minute, second
    # Вывести записи старше 2022 года:
    # print(Entry.objects.filter(pub_date__year__lt=2022))
    # Вывести все записи за февраль доступных годов:
    # print(Entry.objects.filter(pub_date__month=2).values('blog__name', 'pub_date', 'headline'))
    # Вывести имя пользователя авторов, где есть публикации 1-15 апреля 23 г
    # print(Entry.objects.filter(pub_date__year=2023).filter(pub_date__day__gte=1).filter(pub_date__day__lte=15).values_list('author__name').distinct())
    # Вывести статьи опубликованные в ПН:
    # Американская неделя: ВС ПН ВТ СР ЧТ ПТ СБ; ПН - 2ой день недели:
    # print(Entry.objects.filter(pub_date__week_day=2).values('blog__name', 'pub_date', 'headline'))

    # date, time
    # __date и __time НЕ ПРИМЕНЯЮТСЯ к DateField, ТОЛЬКО к DateTimeField
    # Вывод всех записей по конкретной дате:
    # print(Entry.objects.filter(pub_date__date=datetime.date(2021, 6, 1)))
    # Вывод всех записей новее конкретной даты:
    # print(Entry.objects.filter(pub_date__date__gt=datetime.date(2024, 1, 1)))
    # Вывод записей по конкретному времени:
    # print(Entry.objects.filter(pub_date__time=datetime.time(12, 00)))
    # Записи с 6 утра до 17 вечера
    # print(Entry.objects.filter(pub_date__time__range=(datetime.time(6), datetime.time(17))))

    # isnull
    # Все авторы без указанного города
    # print(AuthorProfile.objects.filter(city__isnull=True))

    # regex, iregex; совпадение с регулярками
    # Записи, где встречается заданный паттерн:
    # print(Entry.objects.filter(body_text__regex=r'\w*стран\w*'))
    # Записи авторов с почтовыми доменами:
    # print(Entry.objects.filter(author__email__iregex='\w+(@gmail.com|@mail.ru)'))

    """ПРИМЕНЯЕМЫЕ МЕТОДЫ ДЛЯ ФОРМИРОВАНИЯ ЗАПРОСА"""
    # all() вывод все значений в таблице
    # first() вывод первого значения

    # QuerySet не выполняется сразу, можно делать последовательные запросы
    # all_obj = Blog.objects.all()
    # obj_first = all_obj.first()
    # print("Разные запросы на вывод в Blog\n", f"Первое значение таблицы = {obj_first}\n",
         # f"Все значения = {all_obj}")

    # Объект QuerySet итерируемый, к нему можно обращаться [], слайсировать, for и т.д.
    # all_obj = Blog.objects.all()
    # for idx, value in enumerate(all_obj):
    #     print(f"idx = {idx}, value = {value}")
    # print(all_obj[0])  # Нулевой элемент
    # print(all_obj[2:4])  # 2 и 3 элементы
    """Получение последнего элемента all_obj[-1] не возможно
    Но можно воспользоваться latest('<name_field>')"""
    # print(all_obj.latest('id'))
    # print(Blog.objects.latest('id'))

    # get() - получение конкретного элемента - objects.get(**conditions)
    # print(Blog.objects.get(id=1, name='Путешествие по миру'))

    # filter(**conditions)

    # exclude() - выводит записи КРОМЕ указанных в условии

    # exists() - проверка существования элементов в БД
    # Он применяется прямо к объекту, но только объекту
    # objects.filter(**conditions).exists()
    # Пример для get
    # try:
    #     Blog.objects.get(id=2, name="Путешествия по миру")
    # except Blog.DoesNotExist:
    #     print("Не существует")
    # # Пример для filter
    # print(Blog.objects.filter(id=2, name="Путешествия по миру").exists())

    # count()
    # print(Blog.objects.count())  # Можно ко всей таблице
    # print(Blog.objects.filter(id__gte=2).count())  # Можно к запросу
    # all_data = Blog.objects.all()
    # filtered_data = all_data.filter(id__gte=2)
    # print(filtered_data.count())  # Можно к частным запросам

    # order_by()
    """ По умолчанию результаты упорядочиваются с помощью кортежа, 
    заданного параметром ordering в классе Meta модели."""
    # filtered_data = Blog.objects.filter(id__gte=2)
    # print(filtered_data.order_by("id"))  # упорядочивание по возрастанию по полю id
    # print(filtered_data.order_by("-id"))  # упорядочивание по уменьшению по полю id
    # print(filtered_data.order_by("-name", "id"))  # упорядочивание по двум параметрам, сначала по первому на уменьшение,
    # # затем второе на увеличение. Можно упорядочивание провести по сколь угодно параметрам.

    """ annotate()
    Аннотирует каждый объект в QuerySet с помощью предоставленного
    списка выражений запроса. Выражение может быть простым значением,
    ссылкой на поле в модели (или любых связанных моделях) или 
    агрегированным выражением (средние значения, суммы и т.д.),
    которое было вычислено для объектов, связанных с объектами 
    в QuerySet."""

    # Запрос, аннотирующий количество статей для каждого блога,
    # при этом добавляется новая колонка number_of_entries для вывода
    # entry = Blog.objects.annotate(number_of_entries=Count('entry')).values('name', 'number_of_entries')
    # print(entry)

    """ alias()
    Основная разница между annotate() и alias() заключается в том,
    что annotate() используется для добавления агрегированных 
    значений к каждому объекту в QuerySet, тогда как alias() 
    используется для создания псевдонимов для полей или связей 
    в запросе, чтобы использовать их в других частях запроса.
    """
    # blogs = Blog.objects.alias(entries=Count('entry')).filter(entries__gt=4)
    # print(blogs)
    ## Выведет ошибку, так как поле entries не существует, виду различий между alias и annotate
    # blogs = Blog.objects.alias(entries=Count('entry')).filter(entries__gt=4).values('blog', 'entries')

    """
    Аргумент aggregate() описывает агрегированное значение, 
    которое мы хотим вычислить.
    aggregate() - это терминальное предложение для QuerySet, 
    которое при вызове возвращает словарь пар имя-значение. 
    Имя - это идентификатор совокупного значения; 
    значение - это вычисленный агрегат. 
    Имя автоматически генерируется из имени поля и 
    агрегатной функции.
    Если вы хотите вручную указать имя для агрегированного значения,
    вы можете сделать это, указав это имя при указании 
    агрегатного предложения.
    """
    """
    Всего поддерживаются данные агрегационные функции:

    Avg
    Count
    Max, Min
    StdDev, Variance
    Sum
    
    В общем случае функции могут принимать следующие параметры:
    expression (обязательный): Поле или выражение, для которого
    нужно вычислить среднее значение. Может быть именем поля 
    модели или выражением, состоящим из полей, функций и операторов.
    
    output_field: Опциональный параметр, позволяющий указать тип
    поля для вывода. По умолчанию output_field принимает значение
    FloatField(), чтобы вернуть среднее значение в виде числа 
    с плавающей запятой. Однако вы можете указать другой тип поля,
    если требуется.
    
    distinct (логическое значение): Указывает, следует ли 
    учитывать только уникальные значения при вычислении среднего
    значения. Если distinct=True, будут учтены только уникальные
    значения поля. По умолчанию distinct=False.
    
    filter (условие фильтрации): Позволяет задать условие 
    фильтрации для агрегации. Только объекты, удовлетворяющие
    этому условию, будут учтены при вычислении среднего значения.
    
    default (значение по умолчанию): Устанавливает значение, 
    которое будет возвращено, если агрегация не возвращает 
    результат. Это может быть полезно, если вы хотите задать 
    значение по умолчанию, если нет объектов для агрегации.
    """

    # avg возвращает среднее значение
    # class Avg(expression, output_field=None, distinct=False, filter=None, default=None, **extra)
    # Вычислить среднюю оценку только для уникальных значений
    # average_rating = Entry.objects.aggregate(
    #     average_rating1=Avg('rating', distinct=True)
    # )
    # print(average_rating)
    # Вычислить среднюю оценку с заданным значением по умолчанию(допустим
    # значение у поля None), если агрегация не возвращает результат
    # average_rating_with_default = Entry.objects.aggregate(
    #     average_rating2=Avg('rating', default=5.0)
    # )
    # print(average_rating_with_default)
    # Вычислить среднюю оценку только для статей, опубликованных после 2023 года
    # average_rating = Entry.objects.aggregate(
    #     average_rating3=Avg('rating', filter=Q(pub_date__year__gt=2023)))
    # print(average_rating)

    # count()
    # Возвращает количество объектов, связанных через предоставленное выражение.
    # class Count(expression, distinct=False, filter=None, **extra)
    # Вычислить число уникальных авторов статей(которые написали хотя бы одну статью)
    # count_authors = Entry.objects.aggregate(
    #     count_authors=Count('author', distinct=True)
    # )
    # print(count_authors)
    # Получить статьи с количеством тегов
    # entries_with_tags_count = Entry.objects.annotate(
    #     tag_count=Count('tags')).values('id', 'tag_count')
    # print(entries_with_tags_count)

    # max, min
    # Возвращает максимальное/минимальное значение данного выражения
    # class Max(expression, output_field=None, filter=None, default=None, **extra)
    # class Min(expression, output_field=None, filter=None, default=None, **extra)

    # Вычислить максимальную и минимальную оценку
    # calc_rating = Entry.objects.aggregate(
    #     max_rating=Max('rating'), min_rating=Min('rating')
    # )
    # print(calc_rating)

    # StdDev, Variance
    # Возвращает стандартное отклонение данных в предоставленном выражении.
    # class StdDev(expression, output_field=None, sample=False, filter=None, default=None, **extra)
    # Возвращает дисперсию данных в предоставленном выражении.
    # class Variance(expression, output_field=None, sample=False, filter=None, default=None, **extra)
    # Вычислить среднее квадратическое отклонение и дисперсию оценки
    # calc_rating = Entry.objects.aggregate(
    #     std_rating=StdDev('rating'), var_rating=Variance('rating')
    # )
    # print(calc_rating)

    # Sum
    # Вычисляет сумму всех значений данного выражения
    # class Sum(expression, output_field=None, distinct=False, filter=None, default=None, **extra)
    # Вычислить общее число комментариев в БД
    # calc_rating = Entry.objects.aggregate(
    #     sum_comments=Sum('number_of_comments')
    # )
    # print(calc_rating)

    # reverse()
    # Если вам нужно просто изменить порядок элементов в наборе запросов на обратный, вы можете использовать метод reverse()
    # filtered_data = Blog.objects.filter(id__gte=2).order_by("id")
    # print(filtered_data)  # упорядочивание по возрастанию по полю id
    # print(filtered_data.reverse())  # поменяли направление
    # Если порядок не указан или в модели, или через order_by, то reverse работать не будет

    # distinct()
    # Возвращает новый QuerySet, который использует SELECT DISTINCT, исключая повторы
    # Работает только с POSTGRESQL
    # print(Entry.objects.order_by('author', 'pub_date').distinct('author', 'pub_date'))  # Не работает в SQLite
    # distinct('author', 'pub_date') - оставляет уникальные строки по колонкам author, pub_date
    # distinct() - старается оставить уникальные данные по всем колонкам
    # Аналогично с поиском по полю можно обращаться к связанным данным distinct('author__name', 'pub_date')

    # values()
    # Возвращает QuerySet, который возвращает словари, а не экземпляры модели, когда используется как итеративный.
    # Обычный запрос
    # print(Blog.objects.filter(name__startswith='Фитнес'))
    # Запрос раскрывающий значения
    # print(Blog.objects.filter(name__startswith='Фитнес').values())
    # Вывод всех строк с их раскрытием
    # print(Blog.objects.values())
    # Вывод всех строк с сохранением в запросе только необходимых столбцов
    # print(Blog.objects.values('id', 'name'))  # Обратите внимание, что данные отсортированы по полю name

    # values_list()
    # Это похоже на values(), за исключением того, что вместо возврата словарей он возвращает кортежи при повторении.
    # Вывод всех строк с их раскрытием
    # print(Blog.objects.values_list())
    # Вывод всех строк с сохранением в запросе только необходимых столбцов
    # print(Blog.objects.values_list('id', 'name'))  # Обратите внимание, что данные отсортированы по полю name

    """union(), intersection(), difference()"""
    # union()
    # union() использует оператор SQL UNION для объединения результатов двух или более QuerySet’ов
    # qs1.union(qs2, qs3) или так qs1.union(qs2).union(qs3)
    # blog_a_entries = Entry.objects.filter(blog__name='Путешествия по миру')
    # blog_b_entries = Entry.objects.filter(blog__name='Кулинарные искушения')
    # blog_c_entries = Entry.objects.filter(blog__name='Фитнес и здоровый образ жизни')
    # result_qs = blog_a_entries.union(blog_b_entries, blog_c_entries)
    # print(result_qs)
    # Для такой задачи может хорошо подойти in (ответ будет аналогичен), правда порядок может быть другой
    # print(Entry.objects.filter(
    #     blog__name__in=['Путешествия по миру', 'Кулинарные искушения', 'Фитнес и здоровый образ жизни']))

    # intersection()
    # qs1.intersection(qs2, qs3) или qs1.intersection(qs2).intersection(qs3)
    # blog_a_entries = Entry.objects.filter(blog__name='Путешествия по миру').values('author')
    # blog_b_entries = Entry.objects.filter(blog__name='Кулинарные искушения').values('author')
    # blog_c_entries = Entry.objects.filter(blog__name='Фитнес и здоровый образ жизни').values('author')
    # result_qs = blog_a_entries.intersection(blog_b_entries, blog_c_entries)
    # print(result_qs)

    # difference()
    # qs1.difference(qs2, qs3) или qs1.difference(qs2).difference(qs3)
    # blog_a_entries = Entry.objects.filter(blog__name='Путешествия по миру').values('author')
    # blog_b_entries = Entry.objects.filter(blog__name='Кулинарные искушения').values('author')
    # blog_c_entries = Entry.objects.filter(blog__name='Фитнес и здоровый образ жизни').values('author')
    # result_qs = Entry.objects.values('author').difference(blog_a_entries, blog_b_entries, blog_c_entries)
    # print(result_qs)

    # select_related()
    """
    Возвращает QuerySet, который будет «следовать» отношениям 
    внешнего ключа, выбирая дополнительные данные связанного 
    объекта при выполнении своего запроса. 
    Это повышение производительности, которое приводит к 
    одному более сложному запросу, но означает, что дальнейшее 
    использование отношений внешнего ключа не потребует 
    запросов к базе данных.
    
    Для отображения характеристик запросов воспользуемся 
    connection из django.db. 
    connection.queries позволяют получить словарь, где 
    содержится запрос в БД и время его выполнения
    
    Также можно использовать django-debug-toolbar 
    или django-silk
    """
    # Стандартный поиск:
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # entry = Entry.objects.get(id=5)
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # blog = entry.blog
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # print('Результат запроса = ', blog)
    # TODO Стоит повторить материал
    # Пример с select_related:
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # entry = Entry.objects.select_related('blog').get(id=5)
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # blog = entry.blog
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # print('Результат запроса = ', blog)

    # prefetch_related()
    # Возвращает QuerySet, который автоматически извлекает в одном пакете связанные объекты для каждого из указанных поисков.

    """
    select_related работает путем создания соединения 
    (join) SQL и включения полей связанного объекта в оператор 
    SELECT. По этой причине select_related получает связанные 
    объекты в одном запросе к базе данных. Тем не менее, чтобы 
    избежать гораздо большего результирующего набора, который 
    мог бы возникнуть в результате объединения через отношение 
    „many“, select_related ограничен однозначными отношениями 
    - внешним ключом и один-к-одному.
    """

    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # entry = Entry.objects.all()
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # for row in entry:
    #     tags = [tag.name for tag in row.tags.all()]
    #     print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    #     print('Результат запроса = ', tags)

    # тот же пример с префетч:
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # entry = Entry.objects.prefetch_related("tags")
    # print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    # for row in entry:
    #     tags = [tag.name for tag in row.tags.all()]
    #     print("Число запросов = ", len(connection.queries), " Запросы = ", connection.queries)
    #     print('Результат запроса = ', tags)

    """Дополнительный функционал, позволяющий создавать сложные запросы"""
    # F-выражения
    """
    Объект F() представляет значение поля модели, преобразованное 
    значение поля модели или аннотированный столбец. 
    Он позволяет ссылаться на значения полей модели и 
    выполнять операции с базой данных, используя их 
    без необходимости извлекать их из базы данных
    в память Python
    """
    # Вывести статьи, где число комментариев на сайте больше числа комментариев на сторонних ресурсах:
    # print(Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks')).values('id',
    #                                                                                    'number_of_comments',
    #                                                                                    'number_of_pingbacks'))

    # Q-объекты
    """
    Объект Q() представляет собой условие SQL, которое 
    может быть использовано в операциях, связанных с базой данных.
    Это похоже на то, как объект F() представляет значение поля
    модели или аннотации. Они позволяют определять и повторно 
    использовать условия и объединять их с помощью таких 
    операторов, как | (OR), & (AND) и ^ (XOR)
    """
    # Получение всех записей, у которых заголовок содержит 'ключевое слово' или текст содержит 'определенное слово'
    # entries = Entry.objects.filter(
    #     Q(headline__icontains='тайны') | Q(body_text__icontains='город'))
    # print(entries)
    # Получение записей блога "Путешествия по миру" с датами публикаций между 1 мая 2022 и 1 мая 2023
    # entries = Entry.objects.filter(
    #     Q(blog__name='Путешествия по миру') & Q(pub_date__date__range=(date(2022, 5, 1), date(2023, 5, 1))))
    # print(entries)
    # XOR(^) отличается от OR тем, что только ОДНО условий будет истинным

    # ExpressionWrapper()
    # ExpressionWrapper окружает другое выражение и предоставляет доступ к свойствам, таким как output_field, которые могут быть недоступны для других выражений.
    # ExpressionWrapper необходим при использовании арифметики на выражениях F() с различными типами
    # class ExpressionWrapper(expression, output_field)

    # Case, When, Value
    # Получение всех записей с полем is_popular, которое равно True, если значение поля rating больше равно 4, иначе False
    # entries = Entry.objects.annotate(
    #     is_popular=Case(
    #         When(rating__gte=4, then=True),
    #         default=False,
    #         output_field=BooleanField()
    #     )
    # ).values('id', 'rating', 'is_popular')
    # print(entries)

    # Создание описательной метки для числа тегов в статье
    # entries = Entry.objects.annotate(
    #     count_tags=Count("tags"),
    #     tag_label=Case(
    #         When(count_tags__gte=3, then=Value('Много')),
    #         When(count_tags=2, then=Value('Средне')),
    #         default=Value('Мало'),
    #         output_field=CharField()
    #     )
    # ).values('id', 'count_tags', 'tag_label')
    # print(entries)

    # Subquery() - явный подзапрос
    # class Subquery(queryset, output_field=None)
    """
    Subquery может быть полезным в следующих случаях:
    Фильтрация: Вы можете использовать Subquery для фильтрации 
    записей основного запроса на основе результатов другого 
    запроса. Например, вы можете получить список ID записей из 
    одной таблицы и использовать их в фильтрации другой таблицы.
    
    Аннотация: Subquery может использоваться для аннотации 
    значений в основном запросе на основе результатов другого 
    запроса. Например, вы можете аннотировать каждую запись с 
    количеством связанных записей из другой таблицы.
    
    Сортировка: Subquery может быть использован для сортировки 
    записей основного запроса на основе результатов другого 
    запроса. Например, вы можете отсортировать записи по 
    значению, вычисленному в другом запросе.
    
    Ограничение (Limit): Subquery может использоваться для 
    ограничения количества записей основного запроса на основе 
    результатов другого запроса. Например, вы можете ограничить 
    основной запрос только теми записями, которые присутствуют 
    в другом запросе.
    """
    # Получаем список ID авторов без биографии
    # subquery = AuthorProfile.objects.filter(bio__isnull=True).values('author_id')
    # Фильтруем записи блога по авторам
    # query = Entry.objects.filter(author__in=Subquery(subquery))
    # print(query)
    # Аналогично можно подключиться так, так как есть непрямая связь между Author и AuthorProfile через первичный ключ
    # print(Entry.objects.filter(author__authorprofile__bio__isnull=True))

    """Необработанные выражения SQL"""
    # Иногда выражения базы данных не могут легко выразить сложное предложение WHERE.
    # Поэтому в крайних случаях использует "сырой" SQL
    # Составляем SQL-запрос
    # sql = """
    # SELECT id, headline
    # FROM db_entry
    # WHERE headline LIKE '%%тайны%%' OR body_text LIKE '%%город%%'
    # """
    # Выполняем запрос
    # with connection.cursor() as cursor:
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #
    # # Выводим результаты
    # for result in results:
    #     print(result)
    # Также можно вызвать метод raw() и передать туда параметры.
    # Выполняем сырой SQL-запрос
    # results = Entry.objects.raw(
    #     """
    #     SELECT id, headline
    #     FROM db_entry
    #     WHERE headline LIKE '%%тайны%%' OR body_text LIKE '%%город%%'
    #     """
    # )
    # Выводим результаты
    # for result in results:
    #     print(result.id, result.headline)

    """Оконные функции"""
    # class Window(expression, partition_by=None, order_by=None, frame=None, output_field=None)
    # Получаем queryset статей блога с аннотациями, используя оконные функции
    # queryset = Entry.objects.annotate(
    #     avg_comments=Window(
    #         expression=Avg('number_of_comments'),
    #         partition_by=F('blog'),
    #     ),
    #     max_comments=Window(
    #         expression=Max('number_of_comments'),
    #         partition_by=F('blog'),
    #     ),
    #     min_comments=Window(
    #         expression=Min('number_of_comments'),
    #         partition_by=F('blog'),
    #     ),
    #
    # ).values('id', 'headline', 'avg_comments', 'max_comments', 'min_comments')
    # print(queryset)
