from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(TrainStop)
admin.site.register(TicketBooked)

