from rest_framework import serializers
from user.models import User, Leaves
from datetime import date


class LeaveRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leaves
        fields = ('user', 'start', 'end', 'attachment')

    def validate(self, attrs):
        start = attrs['start']
        end = attrs['end']
        today = date.today()
        if (start - today).days < 1:
            raise serializers.ValidationError("Leave in past or on today is not possible.")
        if start > end:
            raise serializers.ValidationError("Start date should not be after end date")
        if (end - start).days + 1 > 4:
            raise serializers.ValidationError("Leave for more than 4 days not allowed")

        return attrs


class LeaveListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leaves
        fields = ('user', 'start', 'end', 'attachment')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, attrs):

        password = attrs['password']
        confirm_password = attrs['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password must be same.")

        email = attrs['email']
        user = User.objects.filter(email=email).exists()

        if user:
            raise serializers.ValidationError('This email has been registered.')

        return attrs

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], last_name=validated_data['last_name'],
                                   first_name=validated_data['first_name'])

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name')