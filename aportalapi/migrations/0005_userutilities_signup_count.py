from django.db import migrations, models


def count_current_signups(apps, schema_editor):
    # Past nights were cleared, so the only history left is whoever is on the sheet now
    UserUtilities = apps.get_model('aportalapi', 'UserUtilities')
    SignupSheet = apps.get_model('aportalapi', 'SignupSheet')
    signed_up = SignupSheet.objects.values_list('user_id', flat=True)
    UserUtilities.objects.filter(user_id__in=signed_up).update(signup_count=1)


class Migration(migrations.Migration):

    dependencies = [
        ('aportalapi', '0004_signupsheet_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='userutilities',
            name='signup_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(count_current_signups, migrations.RunPython.noop),
    ]
