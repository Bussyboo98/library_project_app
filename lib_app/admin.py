from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('user_name','matric_number', 'name', 'email', 'gender', 'department', 'is_active', 'is_staff')
    search_fields = ('matric_number', 'name', 'email')
    list_filter = ('is_active', 'is_staff', 'gender', 'department')
    ordering = ('matric_number',)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'author', 'ISBN', 'publication_year',  'available_copies', 'total_copies')
    search_fields = ('book_title', 'author', 'ISBN')

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'borrowed_date', 'returned_date', 'is_borrowed', 'is_returned')
    list_filter = ('borrowed_date', 'is_borrowed', 'is_returned')
    search_fields = ('book__book_title', 'borrower__user_name')

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('borrowing', 'returned_date', 'returned_condition')
    search_fields = ('borrowing__book__book_title', 'borrowing__borrower__username')
