# Generated by Django 3.2 on 2022-01-28 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autopost', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtoroUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='scheduledposts',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scheduledposts',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='etoro_user', to='autopost.etorouser'),
        ),
    ]
