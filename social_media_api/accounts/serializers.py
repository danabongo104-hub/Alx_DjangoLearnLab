from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """Handle new user creation and returns a token immediately."""
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password'}
                                     )
    
    # Convenience field — the token is returned so the client can start
    # making authenticated requests right away without a separate login call
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token' ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exits():
            raise serializers.ValidationError("A user with that email alreasy exists. ")
        return value
    
    def create(self, validated_data):
        # Use the create_user method to ensure the password is hashed
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Generate a token for the new user
        Token.objects.create(user=user)
        return user
    
    def get_token(self, obj):
        # Retrieve the just-created user and return their token
        token, _ = Token.objects.get(user=obj)
        return token.key

class LoginSerializer(serializers.Serializer):
    """Validates credentials and returns the existing or newly created token."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        # authenticate() checks username + hashed password
        # Returns None if credentials are invalid (never raises on its own)
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled.")
        # Attach the user to validated_data so the view can access it
        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Read/update the authenticated user's own profile.

    WHY read_only_fields for username?
        Changing a username is a disruptive operation (it can break
        external references). We deliberately lock it after registration.
        If the project ever needs username changes, a dedicated endpoint
        with extra validation is the right approach.
    """
    # Show follower/following counts rather than the full list (performance)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio',
            'profile_picture', 'followers_count', 'following_count',
        ]
        read_only_fields = ['id', 'username']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
