#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sky_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
from django.db import models

class Department(models.Model):
    departmentName = models.CharField(max_length=200)
    departmentLeader = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True)

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
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLES)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

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
