from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Advertisement, AdvertisementStatusChoices, FavoriteAdvertisement
from .serializers import AdvertisementSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdvertisementFilter


class AdvertisementViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Advertisement.objects.filter(
                Q(status=AdvertisementStatusChoices.OPEN)
                | Q(status=AdvertisementStatusChoices.DRAFT, creator=user)
            )
        return Advertisement.objects.filter(status=AdvertisementStatusChoices.OPEN)

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        open_ads_count = Advertisement.objects.filter(
            creator=user, status=AdvertisementStatusChoices.OPEN
        ).count()
        if open_ads_count >= 10:
            raise serializer.ValidationError(
                "You cannot have more than 10 open advertisements."
            )
        serializer.save(creator=user)

    @action(detail=True, methods=["post"])
    def add_to_favorites(self, request, pk=None):
        advertisement = self.get_object()
        if advertisement.creator == request.user:
            return Response(
                {"detail": "You cannot add your own advertisement to favorites."},
                status=403,
            )

        favorite, created = FavoriteAdvertisement.objects.get_or_create(
            user=request.user, advertisement=advertisement
        )
        if created:
            return Response({"detail": "Advertisement added to favorites."}, status=201)
        return Response(
            {"detail": "Advertisement is already in favorites."}, status=200
        )

    @action(detail=True, methods=["delete"])
    def remove_from_favorites(self, request, pk=None):
        advertisement = self.get_object()
        favorite = FavoriteAdvertisement.objects.filter(
            user=request.user, advertisement=advertisement
        ).first()
        if favorite:
            favorite.delete()
            return Response(
                {"detail": "Advertisement removed from favorites."}, status=204
            )
        return Response({"detail": "Advertisement is not in favorites."}, status=404)

    @action(detail=False, methods=["get"])
    def favorites(self, request):
        favorites = FavoriteAdvertisement.objects.filter(user=request.user)
        advertisements = [fav.advertisement for fav in favorites]
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data)
