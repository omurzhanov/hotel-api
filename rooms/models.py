from django.contrib.auth.models import User
from django.db import models
from account.models import MyUser

class Room(models.Model):
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    city = models.CharField(max_length=100)
    price = models.IntegerField(help_text="USD per night")
    beds = models.IntegerField(default=1)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    instant_book = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="rooms"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    favs = models.ManyToManyField(MyUser, related_name="favs", blank=True)
    likes = models.ManyToManyField(MyUser, related_name='likes', blank=True)

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']

class RoomImage(models.Model):
    image = models.ImageField(upload_to='rooms', blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')


class Review(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=1, related_name='room_reviews')
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}'s comment:{self.comment}"


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_ratings')
    rating = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['rating', ]

    def __str__(self):
        return str(self.room)+"---"+str(self.user)