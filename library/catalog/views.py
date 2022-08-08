from django.shortcuts import render
# Библиотека для предоставления страницы списка объектов
from django.views import generic
from .models import Book, Author, BookInstance, Genre
# LoginRequiredMixin обеспечивает проверку статуса входа в систему
# PermissionRequiredMixin проверяет что текущий пользователь имеет все указанные права доступа.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
# HttpResponseRedirect: Данный класс перенаправляет на другой адрес
from django.http import HttpResponseRedirect
# reverse(): Генерирует URL-адрес при помощи соответствующего имени URL  и дополнительных аргументов.
from django.urls import reverse
# datetime: Библиотека Python для работы с датами и временим.
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RenewBookForm
from .forms import RenewBookModelForm
# CreateView, UpdateView, DeleteView - для создания, обновления и удаления объектов
from django.views.generic import CreateView, UpdateView, DeleteView
# reverse_lazy() - Для перехода на страницу списка авторов после удаления одного из них
from django.urls import reverse_lazy



# Функция отображения для домашней страницы сайта.
def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (статус = 'д')
    num_instances_available = BookInstance.objects.filter(status__exact='д').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Количество посещений домашней страницы библиотеки, подсчитанное в переменной сессии.
    # Получаем значение 'num_visits' из сессии. Возвращаем 0, если оно не было установлено ранее.
    num_visits = request.session.get('num_visits', 0)
    # При получении запроса увеличиваем значение сессии на 1
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html', context={'num_books': num_books, 'num_instances': num_instances,
                               'num_instances_available': num_instances_available,
                               'num_authors': num_authors,
                               'num_visits': num_visits},
    )


# Определение класса предстовления на основе базового класса ListView
class BookListView(generic.ListView):
    model = Book
    # Количество книг для постраничного отображения
    paginate_by = 10



# Определение класса предстовления на основе базового класса DetalView
class BookDetailView(generic.DetailView):
    model = Book


# Общее представление списка на основе классов для списка авторов.
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


# Общий вид подробностей на основе классов для автора.
class AuthorDetailView(generic.DetailView):
    model = Author


# Представление для получения списка всех книг, которые были предоставлены текущему пользователю.
# LoginRequiredMixin, наследуется для того, чтобы только вошедший пользователь смог вызвать это представление.
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    # Форма списка экземпляров книг, взятых пользователем
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    # Показывает всзятые книги пользователя, отсортированные начиная с самых старых due_back
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='в').order_by('due_back')


# Представление для получения списка всех книг, предоставленных всем пользователям.
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    # Показывает всзятые книги пользователей, отсортированные начиная с самых старых due_back
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='в').order_by('due_back')



# Представление для получения списка всех книг из библиотеки.
class LoanedBooksAllListViewAll(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all_books.html'
    paginate_by = 10

    # Показывает все книги отсортированные по названию
    def get_queryset(self):
        return BookInstance.objects.order_by('book')



@login_required
# Ограничение доступа к отображению (открыть доступ только библиотекарям)
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    # get_object_or_404(): Возвращает определённый объект из модели
    # в зависимости от значения его первичного ключа,
    # или выбрасывает исключение Http404, если данной записи не существует.
    book_instance = get_object_or_404(BookInstance, pk=pk)  # pk - получение текущего объекта типа BookInstance

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        # Создаём экземпляр формы и заполняем данными из запроса:
        # form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)

        # Проверка валидности формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data и  присваивание их полю due_back
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Перенаправление на новый URL.  Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed'))

        return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'book_instance': book_instance})

    # Если это GET (или другой метод), тогда создаём форму по умолчанию
    else:
        # Создаём форму по умолчанию и передаём ей начальное значение для поля renewal_date
        # (3 недели, начиная с текущей даты).
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # initial - начальное значение для поля renewal_date
        # form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

        # Создаём HTML-страницу, в качестве параметров шаблон и контекст, который содержит объект формы.
        context = {
            'form': form,
            'book_instance': book_instance
        }
        return render(request, 'catalog/book_renew_librarian.html', context)


# Классы для создания, изменения и удаления авторов
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    #  В случае успешного удаления перенапрявляем на Авторов
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


# Классы для создания, изменения и удаления книг
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book')
    permission_required = 'catalog.can_mark_returned'