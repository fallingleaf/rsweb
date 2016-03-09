from django.db import models
from django.db import connection

from nationbuilder.helpers import convertToDbTime as dbtime


class Event(models.Model):
    ENTER = 'enter'
    HIGHFIVE = 'highfive'
    COMMENT = 'comment'
    LEAVE = 'leave'
    EVENT_CHOICES = (
        (ENTER, 'enter'),
        (HIGHFIVE, 'highfive'),
        (COMMENT, 'comment'),
        (LEAVE, 'leave')
    )
    
    user = models.CharField(max_length=128)
    event_date = models.DateTimeField()
    event_type = models.CharField(max_length=128, 
                                choices=EVENT_CHOICES, 
                                default=COMMENT)
                                
    comment = models.TextField(null=True)
    otheruser = models.CharField(max_length=128, null=True)
    
    @staticmethod
    def getSummary(from_date, to_date, group):
        sql = """
        SELECT DATE_TRUNC(%s, event_date) AS "date",
            SUM(CASE WHEN event_type = %s THEN 1 ELSE 0 END) AS enters,
            SUM(CASE WHEN event_type = %s THEN 1 ELSE 0 END) AS leaves,
            SUM(CASE WHEN event_type = %s THEN 1 ELSE 0 END) AS comments,
            SUM(CASE WHEN event_type = %s THEN 1 ELSE 0 END) AS highfives 
            FROM nationbuilder_event WHERE event_date BETWEEN %s AND %s 
            GROUP BY DATE_TRUNC(%s, event_date)
        """
        from_date = dbtime(from_date)
        to_date = dbtime(to_date)
        result = []
        with connection.cursor() as cursor:
            cursor.execute(sql, [group, Event.ENTER, Event.LEAVE, Event.COMMENT, 
                                Event.HIGHFIVE, from_date, to_date, group])
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return result
        
        
    
    