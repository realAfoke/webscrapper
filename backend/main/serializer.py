from rest_framework import serializers
from .models import Posts,SubText
from datetime import datetime,timedelta

class SubTextSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubText
        fields="__all__"

class PostSerializer(serializers.ModelSerializer):
    post=SubTextSerializer(many=True,read_only=True)
    time=serializers.SerializerMethodField()

    class Meta:
        model=Posts
        fields=['id','ranking','source','title','title_url','post','time']
    
    def get_time(self,obj):
        sub=obj.post.order_by('-time').first()
        str_date=datetime.fromisoformat(str(sub.time)).replace(tzinfo=None)
        str_date=str_date - timedelta(hours=24)
        diff=datetime.now() - str_date
        hours,remainder=divmod(int(diff.total_seconds()),3600)
        minute,_=divmod(remainder,60)
        if hours > 24:
            time=f"{hours//24} days ago"
        else:
            time=f"{hours} hours,{minute} minute ago"
        return time if sub else None
    




