from django.conf import settings
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.views.generic import View
from pathlib import Path
import json
import os
import re
import subprocess

RUN_AS_MUNKIADMIN = settings.RUN_AS_MUNKIADMIN
MDMCTL_JSON = settings.MDMCTL_JSON
SYNC_DEP_DEVICES = settings.SYNC_DEP_DEVICES

@never_cache
def login_method(request):
	# If user is already authenticated, user is redirected to root page.
	if request.user.is_authenticated:
		return HttpResponseRedirect('/')
	if request.POST:
		# We use next parameter to redirect when user login is successful.
		try:
			next_page = request.POST['next']
		except:
			next_page = ''
		# Username & password parameters has to be present.
		try:
			username = request.POST['username']
			password = request.POST['password']
		except:
			return render(request, 'DEP/login.html')
		# Authenticating user.
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if next_page:
					return HttpResponseRedirect(next_page)
				else:
					return HttpResponseRedirect('/')
		else:
			context = {'first_attempt': False, 'next': next_page}
			return render(request, 'DEP/login.html', context)
	else:
		next = ''
		try:
			next = request.GET['next']
		except:
			pass
		context = {'first_attempt': True, 'next': next}
		return render(request, 'DEP/login.html', context)


@never_cache
@login_required(login_url='/login')
def main_method(request):
# e.g. mdmctl get devices | wc -l
	try:
		output = subprocess.check_output("ls / | wc -l", stderr=subprocess.STDOUT, shell=True, timeout=3, universal_newlines=True)
		search = re.search('\d+', output, re.IGNORECASE) #search number only
		if search:
			ios_number = int(search.group(0)) #take whole match
		else:
			ios_number = 0
	except subprocess.CalledProcessError as exc:
			ios_number = 0


	try:
		output = subprocess.check_output("ls / | wc -l", stderr=subprocess.STDOUT, shell=True, timeout=3, universal_newlines=True)
		search = re.search('\d+', output, re.IGNORECASE) #search number only
		if search:
			macos_number = int(search.group(0)) #take whole match
		else:
			macos_number = 0
		
	except subprocess.CalledProcessError as exc:
			macos_number = 0
	try:
		output = subprocess.check_output("ls / | wc -l", stderr=subprocess.STDOUT, shell=True, timeout=3, universal_newlines=True)
		search = re.search('\d{4}', output, re.IGNORECASE) #search number only
		if search:
			blocked = int(search.group(0)) #take whole match
		else:
			blocked = 0
		
	except subprocess.CalledProcessError as exc:
			blocked = 0
		
	
    
	




	context = {'number_of_iOSdevices': ios_number, 'number_of_OSdevices': macos_number, 'number_of_blocked': blocked}

	return render(request, 'DEP/main.html', context)


@never_cache
@login_required(login_url='/login')
def add_device_method(request):
	return render(request, 'DEP/adddevice.html')





@never_cache
@login_required(login_url='/login')
def remove_device_method(request):
	return render(request, 'DEP/removedevice.html')

@never_cache
@login_required(login_url='/login')
def system_journal_method(request):

	try:
		output = subprocess.check_output(
			"{} \"{}\"".format(RUN_AS_MUNKIADMIN, "journalctl -u micromdm.service -f --no-pager"),
			stderr=subprocess.STDOUT,
			shell=True,
			timeout=3,
			universal_newlines=True)
		search = re.search('level: (debug|inactive) \((?:dead|running)\) since [^;]*; (.+) ago', output, re.IGNORECASE)
		if search:
			server_name = "microMDM"
			service_status = search.group(1)
			last_restart = search.group(2)
		else:
			server_name = "microMDM"
			service_status = "error"
			last_restart = "error"
	except subprocess.CalledProcessError as exc:
		server_name = "microMDM"
		service_status = "error"
		last_restart = "error"

	context = {'rows': [{'server_name':server_name, 'service_status':service_status,'last_restart':last_restart}]}



	return render(request, 'DEP/systemjournal.html', context)

