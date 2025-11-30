from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializer import MusicActionSerializer
from .models import MusicAction

class MusicControlView(generics.GenericAPIView):
    serializer_class = MusicActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            music_action = serializer.save(user=request.user)
            
            # Here you can integrate real music control logic, e.g., sending commands to device
            # For now, just return the action
            return Response({
                "message": f"Action '{music_action.action}' sent to device {music_action.device.name}."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
