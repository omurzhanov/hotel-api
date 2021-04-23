from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rooms.views import RoomsViewSet, LikeView, RatingViewSet, AddReviewView

router = DefaultRouter()
router.register('', RoomsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:id>/', LikeView.as_view(), name='like'),
    path('rate/<int:id>/', RatingViewSet.as_view(), name='rate-post'),
    path('review/<int:room_id>/', AddReviewView.as_view(), name='add-comment'),
]