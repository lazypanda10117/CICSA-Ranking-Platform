from django.shortcuts import render
from api.client_api import *


def index(request):
    return regattas(request)


def scoring(request, id):
    page_data = ScoringPageAPI(request).grabPageData(id=id)
    return render(request, 'client/regatta.html', dict(regatta=page_data))


def rotation(request, id):
    page_data = RotationPageAPI(request).grabPageData(id=id)
    return render(request, 'client/rotation.html', dict(regatta=page_data))


def regattas(request):
    page_data = RegattasPageAPI(request).grabPageData()
    return render(request, 'client/regattas.html', dict(regattas=page_data))


def schools(request):
    page_data = SchoolsPageAPI(request).grabPageData()
    return render(request, 'client/teams.html', dict(regions=page_data))


def school(request):
    page_data = SchoolPageAPI(request).grabPageData()
    return render(request, 'client/team.html', dict(school=page_data))


def seasons(request):
    page_data = SeasonPageAPI(request).grabPageData()
    return render(request, 'client/seasons.html', dict(seasons=page_data))


def news(request):
    page_data = NewsPageAPI(request).grabPageData()
    return render(request, 'client/news.html', dict(news=page_data))


def specific_news(request):
    page_data = SpecificNewsPageAPI(request).grabPageData()
    return render(request, 'client/specific_news.html', dict(news=page_data))

# def home(request):
#     standings = []  # array of standings
#     regattas = []
#     for x in y:
#         regatta = dict(
#             name=1,
#             university=1,
#             location=1,
#             date=1
#         )
#         regattas.append(regatta)
#     all_news = 1  # array of news
#     return render(request, 'client/home.html', {'standings': standings, 'regattas': regattas, 'all_news': all_news})
#
# def scoring(request):
#     #ranking arrays with school
#     #detail scores for each rotation
#     #get data from event_activity
#     #compile data
#     #find current ranking
#     return 0;
#
# def teams(request):
#     regions = []
#     for x in y:
#         teams = []
#         for x in y:
#             team = dict(
#                 university=1,
#                 mascot=1,
#                 location=1
#             )
#             teams.append(team)
#         region = dict(
#             name=1,
#             teams=teams
#         )
#         regions.append(region)
#     return render(request, 'client/teams.html', {'regions': regions})
#
#
# def team(request, team_pk):
#     if 'not valid team':
#         raise Http404("This is not a valid team.")
#
#     people = []
#     for x in y:
#         person = dict(
#             name=1,
#             position=1,
#             grad_year=1,
#             years_sailing_cicsa=1,
#             home_club=1
#         )
#         people.append(person)
#     results = []
#     for x in y:
#         result = dict(
#             event=1,
#             position=1
#         )
#         results.append(result)
#     team = dict(
#         school=1,
#         mascot=1,
#         region=1,
#         location=1,
#         yacht_club=1,
#         captain=1,
#         people=people,
#     )
#     return render(request, 'client/teams.html', {'team': team})
#
#
# def regattas(request):
#     regattas = []
#     for x in y:
#         regatta = dict(
#             date=1,
#             name=1,
#             host=1,
#             location=1,
#             scoring=1
#         )
#         regattas.append(regatta)
#     return render(request, 'client/regattas.html', {'regattas': regattas})
#
#
# def standing(request):
#     pass;
#
# # def regatta(request, regatta_pk):
# # 	return render(request, 'client/regattas.html', {})