@never_cache
@login_required(login_url='/login')
def show_devices_method(request):
	try:
		serial_numbers = []
		with open(MDMCTL_JSON, 'r') as json_file:
			dep_json = json.load(json_file)
		if dep_json.get('devices', ''):
			for i in dep_json.get('devices', ''):
				serial_numbers.append({"serial_number": i})
		context = {'rows': serial_numbers}
	except:
		context = {'rows': []}

	return render(request, 'DEP/showdevices.html', context)

@never_cache
@login_required(login_url='/login')
def api_command_method(request):

	if request.POST:
		subprocess.call(SYNC_DEP_DEVICES)

	return render(request, 'DEP/api.html')

@never_cache
@login_required(login_url='/login')
def manifest_method(request):
	return render(request, 'DEP/manifest.html')

@never_cache
@login_required(login_url='/login')
def service_status_method(request):
	# context = {'rows': [{'server_name':1, 'service_status':534988,'last_restart':'A'},
	#                     {'server_name': 1, 'service_status': 534988, 'last_restart': 'A'},
	#                     {'server_name': 1, 'service_status': 534988, 'last_restart': 'A'}]}

	try:
		output = subprocess.check_output(
			"{} \"{}\"".format(RUN_AS_MUNKIADMIN, "systemctl status micromdm.service --no-pager"),
			stderr=subprocess.STDOUT,
			shell=True,
			timeout=3,
			universal_newlines=True)
		search = re.search('Active: (active|inactive) \((?:dead|running)\) since [^;]*; (.+) ago', output, re.IGNORECASE)
		if search:
			server_name = "microMDMserver"
			service_status = search.group(1)
			last_restart = search.group(2)
		else:
			server_name = "microMDMserver"
			service_status = "error"
			last_restart = "error"
	except subprocess.CalledProcessError as exc:
		server_name = "microMDMserver"
		service_status = "error"
		last_restart = "error"

	context = {'rows': [{'server_name':server_name, 'service_status':service_status,'last_restart':last_restart}]}

	return render(request, 'DEP/servicestatus.html', context)

@never_cache
@login_required(login_url='/login')
def add_method(request):
	if request.POST:
		try:
			with open(MDMCTL_JSON, 'r') as json_file:
				dep_json = json.load(json_file)
		except:
			return JsonResponse({'result': 'Error', 'details': 'Cannot open local json file'})

		try:
			device_id = ''
			device_id = request.POST['id']
		except:
			pass

		if not device_id:
			return JsonResponse({'result': 'Error', 'details': 'Blank Device ID filled in'})

		if not dep_json.get('devices', ''):
			return JsonResponse({'result': 'Error', 'details': 'No devices list in json file'})

		if device_id in dep_json['devices']:
			return JsonResponse({'result': 'Error', 'details': 'Already in'})
		else:
			dep_json['devices'].append(device_id)
			try:
				with open(MDMCTL_JSON, 'w') as json_file:
					json.dump(dep_json, json_file)
			except:
				return JsonResponse({'result': 'Error', 'details': 'Error dumping updated json'})
			return JsonResponse({'result': 'Success', 'details': 'Newly added. Please apply.'})
	else:
		return JsonResponse({'result': 'Error', 'details': 'Use POST method'})


@never_cache
@login_required(login_url='/login')
def remove_method(request):
	if not request.user.is_superuser:
		return JsonResponse({'result': 'Error', 'details': 'Permission denied - you have to be superuser'})

	if request.POST:
		try:
			with open(MDMCTL_JSON, 'r') as json_file:
				dep_json = json.load(json_file)
		except:
			return JsonResponse({'result': 'Error', 'details': 'Cannot open local json file'})

		try:
			device_id = ''
			device_id = request.POST['id']
		except:
			pass

		if not device_id:
			return JsonResponse({'result': 'Error', 'details': 'Blank Device ID filled in'})

		if not dep_json.get('devices', ''):
			return JsonResponse({'result': 'Error', 'details': 'No devices list in json file'})

		if device_id not in dep_json['devices']:
			return JsonResponse({'result': 'Questionable', 'details': 'Not present in devices'})
		else:
			dep_json['devices'].remove(device_id)
			try:
				with open(MDMCTL_JSON, 'w') as json_file:
					json.dump(dep_json, json_file)
			except:
				return JsonResponse({'result': 'Error', 'details': 'Error dumping updated json to local file'})
			return JsonResponse({'result': 'Success', 'details': 'Removed selected Device ID'})
	else:
		return JsonResponse({'result': 'Error', 'details': 'Use POST method'})


