from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from django.contrib.auth import authenticate
from .utils.error import ModelAlreadyExists


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source='username',required=False,read_only=True)
    
    class Meta:
        model = User
        fields = ['id','name','email','created_at','first_name','last_name','password']
        read_only_fields = ['is_active','is_superuser','is_staff','created_at']
        extra_kwargs = {
            "email": {
                "validators": []
            },
            "password": {
                "write_only": True
            },
            "first_name": {
                "write_only": True,
            },
            "last_name": {
              "write_only": True,
            },
            "name": {
                "read_only": True
            },
            "pk": {
                "read_only": True
            },
            "created_at": {
                "read_only": True
            }
        }
    
    def validate(self,data):

        if data['email'] is None:
            raise serializers.ValidationError('email not found')
        
        if data['password'] is None:
            raise serializers.ValidationError('password not found')        
        
        if data['first_name'] is None:
            raise serializers.ValidationError('first_name not found')
        
        if data['last_name'] is None:
            raise serializers.ValidationError('last_name not found')
        
        return data

    def create(self,data):
        try:

            user_exists = User.objects.filter(email=data.get('email')).exists()
            if user_exists:
                raise ModelAlreadyExists("user with these email already exists")
            
            user = User.objects.create(**data)
            return user
        
        except Exception as err:
            raise Exception(str(err))

class JwtTokenObtainSerializer(TokenObtainPairSerializer):
    """
        this library uses default django authentication , so this simple jwt
        expects username field. as we used email as default field for authentication
        we need to override the validate method here.
    """
    
    email = serializers.EmailField(required=True)
    password = PasswordField()
    
    username_field = 'email'
    
    
    def validate_email(self,data):
        if not data:
            raise serializers.ValidationError("email is required")
        return data
    
    
    def validate_password(self,data):
        if not data:
            raise serializers.ValidationError("password is required")
        return data
        
    
    def validate(self,attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        if not email or not password:
            raise serializers.ValidationError("email and password fields are required")            
        

        user = authenticate(request=self.context.get('request'),email=email,password=password)
        if not user:
            raise User.DoesNotExist("user not found")
            
        if not user.is_active:
            raise serializers.ValidationError("user is not active")            
        
        refresh_token = self.get_token(user)
        return {
            'token': str(refresh_token.access_token),
            'refresh_token': str(refresh_token),
        }
            
    
    @classmethod
    def get_token(cls, user):
        """
            from source code, it is clear the token can be Modifiable
            as it is using __setitem__ & __getitem__
        """
        
        token = super().get_token(user)
        
        token['email'] = user.email
        token['username'] = user.username
        token['user_id'] = user.id
        
        return token