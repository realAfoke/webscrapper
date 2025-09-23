from rest_framework import serializers
from .models import Posts,SubText

class SubTextSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubText
        fields="__all__"

class PostSerializer(serializers.ModelSerializer):
    post=SubTextSerializer(many=True,read_only=True)
    class Meta:
        model=Posts
        fields=['id','ranking','source','title','title_url','post']



