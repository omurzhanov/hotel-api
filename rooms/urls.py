from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rooms.views import RoomsViewSet, LikeView, RatingViewSet, AddReviewView, SaveView, UserSavedView, GetSaversView

router = DefaultRouter()
router.register('', RoomsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:id>/', LikeView.as_view(), name='like'),
    path('rate/<int:id>/', RatingViewSet.as_view(), name='rate'),
    path('review/<int:room_id>/', AddReviewView.as_view(), name='add-comment'),
    path('save/<int:id>/', SaveView.as_view(), name='save'),
    path('<int:id>/get-savers/', GetSaversView.as_view(), name='get-savers'),
    path('saved/', UserSavedView.as_view(), name='saved'),
]