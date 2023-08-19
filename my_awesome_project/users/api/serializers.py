from django.contrib.auth import get_user_model
from rest_framework import serializers

from my_awesome_project.users.models import User as UserType

from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=42)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        user = super(CustomRegisterSerializer, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()

        # You must return the original result.
        return user
