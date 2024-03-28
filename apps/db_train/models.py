from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import datetime
# Создайте свои модели здесь


class Author(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+79\d{9}$',
        message="Телефонный номер должен быть формата: '+79123456789'."
    )

    username = models.SlugField(verbose_name='Имя аккаунта',
                                help_text='Введите username, не длиннее 50 символов. Использовать нужно латиницу, разделяя фразы "-".',
                                unique=True)

    email = models.EmailField(verbose_name='Адрес электронной почты',
                              help_text='Адрес почты в формате *@*.*',
                              unique=True)

    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия',
                                 help_text='Ограничение - 100 символов.',
                                 null=True,
                                 blank=True)

    first_name = models.CharField(max_length=100,
                                 verbose_name='Имя',
                                 help_text='Ограничение - 100 символов.',
                                 null=True,
                                 blank=True)

    middle_name = models.CharField(max_length=100,
                                 verbose_name='Отчество',
                                 help_text='Ограничение - 100 символов.',
                                 null=True,
                                 blank=True)

    gender = models.CharField(max_length=1, choices=[('м', 'мужской'), ('ж', 'женский')],
                              verbose_name='Пол',
                              help_text='Выберите пол',
                              null=True,
                              blank=True)

    self_esteem = models.DecimalField(max_digits=2, decimal_places=1,
                                      validators=[MinValueValidator(0, "Диапазон [0.0, 5.0]"),
                                                  MaxValueValidator(5, "Диапазон [0.0, 5.0]")],
                                      verbose_name='Уровень самооценки',
                                      help_text='Введите уровень вашей самооценки, только честно! Градация 0 - 5, где 0 - молодец, 5 - умница.',
                                      null=True,
                                      blank=True)

    phone_number = models.CharField(max_length=12,
                                    validators=[phone_regex],
                                    help_text='Введите номер телефона без пробелов в формате+79998887766',
                                    null=True,
                                    blank=True,
                                    unique=True)

    city = models.CharField(max_length=100,
                            verbose_name="Город",
                            help_text="Введите название города",
                            null=True,
                            blank=True)

    bio = models.TextField(verbose_name="Биография",
                           help_text="Расскажите немного о себе.",
                           null=True,
                           blank=True)

    age = models.IntegerField(null=True, editable=False)

    date_birth = models.DateField(verbose_name="Дата рождения",
                                  help_text="Посланцев из будущего не приветствуем!",
                                  null=True,
                                  blank=True)

    status_rule = models.BooleanField(verbose_name="Согласие с правилами",
                                      help_text="Подпиши контракт с дьяволом")

    image = models.ImageField(upload_to='foto_profile',
                              verbose_name="Картинка профиля",
                              help_text="Можно не своё, Райан Гослинг - подойдет",
                              null=True,
                              blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        initials = None
        if self.first_name and self.middle_name:
            initials = f"{self.first_name.upper()[0]}.{self.middle_name.upper()[0]}."
        return f"{self.username} - {self.last_name} {initials}"

    def save(self, *args, **kwargs):
        if self.date_birth:
            today = datetime.today()
            additional_year = (today.month, today.day) < (self.date_birth.month, self.date_birth.day)
            self.age = today.year - self.date_birth.year - additional_year
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Автор",
        verbose_name_plural = "Авторы"


class AuthorProfile(models.Model):
    author = models.OneToOneField('Author', on_delete=models.CASCADE)
    stage = models.IntegerField(default=0,
                                blank=True,
                                verbose_name='Стаж',
                                help_text='Стаж в годах')

    def __str__(self):
        return f'Автор: {self.author.username}; Стаж: {self.stage} лет'


class Entry(models.Model):
    text = models.TextField(verbose_name='Текст статьи',)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='entries')
    tags = models.ManyToManyField('Tag', related_name='entries')

    def __str__(self):
        return f'Автор статьи: {self.author.username}; Текст: {self.text}'


class Tag(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название')

    def __str__(self):
        return f'Тег: {self.name}'
