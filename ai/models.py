from django.db import models


# results in a table with the structure
# | id | user_id | name | email |
# |----|---------|------|-------|

# Create your models here.
class AICore(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, )
    name = models.CharField(max_length=100)
    email = models.EmailField()

# Once you've defined the model (above) and you've configured the database connection in settings.py (defaults to sqlite3
# and nothing needs to be done) you can run the following commands to create the database
# python manage.py makemigrations

# create a row in the table
# new_user = AICore.objects.create(name='John Doe', email='john@email.com')
# new_user.save()

# get all rows in the table
# all_users = AICore.objects.all()

# get a specific row in the table
# user = AICore.objects.get(id=1)


# 