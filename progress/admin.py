from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Department, Team, Users, Session, HealthCard, VotingCard

admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Users)
admin.site.register(Session)
admin.site.register(HealthCard)
admin.site.register(VotingCard)
