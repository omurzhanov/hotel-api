from django.db.models import Q
from rest_framework import generics, viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.serializers import GuestSerializer
from .serializers import RoomSerializer, RoomImageSerializer, RatingSerializer, ReviewSerializer, HostSerializer
from django.utils import timezone
from rooms.models import Room, RoomImage, Rating
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from .permissions import IsHost
from .pagination import RoomPagination, CommentPagination, RatingPagination


class RoomsViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsHost]
    pagination_class = RoomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(address__icontains=q) | Q(name__icontains=q) | Q(city__icontains=q))
        serializer = RoomSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)

    # filtering using queryset by the date
    @action(detail=False, methods=['get'])
    def recent(self, request, pk=None):
        queryset = self.queryset
        days_count = int(self.request.query_params.get('days', default=0))
        print(days_count)
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__lte=start_date)
        serializer = RoomSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # filtering by my posts using action decorator, url -> v1/api/rooms/own/
    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)


'''COMMENT POST --- POST, [text]'''


class AddReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, room_id=None):
        room = Room.objects.get(pk=room_id)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(room=room, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    pagination_class = RatingPagination

    def post(self, request, id=None):
        room = Room.objects.get(pk=id)
        user = self.request.user
        room_rating = Rating.objects.filter(room=room, user=user)
        if not room_rating:
            serializer = RatingSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(room=room, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('You have already rated this room', status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None, id=None):
        room = Room.objects.get(pk=id)
        user = self.request.user
        if user.is_authenticated:
            if user in room.likes.all():
                like = False
                room.likes.remove(user)
            else:
                like = True
                room.likes.add(user)
        data = {
            'like': like
        }
        return Response(data)


'''GET THE LIST OF SAVED ROOMS --- GET '''


class UserSavedView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        favorited = user.favs.all()
        queryset = Room.objects.all().filter(pk__in=favorited)
        return queryset


class SaveView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None, id=None):
        room = Room.objects.get(pk=id)
        user = self.request.user
        if user.is_authenticated:
            if user in room.favs.all():
                favorite = False
                room.favs.remove(user)
            else:
                favorite = True
                room.favs.add(user)
            data = {
                'saved': favorite
            }
            return Response(data)


'''GET THE LIST OF FAVORITERS --- GET '''

class GetSaversView(generics.ListAPIView):
    serializer_class = HostSerializer
    pagination_class = CommentPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs['id']
        queryset = Room.objects.get(
            pk=post_id).favs.all()
        return queryset


class RoomImageView(generics.ListCreateAPIView):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}
