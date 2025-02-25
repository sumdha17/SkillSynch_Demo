from rest_framework import serializers
from user.models import CustomUser
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False,
        validators=[RegexValidator(r'^[98]\d{9}$', message="Phone number must start with 9 or 8 and be exactly 10 digits long."),]
    )
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name",  "type", "email", "status","phone_number", "password"]
        extra_kwargs = {'password': {'write_only': True}}             #
        
    def create(self, validated_data):
        """Create user with hashed password"""
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    
    def update(self, instance, validated_data):
        """Update user details with password handling"""
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)  # Hashes the password before saving
            else:
                setattr(instance, attr, value)    # Dynamically updates other fields
        instance.save()          # Saves the updated instance to the database
        return instance             # Returns the updated user instance
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate user
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data
    
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator()])

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account exists for this email.")
        return value
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate_password(self, value):
        if "new_password" != "confirm_password":
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return value
    
    
    
class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "username", "status","phone_number","type"]
            
    
