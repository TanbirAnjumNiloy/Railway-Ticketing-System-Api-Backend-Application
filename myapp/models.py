from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100)
    balance = models.IntegerField("")

    def __str__(self):
        return self.user_name


class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()


class Train(models.Model):
    train_id = models.IntegerField(primary_key=True)
    train_name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    service_start = models.CharField(max_length=255, default=0)
    service_ends = models.CharField(max_length=255, default=0)
    num_stations = models.IntegerField(default=0)


class TrainStop(models.Model):
    train_stop_id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival_time = models.CharField(max_length=100, null=True)
    departure_time = models.CharField(max_length=100, null=True)
    fare = models.IntegerField(null=True)


class TicketBooked(models.Model):
    ticket_id = models.CharField(primary_key=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_id
