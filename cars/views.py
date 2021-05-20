from rest_framework import viewsets

from .models import Car, Make, Model, Trim
from .serializers import (
    CarSerializer,
    MakeSerializer,
    ModelSerializer,
    TrimSerializer,
)


class MakeViewSet(viewsets.ModelViewSet):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'models']


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'trims', 'make']


class TrimViewSet(viewsets.ModelViewSet):
    queryset = Trim.objects.all()
    serializer_class = TrimSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'cars', 'model']


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = []
    filterset_fields = ['id', 'owner', 'color', 'year', 'trim']
