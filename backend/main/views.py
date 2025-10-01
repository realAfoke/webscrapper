from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . serializer import PostSerializer
from . models import Posts
from django.db.models import Q

# Create your views here.

class SearchPost(generics.ListAPIView):
    queryset=Posts.objects.all()
    serializer_class=PostSerializer
    def get_queryset(self):
        data=dict(self.request.query_params)
        q_object=Q()
        for k,v in data.items():
            if k in ['page','page_size','ordering']:
                continue
            q_object |=Q(**{f"{k}__icontains":v[0]})
        return super().get_queryset().filter(q_object).order_by('ranking')

class PostListView(SearchPost):
    pass

