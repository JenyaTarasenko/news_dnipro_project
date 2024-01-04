from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'news'



urlpatterns = [
    path('', views.list_view, name='list_view'),#первая страница
    path('<int:year>/<int:month>/<int:day>/<slug:news>/', views.detail_views, name='news_detail'),#детальная информация
    # path('category/<int:category_id>/', views.detail_category, name='category_posts'),
    # path('news/<int:year>/<int:month>/<int:day>/<slug:news>/', views.post_comment, name='post_comment'),#коментарии
    path('comment/<int:news_id>/', views.post_comment, name='post_comment'),
    path('register/', views.register, name='register'),#регистрация пользователя
]


