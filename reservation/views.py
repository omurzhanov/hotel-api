from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import MyUser
from .serializers import GuestSerializer, ReservationSerializer
from.models import Reservation
@api_view(['GET','POST'])
def api_guest_list_view(request):
    guest = MyUser.objects.all()
    if request.method == 'GET':
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)
    if request.method =='POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','POST'])
def api_booking_list_view(request):
    reservations = Reservation.objects.all()
    print(reservations)
    if request.method =='GET':
        serializer = ReservationSerializer(reservations,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer=ReservationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(guest=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)