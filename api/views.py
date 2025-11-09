from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken as JWTRefreshToken
from .serializers import (
    MessageSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    TokenRefreshSerializer,
)
from .models import User, RefreshToken, PasswordResetToken


class HelloView(APIView):
    """
    A simple API endpoint that returns a greeting message.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: MessageSerializer}, 
        description="Get a hello world message"
    )
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        serializer = MessageSerializer(data)
        return Response(serializer.data)


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    Creates a new user account with the default 'user' role.
    Does not automatically log in the user - they must use the login endpoint.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                description="User successfully registered"
            ),
            400: OpenApiResponse(description="Validation error")
        },
        description="Register a new user account. Creates user with default 'user' role."
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(
            {
                "message": "User registered successfully. Please log in.",
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )


class UserLoginView(APIView):
    """
    API endpoint for user login/authentication.
    
    Validates user credentials and returns JWT access and refresh tokens.
    Creates a refresh token record in the database for token management.
    """
    permission_classes = [AllowAny]
    
    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "access": {"type": "string"},
                        "refresh": {"type": "string"},
                        "user": {"type": "object"}
                    }
                },
                description="Login successful"
            ),
            400: OpenApiResponse(description="Invalid credentials")
        },
        description="Authenticate user and return JWT tokens"
    )
    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens using Simple JWT
        jwt_refresh = JWTRefreshToken.for_user(user)
        access_token = str(jwt_refresh.access_token)
        refresh_token_str = str(jwt_refresh)
        
        # Store the JWT refresh token in database for tracking purposes
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = self.get_client_ip(request)
        
        # Calculate expiration time based on Simple JWT settings
        from django.conf import settings
        refresh_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
        expires_at = timezone.now() + refresh_lifetime
        
        # Create token record with the actual JWT token string
        RefreshToken.objects.create(
            user=user,
            token=refresh_token_str,
            expires_at=expires_at,
            user_agent=user_agent or "",
            ip_address=ip_address
        )
        
        # Return tokens and user data
        user_serializer = UserSerializer(user)
        
        return Response(
            {
                "access": access_token,
                "refresh": refresh_token_str,
                "user": user_serializer.data
            },
            status=status.HTTP_200_OK
        )


class TokenRefreshView(APIView):
    """
    API endpoint for refreshing access tokens.
    
    Accepts a refresh token and returns a new access token.
    Uses Simple JWT for token validation and generation.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "access": {"type": "string"},
                        "refresh": {"type": "string", "nullable": True}
                    }
                },
                description="Token refreshed successfully"
            ),
            400: OpenApiResponse(description="Invalid or expired refresh token")
        },
        description="Refresh access token using refresh token"
    )
    def post(self, request):
        refresh_token_str = request.data.get('refresh')
        
        if not refresh_token_str:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Use Simple JWT to validate and refresh the token
            jwt_refresh = JWTRefreshToken(refresh_token_str)
            new_access_token = str(jwt_refresh.access_token)
            
            response_data = {
                "access": new_access_token
            }
            
            # If token rotation is enabled, Simple JWT will blacklist the old token
            # and we should return the new refresh token
            from django.conf import settings
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                # Get the new refresh token after rotation
                new_refresh_token = str(jwt_refresh)
                response_data["refresh"] = new_refresh_token
                
                # Update our database record with the new token
                try:
                    old_token = RefreshToken.objects.get(token=refresh_token_str)
                    # Mark old token as revoked
                    old_token.revoke()
                    
                    # Create new token record
                    refresh_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
                    expires_at = timezone.now() + refresh_lifetime
                    
                    RefreshToken.objects.create(
                        user=old_token.user,
                        token=new_refresh_token,
                        expires_at=expires_at,
                        user_agent=old_token.user_agent,
                        ip_address=old_token.ip_address
                    )
                except RefreshToken.DoesNotExist:
                    # Token not in our database, but valid JWT - this is ok
                    pass
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserLogoutView(APIView):
    """
    API endpoint for user logout.
    
    Revokes the provided refresh token, effectively logging out the user
    from the current device/session.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "refresh": {"type": "string"}
            },
            "required": ["refresh"]
        },
        responses={
            200: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                description="Logout successful"
            ),
            400: OpenApiResponse(description="Invalid refresh token")
        },
        description="Logout user by revoking refresh token"
    )
    def post(self, request):
        refresh_token_str = request.data.get('refresh')
        
        if not refresh_token_str:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Blacklist the token using Simple JWT
            jwt_refresh = JWTRefreshToken(refresh_token_str)
            jwt_refresh.blacklist()
            
            # Also revoke it in our database if it exists
            try:
                refresh_token = RefreshToken.objects.get(token=refresh_token_str)
                refresh_token.revoke()
            except RefreshToken.DoesNotExist:
                # Token not in our database, but blacklisted in JWT - this is ok
                pass
            
            return Response(
                {"message": "Logout successful."},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(generics.RetrieveAPIView):
    """
    API endpoint to get current authenticated user's data.
    
    Returns user profile information including roles and permissions.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Authentication required")
        },
        description="Get current authenticated user information"
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def get_object(self):
        return self.request.user


