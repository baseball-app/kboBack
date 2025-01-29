from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.uploads.services import UploadProfileService


class UploadsViewSet(GenericViewSet):

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def profile(self, request):
        service = UploadProfileService()
        file_key = service.get_filekey(request)
        return Response(status=status.HTTP_200_OK, data={"file_key": file_key})
