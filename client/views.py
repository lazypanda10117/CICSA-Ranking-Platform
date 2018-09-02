from django.shortcuts import render
from django.http import Http404

# Create your views here.

def home(request):
	standings = 1 # array of standings
	regattas = []
	for x in y:
		regatta = dict(
			name=1,
			university=1,
			location=1,
			date=1
		)
		regattas.append(regatta)
	all_news = 1 # array of news
	return render(request, 'client/home.html', {'standings': standings, 'regattas': regattas, 'all_news': all_news})

def teams(request):
	regions = []
	for x in y:
		teams = []
		for x in y:
			team = dict(
				university=1,
				mascot=1,
				location=1
			)
			teams.append(team)
		region = dict(
			name=1,
			teams=teams
		)
		regions.append(region)
	return render(request, 'client/teams.html', {'regions': regions})

def team(request, team_pk):

	if 'not valid team':
		raise Http404("This is not a valid team.")

	people = []
	for x in y:
		person = dict(
			name=1,
			position=1,
			grad_year=1,
			years_sailing_cicsa=1,
			home_club=1
		)
		people.append(person)
	results = []
	for x in y:
		result = dict(
			event=1,
			position=1
		)
		results.append(result)
	team = dict(
		school=1,
		mascot=1,
		region=1,
		location=1,
		yacht_club=1,
		captain=1,
		people=people,
	)
	return render(request, 'client/teams.html', {'team': team})

def regattas(request):
	regattas = []
	for x in y:
		regatta = dict(
			date=1,
			name=1,
			host=1,
			location=1,
			scoring=1
		)
		regattas.append(regatta)
	return render(request, 'client/regattas.html', {'regattas': regattas})

# def regatta(request, regatta_pk):
# 	return render(request, 'client/regattas.html', {})