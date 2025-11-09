# Django API Boilerplate - LLM Modification Guide

## Project Overview

This project uses Python 3.12.

This is a Django REST API boilerplate with built-in authentication system using:
- **Django**: Web framework
- **Django REST Framework (DRF)**: API functionality
- **drf-spectacular**: OpenAPI 3.0 schema generation
- **djangorestframework-simplejwt**: JWT authentication

There are also optional dependencies suggested by DRF installed that you can use:
- django-filter
- django-guardian

Always consider used libraries versions from requirements.txt to use for gathering actual docs if needed.
Please note that there are always docs in docs/ directory for django, django-filter, django-guardian, djangorestframework, drf-spectacular for exact used versions of these libraries, you can try to gather info from there when addressing a complex task or a bug.

Please note that you must not add any additional libraries to the project. You can only use libraries listed in requirements.txt.

**Important**: This project generates static OpenAPI spec files (`openapi.yml`) for frontend generation. No web-based documentation UI is exposed.

## Authentication System Overview

This template includes a complete authentication system with:

### Core Features
1. **Email-based authentication** - Users log in with email instead of username
2. **JWT tokens** - Secure, stateless authentication using access and refresh tokens
3. **Role-based access control (RBAC)** - Flexible permission system using roles
4. **Password reset** - Secure token-based password reset functionality
5. **Token management** - Refresh token rotation and blacklisting

### Models

#### User Model (`api.User`)
Custom user model with email as the primary identifier:
- **Fields**: `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `date_joined`
- **Relationships**: Many-to-many with `Role` model
- **Methods**:
  - `has_permission(permission_name)` - Check if user has a specific permission
  - `add_role(role_name)` - Add a role to user
  - `remove_role(role_name)` - Remove a role from user
  - `get_all_permissions()` - Get combined permissions from all roles

#### Role Model (`api.Role`)
Flexible role system with JSON-based permissions:
- **Fields**: `name`, `description`, `permissions` (JSONField), `is_active`
- **Methods**:
  - `has_permission(permission_name)` - Check if role has a specific permission

**Permission Structure Examples:**
```python
# Simple list structure
{
    "permissions": ["create_post", "edit_post", "delete_post"]
}

# Resource-based structure
{
    "posts": ["create", "read", "update", "delete"],
    "comments": ["create", "read", "delete"],
    "users": ["read"]
}

# Advanced structure with conditions
{
    "posts": {
        "create": true,
        "edit": {"condition": "own_only"},
        "delete": {"condition": "own_only"},
        "publish": false
    }
}
```

#### RefreshToken Model (`api.RefreshToken`)
Manages JWT refresh tokens:
- **Fields**: `user`, `token`, `expires_at`, `is_revoked`, `user_agent`, `ip_address`
- **Methods**:
  - `is_valid()` - Check if token is valid
  - `revoke()` - Revoke the token
  - `create_token(user, ...)` - Create new refresh token
  - `revoke_all_user_tokens(user)` - Revoke all tokens for a user
  - `cleanup_expired_tokens()` - Delete expired tokens

#### PasswordResetToken Model (`api.PasswordResetToken`)
Manages password reset tokens:
- **Fields**: `user`, `token`, `expires_at`, `is_used`, `ip_address`
- **Methods**:
  - `is_valid()` - Check if token is valid
  - `mark_as_used()` - Mark token as used
  - `create_token(user, ...)` - Create new reset token
  - `cleanup_expired_tokens()` - Delete expired tokens

### How to Extend Roles and Permissions

#### Adding New Roles

1. **Via Django Admin**:
   - Go to `/admin/api/role/`
   - Click "Add role"
   - Set name, description, and permissions JSON
   - Save

2. **Via Code**:
```python
from api.models import Role

# Create a new role
role = Role.objects.create(
    name='moderator',
    description='Can moderate content',
    permissions={
        'posts': ['read', 'update', 'delete'],
        'comments': ['read', 'update', 'delete'],
        'users': ['read']
    },
    is_active=True
)
```

3. **Via Data Migration**:
```python
# In a migration file
def create_moderator_role(apps, schema_editor):
    Role = apps.get_model('api', 'Role')
    Role.objects.get_or_create(
        name='moderator',
        defaults={
            'description': 'Moderator role',
            'permissions': {'posts': ['read', 'update', 'delete']},
            'is_active': True,
        }
    )
