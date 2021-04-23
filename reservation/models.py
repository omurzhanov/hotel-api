from django.db import models
from rooms.models import Room
from account.models import MyUser
from datetime import datetime, timedelta, date
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    print(date.today())
    guest = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reservations')
    checkin_date = models.DateField(default=date.today())
    checkout_date = models.DateField(default=date.today() + timedelta(days=1))
    # default=datetime.now() + timedelta(days=1))
    check_out = models.BooleanField(default=False)
    no_of_guests = models.IntegerField(default=1)
    # charge = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return self.guest.email

    def charge(self):
        if self.check_out:
            if self.checkin_date == self.checkout_date:
                return self.room.price
                # self.charge = self.room.price
            else:
                time_delta = self.checkout_date - self.checkin_date
                total_time = time_delta.days
                total_cost = total_time*self.room.price
                return total_cost
                # self.charge = total_cost
        else:
            return 'calculated when checked out'


@receiver(post_save, sender=Reservation)
def RType(sender, instance, created, **kwargs):
    room = instance.room
    if created:
        room.is_available = False
    room.save()
    if instance.check_out ==True:
        room.is_available = True
    room.save()