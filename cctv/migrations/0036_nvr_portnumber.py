from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cctv', '0035_remove_nvr_sno'),
    ]

    operations = [
        migrations.AddField(
            model_name='nvr',
            name='portNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
