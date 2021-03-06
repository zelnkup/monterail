from rest_framework import generics, permissions, status
from rest_framework.response import Response

from tickets.serializers.payment import PaymentSerializer


class PaymentCreate(generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
