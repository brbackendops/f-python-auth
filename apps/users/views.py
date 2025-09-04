from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

# rest framework
from rest_framework import generics , status , serializers
from rest_framework.response import Response

# jwt
from rest_framework_simplejwt.views import TokenObtainPairView

# user serializer
from .serializer import JwtTokenObtainSerializer , UserSerializer
from .utils.error import ModelAlreadyExists

# rate limiter
from .utils.limiter import FixedRateLimiter

rate_limiter = FixedRateLimiter()

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    User = get_user_model()
    
    def perform_create(self,serializer):
        if self.User.objects.filter(email=serializer.validated_data.get("email")).exists():
            raise ModelAlreadyExists("user with these email already exists")  
        
        serializer.save()
    
    @rate_limiter
    def post(self,request,*args,**kwargs):
        try:
            body = request.data
            serializer = self.get_serializer(data=body)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        except ModelAlreadyExists as err:
            return Response(
                {
                    "status": "error",
                    "error_name": err.__class__.__name__,
                    "error": str(err)
                },
                status=status.HTTP_409_CONFLICT
            )            
        except serializers.ValidationError as err:
            return Response(
                {
                    "status": "error",
                    "error_name": err.__class__.__name__,
                    "error": err.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as err:
            print(err.__class__.__name__, str(err))
            return Response(
                {
                    "status": "error",
                    "error_name": err.__class__.__name__,
                    "error": str(err)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class JwtTokenObtainView(TokenObtainPairView):
    serializer_class = JwtTokenObtainSerializer
    
    
    def post(self,request,*args,**kwargs):
        try:
            return super().post(request,*args,**kwargs)
        except ObjectDoesNotExist as err:
            return Response(
                {
                    "status": "error",
                    # "error_name": err.__class__.__name__,
                    "error": "Invalid email or password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )    
        except serializers.ValidationError as err:
            return Response(
                {
                    "status": "error",
                    "error_name": err.__class__.__name__,
                    "error": err.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )                    
        except Exception as err:
            return Response(
                {
                    "status": "error",
                    "error_name": err.__class__.__name__,
                    "error": str(err)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )            
    