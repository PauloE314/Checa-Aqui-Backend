from rest_framework import serializers
from reviews.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        exclude = ('like_users', )
        extra_kwargs = {
            'store': {'write_only': True},
        }

    formated_store = serializers.SerializerMethodField()
    

    def get_formated_store(self, review):
        formated_store = [review.store, review.get_store_display()]
        return formated_store

    def to_representation(self, instance):
        representation = super(ReviewSerializer, self).to_representation(instance)
        representation['author'] = self.get_user(instance)

        return representation
    
    def get_user(self, instance):
        author = instance.author
        serializer_author = UserSerializer(author)
        return serializer_author.data



class ReviewSerializer_WithoutAuthorData(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        exclude = ('like_users', )
        extra_kwargs = {
            'store': {'write_only': True},
            'author': {'write_only': True}
        }

    formated_store = serializers.SerializerMethodField()

    def get_formated_store(self, review):
        formated_store = [review.store, review.get_store_display()]
        return formated_store