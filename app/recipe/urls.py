from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)  # auto create urls for all tags
router.register('ingredients', views.IngredientViewSet)  # auto create urls...

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
