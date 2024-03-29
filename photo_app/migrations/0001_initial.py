# Generated by Django 4.1.2 on 2022-10-21 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='blank', max_length=256)),
                ('photo', models.ImageField(upload_to='photos')),
                ('take_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='photo_app.photo')),
                ('album_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='photo_app.photo')),
                ('camera_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=256)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo_app.photo')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(choices=[(1, 'Warsaw'), (2, 'London'), (3, 'Gdansk'), (4, 'Krakow'), (5, 'Berlin'), (6, 'Madrit')], max_length=256)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo_app.photo')),
            ],
        ),
    ]
