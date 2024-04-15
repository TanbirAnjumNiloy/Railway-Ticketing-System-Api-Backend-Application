from rest_framework import serializers
from .models import User
from .models import Station, Train, TrainStop, TicketBooked


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "balance"]

    def validate_balance(self, value):
        if value > 10000:
            raise serializers.ValidationError("Balance cannot exceed 10,000.")
        elif value < 100:
            raise serializers.ValidationError("Balance cannot be less than 100.")
        return value


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["station_id", "station_name", "longitude", "latitude"]


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            "train_id",
            "train_name",
            "capacity",
            "service_start",
            "service_ends",
            "num_stations",
        ]


class TrainStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainStop
        fields = [
            "train_stop_id",
            "train",
            "station",
            "arrival_time",
            "departure_time",
            "fare",
        ]
        extra_kwargs = {"station": {"required": False}}


class TicketBookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketBooked
        fields = ["ticket_id", "timestamp", "user"]
