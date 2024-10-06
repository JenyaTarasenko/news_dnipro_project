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
    path('category/<slug:category_slug>/', views.category_news_detail, name='detail_category'),#детальная информация категории
    # path('registration/', views.register_view, name='registration'),#регистрация пользователя
    # path('search/<slug:category_slug>', views.news_search, name='search_news'),
]


