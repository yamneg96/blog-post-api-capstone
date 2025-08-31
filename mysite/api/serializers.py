from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Category, Tag

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
        read_only_fields = ("id", "slug")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")
        read_only_fields = ("id", "slug")


class PostSerializer(serializers.ModelSerializer):
    # Author is read-only: always set by the backend (request.user)
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(required=False, allow_null=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "content",
            "author",
            "category",
            "tags",
            "published_date",
            "is_published",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at", "author")

    def create_or_get_category(self, category_data):
        if not category_data:
            return None
        obj, _ = Category.objects.get_or_create(name=category_data.get("name"))
        return obj

    def create_or_get_tags(self, tags_data):
        tag_objs = []
        for tag in tags_data or []:
            obj, _ = Tag.objects.get_or_create(name=tag.get("name"))
            tag_objs.append(obj)
        return tag_objs

    def create(self, validated_data):
        category_data = validated_data.pop("category", None)
        tags_data = validated_data.pop("tags", None)

        category = self.create_or_get_category(category_data)
        post = Post.objects.create(category=category, **validated_data)

        tag_objs = self.create_or_get_tags(tags_data)
        if tag_objs:
            post.tags.set(tag_objs)
        return post

    def update(self, instance, validated_data):
        category_data = validated_data.pop("category", None)
        tags_data = validated_data.pop("tags", None)

        if category_data is not None:
            instance.category = self.create_or_get_category(category_data)

        if tags_data is not None:
            tag_objs = self.create_or_get_tags(tags_data)
            instance.tags.set(tag_objs)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
