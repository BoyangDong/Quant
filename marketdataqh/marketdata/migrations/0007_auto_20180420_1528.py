# Generated by Django 2.0.2 on 2018-04-20 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketdata', '0006_auto_20180420_1527'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='accessrecord',
            unique_together={('interface', 'multicastGroup', 'created')},
        ),
    ]