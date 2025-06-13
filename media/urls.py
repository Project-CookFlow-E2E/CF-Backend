from media.views.imageViewSet import ImageWriteDeleteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'images', ImageWriteDeleteViewSet, basename='image-write')

urlpatterns += router.urls
