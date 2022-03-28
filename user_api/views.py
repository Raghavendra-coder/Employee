from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import LeaveRequestSerializer, LeaveListSerializer, UserSerializer, CreateUserSerializer, \
    UserListSerializer
from user.models import Leaves, User


class LeaveRequest(APIView):

    def get(self, request):
        if request.user.is_superuser:
            leaves = Leaves.objects.all().select_related('user')
        else:
            leaves = Leaves.objects.filter(user=request.user).select_related('user')
        serializer = LeaveListSerializer(leaves, many=True)
        response = serializer.data
        return Response(response)

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
        else:
            response = serializer.errors

        return Response(response)


class EmployeeDetail(APIView):

    def get_object(self, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            return user
        else:
            return False

    def get(self, request, *args, **kwargs):
        user = self.get_object(kwargs['pk'])
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.data.pop('password')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = self.get_object(kwargs['pk'])
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.get_object(kwargs['pk'])
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeList(APIView):

    def get(self, request):
        employees = User.objects.exclude(is_superuser=True)
        serializer = UserListSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
