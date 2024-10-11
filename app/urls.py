# app/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from quadros.views import PicturesListView, NewPictureView,PicDetailView, PicUpdateView, PicDeleteView 
from accounts.views import register_view, login_view  , logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("pictures/", PicturesListView.as_view(), name="pictures_list"),
    path('new_picture/', NewPictureView.as_view(), name='new_picture'),
    path("register/", register_view, name="register"),  
    path("login/", login_view, name='login'),     
    path("logout/", logout_view, name='logout'),
    path('pictures/<int:pk>/', PicDetailView.as_view(), name='pic_detail'),
    path('pictures/<int:pk>/update/', PicUpdateView.as_view(), name='pic_update'),
    path('pictures/<int:pk>/delete/', PicDeleteView.as_view(), name='pic_delete'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
