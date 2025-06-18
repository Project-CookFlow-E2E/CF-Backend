import random
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from recipes.models.recipe import Recipe
from recipes.serializers.recipeSerializer import RecipeSerializer, RecipeAdminSerializer
from media.services.image_service import update_image_for_instance


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Recipe.

    Usuarios autenticados pueden realizar todas las operaciones CRUD.
    Usuarios NO autenticados solo pueden hacer GET (listar y ver recetas).

    Attributes:
        queryset (QuerySet): Obtiene todos los objetos Recipe.
        permission_classes (list): Controla el acceso según autenticación.
        get_serializer_class (func): Selecciona el serializer según el tipo de usuario.

    Author:
        {Lorena Martínez}
    """
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user_id', 'id']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return RecipeAdminSerializer
        return RecipeSerializer

    def perform_create(self, serializer): 
        recipe = serializer.save(user_id=self.request.user)

        image_file = self.request.FILES.get("recipe_image")
        if image_file:
            update_image_for_instance(
                image_file=image_file,
                user_id=self.request.user.id,
                external_id=recipe.id,
                image_type="RECIPE"
            )

    @action(detail=False, methods=['get'])
    def random(self, request):
        """
        Returns a specified number of random recipes by picking random IDs.
        Query parameter 'count' (default: 5) to specify how many random recipes.
        This method is more efficient than order_by('?') for large tables.
        Filters (like user_id or current user) applied via get_queryset will work as expected.
        """
        count = int(request.query_params.get('count', 5))

        all_recipe_ids = list(self.get_queryset().values_list('id', flat=True))

        if not all_recipe_ids:
            return Response([])

        if len(all_recipe_ids) <= count:
            random_ids = all_recipe_ids
        else:
            random_ids = random.sample(all_recipe_ids, count)

        random_recipes = self.get_queryset().filter(id__in=random_ids)

        serializer = self.get_serializer(random_recipes, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Limitar resultados si se pasa el parámetro 'limit'
        limit = request.query_params.get('limit')
        if limit is not None and limit.isdigit():
            queryset = queryset[:int(limit)]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
