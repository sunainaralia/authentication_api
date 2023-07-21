from practice.utils import Util
from practice.models import User
from rest_framework import serializers
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class UserSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'})
    class Meta:
        model=User
        fields=['email','name','tc','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self,data):
        password=data.get('password')
        password2=data.get('password2')
        if password!=password2:
            raise serializers.ValidationError('password does not match')
        return data
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']
class ChangePasswordSerializer(serializers.Serializer):
    password1=serializers.CharField(style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password1','password2']
    def validate(self, attrs):
        password1=attrs.get('password1')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password1!=password2:
            raise serializers.ValidationError("password and confirm password are not matched") 
        user.set_password(password1)
        user.save()
        return attrs
class SendResetPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print(link)
            body='click following link to reset your password'+link
            data={
                'subject':'Reset your password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("this email is not registered")
class UserResetPasswordSerializer(serializers.Serializer):
    password1=serializers.CharField(style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password1','password2']
    def validate(self, attrs):
        try:
            password1=attrs.get('password1')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if password1!=password2:
                raise serializers.ValidationError("password and confirm password are not matched") 
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("token is expired or not valid")
            user.set_password(password1)
            user.save()
            return attrs
        except:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("token is expired or not valid")


