from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, permissions, generics, status, pagination, filters
from rest_framework.views import APIView
from .serializers import \
    PostBlogSerializer, AddPostBlogSerializer, UpdPostBlogSerializer,\
    PostNewsSerializer, \
    TagSerializer, \
    GetCommentsSerializer, CommentsSerializer, \
    GetReviewSerializer, PostReviewSerializer, \
    UserRegisterSerializer, UserProfileSerializer, UserChangePasswordSerializer, \
    ContactSerializer, \
    GetGallerySerializer, AddGallerySerializer, UpdGallerySerializer, \
    PhotosSerializer, PhotoSerializer
from .models import PostBlog, PostNews, Comments, Review
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.core.mail import send_mail
from photologue.models import Gallery, Photo


from .permissions import IsAdminOrReadOnly

from django.core.files import File
import io
import os
from .image_management import COLORS, create_avatar, delete_avatar

# Create your views here.


class PostBlogSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = max(page_size, len(PostBlog.objects.all()))

class NewsSetPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = max(page_size, len(PostNews.objects.all()))



""" class GetGalleriesView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GetGallerySerializer
    permission_classes = [permissions.AllowAny]
class GetGalleryView(generics.RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GetGallerySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
class AddGalleryView(generics.CreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GetGallerySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly] """
class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.prefetch_related('photos').all()
    serializer_class = GetGallerySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request):
        data = request.data
        serializer = AddGallerySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, slug=None):
        data = request.data
        instance = Gallery.objects.get(slug=slug)
        serializer = UpdGallerySerializer(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



class GetAddPhotosView(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotosSerializer
    permission_classes = [IsAdminOrReadOnly]
class GetUpdDelPhotoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image.close()
        image = str(instance.image)
        compressed_image = image.split('.')[0] + '_compressed.webp'
        self.perform_destroy(instance)
        #os.remove(settings.MEDIA_URL[1:] + image)
        os.remove(settings.MEDIA_URL[1:] + compressed_image)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class PostBlogViewSet(viewsets.ModelViewSet):
    queryset = PostBlog.objects.select_related('images', 'author').prefetch_related('favourite', 'tags').all()
    serializer_class = PostBlogSerializer
    lookup_field = 'slug'
    pagination_class = PostBlogSetPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['h1', 'title', 'description', 'content']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        sorting_type = request.query_params.get("sorted")
        ordered_queryset = queryset

        if sorting_type == 'new':
            ordered_queryset = queryset.order_by('-created_at')
        elif sorting_type == 'most_liked':
            ordered_queryset = PostBlog.objects \
            .annotate(favourites_count=Count('favourite')) \
            .order_by("-favourites_count", "-created_at")
        elif sorting_type == 'most_viewed':
            ordered_queryset = queryset.order_by('-views', '-created_at')

        page = self.paginate_queryset(ordered_queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            data = serializer.data
            return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        serializer = AddPostBlogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug=None, *args, **kwargs):
        instance = PostBlog.objects.get(slug=slug)
        data = request.data
        serializer = UpdPostBlogSerializer(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    """ def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = post.views + 1
        post.save(update_fields=['views',])

        serializer = self.get_serializer(post)
        return Response(serializer.data, status=200) """

class AddViewsToPostBlogView(generics.GenericAPIView):
    queryset = PostBlog.objects.all()
    serializer_class = PostBlogSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = post.views + 1
        post.save(update_fields=['views',])

        serializer = self.get_serializer(post)
        return Response(serializer.data, status=200)



class SearchPostsForReviewView(generics.ListAPIView):
    queryset = PostBlog.objects.select_related('author', 'images').prefetch_related('tags', 'favourite').all()
    serializer_class = PostBlogSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'title', 'h1']


"""     def update(self, request, *args, **kwargs):
        post = self.get_object()        
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data) """


class PostNewsViewSet(viewsets.ModelViewSet):
    queryset = PostNews.objects.select_related('author').all()
    serializer_class = PostNewsSerializer
    lookup_field = 'slug'
    pagination_class = NewsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['h1', 'title', 'description', 'content']
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image = ''
        if instance.image:
            image = str(instance.image)
        self.perform_destroy(instance)
        if image:
            os.remove(settings.MEDIA_URL[1:] + image)
        return Response(status=status.HTTP_204_NO_CONTENT)




class TagViewList(generics.ListAPIView):
    queryset = PostBlog.objects.all()
    serializer_class = PostBlogSerializer
    pagination_class = PostBlogSetPagination
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        sorting_type = request.query_params.get("sorted")
        ordered_queryset = queryset

        if sorting_type == 'new':
            ordered_queryset = queryset.order_by('-created_at')
        elif sorting_type == 'most_liked':
            ordered_queryset = PostBlog.objects \
            .annotate(favourites_count=Count('favourite')) \
            .order_by("-favourites_count", "-created_at")
        elif sorting_type == 'most_viewed':
            ordered_queryset = queryset.order_by('-views', '-created_at')

        page = self.paginate_queryset(ordered_queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            data = serializer.data
            return self.get_paginated_response(data)

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return PostBlog.objects.filter(tags=tag)


class DeleteTagView(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser]

""" def delete(self, request):
        post = get_object_or_404(PostBlog, slug = request.data.get('slug'))
        if request.user in post.favourite.all():
            post.favourite.remove(request.user)
            return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Уже удален'}, status=status.HTTP_400_BAD_REQUEST)
         """
class TagsViewList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]



class AsideBlogViewList(generics.ListAPIView):
    queryset = PostBlog.objects.all().order_by('-created_at')[:3]
    serializer_class = PostBlogSerializer
    permission_classes = [permissions.AllowAny]



class AsideNewsViewList(generics.ListAPIView):
    queryset = PostNews.objects.select_related('author').all().order_by('-created_at')[:3]
    serializer_class = PostNewsSerializer
    permission_classes = [permissions.AllowAny]



class AddFavouritePostView(APIView):
    serializer_class = PostBlogSerializer
    queryset = PostBlog.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        post = get_object_or_404(PostBlog, slug=request.data.get('slug'))
        if request.user not in post.favourite.all():
            post.favourite.add(request.user)
            return Response({'detail': 'User added to post'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Уже поставлен'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post = get_object_or_404(PostBlog, slug = request.data.get('slug'))
        if request.user in post.favourite.all():
            post.favourite.remove(request.user)
            return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Уже удален'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = PostBlog.objects.filter(favourite=request.user).select_related('images', 'author').prefetch_related('favourite', 'tags')
        serializer = PostBlogSerializer(posts, many=True)

        return Response(serializer.data)



""" class IsFavouriteView(APIView):
    queryset = PostBlog.objects.all()

    def get(self, request):
        data = request.data.get('slug', '')
        current_username = request.user.username
        post = PostBlog.objects.get(slug=data)
        for i in post.favourite.all():
            if current_username in i.username:
                return Response(True)
        return Response(False) """


class GetCommentsView(APIView):
    serializer_class = GetCommentsSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        blog_or_news = request.data.get('post')
        if blog_or_news == 'blog':
            post = get_object_or_404(PostBlog, slug=request.data.get('slug'))
            comments = Comments.objects.filter(post_blog = post).select_related('post_blog__images', 'post_news', 'author')
        elif blog_or_news == 'news':
            post = get_object_or_404(PostNews, slug=request.data.get('slug'))
            comments = Comments.objects.filter(post_news = post).select_related('post_blog__images', 'post_news', 'author')
        else:
            return Response({'detail': 'Ошибка. Данной модели поста не существует'})
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)


class CommentsView(APIView):
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    """ def get(self, request):
        blog_or_news = request.data.get('post')
        if blog_or_news == 'blog':
            post = get_object_or_404(PostBlog, slug=request.data.get('slug'))
            comments = Comments.objects.filter(post_blog = post)
        elif blog_or_news == 'news':
            post = get_object_or_404(PostNews, slug=request.data.get('slug'))
            comments = Comments.objects.filter(post_news = post)
        else:
            return Response({'detail': 'Ошибка. Данной модели поста не существует'})
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data) """

    
    def post(self, request):
        data = request.data
        current_username = request.user.username

        if 'author' not in data:
            data['author'] = current_username
        
        error = self.validate_data_or_error(data, current_username)
        if error:
            return Response({'detail': error})
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def put(self, request):
        data = request.data
        current_user = request.user
        current_username = current_user.username
        instance = Comments.objects.get(id=data['id'])

        if 'post_news' in data or 'post_blog' in data:
            return Response({'detail': 'Нельзя изменить пост комментария'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            post_blog = instance.post_blog
            post_news = instance.post_news
            if post_blog:
                data['post_blog'] = post_blog.slug
            elif post_news:
                data['post_news'] = post_news.slug

        if 'created_at' in data:
            return Response({'detail': 'Нельзя изменить дату создания комментария'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['created_at'] = instance.created_at

        if 'author' in data:
            if data['author'] != current_username:
                return Response({'detail': 'Нельзя оставить комментарий за другого пользователя'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['author'] = current_username
        if current_user != instance.author:
            return Response({'detail': 'Нельзя оставить комментарий за другого пользователя'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def delete(self, request, *args, **kwargs):
        data = request.data
        current_user = request.user
        current_username = current_user.username
        errorUser = 'Ошибка. Неверный пользователь'
        try:
            if data['author'] != current_username:
                return Response({'detail': errorUser}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        comments = get_object_or_404(Comments, id=data['id'])
        if (comments.author == current_user) or current_user.is_superuser:
            comments.delete()
            return Response({'detail': 'Запись успешно удалена'})
        return Response({'detail': errorUser}, status=status.HTTP_400_BAD_REQUEST)
        


    def validate_data_or_error(self, data, current_username):
        error = False
        try:
            if data['author'] != current_username:
                error = 'Ошибка. Неверный пользователь'
                return error
        except:
            pass

        if 'post_news' not in data and 'post_blog' not in data:
            error = 'Ошибка. В заголовке нет поста'
            return error
        try:
            if data['post_news'] and data['post_blog']:
                error = 'Ошибка. Нельзя опубликовать (удалить) комментарий сразу на две модели поста.'
                return error
        except:
            pass
        return error      



class CommentsUserView(generics.ListAPIView):
    serializer_class = GetCommentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-post_blog', '-post_news']

    def get_queryset(self):
        user = self.request.user
        comments = Comments.objects.filter(author=user).select_related('post_blog__images', 'post_news', 'author')
        return comments



class ReviewUserView(generics.ListAPIView):
    serializer_class = GetReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        review = Review.objects.filter(user=user).select_related('product__images', 'user')
        return review



class ReviewView(APIView):
    serializer_class = PostReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return Review.objects.select_related('product__images', 'user').all()
        
    def get(self, request):
        review = self.get_queryset()
        serializer = GetReviewSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        current_user = request.user
        if 'user' in data:
            if data['user'] != current_user.username:
                return Response({'detail': 'Ошибка. Можно оставить отзыв только со своего профиля'})
        else:
            data['user'] = current_user.username
        if 'first_name' not in data:
            if current_user.first_name:
                data['first_name'] = current_user.first_name
        if 'email' not in data:
            if current_user.email:
                data['email'] = current_user.email

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def put(self, request):
        data = request.data
        current_username = request.user.username
        
        if 'id' in data:
            review = get_object_or_404(Review, id=data['id'])
        else:
            return Response({'detail': 'Ошибка, нет id'})

        if 'user' in data:
            if data['user'] != current_username:
                return Response({'detail': 'Ошибка. Нельзя оставить отзыв с чужого профиля'})
        else:
            data['user'] = current_username

        if 'created_at' in data:
            return Response({'detail': 'Ошибка. Нельзя поменять дату отзыва'})
        serializer = self.serializer_class(data=data, instance=review)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        data = request.data
        current_user = request.user
        current_username = current_user.username

        if 'author' in data:
            return Response({'detail': 'Ошибка. Нельзя удалять чужие отзывы'})
        else:
            review = get_object_or_404(Review, id=data['id'])
            if review.user.username == current_username or current_user.is_superuser:
                review.delete()

                return Response({'detail': 'Запись успешно удалена'})
            else:
                return Response({'detail': 'Ошибка. Нельзя удалять чужие отзывы'})



class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data

        if 'first_name' in data:  
            if data['first_name']:
                msg = data['first_name'][0].upper()
            else:
                msg = 'N'
        else:
            msg = 'N'
        avatar_path = create_avatar(msg)

        avatar = open(avatar_path, 'rb')
        data['avatar'] = File(avatar)

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            # delete temp avatar that was needed to add img to database
            # etherwise there are two images
            
            delete_avatar(avatar_path, avatar)

            return Response(
                {'user': serializer.data,},
                status=status.HTTP_200_OK
                )

        
        avatar_error = delete_avatar(avatar_path, avatar)
        errors = serializer.errors
        if avatar_error:
            errors['avatar'] = avatar_error
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)




class UserProfileView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        data = request.data
        user = request.user
        old_avatar = str(user.avatar)
        instance = user
        serializer = self.get_serializer(data=data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if 'avatar' in data:
                try:
                    os.remove(settings.MEDIA_URL[1:] + old_avatar)
                except:
                    pass
            return Response({
                'user': serializer.data
            })
        else:
            return Response({
                'detail': 'Ошибка'
            })

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({
            'user': serializer.data
        })

    def delete(self, request):
        user = request.user
        avatar = str(user.avatar)
        user.delete()
        os.remove(settings.MEDIA_URL[1:] + avatar)
        return Response({'detail': 'Пользователь успешно удален'})



class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "Пароль успешно изменен!"}, status=status.HTTP_200_OK)



class ContactView(APIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['gravity2507@gmail.com'])
            return Response({'detail': 'Письмо успешно отправлено'})



""" class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST) """



""" class GetFavouritePostView(generics.ListAPIView):
    serializer_class = PostBlogSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.favourite.all().order_by('-id') """





