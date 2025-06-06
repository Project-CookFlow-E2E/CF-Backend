from rest_framework.routers import DefaultRouter
from recipes.views.step_viewset import StepViewSet, StepAdminViewSet

router = DefaultRouter()
router.register(r'steps', StepViewSet)
router.register(r'admin/steps', StepAdminViewSet) 

urlpatterns = router.urls
