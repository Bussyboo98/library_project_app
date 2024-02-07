from django.urls import path
from lib_app import views
from .views import *

app_name = 'lib_app'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('book/<slug:slug>/', BookDetailView.as_view(), name='book_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('borrow/<slug:slug>/', borrow_details, name='borrow_details'),
    path('borrow_book/<slug:slug>/', views.borrow_book, name='borrow_book'),
    path('return_book/<int:borrowing_id>/', return_book, name='return_book'),
    path('borrow-success/', views.borrow_success, name='borrow_success'),
    path('change-password/', views.change_password, name='change'),
    path('borrowed-books/', borrowed_books, name='borrowed_books'),
    path('logout/', views.logout_view, name='logout'),
       
]