from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Users, Team, Department, Session, VotingCard, HealthCard



# Team Leader Dashboard
# @login_required
def team_leader_progress_report(request):
    # user = request.user

    # Only allow access to Team Leaders
    # if not hasattr(user, 'role') or user.role != 'Team Leader':
    #     return render(request, 'progress/not_authorised.html')

    sessions = Session.objects.order_by('sessionDate')
    selected_session_id = request.GET.get("session")

    if selected_session_id:
        selected_session = Session.objects.filter(id=selected_session_id).first()
    else:
        selected_session = sessions.last()

    page_number = int(request.GET.get("page", 1))
    vote_summary = []

    if selected_session:
        cards = list(HealthCard.objects.filter(team__votingcard__session=selected_session).distinct())
        for card in cards:
            votes = VotingCard.objects.filter(session=selected_session, card=card)
            vote_summary.append({
                "label": card.cardTitle,
                "Green": votes.filter(vote="Green").count(),
                "Amber": votes.filter(vote="Amber").count(),
                "Red": votes.filter(vote="Red").count()
            })

    paginator = Paginator(vote_summary, 2)
    page_obj = paginator.get_page(page_number)

    context = {
        "sessions": sessions,
        "selected_session": selected_session,
        "page_number": page_number,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "labels": [item["label"] for item in page_obj],
        "green_counts": [item["Green"] for item in page_obj],
        "amber_counts": [item["Amber"] for item in page_obj],
        "red_counts": [item["Red"] for item in page_obj]
    }
    return render(request, "progress/team_leader_report.html", context)


# Department Leader Dashboard
# @login_required
def department_leader_progress(request):
    # user = request.user
    user = Users.objects.get(name="John")

    # if user.role != 'Department Leader':
    #     return render(request, 'progress/not_authorised.html')

    sessions = Session.objects.order_by('sessionDate')
    departments = Department.objects.all()

    selected_session_id = request.GET.get("session")
    selected_department_id = request.GET.get("department")
    selected_team_id = request.GET.get("team")

    selected_session = Session.objects.filter(id=selected_session_id).first() if selected_session_id else sessions.last()
    selected_department = Department.objects.filter(id=selected_department_id).first() if selected_department_id else user.department
    selected_team = Team.objects.filter(id=selected_team_id).first() if selected_team_id else None

    is_own_department = (user.department.id == selected_department.id)
    teams = Team.objects.filter(department=selected_department)
    show_chart = is_own_department  # Only show chart if it is user's own department

    
    # Filter cards based on team selection
    if selected_team:
        report_cards = HealthCard.objects.filter(team=selected_team)
    else:
        report_cards = HealthCard.objects.filter(team__in=teams)


    report = []

    if is_own_department:
        if selected_team:
            # Detailed report for selected team
            cards = HealthCard.objects.filter(team=selected_team)
            for card in cards:
                votes = VotingCard.objects.filter(session=selected_session, card=card)
                report.append({
                    "team": selected_team.teamName,
                    "card": card.cardTitle,
                    "green": votes.filter(vote='Green').count(),
                    "amber": votes.filter(vote='Amber').count(),
                    "red": votes.filter(vote='Red').count()
                })
        else:
            # All Teams selected in own department –> summary per healthcard
            card_titles = HealthCard.objects.filter(team__in=teams).values_list('cardTitle', flat=True).distinct()
            for title in card_titles:
                related_cards = HealthCard.objects.filter(team__in=teams, cardTitle=title)
                votes = VotingCard.objects.filter(session=selected_session, card__in=related_cards)
                report.append({
                    "team": "All Teams",
                    "card": title,
                    "green": votes.filter(vote='Green').count(),
                    "amber": votes.filter(vote='Amber').count(),
                    "red": votes.filter(vote='Red').count()
                })



    # If you're summarizing all teams, use full report, else paginate
    if selected_team is None and is_own_department:
        labels = [item["card"] for item in report]
        green_counts = [item["green"] for item in report]
        amber_counts = [item["amber"] for item in report]
        red_counts = [item["red"] for item in report]
        
        page_number = 1
        has_next = False
        has_previous = False
    else:
        page_number = int(request.GET.get("page", 1))
        paginator = Paginator(report, 15)
        page_obj = paginator.get_page(page_number)

        labels = [item["card"] for item in page_obj]
        green_counts = [item["green"] for item in page_obj]
        amber_counts = [item["amber"] for item in page_obj]
        red_counts = [item["red"] for item in page_obj]
        
        has_next = page_obj.has_next() if 'page_obj' in locals() else False
        has_previous = page_obj.has_previous() if 'page_obj' in locals() else False



    user_department = user.department
    other_department = Department.objects.exclude(id=selected_department.id).first()
    # Summary of the OTHER department (not team-specific)
    summary_report = []
    
    

    if other_department:
        other_teams = Team.objects.filter(department=other_department)
        card_titles = HealthCard.objects.filter(team__in=other_teams).values_list('cardTitle', flat=True).distinct()
        
        for title in card_titles:
            related_cards = HealthCard.objects.filter(team__in=other_teams, cardTitle=title)
            summary_report.append({
                "card": title,
                "green": VotingCard.objects.filter(session=selected_session, card__in=related_cards, vote='Green').count(),
                "amber": VotingCard.objects.filter(session=selected_session, card__in=related_cards, vote='Amber').count(),
                "red": VotingCard.objects.filter(session=selected_session, card__in=related_cards, vote='Red').count()
            })

    return render(request, "progress/department_leader_progress.html", {
        "sessions": sessions,
        "departments": departments,
        "teams": teams,
        "selected_session": selected_session,
        "selected_department": selected_department,
        "selected_team": selected_team,
        "report": report,
        "summary_report": summary_report,
        "labels": labels,
        "green_counts": green_counts,
        "amber_counts": amber_counts,
        "red_counts": red_counts,
        "page_number": page_number,
        "has_next": has_next,
        "has_previous": has_previous,
        "is_own_department": is_own_department,
        "show_chart": show_chart,
    })





