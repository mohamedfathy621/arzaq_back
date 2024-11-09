from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import User, Medications
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import  check_password
from rest_framework_simplejwt.tokens import RefreshToken
import json
import os
project_root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(project_root, 'dummy_list.json')
@csrf_exempt
def register(request):
    if request.method =='POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'faliure', 'message': 'Username already exists','errors':{'username':'Username already exists'}}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'faliure', 'message': 'Email already exists','errors':{'email':'Email already exists'}}, status=400)
            
            user = User(username=username, email=email)
            user.set_password(password)  
            user.save()  
            return JsonResponse({'status': 'success', 'user_id': user.id,'message':'Registeration successful'}, status=201)
        except json.JSONDecodeError:
             return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
@csrf_exempt
def login(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'This is the login endpoint'})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')  
            if User.objects.filter(username=username).exists():
                 user = User.objects.get(username=username)
                 is_correct = check_password(password, user.password)
                 if is_correct:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    return JsonResponse({'status':'success',"message": "Authentication successful",'access_token': access_token,'refresh_token': refresh_token}, status=200)
                 else:
                    return JsonResponse({'status': 'faliure',"message": "wrong password",'errors':{'password':'wrong password'}}, status=400)
            else:
                return JsonResponse({'status': 'faliure',"message": "Invalid username or password",'errors':{'username':'wrong username','password':'wrong password'}}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
@csrf_exempt
def refresh_access_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        refresh_token = data.get('refresh',None)
    
        if not refresh_token:
            return JsonResponse({'status': 'faliure',"message": "session has expired"}, status=400)
        try:
        # Decode and verify the refresh token using simplejwt
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return JsonResponse({'status':'success',"message": "welcome back",'access_token': access_token,'refresh_token': refresh_token}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e),'status': 'faliure',"message": "session has expired",'token':refresh_token}, status=500)


@permission_classes([IsAuthenticated])
def load_medications(request):
    if request.method == 'GET':
        try:
            medications = Medications.objects.all()
            medication_list = list(medications.values())  # Converts to list of dictionaries
            return JsonResponse({"status": "success", "medications": medication_list}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)      

@csrf_exempt
def populate(request):
     if request.method == 'POST':
         data = json.loads(request.body)
         username = data.get('username')
         password = data.get('password')
         try:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                is_correct = check_password(password, user.password)
                if is_correct:
                    with open(file_path, 'r') as file:
                        medic_list = json.load(file)['medications']
                    for item in medic_list:
                        medication=Medications(name=item['name'], category=item['category'],dosage_form=item['dosage_form'],brand_name=item['brand_name'],concentration=item['concentration'],price=item['price'],refill_requests=0,refills_issued=0,image_url=item['image_url'])
                        medication.save()
                return JsonResponse({'status':'success',"message": "data inserted"}, status=200)
            return JsonResponse({'status':'faliure',"message": "wrong credintals"}, status=400)
         except Exception as e:
            return JsonResponse({"error": str(e),'data':medic_list}, status=500)
