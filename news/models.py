from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta


class Category(models.Model):
    """
    Категории на которые делится новости
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name



class  News(models.Model):
    """
    новости
    """

    class Status(models.TextChoices):
        """
        класс Status подклассирован
        выводит опубликована ли новость
        """
        DRAFT = 'DF', 'Daft'
        PUBLISHED = 'pb', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')#уникальные дата и время для вывода слагов статтей
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.DRAFT)

    @classmethod
    def get_news_of_the_week(cls, count=5):
        """
        метод новости недели
        """
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23,  minutes=59, seconds=59)
        return cls.objects.filter(pub_date__range=[start_of_week, end_of_week])[:count]

    @classmethod
    def get_top_news(cls, count=5):
        return cls.objects.order_by('-rating')[:count]




    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),
                   ]# Указанная опция по- зволяет определять в модели индексы базы данных,



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug]

                       )
    def get_related_news(self):
        """
        метод выводит похожие с категориями новости
        """
        return News.objects.filter(categories__in=self.categories.all().exclude(pk=self.pk).distinct())






