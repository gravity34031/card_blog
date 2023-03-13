from django.urls import path, include
from rest_framework.routers import DefaultRouter




urlpatterns = None
app_name = 'something'
from .views import \
PostBlogViewSet, PostNewsViewSet, AddViewsToPostBlogView, \
TagViewList, TagsViewList, DeleteTagView, \
AsideBlogViewList, AsideNewsViewList, \
AddFavouritePostView, \
GetCommentsView, CommentsView, CommentsUserView, \
SearchPostsForReviewView, ReviewView, ReviewUserView, \
UserRegisterView, UserProfileView, UserChangePasswordView, \
ContactView, \
GalleryViewSet, \
GetAddPhotosView, GetUpdDelPhotoView
#GetGalleriesView, GetGalleryView, \
router = DefaultRouter()
router.register('blog_posts', PostBlogViewSet, basename='blog_posts')
router.register('news_posts', PostNewsViewSet, basename='news_posts')
router.register('gallery', GalleryViewSet, basename='gallery')


urlpatterns = [
    path('', include(router.urls)),
    path('view/<slug:slug>/', AddViewsToPostBlogView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('change_password/', UserChangePasswordView.as_view()),
    path('tags/', TagsViewList.as_view()),
    path('tags/<slug:tag_slug>/', TagViewList.as_view()),
    path('tag_del/<slug:slug>/', DeleteTagView.as_view()),
    path('aside-blog/', AsideBlogViewList.as_view()),
    path('aside-news/', AsideNewsViewList.as_view()),
    path('favourite/', AddFavouritePostView.as_view()),
    path('get_comments/', GetCommentsView.as_view()),
    path('comments/', CommentsView.as_view()),
    path('profile/comments/', CommentsUserView.as_view()),
    path('profile/review/', ReviewUserView.as_view()),
    path('review/', ReviewView.as_view()),
    path('search_blog_review/', SearchPostsForReviewView.as_view()),
    path('contact/', ContactView.as_view()),

    #path('gallery/', GetGalleriesView.as_view()),
    #path('gallery/<slug:slug>/', GetGalleryView.as_view()),
    path('photo/', GetAddPhotosView.as_view()),
    path('photo/<slug:slug>/', GetUpdDelPhotoView.as_view()),
]
