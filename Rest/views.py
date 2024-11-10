from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum,Count
from .models import Medications,Refill_orders
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import  check_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from Rest.helpscript import dates
import json
import os
project_root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(project_root, 'dummy_list.json')

# this is a serializer used to handle valdiation and insertion for registartion#
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    #the password is not saved in the database for security reasons 
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

#this view works on a post method
#first it checks the data using the serializer
#on validation it inserts the data and repsonds with status 201 and a message to notify the user
#on faliure it responds with status 400 and a message to notify the user
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'success', 'user_id': user.id, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)

        return Response({'status': 'failure', 'errors': {'username': 'username already in use'},'message': 'username already in use'}, status=status.HTTP_400_BAD_REQUEST)

#this is the login view
##first it checks if the user is in the database
##if faliure it responds with status 400 and a message to notify the user about the wrong username
## on sucess it uses django middle ware for authenticaon o
## if sucess the user is sent a status 200 , a token and a message to notify the user 
## on faliure it responds with status 400 and a messsage to notify the user
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow non-authenticated users to log in

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({ 'status': 'failure','message': 'wrong username','errors': {'username': 'Invalid username'} }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'status': 'success',
                'message': 'Authentication successful',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'failure',
            'message': 'Invalid username or password',
            'errors': {'username': 'Invalid username', 'password': 'Invalid password'}
        }, status=status.HTTP_400_BAD_REQUEST)

##this is the refresh token view
##this functions uses django middle ware to checks for the validty of the session
## on sucess it responds with a valid access token
## on faliure it notifies the user the session has ended and an error status
class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        # Get refresh token from request data
        data = request.data
        refresh_token = data.get('refresh', None)

        if not refresh_token:
            return Response(
                {'status': 'failure', 'message': 'Session has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Decode and verify the refresh token using simplejwt
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response(
                {
                    'status': 'success',
                    'message': 'Welcome back',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e), 'status': 'failure', 'message': 'Session has expired', 'token': refresh_token},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

##this is the medication view
## it requires JWT authentication 
## if the token is valid the user is sent a list of medicaitons in the database
## on faliure an error is sent instead
class LoadMedicationsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can access this view

    def get(self, request):
        try:
            # Retrieve all medications from the database
            medications = Medications.objects.all()
            medication_list = list(medications.values())  # Converts to list of dictionaries

            return Response({"status": "success", "medications": medication_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

##THIS is the issue refill request view 
##it requires authentcation 
##if the token is valid the view checks to see if the user still exists in the database to avoid errors
##if so the orderlist is divided into seprate medications
##first the order is saved in the database
##then each medicine has it's refill requests coloumn incremnted with the respective quanataity
## a transaction atomic decorator is used to ensure if an error occurs in any of the operations the operations as a whole is not commited 
class IssueOrderView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self,request):
        try:
            orderlist = request.data.get('orderlist')
            totalprice = request.data.get('totalprice')
            username= request.data.get('username')
            user = User.objects.filter(username=username).first()
            if not user:
                return Response({'status': 'failure', 'message': 'User not found','user':username}, status=404)
            order=Refill_orders(user_id=user,orderlist=orderlist,TotalPrice=totalprice)
            order.save()
            for medicine_name, details in orderlist.items():
                quantity = details.get('quantaity')
                medicine=Medications.objects.filter(name=medicine_name).first()
                if not medicine:
                    return Response({'status': 'failure', 'message': 'medicine not found'}, status=404)
                medicine.refill_requests += quantity
                medicine.save()
            return Response({'status': 'success', 'message': 'Order and medications updated successfully'}, status=201)
        except Exception as e:
            return Response({'error':str(e),'status':'failure','message':'insertion failed'})


##this is the view to get chart data
##first each medication is fetched from the database with only the name and the amount of refill requests
##the total amount of refill requests is fetched from the sum of refill requests database
##users and thier respective order count is fetched from the database
##then orders are fetched from the database and summed occurding to thier time category (yearly,monthly,weekly,daily)
##this data is then put into a json response and sent to the user
class GetAnaltiycs(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            medications = Medications.objects.all()
            medication_list = list(medications.values('name','refill_requests'))
            total_refill_requests = Medications.objects.aggregate(total=Sum('refill_requests'))['total']
            user_order_count = Refill_orders.objects.values('user_id__username').annotate(order_count=Count('id'))
            calender=dates()
            orders_this_year_count = Refill_orders.objects.filter(date__gte=calender['start_of_year']).count()
            orders_this_month_count = Refill_orders.objects.filter(date__gte=calender['start_of_month']).count()
            orders_this_week_count = Refill_orders.objects.filter(date__gte=calender['start_of_week']).count()
            orders_today_count = Refill_orders.objects.filter(date__gte=calender['start_of_day']).count()
            economic_calender={'year':orders_this_year_count,'month':orders_this_month_count,'week':orders_this_week_count,'day':orders_today_count}
            data={'medicines':medication_list,'total_request':total_refill_requests,'users':user_order_count,'economic_calender':economic_calender}
            return Response({'status':'success','message':'retreived data successfully','data':data},status=200)
        except Exception as e:
            return Response({'error':str(e),'status':'failure','message':'insertion failed'})

@csrf_exempt
def populate(request):
     if request.method == 'POST':
         try:
                with open(file_path, 'r') as file:
                    medic_list = json.load(file)['medications']
                for item in medic_list:
                    medication=Medications(name=item['name'], category=item['category'],dosage_form=item['dosage_form'],brand_name=item['brand_name'],concentration=item['concentration'],price=item['price'],refill_requests=0,refills_issued=0,image_url=item['image_url'])
                    medication.save()
                return JsonResponse({'status':'success',"message": "data inserted"}, status=200)
         except Exception as e:
            return JsonResponse({"error": str(e),'data':medic_list}, status=500)

