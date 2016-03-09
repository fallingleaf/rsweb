from collections import OrderedDict
from rest_framework import serializers
from rest_framework.fields import SkipField
from nationbuilder.models import Event


class EventSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source="event_date")
    type = serializers.CharField(source="event_type")
    
    class Meta:
        model = Event
        fields = ('date', 'user', 'type', 'comment', 'otheruser')
        extra_kwargs = {'comment': {'required': False}, 'otheruser': {'required': False}}
    
    def validate(self, data):
        if data['event_type'] == Event.COMMENT:
            if 'comment' not in data or not data['comment']:
                raise serializers.ValidationError("Comment cannot be empty")
        
        if data['event_type'] == Event.HIGHFIVE:
            if 'otheruser' not in data or not data['otheruser']:
                raise serializers.ValidationError("Otheruser cannot be empty")
        
        return data
    
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if not field.write_only]
        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute is not None:
                represenation = field.to_representation(attribute)
                if represenation is None:
                    # Do not seralize empty objects
                    continue
                if isinstance(represenation, list) and not represenation:
                   # Do not serialize empty lists
                   continue
                ret[field.field_name] = represenation

        return ret
            

class SummarySerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    enters = serializers.IntegerField()
    leaves = serializers.IntegerField()
    comments = serializers.IntegerField()
    highfives = serializers.IntegerField()
    
    
    