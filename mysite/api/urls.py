from django.urls import path
from . import views

urlpatterns = [
    path('blogposts/', 
    views.BlogPostListCreate.as_view(), 
    name='blogpost-view-create'),

    path('blogposts/<int:pk>/', 
         views.BlogPostRetrieveUpdateDestroy.as_view(), 
         name="update")
]


# Before running the server, We : (anytime we touch the model(create or update))
# 1. Create a migration : python manage.py makemigrations
# This create a file that will specify what migrations need to be applied.
# 2. Apply the migration : python manage.py migrate
# This will apply the migrations.


# The Docker file specifies how we run our application and 
# The Acorn file all of the services and additional configurations we need.