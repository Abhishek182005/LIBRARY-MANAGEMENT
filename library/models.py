# importing required modules
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

# ----------- Library Management System Models ------------

# Book model to store book details
class Book(models.Model):
    book_name = models.CharField(max_length=150)
    author_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    subject = models.CharField(max_length=2000)
    book_add_date = models.DateField(default=timezone.now)
    book_add_time = models.TimeField(default=timezone.now) 

    class Meta:
        unique_together = ("book_name", "author_name")

    def __str__(self):
        return self.book_name


# IssuedItem model to store issued book details
class IssuedItem(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(default=date.today(), blank=False)
    return_date = models.DateField(blank=True, null=True)

    # property to get book name
    @property
    def book_name(self):
        return self.book_id.book_name

    # property to get author name
    @property
    def username(self):
        return self.user_id.username

    def __str__(self):
        return (
            self.book_id.book_name
            + " issued by "
            + self.user_id.first_name
            + " on "
            + str(self.issue_date)
        )