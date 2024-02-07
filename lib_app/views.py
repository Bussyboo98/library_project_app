from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.contrib.auth import update_session_auth_hash


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

class BookListView(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 10 

class BookDetailView(DetailView):
    model = Book
    template_name = 'book-details.html'
    context_object_name = 'book'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Registration successful!')
            return redirect('lib_app:login') 
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check for 'next' parameter in the query string
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                # If 'next' is not provided, redirect to the default dashboard_account
                return redirect('lib_app:dashboard')
        else:
            messages.error(request, 'Username and Password do not match')

    return render(request, 'login.html')

# @login_required(login_url='/login/')
def dashboard(request):
    return render(request, "backend/index.html")



@login_required(login_url='/lib_app/login/')

def borrow_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    if request.method == 'POST':
        form = BorrowingForm(request.POST)
        if form.is_valid():
            borrowing = form.save(commit=False)
            borrowing.book = book
            borrowing.borrower = request.user
            borrowing.is_borrowed = True
            borrowing.save()
            book.available_copies -= 1
            book.save()
            print("Borrowing successful!")
            return redirect('lib_app:borrow_success')  # Redirect to a success page or wherever you like
        else:
            print("Form is not valid:", form.errors)
    else:
        form = BorrowingForm()
    
    return render(request, 'borrow_details.html', {'form': form, 'book': book})

def borrow_success(request):
    return render(request, 'borrow-success.html')

def return_book(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id, borrower=request.user, is_borrowed=True)

    if borrowing.is_returned:
        messages.warning(request, f"This book has already been returned.")
    else:
        # Set is_returned to True
        borrowing.is_returned = True
        borrowing.save()

        messages.success(request, f"You have successfully returned '{borrowing.book.book_title}'.")

    # Redirect to the page where the user borrowed the book
    return redirect('lib_app:borrowed_books')

def borrowed_books(request):
    borrowed_books = Borrowing.objects.filter(borrower=request.user, is_borrowed=True)
    return render(request, 'backend/borrowed-books.html', {'borrowed_books': borrowed_books})


# @login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(data=request.POST,user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'You Have Successfully Updated Your Password.')
    else:
        pass_form = PasswordChangeForm(user=request.user)
        messages.error(request, 'An error occured. Please try again!.')
    return render(request, 'backend/change-password.html', {'pass':pass_form})

# @login_required(login_url='/dashboard/')
def edit_form(request):
    if request.method == 'POST':
        edit_form = EditUserForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'User edited successfully.')
    else:
        edit_form = EditUserForm(instance=request.user)
    return render(request, 'backend/edit-user-profile.html', {'edit_key':edit_form})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('lib_app:login')
