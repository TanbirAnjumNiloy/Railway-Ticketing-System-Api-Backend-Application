# Generated by Django 4.2.10 on 2024-02-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_station_train_trainstop_ticketbooked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketbooked',
            name='ticket_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ticketbooked',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]