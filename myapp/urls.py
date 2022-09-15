from django.urls import re_path, path # Django phiên bản nhơ 4.0 là url
# Từ 4.0 đổi thành re_path
# Import view mới viết vào.
# from views import my_view
from django.contrib.auth import views as auth_views
from . import views, class_views, user_views
# from .views import my_view
app_name = 'myapp'
urlpatterns = [
    re_path(r"^$", views.index, name='index'),
    re_path(r"^pet/add$", views.add_pet, name='add_pet'),
    re_path(r"^pet/view/(?P<pet_id>[\w]+)$", views.detail_pet, name="detail_pet"), 
    # path("update/<str:pet_id>", views.update_pet, name='update_pet'),
    re_path(r"^pet/update/(?P<pet_id>[\w]+)$", views.update_pet, name="update_pet"), 
    re_path(r"^pet/delete/(?P<pet_id>[\w]+)$", views.delete_pet, name="delete_pet"), 

    re_path(r"^class$", class_views.PetListView.as_view(), name='class_index'),
    re_path(r"^class/add$", class_views.PetCreateView.as_view(), name='class_add_pet'),
    re_path(r"^class/view/(?P<pk>[\w]+)$", class_views.PetDetailView.as_view(), name='class_detail_pet'),
    re_path(r"^class/update/(?P<pk>[\w]+)$", class_views.PetUpdateView.as_view(), name='class_update_pet'),
    re_path(r"^class/delete/(?P<pk>[\w]+)$", class_views.PetDeleteView.as_view(), name='class_delete_pet'),
    
    re_path(r"^user/register$",user_views.register_user, name='register_user'),
    re_path(r"^user/login$",user_views.login_user, name='login_user'),
    re_path(r"^user/logout$", auth_views.LogoutView.as_view(next_page='/'), name='logout_user'),
    re_path(r"^user/change$", user_views.change_password, name='change_password'),
    re_path(r"^user/validate$", user_views.validate_username, name='validate_username'),
]