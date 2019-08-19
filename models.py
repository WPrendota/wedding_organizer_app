from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.admin import User
from datetime import datetime


class Wedding(models.Model):
    hall_name = models.CharField("Hall name: ", max_length=40)
    date = models.DateField(("Date: "), default=datetime.today)
    city = models.CharField("City: ", max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.hall_name


class Table(models.Model):
    number = models.IntegerField("Number: ")
    max_size = models.IntegerField("Max. number of seats: ")
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Wedding hall: " + str(self.wedding) + ", Table number: " + str(self.number)


class Guest(models.Model):
    title_choices = (("Mrs", "Mrs."), ("Mr", "Mr."))
    family_side_choices = (("Bride", "Bride"), ("Groom", "Groom"))

    title = models.CharField("Title: ", choices=title_choices, max_length=40)
    first_name = models.CharField("First Name: ", max_length=40)
    second_name = models.CharField("Second Name: ", max_length=40)
    family_side = models.CharField("Family Side: ", choices=family_side_choices, max_length=40)
    chair_number = models.IntegerField("Chair number: ")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.second_name
