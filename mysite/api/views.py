from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostListCreate(generics.ListCreateAPIView):
  queryset = BlogPost.objects.all() #Getting all the blog post models.
  serializer_class = BlogPostSerializer #Specifying the serializer class to convert the model instances to JSON.

  def delete(self, request, *args, **kwargs):
    BlogPost.objects.all().delete() # Delete all blog posts
    return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
  queryset = BlogPost.objects.all()
  serializer_class = BlogPostSerializer
  lookup_field = 'pk' #Specifying the field to look up the instance.
# We use the django rest_framework views to use the generics.

