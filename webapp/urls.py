from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home,
    about_page,
    login_page,
    services_page,
    contacts_page,
    dashboard_page,
    cart_page,
    checkout_page,
    updateproduct,
    update_cart_item,
    delete_cart_item,
    payment_view,
    process_payment,
    register,  
    user_login, 
   

)

urlpatterns = [
    path('', home, name='home_page'),
    path('about/', about_page, name='aboutpage'),
    path('login/', login_page, name='login_page'),
    path('services/', services_page, name='servicespage'),
    path('contacts/', contacts_page, name='contactpage'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('cart/', cart_page, name='cart'),
    path('checkout/', checkout_page, name='checkout'),
    path('update_product/', updateproduct, name='update_product'),
    path('update_cart_item/<int:product_id>/', update_cart_item, name='update_cart_item'),
    path('delete_cart_item/<int:product_id>/', delete_cart_item, name='delete_cart_item'),
    path('payment/', payment_view, name='payment'),
    path('process_payment/', process_payment, name='process_payment'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('user_login/', user_login, name='user_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    

]
