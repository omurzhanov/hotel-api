from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.core.paginator import Paginator
from django.db.models import Avg

class HostSerializer(serializers.ModelSerializer):
    """Serializer for object author info"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'avatar')


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the comment objects"""
    user = HostSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'comment', 'created_at')
        read_only_fields = ('user', 'id', 'created_at')


class RoomSerializer(serializers.ModelSerializer):
    host = HostSerializer(read_only=True)
    liked_by_req_user = serializers.SerializerMethodField()
    rated_by_req_user = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField('paginated_room_ratings')
    number_of_reviews = serializers.SerializerMethodField()
    room_reviews = serializers.SerializerMethodField('paginated_room_reviews')

    class Meta:
        model = Room
        fields = ('id', 'host', 'name', 'address', 'city', 'price', 'beds', 'bedrooms', 'bathrooms', 'created_at', 'is_available', 'number_of_likes','liked_by_req_user', 'number_of_reviews',
                  'room_reviews', 'rated_by_req_user', 'average_rating', 'rating')


    def get_number_of_reviews(self, obj):
        return Review.objects.filter(room=obj).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = RoomImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representation

    def get_liked_by_req_user(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()

    def get_average_rating(self, obj):
        rating = obj.room_ratings.all().aggregate(Avg('rating')).get('rating__avg')
        return rating

    def paginated_room_ratings(self, obj):
        page_size = 10
        paginator = Paginator(obj.room_ratings.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1

        room_ratings = paginator.page(page)
        serializer = RatingSerializer(room_ratings, many=True)

        return serializer.data

    def paginated_room_reviews(self, obj):
        page_size = 5
        paginator = Paginator(obj.room_reviews.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1

        room_reviews = paginator.page(page)
        serializer = ReviewSerializer(room_reviews, many=True)
        return serializer.data

    def get_rated_by_req_user(self, obj):
        user = self.context['request'].user
        print(obj)
        rating = Rating.objects.filter(room=obj, user=user)
        if rating:
            return True
        else:
            return False


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'rating')
        read_only_fields = ('user',)
        ordering = ['-rating', ]

    def validate_user(self, obj):
        user = self.context['request'].user
        print(user)
        if user in obj.ratings:
            raise serializers.ValidationError('You have already rated the post')
        return obj

    def validate(self, attrs):
        rating = attrs.get('rating')
        if rating > 5:
            raise serializers.ValidationError('The value must not exceed 5')
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['rating'] = instance.rating
        return representation


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation