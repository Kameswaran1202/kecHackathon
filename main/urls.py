from django.urls import path
from django.shortcuts import render
from main import views

urlpatterns = [
    path('', views.home, name="home"),
    path('newpost', views.newpost, name="newpost"),
    path('blog/<slug:slug>/', views.viewpost, name="viewpost"),
    path('my-private-post', views.allmyprivatepost, name="allmyprivatepost"),
    path('my-public-post', views.allmypublicpost, name="allmypublicpost"),
    path('make-public-private/<slug:slug>', views.makepublicprivate, name="makepublicprivate"),
    path('delete-post/<slug:slug>', views.deletePost, name="deletepost"),
    path("follow_unfollow/<str:username>/", views.follow_unfollow, name="follow_unfollow"),
    path("like_unlike/<slug:slug>", views.like_unlinked, name="like_unlinked"),
    path('search/', views.search, name="search"),
    path('validateReport/', views.validateReport, name="validateReport"),
    path('ban-user/<slug:slug>', views.banUser, name="banUser"),
    path('delete-article/<slug:slug>', views.deleteArticle, name="deleteArticle"),
    path('ignore-report/<slug:slug>', views.ignoreReport, name="ignoreReport"),
    path('report/<slug:slug>/<int:id>', views.reportPost, name="reportPost"),
    path('more/highlight/', views.moreh, name="moreh"),
    path('more/official/', views.moreo, name="moreo"),
    path('more/others/', views.more, name="more"),
    path('postcomment/<slug:slug>', views.postcomment, name="postcomment"),
]

def custom_404(request, exception):
    return render(request, 'error.html')

# url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
# re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 