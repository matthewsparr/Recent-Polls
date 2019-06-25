from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template 
from .models import Question, Choice, Category
import json
import requests
from django.utils import timezone

## resource links
new_york_data_url = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
huffington_data_url = 'https://elections.huffingtonpost.com/pollster/api/v2/polls'

def index(request, category):
	category_id = Category.objects.get(category=category).id
	questions = Question.objects.filter(category_id=category_id)
	template = get_template('polls/index.html')
	context = {
        'questions':questions,
        'category_id': category,
	}
	return HttpResponse(template.render(context, request))

def main(request):
	grab_new_york_data()
	grab_huffington_data()
	category_list = Category.objects.all()
	template = get_template('polls/main.html')
	context = {
		'category_list': category_list,
	}
	return HttpResponse(template.render(context, request))

def results(request, category, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question, 'category':category})

def grab_new_york_data():
	## check if category was already created
	if Category.objects.filter(category='New-York').exists():
		pass
	else:
		category = Category.objects.create(category="New-York")
		r = requests.get(new_york_data_url)
		data = r.json()
		new_york_data = []
		choices = ['Very Conservative', 'Conservative', 'Moderate', 'Liberal', 'Very Liberal', 'None of the above']
		## grab and store poll percentages for each choice as well as the year and total poll population
		for i in data:
			if i['Geography'] == 'New York':
				results = {}
				results['Total'] = int(i['N Size'].replace(',',''))
				results['Year'] = i['Time']
				results['Very Conservative'] = int(round(100 * i['Very conservative']))
				results['Conservative'] = int(round(100 * i['Conservative, (or)']))
				results['Moderate'] = int(round(100 * i['Moderate']))
				results['Liberal'] = int(round(100 * i['Liberal, (or)']))
				results['Very Liberal'] = int(round(100 * i['Very liberal']))
				results['None of the above'] = int(round(100 * i['NA']))
				new_york_data.append(results)
		## store each question and choices in database
		for i in new_york_data:
			question = Question.objects.create(category=category, question_text=str(i['Year']) + ' ' + 'New York Political Leanings', pub_date=timezone.now(), total_polled=i['Total'])
			choice1 = Choice.objects.create(question=question, choice_text='Very Conservative', percentage=i['Very Conservative'])
			choice2 = Choice.objects.create(question=question, choice_text='Conservative', percentage=i['Conservative'])
			choice3 = Choice.objects.create(question=question, choice_text='Moderate', percentage=i['Moderate'])
			choice4 = Choice.objects.create(question=question, choice_text='Liberal', percentage=i['Liberal'])
			choice5 = Choice.objects.create(question=question, choice_text='Very Liberal', percentage=i['Very Liberal'])
			choice6 = Choice.objects.create(question=question, choice_text='None of the above', percentage=i['None of the above'])
	return HttpResponse('Done')	

def grab_huffington_data():
	## check if category exists, if so, delete data to be replaced with new/updated
	if Category.objects.filter(category='Recent-Polls').exists():
		category_id = Category.objects.get(category='Recent-Polls').id
		questions = Question.objects.filter(category_id=category_id)
		questions.delete()
		category = Category.objects.get(category='Recent-Polls')
	else:
		category = Category.objects.create(category="Recent-Polls")
	r = requests.get(huffington_data_url)
	data = r.json()['items']
	## only first 25 polls are grabbed so another request is needed to get an additional 15 polls
	next_cursor = r.json()['next_cursor']
	r2 = requests.get(huffington_data_url+"?cursor="+next_cursor)
	data = data + r2.json()['items'][0:15]
	## iterate through each poll, grabbing relevant data and storing in database
	for poll in data:
		slug = poll['slug']
		survey_house = poll['survey_house']
		created_at = poll['created_at']
		for i in poll['poll_questions']:
			poll_name = i['question']['name']
			for j in i['sample_subpopulations']:
				subpopulation = j['name']
				observations = j['observations']
				if not observations:
					observations=0
				question = Question.objects.create(category=category, question_text=survey_house + ' - ' + poll_name + ' - ' + subpopulation, pub_date=created_at, total_polled=observations)
				for k in j['responses']:
					choice_text = k['text']
					choice_value = k['value']
					choice = Choice.objects.create(question=question, choice_text=choice_text, percentage=choice_value)
	return HttpResponse('Done')


