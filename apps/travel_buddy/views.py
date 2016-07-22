from django.shortcuts import render, redirect, HttpResponse
from .models import Validator, User, Travel, User_travel, UserManager
import bcrypt
from django.core.urlresolvers import reverse
# Create your views here.
def login_registration(request):
	return render(request, 'travel_buddy/index.html')
def login_process(request):
	validator = Validator()
	usermanager = UserManager()
	formInput = {'email': 1, 'password': 1}
	validator.isShort(request.POST, formInput)
	validator.emailInvalid(request.POST)
	if not validator.error:
		if not usermanager.exist(request.POST):
			request.session['exist'] = False
			validator.msg['emailNotExist'] = 'This email has not registered. Please register first'
			context = {
				'msg': validator.msg
			}
			return render(request, 'travel_buddy/index.html', context)
		curUser = User.objects.get(email=request.POST['email'])
		if bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), curUser.password.encode(encoding='utf-8')) == curUser.password.encode(encoding='utf-8'):
			context = {
				'curUser': curUser
			}
			request.session['fname'] = curUser.first_name
			request.session['lInit'] = curUser.last_name[:1].capitalize()
			request.session['user_id'] = curUser.id
			return redirect(reverse('tb_show_travels'))
		else:
			validator.msg['pwErr'] = 'Password incorrect!'
	context = {
			'msg': validator.msg
		}
	return render(request, 'travel_buddy/index.html', context)
def registration_process(request):
	validator = Validator()
	usermanager = UserManager()
	formInput = {'first_name': 3, 'last_name':3, 'email': 1, 'password': 8}
	validator.isShort(request.POST, formInput)
	validator.emailInvalid(request.POST)
	if not validator.error:
		if usermanager.exist(request.POST):
			request.session['exist'] = True
			validator.msg['emailExist'] = 'This email has registered already. Please log in'
			context = {
				'msg': validator.msg
			}
			return render(request, 'travel_buddy/index.html', context)
		pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
		User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
		curUser = User.objects.get(email=request.POST['email'])
		context = {
			'curUser': curUser
		}
		request.session['fname'] = curUser.first_name
		request.session['lInit'] = curUser.last_name[:1].capitalize()
		request.session['user_id'] = curUser.id
		return redirect(reverse('tb_show_travels'))
	context = {
			'msg': validator.msg
		}
	return render(request, 'travel_buddy/index.html', context)
def show_travels(request):
	curUser = User.objects.get(id=request.session['user_id'])
	otherUsers = User.objects.all().exclude(id=request.session['user_id'])
	# Need to learn through here
	allTravels = Travel.objects.raw('SELECT * FROM travel_buddy_travel JOIN travel_buddy_user_travel ON travel_buddy_travel.id = travel_buddy_user_travel.travel_id JOIN travel_buddy_user ON travel_buddy_user_travel.user_id = travel_buddy_user.id')
	ownTravels = Travel.objects.raw('SELECT * FROM travel_buddy_travel JOIN travel_buddy_user_travel ON travel_buddy_travel.id = travel_buddy_user_travel.travel_id JOIN travel_buddy_user ON travel_buddy_user_travel.user_id = travel_buddy_user.id WHERE travel_buddy_user.id = {}'.format(request.session['user_id']))
	otherTravels = Travel.objects.raw('SELECT * FROM travel_buddy_travel JOIN travel_buddy_user_travel ON travel_buddy_travel.id = travel_buddy_user_travel.travel_id JOIN travel_buddy_user ON travel_buddy_user_travel.user_id = travel_buddy_user.id WHERE travel_buddy_user.id != {}'.format(request.session['user_id']))
	context = {
		'allTravels': allTravels,
		'ownTravels': ownTravels,
		'otherTravels': otherTravels,
		'curUser': curUser,
		'otherUsers':otherUsers
	}
	return render(request, 'travel_buddy/travels.html', context)
def add_travel(request):
	return render(request, 'travel_buddy/add_travel.html')
def add_travel_process(request):
	validator = Validator()
	usermanager = UserManager()
	formInput = {'destination': 1, 'description':1}
	validator.isShort(request.POST, formInput)
	if not validator.error:
		Travel.objects.create(destination=request.POST['destination'], plan_detail=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'])
		curTravel = Travel.objects.filter(destination=request.POST['destination'], plan_detail=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'])
		User_travel.objects.create(user_id=request.session['user_id'], travel_id=curTravel[0].id)
		context = {
			'msg': validator.msg
		}
		return redirect(reverse('tb_show_travels'))
def show_detail(request):
	pass
def join_travel(request, dest_id):
	User_travel.objects.create(user_id=request.session['user_id'], travel_id=dest_id)
	return redirect(reverse('tb_show_travels'))
def logout(request):
	usermanager = UserManager()
	usermanager.logout(request.session)
	return redirect(reverse('tb_login_registration'))