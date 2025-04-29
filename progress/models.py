

# Create your models here.
from django.db import models

class Department(models.Model):
    departmentName = models.CharField(max_length=200)
    departmentLeader = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leading_departments'  #avoid clash
    )


class Admin(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Users(models.Model):
    ROLES = [
        ('Engineer', 'Engineer'),
        ('Team Leader', 'Team Leader'),
        ('Department Leader', 'Department Leader'),
        ('Senior Manager', 'Senior Manager'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)  # ensures email is unique for login or identification
    password = models.CharField(max_length=150)  # would ideally be hashed with Django's auth system
    role = models.CharField(max_length=20, choices=ROLES)

    # Engineers and team leaders must belong to a team
    # Department Leaders and Senior Managers might not, hence `blank=True, null=True`
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True)

    # Department is relevant for leaders and SMs
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Team(models.Model):
    teamName = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    teamLeader = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='leads_teams')

class Session(models.Model):
    sessionType = models.CharField(max_length=150)
    sessionName = models.CharField(max_length=150)
    sessionDate = models.DateField()

class HealthCard(models.Model):
    cardTitle = models.CharField(max_length=100)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    cardDescription = models.CharField(max_length=300)
    cardDate = models.DateField()

class VotingCard(models.Model):
    VOTES = [
        ('Green', 'Green'),
        ('Amber', 'Amber'),
        ('Red', 'Red'),
    ]
    voteDate = models.DateField()
    vote = models.CharField(max_length=10, choices=VOTES)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    card = models.ForeignKey('HealthCard', on_delete=models.CASCADE)

class Progress(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    card = models.ForeignKey('HealthCard', on_delete=models.CASCADE)
