import operator
import random

from django.contrib import auth
from django.contrib.auth.models import User as SuperUser
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView  # Create your views here.

from SerotoninRush.models import *
from SerotoninRush.serializers import *


class RegisterUser(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            date_of_birth = request.POST['date_of_birth']
            phone = request.POST['phone']
            email = request.POST['email']
            status = request.POST['status']
            password = request.POST['password']
            # avatar = request.FILES['avatar']
        except:
            return JsonResponse({'message': 'error while receiving data'})
        #   Creating Super user to authenticate with the given data
        try:
            user = SuperUser.objects.create(username=username, is_active=True)
            user.set_password(password)
            user.save()
        except:
            return JsonResponse({'message': 'user already exist'})
        #   creating User with the given Data
        try:
            User.objects.create(username=user, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                                phone=phone, email=email, status=status)
        except:
            return JsonResponse({'message': 'error while creating user'})
        return JsonResponse({'message': 'User created'})


class Login(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        global consumer, token, user_obj
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return JsonResponse({'message': 'error while receiving data'})
        #    authenticate user with the given data
        try:
            user = auth.authenticate(username=username, password=password)
        except:
            return JsonResponse({'message': 'Credentials are not correct !'})
        #   creating User with the given Data

        try:
            if user is not None:
                consumer = User.objects.get(username=user)
                consumer = UserSerializer(consumer).data
                token_count = Token.objects.filter(user=user)
                if len(token_count) > 0:
                    Token.objects.get(user=user).delete()
                    token = Token.objects.create(user=user)
                else:
                    token = Token.objects.create(user=user)
            else:
                return JsonResponse({'message': 'Credentials are not correct !'})
        except:
            return JsonResponse({'message': 'error while getting user info'})
        return JsonResponse({'message': 'success', 'user_obj': consumer, 'username': username, 'token': token.key})


class UpdateInfo(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        global consumer
        try:
            print('here!')
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            date_of_birth = request.POST['date_of_birth']
            email = request.POST['email']
            phone = request.POST['phone']
            username = request.POST['username']
        except:
            return JsonResponse({'message': 'error while receiving data'})
        try:
            print(username)
            user = SuperUser.objects.get(username=username)
            consumer = User.objects.get(username=user)

        except:
            return JsonResponse({'message': 'error while finding user'})
        try:
            consumer.first_name = first_name
            consumer.last_name = last_name
            consumer.date_of_birth = date_of_birth
            consumer.email = email
            consumer.phone = phone
            consumer.save()
            return JsonResponse({'message': 'success'})
        except:
            return JsonResponse({'message': 'error while receiving data'})


class AllMeals(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]

    serializer_class = MealSerializer
    queryset = Meal.objects.filter(status='Approved')


class AddReaction(viewsets.ReadOnlyModelViewSet):
    queryset = UserReaction.objects.all()
    serializer_class = UserReactionSerializer

    def post(self, request):
        try:
            user_name = request.POST.get('username')
            meals = request.POST.get('meals')
            reaction = request.POST.get('reaction')
            meals_id = []
            for i in meals:
                if i != '[' and i != ']' and i != ',':
                    meals_id.append(int(i))
            print(u'the username is : {}, meals : {}, reaction: {}'.format(user_name, meals, reaction))
        except:
            return JsonResponse({'message': 'error while receiving data'})
        # try:
        superuser = SuperUser.objects.get(username=user_name)
        user = User.objects.get(username=superuser)
        for i in meals_id:
            meal = Meal.objects.get(pk=i)
            UserReaction.objects.create(user=user, meal=meal, reaction=int(reaction))
        # except:
        #     return JsonResponse({'message': 'error while adding meals'})
        return JsonResponse(
            {'message': u'the username is : {}, meals : {}, reaction: {}'.format(user_name, meals, reaction)})


class NewsAPI(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class GetUserInfoViaToken(viewsets.ReadOnlyModelViewSet):
    def post(self, request):
        try:
            token = request.POST.get('token')
            user = Token.objects.get(key=token).user
            consumer = User.objects.get(username=user)
            consumer = UserSerializer(consumer).data
            return JsonResponse({'message': 'success', 'user_obj': consumer, 'username': user.username, 'token': token})
        except:
            return JsonResponse({'message': 'false'})


class PendingMeals(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            pending_meals = Meal.objects.filter(status='Pending').values()
            return JsonResponse({'message': 'success', 'pending_meals': list(pending_meals)})
        except:
            return JsonResponse({'message': 'false'})


class ChangeMealStatus(APIView):
    def post(self, request):
        try:
            meal = Meal.objects.get(pk=request.POST.get('pk'))
            new_state = request.POST.get('state')
            meal.status = new_state
            meal.save()
            return JsonResponse({'message': 'success'})
        except:
            return JsonResponse({'message': 'something went wrong'})


class correlation(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request):
        # getting the user by his token ..
        try:
            user_token = request.POST.get('token')
            token_object = Token.objects.get(key=user_token)
            user = token_object.user
            user = User.objects.get(username=user)
        except Exception as e:
            print('error while getting user {}'.format(e))
            return JsonResponse({'message': 'Error'})
        # getting the user entries ..
        reactions = UserReaction.objects.filter(user=user).values()
        if len(reactions) < 10:
            return JsonResponse({'message': 'error', 'value': 'sorry, you dont have enough data'})
        reactions = list(reactions)
        points = {'fats': 0, 'protein': 0, 'carbohydrate': 0, 'calories': 0}
        for meal in reactions:
            meal_object = Meal.objects.get(id=meal['meal_id'])
            # print(meal_object)
            meal['protein'] = meal_object.protein
            meal['carbohydrate'] = meal_object.carbohydrate
            meal['calories'] = meal_object.calories
            meal['fats'] = meal_object.fats
        for meal in reactions:
            if meal['fats'] > meal['protein']:
                if meal['fats'] > meal['carbohydrate']:
                    if meal['fats'] > meal['calories']:
                        points['fats'] += meal['reaction']
            elif meal['protein'] > meal['carbohydrate']:
                if meal['protein'] > meal['calories']:
                    points['protein'] += meal['reaction']
            elif meal['carbohydrate'] > meal['calories']:
                points['carbohydrate'] += meal['reaction']
            else:
                points['calories'] += meal['reaction']
        highest_value = max(points, key=points.get)
        if highest_value == 'fats':
            meals = Meal.objects.filter(fats__gte=30)
        elif highest_value == 'carbohydrate':
            meals = Meal.objects.filter(carbohydrate__gte=25)
        elif highest_value == 'protein':
            meals = Meal.objects.filter(protein__gte=20)
        elif highest_value == 'calories':
            meals = Meal.objects.filter(calories__gte=80)
        meals = list(meals.values())
        meals = meals[:30]
        return JsonResponse({'message': 'success', 'best_for_you': highest_value, 'meals': meals})
