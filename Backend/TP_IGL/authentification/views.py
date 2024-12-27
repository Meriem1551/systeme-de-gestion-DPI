from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer , UserRegisterSerializer
from rest_framework.generics import CreateAPIView


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Extract the user's role from the validated data
        role = serializer.validated_data.get('role')

        # Add the role to the response data
        response_data = serializer.data
        response_data['role'] = role  # Attach role to the response

        return Response(response_data, status=status.HTTP_200_OK)


class AddUserView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        # Save the user instance created from the serializer
        user = serializer.save()

        # After user is saved, generate the access token for that user
        tokens = user.tokens()  # Generate the access token
        # Add the tokens and other relevant info to the response
        return {
            'username': user.username,
            'full_name': user.get_full_name(),
            'role': user.role,
            'access_token': tokens['access'],  # Return only access token
            'id': user.id,
        }

    def post(self, request, *args, **kwargs):
        # Get serializer and validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform user creation
        response_data = self.perform_create(serializer)

        # Return a response with the user data and token
        return Response(response_data, status=status.HTTP_201_CREATED)


class RegisterView(GenericAPIView):
        serializer_class = UserRegisterSerializer



        def post(self, request):
            user = request.data
            serializer = self.serializer_class(data=user)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user_data = serializer.data

                return Response({
                    'data': user_data,
                    'message': 'thanks for signing up '
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
