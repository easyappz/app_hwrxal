from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from api.models import User, Role, RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for Role model.
    Used for nested representation in UserSerializer.
    """
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles:
    - Email and password validation
    - Password confirmation matching
    - Password strength validation
    - Automatic role assignment (default 'user' role)
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Password must meet security requirements"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Must match the password field"
    )
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate_email(self, value):
        """
        Validate that email is not already registered.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    def validate_password(self, value):
        """
        Validate password strength using Django's password validators.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
        """
        Validate that password and password_confirm match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Passwords do not match."
            })
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user with hashed password and default 'user' role.
        """
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop('password_confirm')
        
        # Extract password to hash it properly
        password = validated_data.pop('password')
        
        # Create user instance
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Assign default 'user' role
        try:
            default_role = Role.objects.get(name='user', is_active=True)
            user.roles.add(default_role)
        except Role.DoesNotExist:
            # If default role doesn't exist, user is created without role
            # This should be handled by create_default_roles management command
            pass
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login/authentication.
    
    Validates user credentials (email and password).
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """
        Validate user credentials.
        """
        email = attrs.get('email', '').lower()
        password = attrs.get('password')
        
        if email and password:
            # Authenticate user
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.",
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    "User account is disabled.",
                    code='authorization'
                )
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'.",
                code='authorization'
            )
        
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    
    Used for:
    - Displaying user information
    - User profile retrieval
    
    Extensibility:
    - Add new fields to the 'fields' list as you extend the User model
    - Example: 'phone_number', 'avatar', 'bio', 'birth_date'
    """
    roles = RoleSerializer(many=True, read_only=True)
    
    # ### EXTENSIBILITY SECTION ###
    # Add serializer fields for new User model fields here
    # Examples:
    # phone_number = serializers.CharField(read_only=True)
    # avatar = serializers.ImageField(read_only=True)
    # bio = serializers.CharField(read_only=True)
    # ### END EXTENSIBILITY SECTION ###
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'roles',
            'date_joined',
            'is_active',
            # ### Add new fields here when extending ###
            # 'phone_number',
            # 'avatar',
            # 'bio',
            # ### END ###
        ]
        read_only_fields = [
            'id',
            'email',
            'roles',
            'date_joined',
            'is_active',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    
    Excludes sensitive fields like email and password.
    Users should use separate endpoints for changing those.
    
    Extensibility:
    - Add new editable fields as you extend the User model
    - Example: 'phone_number', 'bio', 'birth_date'
    """
    
    # ### EXTENSIBILITY SECTION ###
    # Add serializer fields for new editable User model fields here
    # Examples:
    # phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    # bio = serializers.CharField(required=False, allow_blank=True)
    # birth_date = serializers.DateField(required=False, allow_null=True)
    # ### END EXTENSIBILITY SECTION ###
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            # ### Add new editable fields here when extending ###
            # 'phone_number',
            # 'bio',
            # 'birth_date',
            # ### END ###
        ]
    
    def validate_first_name(self, value):
        """
        Validate first name (add custom validation if needed).
        """
        return value.strip()
    
    def validate_last_name(self, value):
        """
        Validate last name (add custom validation if needed).
        """
        return value.strip()


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting password reset.
    
    Accepts email and triggers password reset process.
    Note: Should always return success even if email doesn't exist
    to prevent user enumeration attacks.
    """
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """
        Normalize email to lowercase.
        """
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset with token.
    
    Validates:
    - Token validity
    - New password strength
    - Password confirmation matching
    """
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_new_password(self, value):
        """
        Validate new password strength.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
        """
        Validate that new password and confirmation match.
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': "Passwords do not match."
            })
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password for authenticated users.
    
    Requires:
    - Current password verification
    - New password validation
    - Password confirmation matching
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        """
        Validate that old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        """
        Validate new password strength.
        """
        try:
            validate_password(value, user=self.context['request'].user)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
        """
        Validate that new password and confirmation match,
        and that new password is different from old password.
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': "Passwords do not match."
            })
        
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'new_password': "New password must be different from old password."
            })
        
        return attrs
    
    def save(self, **kwargs):
        """
        Change the user's password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer for refreshing access tokens using refresh token.
    
    This is a custom implementation that works with our RefreshToken model.
    If you prefer to use djangorestframework-simplejwt's default behavior,
    you can use their TokenRefreshSerializer directly.
    """
    refresh = serializers.CharField(required=True)
    
    def validate_refresh(self, value):
        """
        Validate that refresh token exists and is valid.
        """
        try:
            refresh_token = RefreshToken.objects.get(token=value)
            
            if not refresh_token.is_valid():
                raise serializers.ValidationError("Refresh token is invalid or expired.")
            
            # Store for later use in view
            self.context['refresh_token_obj'] = refresh_token
            
        except RefreshToken.DoesNotExist:
            raise serializers.ValidationError("Refresh token not found.")
        
        return value


class MessageSerializer(serializers.Serializer):
    """
    Generic message serializer for simple responses.
    """
    message = serializers.CharField(max_length=200)
    timestamp = serializers.DateTimeField(read_only=True)
