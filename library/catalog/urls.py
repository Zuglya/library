from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),    # Просмотр своих взятых книг
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),    # Просмотр всех взятых книг
    path(r'allbooks/', views.LoanedBooksAllListViewAll.as_view(), name='all-books'),    # Просмотр всех книг
]


# Добавляет URL для библиотекаря, чтобы обновить книгу.
# Перенаправляем запросы с адресов формата /catalog/book/<bookinstance id>/renew/
# в функцию с именем renew_book_librarian() в views.py,
# туда же передаём идентификатор id записи BookInstance в качестве параметра с именем pk.
urlpatterns += [
    path('book/<uuid:pk>/renew', views.renew_book_librarian, name='renew-book-librarian'),
]


# Добавляем URL для создания, изменения и удаления авторов
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    # Использовать pk как имя для "захваченного" значения первичного ключа,
    # так как параметр именно с таким именем ожидается классами отображения.
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]


# Добавляем URL для создания, изменеия и удаления книг
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]