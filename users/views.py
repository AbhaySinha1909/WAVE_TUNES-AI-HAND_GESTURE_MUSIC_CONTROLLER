from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # explicitly set backend so Django can attach user.backend
            login(request, user, backend='users.backends.EmailBackend')
            return Response({
                'username': user.username,
                'email': user.email,
                'mobile': user.mobile,
                'full_name': user.full_name,
                'detail': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # make sure request is passed into serializer context (GenericAPIView does this)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # return serializer errors so frontend can see exactly why
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "mobile": user.mobile
        })
