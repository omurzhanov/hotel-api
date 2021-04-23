from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework import serializers
from account.models import MyUser
from rooms.serializers import RoomSerializer
from .models import Reservation


class GuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email')


class ReservationSerializer(serializers.ModelSerializer):
    guest = GuestSerializer
    room = RoomSerializer

    class Meta:
        model = Reservation
        fields =('guest','room', 'no_of_guests','checkin_date','checkout_date','check_out','charge',)
        read_only_fields = ('guest', )
    def validate(self, attrs):
        guest = attrs.get('guest')
        checkin_date = attrs.get('checkin_date')
        checkout_date = attrs.get('checkout_date')
        room = attrs.get('room')
        reserved = Reservation.objects.filter(room=room)
        res = reserved.filter(Q(checkin_date__lte=checkin_date) & Q(checkout_date__gte=checkin_date) | Q(checkin_date__lte=checkout_date) & Q(checkout_date__gte=checkout_date))
        print(checkin_date)
        print(checkout_date)
        print(reserved.filter())
        if res:
            raise serializers.ValidationError('The room is already booked for these dates')
        else:
            return attrs
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['guest'] = instance.guest.email
        representation['room'] = instance.room.name
        return representation


