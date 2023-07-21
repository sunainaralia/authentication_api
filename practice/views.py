from rest_framework.response import Response
from rest_framework import status
from practice.serializers import UserSerializer,LoginSerializer,ProfileSerializer,ChangePasswordSerializer,SendResetPasswordEmailSerializer,UserResetPasswordSerializer
from rest_framework.views import APIView
from .renderers import UserRenderers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistration(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request,format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'msg':'registration succesfull','token':token},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request,format=None):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get("email")
            password=serializer.data.get("password")
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'msg':'login user successfully','token':token},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['email and password are not valid']}},status=status.HTTP_404_NOT_FOUND)
class UserProfile(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
class UserChangePassword(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'user password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class SendPasswordResetEmail(APIView):
        renderer_classes=[UserRenderers]
        def post(self, request, **kwargs):
            serializer=SendResetPasswordEmailSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                return Response({'msg':'password reset link is sent to your registered email'},status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        
        
class ResetPassword(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request,uid,token,**kwargs):
        serializer=UserResetPasswordSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset successully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


            
