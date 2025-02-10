from rest_framework import serializers
from Users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects._create_user(username=validated_data['username'], user_second_name=None,
                                         password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('username', 'password')