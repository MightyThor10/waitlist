# Generated by Django 4.2 on 2023-04-27 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_studentprofile_delete_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messaging', '0002_alter_message_send_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.AddField(
            model_name='message',
            name='professor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='professor_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='student_messages', to='users.studentprofile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='parent_msg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_messages', to='messaging.message', verbose_name='Replied to'),
        ),
    ]
