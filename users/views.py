from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Ensure superAdmin middleware equivalent if needed
def register_user(request):
    # Only Super Admin and Admin can create
    if request.user.role not in ['Super Admin', 'Admin']:
        return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            '_id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'branch': user.branch,
            'token': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Super Admin and Admin can view all users
        if self.request.user.role in ['Super Admin', 'Admin']:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id) # Only see themselves or similar

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if request.user.role not in ['Super Admin', 'Admin']:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Data must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = []
        errors = []
        for index, user_data in enumerate(data):
            serializer = self.get_serializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                results.append(serializer.data)
            else:
                errors.append({'index': index, 'errors': serializer.errors})
        
        if errors:
            return Response({'results': results, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(results, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin']:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['Super Admin', 'Admin']:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