```

#### Extending Permissions

No code changes needed! Just update the permissions JSON:

```python
# Get role and update permissions
role = Role.objects.get(name='user')
role.permissions = {
    'permissions': [
        'view_profile',
        'edit_profile',
        'create_post',  # NEW
        'upload_image',  # NEW
    ]
}
role.save()
```

#### Checking Permissions in Views

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CreatePostView(APIView):
    def post(self, request):
        # Check permission
        if not request.user.has_permission('posts.create'):
            return Response(
                {'error': 'You do not have permission to create posts'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create post logic
        return Response({'message': 'Post created'})
```

#### Creating Custom Permission Classes

```python
# api/permissions.py
from rest_framework.permissions import BasePermission

class CanCreatePost(BasePermission):
    """
    Custom permission to check if user can create posts.
    """
    def has_permission(self, request, view):
        return request.user.has_permission('posts.create')

class CanEditOwnPost(BasePermission):
    """
    Custom permission to check if user can edit their own post.
    """
    def has_object_permission(self, request, view, obj):
        # obj is the Post instance
        if request.user.has_permission('posts.edit'):
            return obj.author == request.user
        return False

# In views.py
from .permissions import CanCreatePost

class CreatePostView(APIView):
    permission_classes = [CanCreatePost]
    
    def post(self, request):
        # User is already authorized by permission_classes
        return Response({'message': 'Post created'})
```

### How to Add New User Fields

The User model is designed to be easily extensible:

1. **Open `api/models.py`**
2. **Find the EXTENSIBILITY SECTION** in the User model
3. **Add new fields**:

```python
class User(AbstractBaseUser, PermissionsMixin):
    # ... existing fields ...
    
    # ### EXTENSIBILITY SECTION ###
    # Add additional profile fields below this comment
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    # ### END EXTENSIBILITY SECTION ###
```

4. **Create and run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Update serializers** to include new fields:
```python
# api/serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone_number', 'avatar', 'bio', 'birth_date', 'country',  # NEW
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
```

### API Endpoints Documentation

The authentication system should expose these endpoints (implement in `api/views.py` and `api/urls.py`):

#### Authentication Endpoints

