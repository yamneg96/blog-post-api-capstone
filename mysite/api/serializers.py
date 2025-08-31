# We specify a class that takes the model and converts it to a JSON format.
from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
  class Meta:
    model = BlogPost
    flields = ['id', 'title', 'content', 'published_date']
    read_only_fields = ['id', 'published_date']
    exclude = []