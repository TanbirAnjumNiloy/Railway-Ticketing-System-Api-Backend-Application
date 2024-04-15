from django.contrib import admin
from django.urls import path
from myapp import views
from django.urls import path
from myapp import views
from myapp.views import user_list
from myapp.views import add_user
from .views import user_list


from django.urls import path
from .views import (
    add_user,
    add_station,
    add_train,
    get_stations,
    fetch_trains_by_station,
    recharge_wallet_balance,
    recharge_wallet_balance,
    purchase_ticket,
)

urlpatterns = [
    # Add User ----------------------------------------------------------------
    path("adduser/", add_user, name="add-user"),
    # Add Station  ------------------------------------------------------------
    path("api/stations/", add_station, name="add-station"),
    # Add Train  --------------------------------------------------------------
    path("api/trains/", add_train, name="add-train"),
    # Get Station  ------------------------------------------------------------
    path("api/stations/all/", get_stations, name="get-stations"),
    ## fetch_trains_by_statio  -----------------------------------------------
    path("api/stations/<int:station_id>/trains/",fetch_trains_by_station,name="fetch-trains-by-station",),
    # recharge_wallet_balance  -------------------------------------------------------------
    path("api/wallets/<int:wallet_id>/",recharge_wallet_balance,name="recharge-wallet-balance",),
    
    path("api/tickets/", purchase_ticket, name="purchase-ticket"),
]
