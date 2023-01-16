from django.db import models
from django.contrib.auth.models import User, AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from photologue.models import Gallery
from core.ru_taggit import RuTaggedItem
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.contrib.auth.models import AbstractUser
#from django.db.models.signals import post_save
#from django.dispatch import receiver

#from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
#from django.contrib.contenttypes.models import ContentType
# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

""" @receiver(post_save, sender=User)
def create_user_useravatar(sender, instance, created, **kwargs):
    if created:
        UserAvatar.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_useravatar(sender, instance, **kwargs):
    instance.profile.save() """



class PostBlog(models.Model):
    h1 = models.CharField(max_length=100) # card header
    title= models.CharField(max_length=50) # title in admin & post header
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200) # card description
    content = RichTextUploadingField()
    price = models.IntegerField()
    images = models.OneToOneField(Gallery, on_delete=models.CASCADE, verbose_name='Галерея') # carousel images
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    favourite = models.ManyToManyField(User, related_name='favourite', verbose_name='Избранное', blank=True)
    tags = TaggableManager(through=RuTaggedItem, verbose_name='Теги')

    def __str__(self):
        return self.title

    #def save(self, *args, **kwargs):
    #    self.slug = slugify(self.title)
    #    super(PostBlog, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Работы'
        ordering = ['-created_at']



class PostNews(models.Model):
    h1 = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200)
    #image = models.ImageField(max_length=200, upload_to='news_posts/',blank=True)
    image = ResizedImageField(force_format='WEBP', quality=70, max_length=200, blank=True, upload_to='news_posts/')
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']



class Comments(models.Model):
    post_blog = models.ForeignKey(PostBlog, on_delete=models.CASCADE, related_name='post_blog', blank=True, null=True, default=None)
    post_news = models.ForeignKey(PostNews, on_delete=models.CASCADE, related_name='post_news', blank=True, null=True, default=None)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')   
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарии'
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.content



class Review(models.Model):
    product = models.ForeignKey(PostBlog, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=200)
    grade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    is_anonymous = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.comment
