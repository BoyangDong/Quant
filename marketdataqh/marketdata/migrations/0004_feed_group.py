# Generated by Django 2.0.2 on 2018-04-20 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketdata', '0003_auto_20180419_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketdata.IGMPSnoopingGroup'),
        ),
    ]