@never_cache
@login_required(login_url='/login')
def apply_method(request):
	if request.POST:
		try:
			output = subprocess.check_output("{} \"mdmctl apply dep-profiles -f {}\"".format(RUN_AS_MUNKIADMIN, MDMCTL_JSON),
											 stderr=subprocess.STDOUT,
											 shell=True,
											 timeout=3,
											 universal_newlines=True)
		except subprocess.CalledProcessError as exc:
			output = exc.output

		if re.search('Defined DEP Profile with UUID [\dA-Za-z]+', output, re.IGNORECASE):
			return JsonResponse({'result': 'Success', 'details': output, 'additional': 'Output looks fine based on '
																					   'standard behaviour'})
		else:
			return JsonResponse({'result': 'Questionable', 'details': output, 'additional': 'Output doesn\'t look '
																							'standard'})
	else:
		return JsonResponse({'result': 'Error', 'details': 'Use POST method'})


@never_cache
@login_required(login_url='/login')
def modular_method(request):
	modular_list = [
		{"method": "journalctl_micromdm_service",
		 "command": "journalctl -u micromdm.service -n 100 --no-pager",
		 "expected_result": "Logs begin at"},
		{"method": "systemctl_status_micromdm_service",
		 "command": "systemctl status micromdm.service --no-pager",
		 "expected_result": "micromdm.service - MicroMDM MDM Server"},
		{"method": "GET APPS",
		 "command": "mdmctl get apps",
		 "expected_result": ""},
		{"method": "restart_micromdm",
		 "command": "sudo service micromdm restart --no-pager",
		 "expected_result": ""},
		 {"method": "sync_dep_devices",
		 "command": "sudo ./sync_dep_devices.sh --no-pager",
		 "expected_result": ""}
	]

	if not request.user.is_superuser:
		return JsonResponse({'result': 'Error', 'details': 'Permission denied - you have to be superuser'})

	if request.POST:
		try:
			method_param = request.POST['method']
		except:
			return JsonResponse({'result': 'Error', 'details': 'Undefined method.'})

		for elem in modular_list:
			if elem['method'] == method_param:
				command, expected_result = elem['command'], elem['expected_result']
				break
		else:
			return JsonResponse({'result': 'Error', 'details': 'Couldn\'t find selected method.'})

		try:
			output = subprocess.check_output("{} \"{}\"".format(RUN_AS_MUNKIADMIN, command),
											 stderr=subprocess.STDOUT,
											 shell=True,
											 timeout=3,
											 universal_newlines=True)
		except subprocess.CalledProcessError as exc:
			output = exc.output

		if re.search(expected_result, output, re.IGNORECASE):
			return JsonResponse({'result': 'Success', 'output': output})
		else:
			return JsonResponse({'result': 'Error', 'details': output})
	else:
		return JsonResponse({'result': 'Error', 'details': 'Use POST method'})


@never_cache
@login_required(login_url='/login')
def get_json_method(request):
	return serve(request, os.path.basename(MDMCTL_JSON), os.path.dirname(MDMCTL_JSON))


@never_cache
@login_required(login_url='/login')
def logout_method(request):
	logout(request)
	return HttpResponseRedirect('/login')


@never_cache
def not_present_method(request):
	return HttpResponse("Not present on the server!", status=404)


