from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Squad
from .serializers import SquadSerializer


@api_view(['GET'])  # what request methods it can respond to
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def getSquads(request):
    squads = Squad.objects.all()
    serializer = SquadSerializer(squads, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSquad(request, pk):
    squad = Squad.objects.get(id=pk)
    serializer = SquadSerializer(squad)
    return Response(serializer.data)
