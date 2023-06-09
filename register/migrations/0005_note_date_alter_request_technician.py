# Generated by Django 4.1.6 on 2023-04-13 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technicianRequest', to=settings.AUTH_USER_MODEL),
        ),
    ]
