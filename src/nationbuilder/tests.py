import urllib
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from nationbuilder.models import Event

class EventTests(APITestCase):
    @classmethod
    def setUpTestData(self):
        now = datetime.now()
        delta = timedelta(seconds=3600)
        
        # Set timestamp
        self.timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.from_date = (now - delta).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.to_date = (now + delta).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Create 4 different events
        self.evt1 = Event(user='user1', event_type='enter', event_date=self.timestamp)
        self.evt2 = Event(user='user2', event_type='comment', comment="test", event_date=self.timestamp)
        self.evt3 = Event(user='user3', event_type='highfive', otheruser='test', event_date=self.timestamp)
        self.evt4 = Event(user='user2', event_type='leave', event_date=self.timestamp)
        
        self.evt1.save()
        self.evt2.save()
        self.evt3.save()
        self.evt4.save()
        
        # Event post data
        self.event_enter = {'date': self.timestamp, 'user': 'test1', 
                            'type': 'enter'}
        self.event_leave = {'date': self.timestamp, 'user': 'test2', 
                            'type': 'highfive', 'otheruser': 'Marty'}
        self.event_comment = {'date': self.timestamp, 'user': 'test3', 
                            'type': 'comment', 'comment': 'this is comment'}
        self.event_highfive = {'date': self.timestamp, 'user': 'test4', 
                            'type': 'highfive', 'otheruser': 'Marty'}
        
        # Expected success, error result
        self.success = {'status': 'ok'}
        self.error = {'status': 'error'}
        
    def test_create_event(self):
        url = reverse('events')
        
        # User enter event
        response = self.client.post(url, self.event_enter, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.success)
        
        # User comment event
        response = self.client.post(url, self.event_comment, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.success)
        
        # User highfive event
        response = self.client.post(url, self.event_highfive, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.success)
        
        # User leave event
        response = self.client.post(url, self.event_leave, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.success)
    
    def test_list_event(self):
        url = reverse('events') + '?' + urllib.urlencode({'from': self.from_date, 'to':self.to_date})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['events']), 4)
    
    def test_summarize_event(self):
        url = reverse('event-summary')
        
        for i in ["minute", "hour", "day"]:
            params = urllib.urlencode({'from': self.from_date, 'to': self.to_date, 'by': i})
            murl = url + '?' + params
            response = self.client.get(murl, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['events']), 1)
        
    
    def test_clear_event(self):
        url = reverse('event-clear')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.success)
        self.assertEqual(Event.objects.count(), 0)
    
    @classmethod
    def tearDownClass(self):
        self.evt1.delete()
        self.evt2.delete()
        self.evt3.delete()
        self.evt4.delete()
        
        