class UpdateUserView(generics.UpdateAPIView):
    """
    API endpoint to update current user's profile.
    
    Allows updating only specific fields (first_name, last_name, etc.).
    Email and password changes require separate endpoints.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    
    @extend_schema(
        request=UserUpdateSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Authentication required")
        },
        description="Update current user profile (partial update)"
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return updated user data
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    
    def get_object(self):
        return self.request.user


class PasswordResetRequestView(APIView):
    """
    API endpoint to request password reset.
    
    Accepts email and generates a password reset token.
    Always returns success to prevent user enumeration attacks.
    
    Note: In production, this should send an email with the reset link.
    For now, the token is stored in the database and can be retrieved for testing.
    """
    permission_classes = [AllowAny]
    
    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={
            200: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                description="Password reset request processed"
            )
        },
        description="Request password reset. Always returns success to prevent user enumeration."
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        # Try to find user, but don't reveal if they exist
        try:
            user = User.objects.get(email=email, is_active=True)
            
            # Create password reset token
            ip_address = self.get_client_ip(request)
            reset_token = PasswordResetToken.create_token(
                user=user,
                ip_address=ip_address,
                expires_in_hours=24
            )
            
            # TODO: Send email with reset link
            # For now, token is stored in database
            # In production: send_password_reset_email(user, reset_token.token)
            
        except User.DoesNotExist:
            # Don't reveal that user doesn't exist
            pass
        
        # Always return success
        return Response(
            {
                "message": "If the email exists, a password reset link has been sent."
            },
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    """
    API endpoint to confirm password reset with token.
    
    Validates the reset token and sets the new password.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={
            200: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                description="Password reset successful"
            ),
            400: OpenApiResponse(description="Invalid or expired token")
        },
        description="Confirm password reset with token and set new password"
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token_str = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token_str)
            
            if not reset_token.is_valid():
                return Response(
                    {"detail": "Password reset token is invalid or expired."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.mark_as_used()
            
            # Optional: Revoke all user's refresh tokens for security
            RefreshToken.revoke_all_user_tokens(user)
            
            return Response(
                {"message": "Password has been reset successfully. Please log in with your new password."},
                status=status.HTTP_200_OK
            )
            
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"detail": "Invalid password reset token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(APIView):
    """
    API endpoint for authenticated users to change their password.
    
    Requires the user to provide their current password for verification.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                description="Password changed successfully"
            ),
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Authentication required")
        },
        description="Change password for authenticated user"
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Optional: Revoke all user's refresh tokens except current one
        # This logs out the user from all other devices
        RefreshToken.revoke_all_user_tokens(request.user)
        
        return Response(
            {"message": "Password changed successfully. Please log in again."},
            status=status.HTTP_200_OK
        )
