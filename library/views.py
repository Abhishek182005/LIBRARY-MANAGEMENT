from django.shortcuts import redirect, render
from .models import Book, IssuedItem
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.paginator import Paginator

# Home view
def home(request):
    return render(request, "home.html")

# Login view to login user
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")
    else:
        return render(request, "login.html")

# Register view to register user
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password1,
                )
                user.save()
                return redirect("login")
        else:
            messages.info(request, "Passwords do not match")
            return redirect("register")
    else:
        return render(request, "register.html")

# Logout view to logout user
def logout(request):
    auth_logout(request)
    return redirect("home")

# Issue view to issue book to user
@login_required(login_url="login")
def issue(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        current_book = Book.objects.get(id=book_id)
        if current_book.quantity > 0:
            IssuedItem.objects.create(user_id=request.user, book_id=current_book)
            current_book.quantity -= 1
            current_book.save()
            messages.success(request, "Book issued successfully.")
        else:
            messages.error(request, "No copies of this book are currently available.")
        return redirect("issue")

    my_items = IssuedItem.objects.filter(user_id=request.user, return_date__isnull=True).values_list("book_id", flat=True)
    books = Book.objects.exclude(id__in=my_items).filter(quantity__gt=0)
    return render(request, "issue_item.html", {"books": books})

# History view to show history of issued books to user
@login_required(login_url="login")
def history(request):
    my_items = IssuedItem.objects.filter(user_id=request.user).order_by("-issue_date")
    paginator = Paginator(my_items, 10)
    page_number = request.GET.get("page")
    show_data_final = paginator.get_page(page_number)
    return render(request, "history.html", {"books": show_data_final})

# Return view to return book to library
@login_required(login_url="login")
def return_item(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        current_book = Book.objects.get(id=book_id)
        issue_item = IssuedItem.objects.filter(user_id=request.user, book_id=current_book, return_date__isnull=True).first()
        if issue_item:
            current_book.quantity += 1
            current_book.save()
            issue_item.return_date = date.today()
            issue_item.save()
            messages.success(request, "Book returned successfully.")
        else:
            messages.error(request, "No such book issued.")
        return redirect("return_item")

    my_items = IssuedItem.objects.filter(user_id=request.user, return_date__isnull=True).values_list("book_id", flat=True)
    books = Book.objects.filter(id__in=my_items)
    return render(request, "return_item.html", {"books": books})
