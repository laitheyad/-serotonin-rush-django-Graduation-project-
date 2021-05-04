from django.conf import settings
from django.db import models


# Create your models here.
class User(models.Model):
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    avatar = models.ImageField(blank=True, null=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    status_selection = [
        ('Customer', 'Customer'),
        ('Nutritionist', 'Nutritionist')
    ]
    status = models.CharField(choices=status_selection, default='Customer', max_length=20)

    def __str__(self):
        return u'{} {} || status: {}'.format(self.first_name, self.last_name, self.status)


class Meal(models.Model):
    name = models.CharField(max_length=250)
    fats = models.FloatField()
    protein = models.FloatField()
    carbohydrate = models.FloatField()
    calories = models.FloatField()
    recipe = models.TextField()
    status_selection = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    ]
    status = models.CharField(max_length=8, default='Pending', choices=status_selection)

    def __str__(self):
        return u' meal id : {}, meal name : {} '.format(self.pk, self.name)


class UserReaction(models.Model):
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    reaction = models.IntegerField()

    def __str__(self):
        return u'username : {}, date : {}, meal : {}, reaction {}'.format(self.user.username, self.date, self.meal,
                                                                          self.reaction)


class News(models.Model):
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=250)
    url = models.CharField(max_length=150)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title
