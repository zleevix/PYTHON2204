from django.urls import re_path, path
from django.contrib.auth import views as auth_views
from . import views, user_views

urlpatterns = [
    re_path(r"^$", views.index, name='index'),
    re_path(r"^product/(?P<product_id>[0-9]+)$", views.view_product, name="view_product"),
    re_path(r"^add/(?P<product_id>[0-9]+)$", views.add_product_to_cart , name="add_product_to_cart"),
    # re_path(r"^change/(?P<action>[a-z]+)/(?P<product_id>[0-9]+)$", views.add_product_to_cart , name="add_product_to_cart"),
    path("change/<str:action>/<int:product_id>", views.change_product_quantity, name="change_product_quantity"),
    re_path(r"^delete/(?P<product_id>[0-9]+)$", views.delete_product_in_cart , name="delete_product_in_cart"),
    re_path(r"^show-cart$", views.show_cart, name="show_cart"),
    re_path(r"^checkout$", views.checkout, name="checkout"),
    
    re_path(r"^user/register$",user_views.register_user, name='register_user'),
    re_path(r"^user/login$",user_views.login_user, name='login_user'),
    re_path(r"^user/logout$", auth_views.LogoutView.as_view(next_page='/'), name='logout_user'),
    re_path(r"^user/validate$", user_views.validate_username, name='validate_username'),
]