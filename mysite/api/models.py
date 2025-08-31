from django.db import models

# ORM maps python objects to database instances.
class BlogPost(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  published_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title
