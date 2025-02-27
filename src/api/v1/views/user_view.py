from api.v1.serealizers.user_serializer import CustomUserSerializer, LoginSerializer, ForgotPasswordSerializer, GetAllUserSerializer,ResetPasswordSerializer, UserAssigneeSerializer
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from api.v1.scripts.email_fun import send_mail_to_reset_password
from django.contrib.auth.hashers import make_password
from django.core.cache import cache


class SignUpAPIView(APIView):
    '''
    Request=
    {
    "first_name" : "user1",
    "last_name" : "aaa",
    "email" : "user1@gmail.com",
    "type" : 7,
    "status" : 4
    }        # if phone num not given then it set null and can create user without password
    '''
    permission_classes = [AllowAny]             # any user can create new account
    
    def post(self, request):            # handels user registration
        serializer = CustomUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)         #return success msg in response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       # return error in response
    
    
    
class UserGetUpdateViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):     
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)      
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       # return error in response
    
    
    
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            subject = "Reset Your Password"
            message = f"Hi..Click On given Link to Reset Password."
            send_mail_to_reset_password(user.email, message, subject, user)
            return Response({"message": "Password reset link is sent to your email."},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordAPIView(APIView):
    def post(self, request, token):
        user_id = cache.get(token)   # Retrieve user ID using the token
        if not user_id:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.password = make_password(new_password)            # Hash and save password
            user.save()
            # Remove token after successful reset
            cache.delete(token)
            
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        
class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]          # Ensure token authentication
    permission_classes = [IsAuthenticated]             # Only logged-in users can log out

    def post(self, request):
        # Get the user's token
        try:
            token = Token.objects.get(user=request.user)
            token.delete()         # Delete the token
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class GetAllUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GetAllUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]              # Only admin can access
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'User created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    
    
class AddAssigneeUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserAssigneeSerializer
    authentication_classes = []
    permission_classes = []  
    
    

    
