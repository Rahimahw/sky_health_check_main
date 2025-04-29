

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Team, Session, HealthCard, Vote

class TeamLeaderReportTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.team = Team.objects.create(name="Team A")
        self.user = get_user_model().objects.create_user(username="tl", password="test123", role="team_leader", team=self.team)
        self.session = Session.objects.create(name="April", date="2025-04-01")
        self.card = HealthCard.objects.create(title="Teamwork")
        Vote.objects.create(user=self.user, session=self.session, card=self.card, vote="green", improving=True)

    def test_report_access(self):
        self.client.login(username="tl", password="test123")
        response = self.client.get(f"/progress/team-leader/report/?session={self.session.id}&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teamwork")
