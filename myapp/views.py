from django.shortcuts import render
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.parsers import JSONParser
import json
from rest_framework import status
from rest_framework import status
from django.http import JsonResponse
from .models import TrainStop, Station
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, TicketBooked
from .serializers import UserSerializer
from datetime import datetime
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from myapp.models import User
from myapp.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import time
import sqlite3
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .serializers import StationSerializer
from .serializers import TrainStopSerializer
from .serializers import TrainSerializer
from .serializers import TrainStopSerializer
from .serializers import TicketBookedSerializer
from .models import User, Station
from .serializers import UserSerializer, StationSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from .models import *
import uuid
from datetime import datetime
from datetime import datetime
from django.db import transaction
from django.http import JsonResponse
from .models import User, TicketBooked
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Train, TrainStop
from .serializers import TrainSerializer, TrainStopSerializer
from django.db.models import Count
from django.db.models.functions import Coalesce

# Add User -------------------------------------------------------------
@api_view(["GET", "POST"])
def add_user(request):
    if request.method == "GET":
        return render(request, 'adduser.html')
    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('add-user')  # Redirect to the adduser.html page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Add Station  -------------------------------------------------------------


@api_view(["POST"])
def add_station(request):
    if request.method == "POST":
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Add Train  -------------------------------------------------------------
    
@api_view(["POST"])
def add_train(request):
    if request.method == "POST":
        train_data = request.data.copy()
        stops_data = train_data.pop("stops", [])

       
        if stops_data:
            first_stop_departure_time = stops_data[0]["departure_time"]
            last_stop_arrival_time = stops_data[-1]["arrival_time"]
            num_stations = len(stops_data)

            train_data["service_start"] = first_stop_departure_time
            train_data["service_ends"] = last_stop_arrival_time
            train_data["num_stations"] = num_stations
        else:
           
            train_data["service_start"] = "00:00"
            train_data["service_ends"] = "23:59"
            train_data["num_stations"] = 0

        train_serializer = TrainSerializer(data=train_data)
        if train_serializer.is_valid():
            train_instance = train_serializer.save()

            for stop_data in stops_data:
                station_id = stop_data.pop("station_id", None)
                if station_id is not None:
                    station_instance, created = Station.objects.get_or_create(
                        station_id=station_id
                    )

                    stop_data["train"] = train_instance.pk
                    stop_data["station"] = station_instance.pk

                    stop_serializer = TrainStopSerializer(data=stop_data)
                    if stop_serializer.is_valid():
                        stop_serializer.save()
                    else:
                        return Response(
                            stop_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {"station_id": ["This field is required."]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(train_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(train_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get Station  -------------------------------------------------------------


@api_view(["GET"])
def get_stations(request):
    if request.method == "GET":
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)


# fetch_trains_by_statio  -------------------------------------------------------------


@api_view(["GET"])
def fetch_trains_by_station(request, station_id):
    try:
        station = get_object_or_404(Station, station_id=station_id)
        trains = TrainStop.objects.filter(station_id=station_id).order_by(
            "departure_time", "arrival_time", "train_id"
        )

        trains_list = []
        for train in trains:
            trains_list.append(
                {
                    "train_id": train.train_id,
                    "arrival_time": train.arrival_time,
                    "departure_time": train.departure_time,
                }
            )

        response_data = {"station_id": station_id, "trains": trains_list}

        return JsonResponse(response_data, status=200)

    except Station.DoesNotExist:
        return JsonResponse(
            {"message": f"station with id: {station_id} was not found"}, status=404
        )


# recharge_wallet_balance  -------------------------------------------------------------


@api_view(["GET", "POST"])
def recharge_wallet_balance(request, wallet_id):
    if request.method == "GET":
        try:
            user = User.objects.get(user_id=wallet_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"message": f"Wallet with id: {wallet_id} was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    elif request.method == "POST":
        amount = request.data.get("recharge")
        if amount is None:
            return Response(
                {"message": "Please provide a recharge amount."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount < 100:
            return Response(
                {"message": "Recharge amount cannot be less than 100 taka."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount > 10000:
            return Response(
                {"message": "Recharge amount cannot exceed 10,000 taka."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(user_id=wallet_id)
            current_balance = user.balance
            new_balance = current_balance + amount
            user.balance = new_balance
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"message": f"Wallet with id: {wallet_id} was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        












def generate_ticket_id():
    unique_id = uuid.uuid4().hex[:6]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"TICKET-{timestamp}-{unique_id}"


@api_view(["POST"])
def purchase_ticket(request):
    if request.method == "POST":
        data = request.data
        wallet_id = data.get("wallet_id")
        time_after = data.get("time_after")
        station_from = data.get("station_from")
        station_to = data.get("station_to")

        try:
            user = User.objects.get(user_id=wallet_id)
            balance = user.balance
            ticket_cost = 1000

            if balance < ticket_cost:
                insufficient = ticket_cost - balance
                return Response(
                    {
                        "message": f"Recharge amount: {insufficient} insufficient to purchase the ticket"
                    },
                    status=status.HTTP_402_PAYMENT_REQUIRED,
                )

            ticket_id = generate_ticket_id()

            with transaction.atomic():
                user.balance -= ticket_cost
                user.save()
                TicketBooked.objects.create(
                    ticket_id=ticket_id, timestamp=datetime.now(), user=user
                )

            response_data = {
                "ticket_id": ticket_id,
                "wallet_id": wallet_id,
                "balance": user.balance,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response(
                {"message": f"Wallet with id: {wallet_id} was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
