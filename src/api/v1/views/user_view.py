from api.v1.serealizers.user_serializer import CustomUserSerializer, LoginSerializer, ForgotPasswordSerializer, GetAllUserSerializer,ResetPasswordSerializer, MeApiSerializer
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
from ..peginations.user_pagination import UserPagination

class SignUpAPIView(APIView):
    """
    API view to handle user registration.
    Permissions:
        - Allows any user to create a new account.
    Methods:
        - post(request): Handles user registration by validating and saving user data.
    Request Body:
        {
            "email": "admin@gmail.com",
            "password": "addmin123",
        }
    Responses:
        - 201 Created: Returns the newly created user data.
        - 400 Bad Request: Returns validation errors if the input is invalid.
    """
    permission_classes = [AllowAny]            
    
    def post(self, request):    
        """
        Handles user registration.
        - Validates the input data.
        - Saves the user if data is valid.
        - Returns appropriate response.
        Returns:
            Response: JSON response with user data or error messages.
        """       
        serializer = CustomUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
    
    
    
class UserGetUpdateViewSet(ModelViewSet):
    """
    ViewSet for retrieving and updating user details.
    Permissions:
        - Only authenticated users can access this view.
    Authentication:
        - Uses Token Authentication.
    Attributes:
        queryset (QuerySet): Retrieves all users from the CustomUser model.
        serializer_class (Serializer): Uses CustomUserSerializer for serialization.
        permission_classes (list): Ensures only authenticated users can access the view.
        authentication_classes (list): Uses TokenAuthentication for user authentication.
    Supported Actions:
        - Retrieve a user's details.
        - Update a user's information.
    Example Usage:
        - GET /users/ -> Retrieve all users.
        - GET /users/{id}/ -> Retrieve a specific user.
        - PUT /users/{id}/ -> Update user details.
        - PATCH /users/{id}/ -> Partially update user details.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = UserPagination
    
    
    
    
class LoginAPIView(APIView):
    """
    API endpoint for user login.
    Permissions:
        - Allows any user to access this view (no authentication required).
    Attributes:
        permission_classes (list): Allows unrestricted access to the login API.
    Methods:
        post(request):
            - Validates the provided credentials using `LoginSerializer`.
            - If valid, retrieves or creates an authentication token for the user.
            - Returns the authentication token and a success message.
            - If invalid, returns validation errors.
    Example Usage:
        - POST /login/
        - Request Body: {"email": "user@example.com", "password": "securepassword"}
        - Response (Success): {"token": "abc123xyz", "message": "Login successful"}
        - Response (Failure): {"error": "Invalid credentials"}
    """
    permission_classes = [AllowAny]
    
    def post(self, request):     
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)      
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       # return error in response
    
    
    
class ForgotPasswordAPIView(APIView):
    """
    API endpoint to handle forgot password functionality.
    Methods:
        post(request):
            - Accepts an email address from the request data.
            - Validates the email using `ForgotPasswordSerializer`.
            - Retrieves the user associated with the provided email.
            - Generates a password reset token and sends an email with a reset link.
            - Returns a success message if the process is completed successfully.
            - Returns an error response if the email is invalid or not found.
    Example Usage:
        - POST /forgot-password/
        - Request Body: {"email": "user@example.com"}
        - Response (Success): {"message": "Password reset link is sent to your email."}
        - Response (Failure): {"email": ["User with this email does not exist."]}
    """
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
    """
    API endpoint to reset the user's password using a token.
    Methods:
        post(request, token):
            - Retrieves the user ID from the cache using the provided token.
            - If the token is invalid or expired, returns an error response.
            - Fetches the corresponding user from the database.
            - Validates the new password using `ResetPasswordSerializer`.
            - Updates and hashes the user's password.
            - Deletes the token from the cache after a successful reset.
            - Returns a success message upon successful password reset.
    Example Usage:
        - POST /reset-password/{token}/
        - Request Body: {"new_password": "new_secure_password", "confirm_password": "new_secure_password"}
        - Response (Success): {"message": "Password reset successfully."}
        - Response (Failure): {"error": "Invalid or expired token."}
    Note:
        - The token is generated and stored in the cache during the forgot password process.
        - The token expires after a set duration (e.g., 1 hour).
    """
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
    
    """
    API endpoint to log out a user by deleting their authentication token.
    Methods:
        post(request):
            - Ensures the request is authenticated using TokenAuthentication.
            - Retrieves the user's token from the database.
            - Deletes the token to log out the user.
            - Returns a success message upon successful logout.
            - If the token does not exist, returns an error response.
    Authentication:
        - Requires TokenAuthentication.
        - Only authenticated users can access this endpoint.
    Example Usage:
        - POST /logout/
        - Headers: {"Authorization": "Token user_token"}
        - Response (Success): {"message": "Logout successful"}
        - Response (Failure): {"error": "Token not found"}
    Note:
        - Logging out removes the user's authentication token, requiring re-login to obtain a new token.
    """
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
    """
    API endpoint to manage user accounts, accessible only by admin users.
    Features:
        - List all users.
        - Retrieve a specific user.
        - Create a new user.
        - Update an existing user.
        - Delete a user.
    Authentication:
        - Requires TokenAuthentication.
        - Only authenticated admin users can access this endpoint.
    Methods:
        create(request, *args, **kwargs):
            - Calls the parent `create` method to add a new user.
            - Returns a success response upon user creation.

        destroy(request, *args, **kwargs):
            - Calls the parent `destroy` method to delete a user.
            - Returns a success response upon user deletion.
    Example Usage:
        - GET /users/ (Retrieve all users)
        - POST /users/ (Create a new user)
        - PUT/PATCH /users/{id}/ (Update user details)
        - DELETE /users/{id}/ (Delete a user)
    Responses:
        - 200 OK for successful operations.
        - 201 Created for successful user creation.
        - 204 No Content for successful deletion.
        - 403 Forbidden if a non-admin user tries to access.
    Notes:
        - This viewset inherits from Django REST Framework's `ModelViewSet`,
          which provides full CRUD operations.
    """
    queryset = CustomUser.objects.all()
    serializer_class = GetAllUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]              # Only admin can access
    pagination_class = UserPagination
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'User created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

class MeAPIView(APIView):
    """
    API endpoint for retrieving authenticated user's profile.
    Authentication:
        - Requires Token Authentication.
        - Only accessible to authenticated users.
    Methods:
        - GET: Retrieve the logged-in user's details.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    """
        Retrieve the authenticated user's details.
        Returns:
            Response (200 OK): A JSON representation of the user profile.
            Response (401 Unauthorized): If the user is not authenticated.
        Example Response:
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "gender": "Male",
            "status": "Active",
            "image": "http://example.com/media/profile.jpg",
            "designation": "Software Engineer"
        }
        """

    def get(self, request):
        """Retrieve logged-in user details"""
        serializer = MeApiSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)




  
    

    

    
