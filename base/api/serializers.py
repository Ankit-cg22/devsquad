from rest_framework.serializers import ModelSerializer
from base.models import Squad


class SquadSerializer(ModelSerializer):
    class Meta:
        model = Squad
        fields = '__all__'
