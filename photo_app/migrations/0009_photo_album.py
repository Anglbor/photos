# Generated by Django 4.0.2 on 2023-03-05 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0008_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='photo_app.album'),
        ),
    ]