from django.db import models
from django.db.models import Q

# Create your models here.
class Posts(models.Model):
    post_id=models.IntegerField(null=True,unique=True)
    ranking=models.IntegerField()
    source=models.CharField(max_length=200)
    title=models.CharField(max_length=500)
    title_url=models.URLField()

    

    def __str__(self):
        return self.title
    
    def lt(self,**kwargs):
        for k,v in kwargs.items():
            q_object=Q(**{f"{k}__lt":v})
        return self.objects.filter(q_object)
    
class SubText(models.Model):
    author=models.ForeignKey(Posts,related_name='post',on_delete=models.CASCADE)
    writer=models.CharField(max_length=200)
    points=models.IntegerField()
    time=models.DateTimeField()
    comments=models.IntegerField(null=True)
