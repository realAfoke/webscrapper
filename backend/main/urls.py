from django.urls import path
from . import views

urlpatterns=[
    path('posts/',views.PostListView.as_view(),name='post-view'),
    # path('post/search')
]