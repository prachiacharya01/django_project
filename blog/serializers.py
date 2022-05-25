from rest_framework import serializers
from .models import Post,comment
from django.contrib.auth.models import User

class UserSerialser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class PostSerializer(serializers.ModelSerializer):
    likes = UserSerialser(many = True, read_only = True)
    class Meta:
        model = Post
        fields = ['id','title','content','date','author','likes']

class commentSerilaizer(serializers.ModelSerializer):
    commentor  = UserSerialser(read_only = True)
    class Meta:
        model = comment
        fields = ['id','post','timestamp','describ','commentor']

