from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Make(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)

    class Meta:
        db_table = "make"

    def __str__(self):
        return self.name


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    make = models.ForeignKey('Make', on_delete=models.CASCADE, related_name='models')

    class Meta:
        db_table = "model"

    def __str__(self):
        return f"{self.make} {self.name}"


class Trim(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    model = models.ForeignKey('Model', on_delete=models.CASCADE, related_name='trims')

    class Meta:
        db_table = "trim"

    def __str__(self):
        return f"{self.model} {self.name}"


class Car(models.Model):
    WHITE = 'WHITE'
    BLACK = 'BLACK'
    SILVER = 'SILVER'
    BLUE = 'BLUE'
    RED = 'RED'
    COLOR_CHOICES = [
        (WHITE, 'WHITE'),
        (BLACK, 'BLACK'),
        (SILVER, 'SILVER'),
        (BLUE, 'BLUE'),
        (RED, 'RED')
    ]

    id = models.AutoField(primary_key=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, null=True, blank=True)
    year = models.IntegerField(validators=[MinValueValidator(
        1900), MaxValueValidator(2100)], null=True, blank=True, default=2015)
    trim = models.ForeignKey('Trim', on_delete=models.CASCADE, related_name='cars')

    class Meta:
        db_table = "car"

    def __str__(self):
        return f"{self.owner}'s {self.color.capitalize()} {self.year} {self.trim}"
