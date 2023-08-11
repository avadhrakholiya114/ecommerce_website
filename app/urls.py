from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('detail/<id>', views.detail),

    # authentication urls
    path('register/', views.register),
    path('login_user/', views.login_user),
    path('Logout_user/', views.Logout_user),

    # profile
    path('profile/', views.profile),
    path('address/', views.address),
    path('update/<id>', views.update),

    # add to cart
    path('addtocart/<id>', views.addtocart, name="addtocart"),
    path('show_cart/', views.show_cart, name="cart"),
    path('pluscart/', views.pluscart, name="pluscart"),
    path('minuscart/', views.minuscart, name="minuscart"),
    path('removecart/', views.removecart, name="removecart"),

    # checkout
    path('checkout/', views.checkout, name="checkout"),

    # chekcout when we click on paymet then page redirect to the payment done
    path('paymentdone/', views.paymentdone, name="paymentdone"),
    path('order/', views.order, name="order"),

    # invoice
    path('invoice/', views.invoice, name="invoice"),

]
