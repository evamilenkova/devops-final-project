"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from bookstore.views import index, search, details, user_login, register_customer, logout_view, handle_form_submission, \
    cart, favourites, place_order, confirmed, filter_books, remove_from_cart, edit_book, add_book, delete_book

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index),
                  path('search/', search, name='search_books'),
                  path('books/<int:book_id>/', details, name='book_details'),
                  path('login/', user_login),
                  path('register/', register_customer),
                  path('logout/', logout_view, name='logout'),
                  path('cart/', cart, name='cart'),
                  path('favourites/', favourites, name='favourites'),
                  path('deliveryinfo/', place_order, name='confirm_delivery'),
                  path('confirmed/', confirmed, name='order_confirmed'),
                  path('filter/', filter_books, name='filter_books'),
                  path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
                  path('book/edit/<int:book_id>/', edit_book, name='book-edit'),
                  path('add/<int:book_id>/', handle_form_submission, name='add'),
                  path('add-book/', add_book, name='add_book'),
                  path('delete-book/<int:book_id>/', delete_book, name='delete_book'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