# Senior Manager Dashboard
# @login_required
def senior_manager_progress(request):

     # user = request.user
    user = Users.objects.get(name="David")

    if user.role != 'Senior Manager':
       return render(request, 'progress/not_authorised.html')
    sessions = Session.objects.order_by('sessionDate')
    departments = Department.objects.all()

    selected_session_id = request.GET.get("session")
    selected_department_id = request.GET.get("department")
    selected_team_id = request.GET.get("team")

    selected_session = Session.objects.filter(id=selected_session_id).first() if selected_session_id else sessions.last()
    selected_department = Department.objects.filter(id=selected_department_id).first() if selected_department_id else None
    selected_team = Team.objects.filter(id=selected_team_id).first() if selected_team_id else None

    report = []
    labels = []
    green_counts = []
    amber_counts = []
    red_counts = []
    show_chart = False

    teams = Team.objects.all()
    if selected_department:
        teams = Team.objects.filter(department=selected_department)

    if selected_team:
        # Team-specific report
        cards = HealthCard.objects.filter(team=selected_team)
        for card in cards:
            votes = VotingCard.objects.filter(session=selected_session, card=card)
            green_count = votes.filter(vote='Green').count()
            amber_count = votes.filter(vote='Amber').count()
            red_count = votes.filter(vote='Red').count()

            report.append({
                "card": card.cardTitle,
                "team": selected_team.teamName,
                "green": green_count,
                "amber": amber_count,
                "red": red_count,
            })

            labels.append(card.cardTitle)
            green_counts.append(green_count)
            amber_counts.append(amber_count)
            red_counts.append(red_count)

            show_chart = True

    elif selected_department:
        # Department-specific summary (overall department votes per healthcard)
        cards = HealthCard.objects.filter(team__in=teams).values_list('cardTitle', flat=True).distinct()

        for title in cards:
            related_cards = HealthCard.objects.filter(team__in=teams, cardTitle=title)
            votes = VotingCard.objects.filter(session=selected_session, card__in=related_cards)

            green_count = votes.filter(vote='Green').count()
            amber_count = votes.filter(vote='Amber').count()
            red_count = votes.filter(vote='Red').count()

            report.append({
                "card": title,
                "team": selected_department.departmentName + " Summary",
                "green": green_count,
                "amber": amber_count,
                "red": red_count,
            })

            labels.append(title)
            green_counts.append(green_count)
            amber_counts.append(amber_count)
            red_counts.append(red_count)

            show_chart = True

    else:
        # All Departments summary (pure global summary)
        cards = HealthCard.objects.values_list('cardTitle', flat=True).distinct()

        for title in cards:
            related_cards = HealthCard.objects.filter(cardTitle=title)
            votes = VotingCard.objects.filter(session=selected_session, card__in=related_cards)

            green_count = votes.filter(vote='Green').count()
            amber_count = votes.filter(vote='Amber').count()
            red_count = votes.filter(vote='Red').count()

            report.append({
                "card": title,
                "team": "All Departments",
                "green": green_count,
                "amber": amber_count,
                "red": red_count,
            })

            labels.append(title)
            green_counts.append(green_count)
            amber_counts.append(amber_count)
            red_counts.append(red_count)

            show_chart = True

    context = {
        "sessions": sessions,
        "departments": departments,
        "teams": teams,
        "selected_session": selected_session,
        "selected_department": selected_department,
        "selected_team": selected_team,
        "report": report,
        "labels": labels,
        "green_counts": green_counts,
        "amber_counts": amber_counts,
        "red_counts": red_counts,
        "show_chart": show_chart,
    }

    return render(request, "progress/senior_manager_progress.html", context)


def not_authorised(request):
    return render(request, 'progress/not_authorised.html')

