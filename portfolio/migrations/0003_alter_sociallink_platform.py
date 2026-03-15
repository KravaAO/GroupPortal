from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sociallink",
            name="platform",
            field=models.CharField(
                choices=[
                    ("twitch", "Twitch"),
                    ("youtube", "YouTube"),
                    ("facebook", "Facebook"),
                    ("twitter", "Twitter / X"),
                    ("instagram", "Instagram"),
                    ("discord", "Discord"),
                    ("github", "GitHub"),
                ],
                max_length=20,
            ),
        ),
    ]
