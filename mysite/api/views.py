from django.shortcuts import render
from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostListCreate(generics.ListCreateAPIView):
  queryset = BlogPost.objects.all() #Getting all the blog post models.
  serializer_class = BlogPostSerializer #Specifying the serializer class to convert the model instances to JSON.

# We use the django rest_framework views to use the generics.

