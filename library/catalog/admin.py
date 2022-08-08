from django.contrib import admin
from .models import Author, Genre, Language, Book, BookInstance

# Register your models here.
# admin: root:adminpassword
# Garry:12wsxzaq!@WSXZAQ
# Russel:12wsxzaq!@WSXZAQ
# Регистрация моделей в админ-панели
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)


# admin.site.register(BookInstance)

# Класс отображения информации о книгах автора
# для отображения в информации об авторе
# TabularInline - горизонтальное расположение связанной таблицы
class BooksInLine(admin.TabularInline):
    # extra = 0 - отключение отображение 3-х дополнительных пустых экземпляров книги,
    # которые отображаются по-умолчанию
    extra = 0
    model = Book


class AuthorAdmin(admin.ModelAdmin):
    # Отображение в админ-панели авторов в формате Имя, Фамилия, Дата рождения, дата смерти
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Отображение полей имени и фамилии друг под другом,
    # полей даты рождения и даты смерти - рядом
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # inlines - Отображение связанной таблицы
    inlines = [BooksInLine]


admin.site.register(Author, AuthorAdmin)


# Класс отображения информации о экземплярах книги
# для отображения в информации о книге
# TabularInline - горизонтальное расположение связанной таблицы
class BooksInstanceInLine(admin.TabularInline):
    # extra = 0 - отключение отображение 3-х дополнительных пустых экземпляров книги,
    # которые отображаются по-умолчанию
    extra = 0
    model = BookInstance


# Декоратор @admin.register(Book) делает то же, что и admin.site.register(Book, BookAdmin)
# @admin.register(Book) == admin.site.register(Book, BookAdmin)
# Регистрация класса Admin для Book с помощью декоратора
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Отображение в админ-панели книги в формате Название, Автор, Жанры
    list_display = ('title', 'author', 'display_genre')
    # Отображение информации об экземплярах книги в информации о книге
    # inlines - Отображение связанной таблицы
    inlines = [BooksInstanceInLine]


# Регистрация класса Admin для BookInstance с помощью декоратора
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Отображение в админ-панели таблицы экземпляров книг в формате Книга, Статус, Дата возврата, ID экземпляра
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    # Добавление в админ-панель фильтра книг по статусу и дате возврата
    list_filter = ('status', 'due_back')

    # Группировка в инормации по доступности книги в разделы: Книга, Импринт, ID
    # и Статус, Дата возврата
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Доступность', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )
