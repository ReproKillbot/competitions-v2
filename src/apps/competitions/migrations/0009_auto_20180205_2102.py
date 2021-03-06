# Generated by Django 2.0.1 on 2018-02-05 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competitions', '0008_auto_20180130_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='description',
            field=models.CharField(blank=True, default='', max_length=240, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='submission', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
