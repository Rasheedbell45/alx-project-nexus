from django.db import migrations
from django.contrib.postgres.indexes import GinIndex

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),  # adjust based on your latest migration
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=GinIndex(fields=['description'], name='product_description_gin'),
        ),
    ]
