from django.db import models
from django.urls import reverse  # Используется для создания URL-адресов путем изменения шаблонов URL-адресов.
import uuid  # Требуется для создания уникальных экземпляров книги
from django.contrib.auth.models import User # Требуется для назначения пользователя заемщиком книги
from datetime import date


# Модель для таблицы книжного жанра
class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=200,
        help_text="Введите жанр книги (научная фантастика, фэнтази, юмор и т.д.)"
    )

    # Метод для возврата названия жанра
    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField('Язык', max_length=200,
                            help_text="Введите язык книги (русский, английский, немецкий, французский и т. д.)")

    # Метод, возвращающий строку языком книги (на сайте администратора и т. д.)
    def __str__(self):
        return self.name


# Модель для книги
class Book(models.Model):
    title = models.CharField('Название книги', max_length=200)
    # Внешний ключ для связи 1 ко многим. 1 автор -> Много книг.
    # null=True - позволяет хранить Null, если автор не выбран
    # on_delete = models.SET_NULL - установит значение автора в Null, если связанная с автором запись будет удалена.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField('Аннотация', max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 символов <a href="https://www.bookchamber.ru/isbn.html">номер ISBN</a>')
    # Нужно отношение ManyToManyField, поскольку жанр может содержать много книг.
    # Книги могут охватывать множество жанров.
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

        # Метод для создания строки жанров книги.
    # Это необходимо для отображения жанра в админ-панели, так как книга - жанр имеет отношение
    # многие ко многим
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанр'


    # Метод для возврата названия книги
    def __str__(self):
        return self.title


    # Возвращает URL-адрес для доступа к определенному экземпляру книги.
    # Нужно определить сопоставление URL-адресов, в котором содержится подробная информация о книге,
    # и определить связанное представление и шаблон
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


# Модель, представляющая конкретный экземпляр книги, который можно взять в библиотеке.
class BookInstance(models.Model):
    # UUIDField используется для поля id, чтобы установить его как primary_key для этой модели.
    # Этот тип поля выделяет глобальное уникальное значение для каждого экземпляра книги
    # (по одному для каждой книги, которые есть в библиотеке)
    id = models.UUIDField('ID в библиотеке', primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор этого экземпляра книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField('Импринт', max_length=200)
    # DateField используется для даты due_back появления книги в библиотеке,
    # когда ожидается, что книга появится после резервирования или обслуживания.
    due_back = models.DateField('Дата возврата', null=True, blank=True)
    # Поле пользователя - заёмщика книги
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Метод возвращает True, если книга просрочена
    @property
    def is_overdue(self):
        # Если Дата возврата существует и Дата возврата больше, чем сегодняшний день, то True
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('т', 'Техническое обслуживание'),
        ('в', 'Взято'),
        ('д', 'Доступно'),
        ('з', 'Зарезервировано'),
    )

    # status - это CharField, который определяет список choice/selection. По-умолчанию: 'т' - Техническое обслуживание.
    status = models.CharField('Статус',
                              max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='т',
                              help_text='Статус книги')

    # Атрибут ordering поле due_back
    # используется для упорядочивания записей, когда они возвращаются в запросе к БД.
    class Meta:
        ordering = ["due_back"]
        # Поле Permission - определяет разрешения.
        # Добавляем разрешение отметить, что книга была возвращена
        permissions = (("can_mark_returned", "Set book as returned"),)

    # Метод, предоставляющий уникальный номер идентификатора книги во всей библиотеке и название книги.
    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)

    class Meta:
        # Атрибут ordering используется для упорядочивания записей,
        # когда они возвращаются в запросе к БД.
        ordering = ['last_name', 'first_name']

    # Возвращает URL-адрес для доступа к информации об авторе
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    # Метод возвращает фамилию и имя автора
    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
