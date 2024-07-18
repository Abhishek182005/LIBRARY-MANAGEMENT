# admin.py
from django.contrib import admin
from .models import Book, IssuedItem

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'author_name', 'quantity', 'subject', 'book_add_date', 'book_add_time')

@admin.register(IssuedItem)
class IssuedItemAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'username', 'issue_date', 'return_date')
