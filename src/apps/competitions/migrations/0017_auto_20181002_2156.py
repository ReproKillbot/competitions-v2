# Generated by Django 2.1 on 2018-10-02 21:56

from django.db import migrations, models
import django.db.models.deletion
import utils.data


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0016_auto_20181002_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('data_file', models.FileField(upload_to=utils.data.PathWrapper('submission_details'))),
            ],
        ),
        migrations.RemoveField(
            model_name='submission',
            name='track',
        ),
        migrations.AddField(
            model_name='submission',
            name='api_key',
            field=models.UUIDField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='result',
            field=models.FileField(default=None, upload_to=utils.data.PathWrapper('submission_result')),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submissiondetails',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='competitions.Submission'),
        ),
    ]
