from rest_framework import viewsets, permissions
from users.models import User
from users.serializer import UserSerializer


# Create your views here.
class UserAPIView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if "password" in self.request.data:
            user.set_password(self.request.data["password"])
            user.save()

    def perform_destroy(self, instance):
        instance.delete()
