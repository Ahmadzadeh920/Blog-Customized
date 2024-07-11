from django.core import exceptions
from django.core.mail import EmailMessage
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import ( RegistrationSerializer,
                          CustomeAuthTokenSerializer ,
                          ResetPasswordRequestSerializer,
                          ResetPasswordSerializer, 
                          ChangePasswordSerializer, 
                          Customized_TOKEN_OBTAIN_PAIR_SERIALIZER
                          )
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


from ...models import CustomUser, PasswordReset, Profile
import os



    #serializer_class = RegistrationSerializer
class RegisterationApiview(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer= RegistrationSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "email":serializer.validated_data["email"],
                }
            return Response(data= data , status= status.HTTP_200_OK)
        return Response(status= status.HTTP_400_BAD_REQUEST , data = {'data': serializer.errors})
    


# this class is customized login
class ObtainAuthToken_Customized(ObtainAuthToken):
    serializer_class = CustomeAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })
        
        
        
# this class is customized logout 
class AuthDiscardedToken(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        # simply delete the token to force a login
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status= status.HTTP_400_BAD_REQUEST , data = {'detail': "you do not log in"})
        
        
        



# this class is customized reset password 
class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()
        if not user: 
             return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()
            reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"
            subject = "this email for reset password"
            message = "plase click this linl for reseting password"+ reset_url
            from_email = "f.ahmadzadeh@gmail.com"
            email = EmailMessage(subject, message, from_email, email)
            email.send()
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        
        
# this class for resting passwork when click the links
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(email=reset_obj.email).first()
        if not user:
             return Response({'error':'No user found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user.set_password(request.data['new_password'])
            user.save()
            
            reset_obj.delete()
            return Response({'success':'Password updated'}, status= status.HTTP_205_RESET_CONTENT)
 
 
 # this class for changing password           
class ChangePasswordView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    
# this class for custimized JWT   
class CustimizedTokenObtainPairView(TokenObtainPairView):
        serializer_class = Customized_TOKEN_OBTAIN_PAIR_SERIALIZER
    
class ProfileAPIView():
    pass