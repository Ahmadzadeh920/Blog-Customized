from django.utils import timezone
from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):

    # this update field equals with timezone.now()
    updated_date = serializers.DateTimeField(default=timezone.now)

    # the fields snippet
    snippet = serializers.ReadOnlyField(source="get_snippet")
    # this fields for relative Urls
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)

    # this fields for obsolute  URLs
    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.id)

    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = Post

        fields = [
            "id",
            "author",
            "title",
            "snippet",
            "body",
            "category",
            "status",
            "updated_date",
            "relative_url",
            "absolute_url",
            "img",
        ]
        read_only_fields = ["author"]

    # this function overwrite
    # if you want some fileds is different in some urls, overwriting to_representation function is one solution
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("body", None)
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}
        ).data

        return rep

    # this function for retrive data from others models such as profile
    # this function values the author with request.user
    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
