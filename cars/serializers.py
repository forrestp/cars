from rest_framework import serializers

from .models import Car, Make, Model, Trim


class MakeSerializer(serializers.ModelSerializer):
    models = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Model.objects.all(),
        required=False
    )

    class Meta:
        model = Make
        fields = ['id', 'name', 'models']


class ModelSerializer(serializers.ModelSerializer):
    trims = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Trim.objects.all(),
        required=False
    )
    make = serializers.PrimaryKeyRelatedField(
        queryset=Make.objects.all(),
    )

    class Meta:
        model = Model
        fields = ['id', 'name', 'trims', 'make']


class TrimSerializer(serializers.ModelSerializer):
    cars = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Car.objects.all(),
        required=False
    )
    model = serializers.PrimaryKeyRelatedField(
        queryset=Model.objects.all(),
    )

    class Meta:
        model = Trim
        fields = ['id', 'name', 'cars', 'model']


class CarSerializer(serializers.ModelSerializer):
    trim = serializers.PrimaryKeyRelatedField(
        queryset=Trim.objects.all(),
    )

    class Meta:
        model = Car
        fields = ['id', 'owner', 'color', 'year', 'trim']
