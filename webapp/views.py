from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def about_page(request):
    return render(request, 'pages/about.html')

def login_page(request):
    return render(request, 'pages/login.html')

def services_page(request):
    return render(request, 'pages/services.html')

def contacts_page(request):
    return render(request, 'pages/contacts.html')

def dashboard_page(request):
    products = Product.objects.all()
    context = {'product': products}
    return render(request, 'pages/dashboard.html', context)

    

@login_required(login_url='login')
def cart_page(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # If UserProfile does not exist, create it
        user_profile = UserProfile.objects.create(user=request.user)

    order, created = Order.objects.get_or_create(user_profile=user_profile, is_complete=False)
    items = order.orderitem_set.all()

    context = {'items': items, 'order': order}
    return render(request, 'pages/cart.html', context)

def checkout_page(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        order, created = Order.objects.get_or_create(user_profile=user_profile, is_complete=False)
        items = order.orderitem_set.all()

        if request.method == 'POST':
            # Handle form submission
            name = request.POST.get('name')
            email = request.POST.get('email')

            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            country = request.POST.get('country')

            shipping_address = ShippingAddress(
                user=request.user,
                order=order,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            shipping_address.save()

            # Update order details if needed
            order.is_complete = True
            order.transaction_id = 'your_transaction_id'  # You can generate a unique transaction ID
            order.save()

            return redirect('payment')  # Redirect to the payment page or any other relevant page

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'pages/checkout.html', context)

def updateproduct(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    user_profile = request.user.userprofile
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user_profile=user_profile, is_complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    response_data = {'message': 'Item was added'}
    return JsonResponse(response_data, safe=False)


@login_required(login_url='login')
def update_cart_item(request, product_id):
    user_profile = request.user.userprofile
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user_profile=user_profile, is_complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('new_quantity', 1))

        if new_quantity > 0:
            order_item.quantity = new_quantity
            order_item.save()
        else:
            order_item.delete()

    return redirect('cart')


@login_required(login_url='login')
def delete_cart_item(request, product_id):
    user_profile = request.user.userprofile
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user_profile=user_profile, is_complete=False)
    order_item = OrderItem.objects.get(order=order, product=product)
    order_item.delete()

    return redirect('cart')
    
def payment_view(request):
    return render(request, 'pages/payment.html', {'payment_status': 'success'})

def process_payment(request):
    return render(request, 'pages/process_payment.html', {'payment_status': 'success'})

from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            
            UserProfile.objects.create(user=user)

            login(request, user)
            success(request, 'Registration successful. You are now logged in.')
            return redirect('dashboard')  
    else:
        form = UserRegistrationForm()

    return render(request, 'pages/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = UserLoginForm()
    return render(request, 'pages/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')  # Add a success message for logout
    return redirect('pages/login.html')