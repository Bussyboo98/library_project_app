from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from tinymce import HTMLField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin




class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, user_name, password, **other_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password, **other_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, user_name, password, **other_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    MALE = 'Male'
    FEMALE = 'Female'
    CHOOSE = ''

    GENDER_OPTIONS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (CHOOSE, 'Select Gender'),
    ]
    user_name = models.CharField(max_length=100, unique=True)
    matric_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=30, choices=GENDER_OPTIONS, default=CHOOSE, blank=True, null=True)
    department = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=True) 
    is_active = models.BooleanField(default=True) 

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email  
    
    def activate_user(self):
        self.is_active =True
        self.save()

    def deactivate_user(self):
        self.is_active = False
        self.save()





class Book(models.Model):
    book_title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13, unique=True)
    publication_year = models.PositiveIntegerField()
    description = HTMLField('Content')
    book_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    language = models.CharField(max_length=20, default='English')
    available_copies = models.PositiveIntegerField(default=0)
    total_copies = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_title  

    def get_book_title(self):
        if self.book_title:
            return self.book_title



class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(default=timezone.now)
    returned_date = models.DateTimeField(null=True, blank=True)
    reason_for_borrowing = models.TextField(blank=True, null=True)
    is_borrowed = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower.user_name} borrowed {self.book.book_title}"
    
class Return(models.Model):
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    returned_date = models.DateTimeField(default=timezone.now)
    returned_condition = models.TextField()

    def __str__(self):
        return f"{self.borrowing.borrower.user_name} returned {self.borrowing.book.book_title}"