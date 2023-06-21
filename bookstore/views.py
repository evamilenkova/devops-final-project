from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from bookstore.forms import CustomAuthenticationForm, CustomerRegistrationForm, DeliveryInfoForm, BookForm, AddBookForm
from bookstore.models import Book, Author, Category, Cart, Favourite, DeliveryInfo, Order


# Create your views here.

def index(request):
    books = Book.objects.all()[:6]
    authors = Author.objects.all()[:6]
    categories = Category.objects.all()[:6]
    context = {"books": books, "authors": authors, "categories": categories}
    return render(request, "index.html", context)


def search(request):
    authors = Author.objects.all()[:5]
    categories = Category.objects.all()[:5]
    search_term = request.GET.get('search_term')
    books = Book.objects.filter(title__icontains=search_term)[:6]
    context = {"books": books, "authors": authors, "categories": categories, "search_term": search_term}
    return render(request, 'index.html', context)


def details(request, book_id=None):
    book = get_object_or_404(Book, id=book_id)
    isInShoppingCart = False
    context = {
        'book': book,
        'isInShoppingCart': isInShoppingCart,
    }
    return render(request, 'details.html', context)


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Redirect to the login page after successful registration
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def handle_form_submission(request, book_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_to_cart':
            book = Book.objects.get(id=book_id)
            quantity = int(request.POST.get('quantity', 1))
            format = request.POST.get('format', 'physical')
            cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            return redirect('/cart')

        elif action == 'add_to_favourites':
            book = Book.objects.get(id=book_id)
            Favourite.objects.get_or_create(user=request.user, book=book)
            return redirect('/favourites')


def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_price = 0
    for item in cart_items:
        item.total_price = item.quantity * item.book.price
        total_price += item.total_price

    return render(request, 'cart.html', {'cart_items': cart_items, "total": total_price})


def favourites(request):
    books_ids = Favourite.objects.filter(user=request.user).values_list('book', flat=True)
    books = Book.objects.filter(id__in=books_ids)
    return render(request, 'favourites.html', {"books": books})


def place_order(request):
    user = request.user
    delivery_info = None

    try:
        delivery_info = DeliveryInfo.objects.get(user=user)
        initial_data = {
            'name': delivery_info.name,
            'surname': delivery_info.surname,
            'address': delivery_info.address,
            'city': delivery_info.city,
            'country': delivery_info.country,
            'phone': delivery_info.phone,
        }
    except DeliveryInfo.DoesNotExist:
        initial_data = {}

    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            if delivery_info:
                delivery_info.name = form.cleaned_data['name']
                delivery_info.surname = form.cleaned_data['surname']
                delivery_info.address = form.cleaned_data['address']
                delivery_info.city = form.cleaned_data['city']
                delivery_info.country = form.cleaned_data['country']
                delivery_info.phone = form.cleaned_data['phone']
                delivery_info.save()
            else:
                delivery_info = DeliveryInfo.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    surname=form.cleaned_data['surname'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    country=form.cleaned_data['country'],
                    phone=form.cleaned_data['phone']
                )

            cart_items = Cart.objects.filter(user=user)
            total_price = 0
            for item in cart_items:
                item.total_price = item.quantity * item.book.price
                total_price += item.total_price

            order = Order.objects.create(
                user=user,
                delivery_info=delivery_info,
                total_price=total_price
            )
            return redirect('/confirmed')
    else:
        form = DeliveryInfoForm(initial=initial_data)

    return render(request, 'deliveryinfo.html', {'form': form})


def confirmed(request):
    Cart.objects.filter(user=request.user).delete()
    return render(request, 'confirm.html')


def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')


def filter_books(request):
    selected_author = request.GET.get('author')
    selected_category = request.GET.get('category')
    authors = Author.objects.all()[:6]
    categories = Category.objects.all()[:6]

    books = Book.objects.all()

    if selected_author:
        books = books.filter(author=selected_author)

    if selected_category:
        books = books.filter(category=selected_category)

    context = {"books": books, "authors": authors, "categories": categories}
    return render(request, 'index.html', context)


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            if 'image' not in request.FILES:  # No new photo uploaded
                form.fields['image'].required = False
            form.save()
            # Redirect to the book details page or any other appropriate URL
            return redirect('book_details', book_id=book_id)
        else:
            print(form.errors)
    else:

        form = BookForm(instance=book)

    return redirect('book_details', book_id=book_id)


def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the book details page or any other appropriate URL
            return redirect('book_details', book_id=form.instance.id)
    else:
        form = AddBookForm()

    return render(request, 'addBook.html', {'form': form})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    # Redirect to the book list page or any other appropriate URL
    return redirect('/')
