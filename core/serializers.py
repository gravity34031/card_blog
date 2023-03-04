from rest_framework import serializers
from .models import PostBlog, PostNews, Comments, Review
from .taggit_serializer import TagListSerializerField, TaggitSerializer
from taggit.models import Tag
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from photologue.models import Gallery, Photo, ImageModel
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
#from django.contrib.contenttypes.models import ContentType
from django_resized import ResizedImageField

#for image compress
from PIL import Image
import os
from datetime import datetime
from .image_management import compress_image

class FavouriteUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug')


# get, add photos
class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'id',
            'title',
            'slug',
            'image'
        )
    def create(self, validated_data):
        image = validated_data.get('image', '')
        
        if not image.name.isascii():
            now = datetime.now()
            time = str(now).replace(' ', '').replace(':', '')
            image.name = 'photologue/photos/' + time + '.jpg'
       
        photo = Photo.objects.create(
            image = image,
            title = validated_data.get('title', ''),
            slug = validated_data.get('slug', ''),
        )
        photo.save()

        #compress image & save
        img = Image.open(photo.image)
        image_name = str(photo.image) 
        img_path = settings.MEDIA_URL[1:] + image_name
        new_img_path = settings.MEDIA_URL[1:] + image_name[:image_name.rfind('.')] + '_compressed' + '.webp'
        compress_image(img, img_path, new_img_path)
        img.save(img_path, optimize=True) # optimize FULL image
        img.close()

        return photo


# update, delete, get instance of the photo 
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'id',
            'title',
            'slug',
            'image'
        )
        extra_kwargs = {
            'title': {'required': False},
            'slug': {'required': False}
        }

"""     def create(self, validated_data):

        photo = Photo.objects.create(
            image = validated_data.get('image', ''),
            title = validated_data.get('title', ''),
            slug = validated_data.get('slug', ''),
        )
        photo.save()
        return photo """


""" class PhotoForGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image',) """

class GetGallerySerializer(serializers.ModelSerializer):
    #photos = serializers.SlugRelatedField(many=True, slug_field='image', queryset=Photo.objects.all())
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Gallery
        fields = ('id', 'photos', 'title', 'slug', 'description')

class AddGallerySerializer(serializers.ModelSerializer):
    photos = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Photo.objects.all(), required=True)
    #photos = PhotoForGallerySerializer(many=True)
    class Meta:
        model = Gallery
        fields = ('id', 'photos', 'title', 'slug', 'description')

    def validate_photos(self, value):
        if not value:
            raise serializers.ValidationError('Поле photos не может быть пустым')
        return value

class UpdGallerySerializer(serializers.ModelSerializer):
    photos = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Photo.objects.all())
    class Meta:
        model = Gallery
        fields = ('id', 'photos', 'title', 'slug', 'description')
        extra_kwargs = {
            'title': {'required': False},
            'slug': {'required': False}
        }

    def validate_photos(self, value):
        if not value:
            raise serializers.ValidationError('Поле photos не может быть пустым')
        return value



class PostBlogSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    favourite = FavouriteUserSerializer(read_only=True, many=True)
    images = serializers.SlugRelatedField(slug_field='slug', queryset=Gallery.objects.all())
    #images = GallerySerializer()

    class Meta:
        model = PostBlog
        fields = (
            'id',
            'h1',
            'title',
            'slug',
            'description',
            'images',
            'content',
            'price',
            'created_at',
            'author',
            'views',
            'favourite',
            'tags'
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'slug': {'required': False}
        }

class AddPostBlogSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=True)
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    favourite = FavouriteUserSerializer(read_only=True, many=True)
    images = serializers.SlugRelatedField(slug_field='slug', queryset=Gallery.objects.all())
    #images = GallerySerializer()

    class Meta:
        model = PostBlog
        fields = (
            'id',
            'h1',
            'title',
            'slug',
            'description',
            'images',
            'content',
            'price',
            'created_at',
            'author',
            'views',
            'favourite',
            'tags'
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'slug': {'required': False}
        }

class UpdPostBlogSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)
    favourite = FavouriteUserSerializer(read_only=True, many=True)
    images = serializers.SlugRelatedField(slug_field='slug', queryset=Gallery.objects.all(), required=False)
    #images = GallerySerializer()

    class Meta:
        model = PostBlog
        fields = (
            'id',
            'h1',
            'title',
            'slug',
            'description',
            'images',
            'content',
            'price',
            'created_at',
            'author',
            'views',
            'favourite',
            'tags'
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'h1': {'required': False},
            'title': {'required': False},
            'slug': {'required': False},
            'description': {'required': False},
            'images': {'required': False},
            'content': {'required': False},
            'price': {'required': False},
            'created_at': {'read_only': True},
            'views': {'read_only': True},
        }



class PostNewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = PostNews
        fields = (
            'id',
            'h1',
            'title',
            'slug',
            'image',
            'description',
            'content',
            'created_at',
            'author'
        )
    def update(self, instance, validated_data):
        old_image = ''
        new_image = ''
        if instance.image:
            old_image = instance.image
        if 'image' in validated_data:
            new_image = validated_data['image']
        instance.h1 = validated_data.get('h1', instance.h1)
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        if old_image and new_image:
            os.remove(settings.MEDIA_URL[1:] + str(old_image))
        return instance



class UserRegisterSerializer(serializers.ModelSerializer):
    """ email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            ) """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'password2',
            'avatar'
        )
        extra_kwargs = {
            'first_name': {'max_length': 15},
            'last_name': {'max_length': 25},
            'username': {'max_length': 30}
        }

    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            username = validated_data['username'],
            avatar = validated_data.get('avatar', '')
        )

        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'detail': 'Ошибка. Пароли не совпадают'})
        user.set_password(password)
        user.save()

        return user



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'avatar',
            'is_superuser'
        )
        extra_kwargs = {
            'username': {'read_only': True, 'max_length': 30},
            'is_superuser': {'read_only': True},
            "date_joined": {'read_only': True},
            'first_name': {'max_length': 15},
            'last_name': {'max_length': 25}
        }

    def put(self, instance, validated_data):
        
        user = User.objects.get(instance)
        user.objects.update(
            first_name = validated_data.get('first_name', instance.first_name),
            last_name = validated_data.get('last_name', instance.last_name),
            email = validated_data.get('email', instance.email),
            avatar = validated_data.get('avatar', instance.avatar),
            username = user.username,
            is_superuser = user.is_superuser
        )
        user.save()
        return user



class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Введен неправильный текущий пароль')
        return value
        
    def validate(self, data):
        old_password = data['old_password']
        password = data['new_password']
        password2 = data['new_password2']
        if old_password == password:
            raise serializers.ValidationError('Новый пароль не может совпадать со старым')
        if password != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        validate_password(password, self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user



class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=50)
    email = serializers.EmailField(max_length=200)
    subject = serializers.CharField(min_length=4)
    message = serializers.CharField(min_length=6)



class PostBlogForCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBlog
        fields = ('title', 'slug', 'id')

class PostNewsForCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostNews
        fields = ('title', 'slug', 'id')

class GetCommentsSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    post_blog = PostBlogForCommentSerializer()
    post_news = PostNewsForCommentSerializer()
    #post_blog = serializers.SlugRelatedField(slug_field='slug', queryset=PostBlog.objects.all(), default=None)
    #post_news = serializers.SlugRelatedField(slug_field='slug', queryset=PostNews.objects.all(), default=None)

    class Meta:
        model = Comments
        fields = '__all__'



class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    post_blog = serializers.SlugRelatedField(slug_field='slug', queryset=PostBlog.objects.all(), default=None)
    post_news = serializers.SlugRelatedField(slug_field='slug', queryset=PostNews.objects.all(), default=None)

    class Meta:
        model = Comments
        fields = '__all__'
        


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(slug_field='slug', queryset=Gallery.objects.all())

    class Meta:
        model = PostBlog
        fields = (
            'id',
            'title',
            'slug',
            'images',
        )

class GetReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserProfileSerializer()

    class Meta:
        model = Review
        fields = '__all__'

class PostReviewSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=PostBlog.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())


    class Meta:
        model = Review
        fields = '__all__'



""" class GallerySerializer(serializers.ModelSerializer):
    #photos = serializers.StringRelatedField(many=True)
    photos = serializers.SlugRelatedField(many=True,slug_field='img_path', queryset=Photo.objects.all())

    class Meta:
        model = Gallery
        fields = ('photos',) """