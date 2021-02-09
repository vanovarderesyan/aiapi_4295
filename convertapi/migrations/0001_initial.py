# Generated by Django 3.0.7 on 2021-02-08 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Convert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(blank=True, choices=[('start', 'start'), ('failed', 'failed'), ('completed', 'completed')], max_length=30, null=True)),
                ('file_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_rel', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
