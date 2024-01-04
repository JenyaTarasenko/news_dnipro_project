from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, News, Comment

from .forms import CommentForm, RegistrationForm, UserProfileForm

from django.views.decorators.http import require_POST
from django.contrib.auth import login



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
                   'cat': cat})





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
    related_news = new_detail.get_related_news()#метод для вывода похожих ровостей по категории
    comments = new_detail.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'news/post/detail.html',
                  {'new_detail': new_detail,
                   'category_detail': category_detail,
                   'related_news': related_news,
                   'comments': comments,
                   'form': form}
                  )




def detail_category(request, category_id):
    """
      детальная информация категорий вывод новостей по категории
      """
    category = Category.objects.get(pk=category_id)
    posts = category.news_set.all()
    return render(request, 'post/category_posts.html',
                  {'posts': posts})


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




def register(request):
    """
    Регистрация
    """
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('news/post/list.html')

        else:
            user_form = RegistrationForm()
            profile_form = UserProfileForm()

        return render(request, 'news/post/registration.html',
                      {'user_form': user_form,
                       'profile_form': profile_form}
                      )

