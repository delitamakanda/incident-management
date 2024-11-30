import json

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from incidents.models import Token, ActivityLog

user = get_user_model()

class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_dashboard_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
class ReportActivityLogsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = user.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        
    def test_report_activity_logs_view(self):
        headers = {
            'Authorization': f'Token {self.token.key}',
            'Content-Type': 'application/json',
        }
        data = {
            'error_message': 'error message',
            'stack_trace': 'stack trace',
        }
        response = self.client.post('/api/report-activity-logs/', data=json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(ActivityLog.objects.exists())
        
        content = json.loads(response.content)
        self.assertIn('data', content)
        self.assertEqual(content['data']['error_message'], 'error message')
        self.assertEqual(content['data']['stack_trace'], 'stack trace')
        self.assertEqual(content['data']['occurence_count'], 1)
        
