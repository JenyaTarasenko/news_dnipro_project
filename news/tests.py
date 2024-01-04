from django.test import TestCase
from django.urls import reverse
from .models import Comment, News, Category
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.utils import timezone
from django.test import SimpleTestCase
from .forms import CommentForm

class NewsModelTesr(TestCase):
    def create_news(self, title="Test News", status=News.Status.DRAFT):
        return News.objects.create(title=title, status=status)

    def test_news_creation(self):
        news = self.create_news()
        self.assertTrue(isinstance(news, News))
        self.assertEqual(news.__str__(),news.title)


    def test_news_default_values(self):
        news = self.create_news()
        self.assertEqual(news.rating, 0)
        self.assertEqual(news.status, news.Status.DRAFT)
        self.assertIsNotNone(news.pub_date)

class CommentModelTest(TestCase):
    def create_news(self, title='Test News', status=News.Status.DRAFT):
        return News.objects.create(title=title, status=status)

    def create_comments(self, post, name='Test User', email='test@test.com', text="Test comment"):
        return Comment.objects.create(post=post, name=name, email=email, text=text)


    def test_comment_creation(self):
        news = self.create_news()
        comment = self.create_comments(news)
        self.assertTrue(isinstance(comment, Comment))
        # self.assertEqual(comment.__str__(), f"Comment by {comment.name} on {comment.text}")


class CaregoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Test Category', slug='test-slug')
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), 'Test Category')



class PostCommentView(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            title='Test News',
            body='Test news',
            status=News.Status.PUBLISHED
        )

    def test_post_comment_view(self):
        response = self.client.post(
            reverse('news:post_comment', args=[self.news.id,]),
            {'name': 'Test User', 'email':  'test@test.com', 'text': 'Test comment'}
        )
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.news, self.news)



class RegistrationFormTest(TestCase):
    def test_registration_form_valid_data(self):
        form_data = {
            'username': 'test user',
            'email': 'test@test.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_registration_form_invalid_data(self):
        form_data = {
            'username': '',
            'email': 'invalid_email',
            'password1': 'testpassword123',
            'password2': 'no_password',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertIn('password2', form.errors)


