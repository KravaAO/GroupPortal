from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Calendar event',
                'verbose_name_plural': 'Calendar events',
                'ordering': ['date', 'start_time', 'title'],
            },
        ),
    ]
