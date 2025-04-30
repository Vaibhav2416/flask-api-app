from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("products/", views.show_products, name="show_products"),
    path("products/add/", views.add_product, name="add_product"),
]
