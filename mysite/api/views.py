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


# A custome API would be like this : (if we don't want to inherit the generic ones.)
# and import like : from rest_framework.views import APIView
# Then : 
# class BlogPostList(APIView):
#   def get(self, request, format=None):
#     title = request.query_params.get('title', '')
      
#     if title: 
#       blog_posts = BlogPost.objects.filter(title__icontains=title)
#     else:
#       blog_posts = BlogPost.objects.all()
#     serializer = BlogPostSerializer(blog_posts, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
