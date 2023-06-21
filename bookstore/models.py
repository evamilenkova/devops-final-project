from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " " + self.surname


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('a', 'Admin'),
        ('r', 'Retailer'),
        ('c', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    ISBN = models.CharField(max_length=100)
    description = models.TextField()
    number_of_pages = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    available_copies = models.IntegerField()
    image = models.ImageField(upload_to="books")

    def __str__(self):
        return self.title


class Cart(models.Model):
    FORMAT_CHOICES = (
        ('audio', 'Audio'),
        ('physical', 'Physical'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    book_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='physical')

    def __str__(self):
        return "User: " + self.user.username + " Book: " + self.book.title


class DeliveryInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return "delivery info for " + self.user.username


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    delivery_info=models.ForeignKey(DeliveryInfo,on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Favourite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return "User: " + self.user.username + " likes  " + self.book.title
