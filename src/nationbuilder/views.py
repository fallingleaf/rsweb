import logging

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from nationbuilder.helpers import convertToDbTime as dbtime
from nationbuilder.models import Event
from nationbuilder.serializers import EventSerializer, SummarySerializer


logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        
        from_date = dbtime(request.query_params['from'])
        to_date = dbtime(request.query_params['to'])
        events = Event.objects.filter(event_date__lte=to_date,
                                    event_date__gte=from_date)
        eserializers = EventSerializer(events, many=True)
        return Response({'events': eserializers.data})
    
    elif request.method == 'POST':
        eserializer = EventSerializer(data=request.data)
        if eserializer.is_valid():
            eserializer.save()
            return Response(dict(status="ok"))
        return Response(dict(status="error"), status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def event_clear(request):
    try:
        Event.objects.all().delete()
    except Exception as e:
        logger.error("Unable to delete events")
        return Response(dict(status="error"), status=status.HTTP_400_BAD_REQUEST)
        
    return Response(dict(status="ok"))


@api_view(['GET'])
def event_summary(request):
    from_date = request.query_params['from']
    to_date = request.query_params['to']
    by = request.query_params['by']
    
    summaries = Event.getSummary(from_date, to_date, by)
    serializer = SummarySerializer(summaries, many=True)
    return Response({"events": serializer.data})
    
    
    