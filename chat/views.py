from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ChatRoom, Message
from .serializers import MessageSerializer


class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        messages = room.messages.order_by("created_at")
        return Response(MessageSerializer(messages, many=True).data)

    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, room=room)
        return Response(serializer.data)
