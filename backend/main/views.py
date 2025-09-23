from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . serializer import PostSerializer
from . models import Posts

# Create your views here.
class PostListView(generics.ListAPIView):
    queryset=Posts.objects.all()
    serializer_class=PostSerializer




