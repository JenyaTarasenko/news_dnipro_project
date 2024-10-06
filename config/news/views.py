from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, News, Comment, UserProfile

from .forms import CommentForm, RegistrationForm, NewsSearchForm

from django.views.decorators.http import require_POST
from django.contrib.auth import login

from django.views.generic import View
from django.views.generic import CreateView




def list_view(request):
    """
    функция для отображения категорий и новостей
    """
    latest_news = News.objects.order_by('-pub_date').first()#первая новость
    news_page = News.objects.all()[:4]#новости 4последние
    new = News.objects.all()#все актуальные новости
    cat = Category.objects.all()#все актуальные категории
    week_news = News.get_news_of_the_week(count=4)#топ новостей за неделю
    top_news = News.get_top_news()#топ новости
    return render(request, 'news/post/list.html',
                  {'new': new,
                   'week_news': week_news,
                   'top_news': top_news,
                   'latest_news': latest_news,
                   'news_page ': news_page,
                   'cat': cat}
                  )





def detail_views(request, year, month,day, news):
    """
    детальная информация новости ,те которые публичны
    """
    new_detail = get_object_or_404(News,
                             status=News.Status.PUBLISHED,
                             slug=news,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    category_detail = new_detail.categories.all()#выводит все категории детально
    category_all = Category.objects.all()
    related_news = new_detail.get_related_news()#метод для вывода похожих ровостей по категории
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = new_detail
            new_comment.save()
            return redirect('news:news_detail', year=year, month=month, day=day, news=news)
    else:
        comment_form = CommentForm()
    comments = new_detail.comments.filter(active=True)

    return render(request, 'news/post/detail.html',
                  {'new_detail': new_detail,
                   'category_detail': category_detail,
                   'related_news': related_news,
                   'comments': comments,
                   'comment_form': comment_form,
                   'category_all': category_all}
                  )




def category_news_detail(request, category_slug):
    """
    детальная информация по связанным категориям
    """
    category = get_object_or_404(Category, slug=category_slug)
    news_list = News.objects.filter(categories=category)

    form = NewsSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        # Разбиваем введенную строку на слова
        search_words = search_query.split()

        # Для каждого слова добавляем фильтр
        for word in search_words:
            news_list = news_list.filter(title__icontains=word)

    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return redirect('news:list_view')
    else:
        user_form = RegistrationForm()
    return render(request, 'news/post/category_detail.html',
                  {'category': category, 'news_list': news_list, 'user_form': user_form, 'search_form': form}
                  )




@require_POST
def post_comment(request, news_id):
    """
    коментарии гостей
    """
    news = get_object_or_404(News, id=news_id,
                             status=News.Status.PUBLISHED)
    comment = None  #комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #создаем обьект Comment не сохраняя его в базе данных
        comment = form.save(commit=False)
        #назначить пост коментария
        comment.news = news
        comment.save()
    return render(request, 'news/post/comment.html',
                  {'news': news, 'form': form, 'comment': comment}
                  )


# @require_POST
# def post_comment(request, news_id):
#     news = get_object_or_404(News, id=news_id, status=News.Status.PUBLISHED)
#     comment = None
#     form = CommentForm(data=request.POST)
#     try:
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.news = news
#             comment.save()
#         else:
#             raise ValueError('Form is valid')
#     except ValueError as e:
#         print(f'Error:{e}')
#         print(form.errors)
#     return render(request, 'news/post/comment.html',
#                       {'news': news, 'form': form, 'comment': comment})

# def register_view(request):
#     """
#     Регистрация
#     """
#     if request.method == 'POST':
#         user_form = RegistrationForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             return redirect('news:list_view')
#     else:
#         user_form = RegistrationForm()
#
#     return render(request, 'news/post/registration/registration.html',
#                   {'user_form': user_form}
#                   )
# def news_search(request, category_slug):
#     """
#     Поиск по словам и заголовкам новсти
#     """
#     category = get_object_or_404(Category, slug=category_slug)
#     news_list =  News.objects.filter(categories=category)
#
#     form =NewsSearchForm(request.GET)
#     if form.is_valid():
#         search_query = form.cleaned_data['search_query']
#         # Разбиваем введенную строку на слова
#         news_words = search_query.split()
#
#         # Для каждого слова добавляем фильтр
#         for word in news_words:
#             news_list = news_list.filte(title__icontains=word)
#     return render(request,
#                   'news/post/page_1.html',
#                   {'category': category, 'news_list': news_list, 'form': form})

