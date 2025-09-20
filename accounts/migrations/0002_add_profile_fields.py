# Generated manually for user profile fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nationality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='degree',
            field=models.CharField(blank=True, help_text="e.g., Bachelor's, Master's", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='major',
            field=models.CharField(blank=True, help_text='Field of study', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='university',
            field=models.CharField(blank=True, help_text='University name', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='graduation_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gpa',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='GPA out of 4.0', max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='current_position',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='work_experience_years',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='relevant_experience',
            field=models.TextField(blank=True, help_text='Internships, projects, skills', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.TextField(blank=True, help_text='Academic and professional interests', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='languages_spoken',
            field=models.TextField(blank=True, help_text='Languages you speak', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_profile',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='portfolio_website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_countries',
            field=models.TextField(blank=True, help_text='Countries of interest for studies', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='budget_range',
            field=models.CharField(blank=True, help_text='Budget range for studies', max_length=50, null=True),
        ),
    ]
