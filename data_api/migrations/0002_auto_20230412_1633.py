# Generated by Django 3.2.18 on 2023-04-12 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdata',
            name='server_num',
            field=models.CharField(default=False, max_length=20),
        ),
        migrations.AddField(
            model_name='taskdata',
            name='time_info',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='taskdata',
            name='run',
            field=models.CharField(default=False, max_length=20),
        ),
    ]