**POST /api/auth/register/**
- Register a new user
- Request body: `{"email": "user@example.com", "password": "password123", "first_name": "John", "last_name": "Doe"}`
- Response: User data + JWT tokens

**POST /api/auth/login/**
- Login with email and password
- Request body: `{"email": "user@example.com", "password": "password123"}`
- Response: `{"access": "<token>", "refresh": "<token>", "user": {...}}`

**POST /api/auth/refresh/**
- Refresh access token using refresh token
- Request body: `{"refresh": "<refresh_token>"}`
- Response: `{"access": "<new_access_token>", "refresh": "<new_refresh_token>"}`

**POST /api/auth/logout/**
- Logout and revoke refresh token
- Request body: `{"refresh": "<refresh_token>"}`
- Response: `{"message": "Logged out successfully"}`

**POST /api/auth/logout-all/**
- Logout from all devices (revoke all refresh tokens)
- Headers: `Authorization: Bearer <access_token>`
- Response: `{"message": "Logged out from all devices"}`

#### Password Reset Endpoints

**POST /api/auth/password-reset/request/**
- Request password reset token
- Request body: `{"email": "user@example.com"}`
- Response: `{"message": "Password reset email sent"}`
- Note: In production, send email with reset link

**POST /api/auth/password-reset/confirm/**
- Reset password using token
- Request body: `{"token": "<reset_token>", "new_password": "newpassword123"}`
- Response: `{"message": "Password reset successful"}`

**POST /api/auth/password-change/**
- Change password (authenticated)
- Headers: `Authorization: Bearer <access_token>`
- Request body: `{"old_password": "oldpass", "new_password": "newpass"}`
- Response: `{"message": "Password changed successfully"}`

#### User Profile Endpoints

**GET /api/users/me/**
- Get current user profile
- Headers: `Authorization: Bearer <access_token>`
- Response: User object with roles and permissions

**PATCH /api/users/me/**
- Update current user profile
- Headers: `Authorization: Bearer <access_token>`
- Request body: `{"first_name": "NewName", "last_name": "NewLastName"}`
- Response: Updated user object

**GET /api/users/me/permissions/**
- Get all permissions for current user
- Headers: `Authorization: Bearer <access_token>`
- Response: `{"permissions": {...}}`

### Example Permission System Usage

#### Example 1: Basic Permission Check

```python
# In a view
class DeletePostView(APIView):
    def delete(self, request, post_id):
        # Check if user has delete permission
        if not request.user.has_permission('posts.delete'):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Delete logic
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

#### Example 2: Role Assignment on Registration

```python
# In registration view
class RegisterView(APIView):
    permission_classes = []  # Allow unauthenticated
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Assign default 'user' role
            user.add_role('user')
            
            # Create tokens
            # ... token creation logic ...
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### Example 3: Admin-Only Endpoint

```python
class AdminDashboardView(APIView):
    def get(self, request):
        # Check if user has admin permissions
        if not request.user.has_permission('admin.access'):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Return admin data
        return Response({
            'total_users': User.objects.count(),
            'total_posts': Post.objects.count(),
        })
```

#### Example 4: Dynamic Role-Based Content

```python
class PostListView(APIView):
    def get(self, request):
        # Regular users see only published posts
        queryset = Post.objects.filter(status='published')
        
        # Moderators and admins see all posts
        if request.user.has_permission('posts.view_all'):
            queryset = Post.objects.all()
        
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
```

### Migration Commands

After setting up or modifying the authentication system:

```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser

# The default 'user' role is created automatically via migration 0003
# To create additional roles, use Django admin or shell:
python manage.py shell
>>> from api.models import Role
>>> Role.objects.create(
...     name='moderator',
...     description='Moderator role',
...     permissions={'posts': ['read', 'update', 'delete']},
...     is_active=True
... )
```

### Database Configuration Notes

#### Current Setup (Development)
- **Database**: SQLite
- **Location**: `persistent/db/db.sqlite3`
- **Benefits**: Simple, no setup required, good for development

#### Switching to PostgreSQL (Production)

1. **Install driver**: Add `psycopg2-binary` to requirements.txt
2. **Update settings.py**:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "your_database_name",
        "USER": "your_database_user",
        "PASSWORD": "your_database_password",
        "HOST": "localhost",
        "PORT": "5432",
        "CONN_MAX_AGE": 600,
    }
}
```
3. **Run migrations**: `python manage.py migrate`

#### Switching to MySQL (Production)

1. **Install driver**: Add `mysqlclient` to requirements.txt
2. **Update settings.py**:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "your_database_name",
        "USER": "your_database_user",
        "PASSWORD": "your_database_password",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}
```
3. **Run migrations**: `python manage.py migrate`

---

## Project Structure

**Key directories and files:**
- `config/` - Django project configuration folder
  - `settings.py` - Main settings (INSTALLED_APPS, REST_FRAMEWORK config)
  - `urls.py` - Root URL configuration
- `api/` - Main API application folder
  - `models.py` - Database models (User, Role, RefreshToken, PasswordResetToken)
  - `serializers.py` - DRF serializers (data validation/transformation)
  - `views.py` - API views/endpoints
  - `urls.py` - API URL routing
  - `permissions.py` - Custom permission classes (create as needed)
- `manage.py` - Django management commands
- `openapi.yml` - Generated API specification (regenerate after changes)
- `requirements.txt` - Dependencies

## Core Patterns Used

### 1. API Views Pattern

Uses `APIView` with `@extend_schema` decorator for documentation:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import YourSerializer

class YourView(APIView):
    @extend_schema(
        request=YourSerializer,  # For POST/PUT/PATCH
        responses={200: YourSerializer},  # Success response
        description="Describe what this endpoint does"
    )
    def get(self, request):
        # Implementation
        return Response(data)
```

### 2. Serializer Pattern

Serializers define data structure and validation:

```python
from rest_framework import serializers

class YourSerializer(serializers.Serializer):
    field_name = serializers.CharField(max_length=200)
    number_field = serializers.IntegerField()
    optional_field = serializers.CharField(required=False)
```

### 3. URL Pattern

Register views in `api/urls.py`:

```python
from django.urls import path
from .views import YourView

urlpatterns = [
    path('endpoint/', YourView.as_view(), name='endpoint-name'),
]
```

## Step-by-Step Modification Instructions

### Adding a New API Endpoint

**Step 1: Create Serializer** (`api/serializers.py`)

```python
class NewEndpointSerializer(serializers.Serializer):
    # Define your data structure
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=0, required=False)
```

**Step 2: Create View** (`api/views.py`)

```python
from drf_spectacular.utils import extend_schema
from .serializers import NewEndpointSerializer

class NewEndpointView(APIView):
    """
    Brief description of this endpoint.
    """

    @extend_schema(
        responses={200: NewEndpointSerializer},
        description="GET method description"
    )
    def get(self, request):
        # Your logic here
        data = {'name': 'John', 'email': 'john@example.com', 'age': 30}
        serializer = NewEndpointSerializer(data)
        return Response(serializer.data)

    @extend_schema(
        request=NewEndpointSerializer,
        responses={201: NewEndpointSerializer},
        description="POST method description"
    )
    def post(self, request):
        serializer = NewEndpointSerializer(data=request.data)
        if serializer.is_valid():
            # Process validated data
            # serializer.validated_data contains clean data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Step 3: Register URL** (`api/urls.py`)

```python
from .views import NewEndpointView

urlpatterns = [
    # ... existing patterns ...
    path('new-endpoint/', NewEndpointView.as_view(), name='new-endpoint'),
]
```

**Step 4: Regenerate Schema**

```bash
python manage.py spectacular --file openapi.yml
```

### Adding Database Models

**Step 1: Define Model** (`api/models.py`)

```python
from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

**Step 2: Create Model Serializer** (`api/serializers.py`)

```python
from rest_framework import serializers
from .models import YourModel

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = ['id', 'name', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

**Step 3: Create CRUD Views** (`api/views.py`)

```python
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelListView(ListCreateAPIView):
    """
    GET: List all items
    POST: Create new item
    """
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer

class YourModelDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single item
    PUT/PATCH: Update item
    DELETE: Delete item
    """
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
```

**Step 4: Register URLs** (`api/urls.py`)

```python
urlpatterns = [
    # ... existing patterns ...
    path('items/', YourModelListView.as_view(), name='item-list'),
    path('items/<int:pk>/', YourModelDetailView.as_view(), name='item-detail'),
]
```

**Step 5: Create and Run Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 6: Regenerate Schema**

```bash
python manage.py spectacular --file openapi.yml
```

## Common Serializer Field Types

```python
# Text fields
field = serializers.CharField(max_length=200)
field = serializers.EmailField()
field = serializers.URLField()
field = serializers.SlugField()
field = serializers.UUIDField()

# Numeric fields
field = serializers.IntegerField(min_value=0, max_value=100)
field = serializers.FloatField()
field = serializers.DecimalField(max_digits=10, decimal_places=2)

# Boolean and choice fields
field = serializers.BooleanField()
field = serializers.ChoiceField(choices=['option1', 'option2', 'option3'])

# Date/time fields
field = serializers.DateTimeField()
field = serializers.DateField()
field = serializers.TimeField()

# Complex fields
field = serializers.ListField(child=serializers.CharField())
field = serializers.DictField()
field = serializers.JSONField()

# Relations (for models)
field = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())
field = serializers.StringRelatedField()

# Common parameters
field = serializers.CharField(
    required=False,        # Optional field
    allow_null=True,       # Allow null values
    allow_blank=True,      # Allow empty strings
    default='value',       # Default value
    read_only=True,        # Not writable
    write_only=True,       # Not readable (e.g., passwords)
)
```

## Common HTTP Status Codes

```python
from rest_framework import status

# Success responses
status.HTTP_200_OK              # GET, PUT, PATCH success
status.HTTP_201_CREATED         # POST success
status.HTTP_204_NO_CONTENT      # DELETE success

# Client error responses
status.HTTP_400_BAD_REQUEST     # Validation error
status.HTTP_401_UNAUTHORIZED    # Authentication required
status.HTTP_403_FORBIDDEN       # Permission denied
status.HTTP_404_NOT_FOUND       # Resource not found

# Server error
status.HTTP_500_INTERNAL_SERVER_ERROR
```

## View Response Patterns

### Simple Response

```python
return Response({'message': 'Success'})
```

### Response with Status Code

```python
return Response(data, status=status.HTTP_201_CREATED)
```

### Error Response

```python
return Response(
    {'error': 'Something went wrong'},
    status=status.HTTP_400_BAD_REQUEST
)
```

### Validation Error Response

```python
serializer = YourSerializer(data=request.data)
if serializer.is_valid():
    # Process data
    return Response(serializer.data, status=status.HTTP_201_CREATED)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## Query Parameters

```python
def get(self, request):
    # Get query parameter: /api/endpoint/?search=value
    search = request.query_params.get('search', '')

    # Get with default
    page = request.query_params.get('page', 1)

    # Get multiple values: /api/endpoint/?tag=python&tag=django
    tags = request.query_params.getlist('tag')
```

## Path Parameters

```python
# In urls.py
path('items/<int:pk>/', YourView.as_view())
path('items/<str:slug>/', YourView.as_view())
path('items/<uuid:id>/', YourView.as_view())

# In view
def get(self, request, pk):
    # Use pk parameter
    pass
```

## Advanced @extend_schema Examples

### Multiple Response Codes

```python
@extend_schema(
    request=InputSerializer,
    responses={
        200: OutputSerializer,
        400: {'description': 'Validation error'},
        404: {'description': 'Not found'},
    },
    description="Detailed description"
)
```

### Query Parameters Documentation

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Search term',
            required=False
        ),
        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Page number',
            required=False
        ),
    ],
    responses={200: YourSerializer(many=True)}
)
def get(self, request):
    pass
```

### List Response (many=True)

```python
@extend_schema(
    responses={200: YourSerializer(many=True)},
    description="Returns a list of items"
)
def get(self, request):
    items = YourModel.objects.all()
    serializer = YourSerializer(items, many=True)
    return Response(serializer.data)
```

## Testing the API

```bash
# GET request
curl http://localhost:8000/api/endpoint/

# POST request
curl -X POST http://localhost:8000/api/endpoint/ \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'

# With authentication
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <access_token>"

# PUT request
curl -X PUT http://localhost:8000/api/endpoint/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"field": "updated value"}'

# DELETE request
curl -X DELETE http://localhost:8000/api/endpoint/1/ \
  -H "Authorization: Bearer <access_token>"
```

## Essential Commands

```bash
# Run development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Regenerate API schema (DO THIS AFTER ANY API CHANGES)
python manage.py spectacular --file openapi.yml

# Django shell (for testing)
python manage.py shell
```

## Checklist for Adding New Features

When adding a new endpoint:

- Create/update serializer in `api/serializers.py`
- Create/update view in `api/views.py`
- Add `@extend_schema` decorator to all HTTP methods
- Register URL in `api/urls.py`
- If using models: create migration and run migrate
- **Regenerate schema**: `python manage.py spectacular --file openapi.yml`
- Test endpoint with curl or HTTP client
- Verify schema has no errors: check for "Errors: 0" in output

General routine after any change:

- Check that server starts and returns no errors via `DJANGO_DEBUG=1 python manage.py runserver`.
- `python manage.py makemigrations` is idempotent so we can run it explicitly for any change, just to be sure.
- Run `ruff format` before commit to maintain the code well-formatted.

## Configuration Files to Modify

### Adding Dependencies

Adding new dependencies is not allowed.

### Changing API Metadata

Edit `config/settings.py`:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Easyapp API',
    'DESCRIPTION': 'API documentation for easyapp',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Add more settings if needed
}
```

## Common Issues and Solutions

### Error: "unable to guess serializer"

**Solution**: Add `@extend_schema` decorator with `request` and `responses` parameters.

### Schema not updating

**Solution**: Run `python manage.py spectacular --file openapi.yml` after any API changes.

### Migration errors

**Solution**:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Import errors

**Solution**: Ensure all new models/serializers/views are imported correctly in their respective files.

### Authentication errors

**Solution**: Ensure you're sending the Authorization header: `Authorization: Bearer <access_token>`

## End of Guide

This boilerplate is designed for:

1. Building REST APIs with authentication quickly
2. Implementing role-based access control easily
3. Generating OpenAPI specs for frontend generation
4. Maintaining clean, documented, and extensible code

Always regenerate `openapi.yml` after modifications so the frontend generation process has the latest API definition.
