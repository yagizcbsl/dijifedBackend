from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework import generics, status
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def sendVerificationMail(request):
    try:
        user = request.user
        mailAddress = user.email
        fields = extraUserFields.objects.get(user=user)
        verificationCode = fields.verificationCode
        email = EmailMessage(
            'Verification Code Dijifed Business Card',
            'Verification code: ' + verificationCode,
            settings.EMAIL_HOST_USER,
            [mailAddress],
            )
        email.fail_silenty = False
        email.send()
        return(Response(status=201))
    except:
        return(Response(status=400))
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def verifyEmail(request):
    try:
        user = request.user
        fields = extraUserFields.objects.get(user=user)
        verificationCode = fields.verificationCode
        data = JSONParser().parse(request)
        sentCode = data["code"]
        if sentCode == verificationCode:
            fields.isVerified = True
            fields.save()
            return(Response(status=201))
        return(Response(status=400))
    except:
        return(Response(status=400))
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['name'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@csrf_exempt
@api_view(['POST'])
def signup(request):
    form = SignUpForm(request.data)
    if form.is_valid():
        user = form.save()
        extraField = extraUserFields.objects.create(user=user)
        return JsonResponse({'message': 'User created successfully.'},status=200)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    try:
        profile = ProfileTable.objects.get(user=user)
    except:
        return HttpResponse(status=404)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data,status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExtraField(request):
    user = request.user
    try:
        field = extraUserFields.objects.get(user=user)
    except:
        return HttpResponse(status=404)
    serializer = FieldSerializer(field)
    return Response(serializer.data,status=201)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateFields(request):
    user = request.user
    field = extraUserFields.objects.get(user=user)
    data = JSONParser().parse(request)
    serializer = FieldSerializer(field, data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    profile = ProfileTable.objects.get(user=user)
    data = JSONParser().parse(request)
    serializer = ProfileSerializer(profile, data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfilePicture(request):
    parser_classes = (MultiPartParser, FormParser)
    serializers = ProfilePictureSerializer
    
    user = request.user
    profile = ProfileTable.objects.get(user=user)
    serializer = ProfilePictureSerializer(profile,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=200)
    return JsonResponse(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateCoverPage(request):
    parser_classes = (MultiPartParser, FormParser)
    serializers = CoverPageSerializer
    
    user = request.user
    profile = ProfileTable.objects.get(user=user)
    serializer = CoverPageSerializer(profile,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=200)
    return JsonResponse(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def initializeProfile(request,userID):
    try:
        profile = ProfileTable.objects.get(userID=userID)
    except:
        return HttpResponse(status=404)
    data = JSONParser().parse(request)
    serializer = ProfileSerializer(profile, data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=200)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def profile_list(request):  
    """
    List all profiles, or create a new profile.
    """
    if request.method == 'GET':
        profiles = ProfileTable.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)
    

@csrf_exempt
@api_view(['GET'])
def profile_detail(request, userID):
    """
    Retrieve, update or delete a profile object.
    """
    try:
        profile = ProfileTable.objects.get(userID=userID)
    except ProfileTable.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)

    # elif request.method == 'PUT':
    #     data = JSONParser().parse(request)
    #     serializer = ProfileSerializer(profile, data=data,partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data,status=201)
    #     return JsonResponse(serializer.errors, status=400)

    # elif request.method == 'DELETE':
    #     profile.delete()
    #     return HttpResponse(status=204)