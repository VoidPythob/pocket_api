from django.urls import include, path
from rest_framework.routers import DefaultRouter

from pocket_api.views import (
    AdminFileUploadView,
    AdminGameDocsView,
    AdminItemCategoryRelationView,
    AdminItemCategoryView,
    AdminItemView,
    AdminLoginView,
    AdminLogoutView,
    AdminPetCreateView,
    AdminPetDetailView,
    AdminPetEggGroupRelationView,
    AdminPetEggGroupView,
    AdminPetFeatureView,
    AdminPetGenerationRelationView,
    AdminPetGenerationView,
    AdminPokemonCsvImportView,
    AdminPetRanceRelationView,
    AdminPetRanceView,
    AdminPetSkillCategoryView,
    AdminPetSkillView,
    AdminRegisterView,
    AdminTagView,
    EggGroupPetsView,
    EggGroupsView,
    FileDownloadView,
    GenerationsView,
    GameDocCategoriesView,
    GameDocsView,
    ItemsView,
    PetCaptureMethodDetailView,
    PetCaptureMethodsView,
    PetFeatureDetailView,
    PetFeatureListView,
    PetFeaturesView,
    PetsView,
    SkillsView,
    TagsView,
)


router = DefaultRouter()
router.register("egg-groups", EggGroupsView)
router.register("generations", GenerationsView)
router.register("game-docs", GameDocsView)
router.register("items", ItemsView)
router.register("pets", PetsView)
router.register("skills", SkillsView)
router.register("tags", TagsView)

urlpatterns = [path("", include(router.urls))]
urlpatterns += [path("files/<str:file_id>/", FileDownloadView.as_view())]
urlpatterns += [path("admin/files/", AdminFileUploadView.as_view())]
urlpatterns += [path("admin/item-categories/", AdminItemCategoryView.as_view())]
urlpatterns += [path("admin/item-categories/<int:pk>/", AdminItemCategoryView.as_view())]
urlpatterns += [path("admin/game-docs/", AdminGameDocsView.as_view())]
urlpatterns += [path("admin/game-docs/<int:pk>/", AdminGameDocsView.as_view())]
urlpatterns += [path("admin/items/", AdminItemView.as_view())]
urlpatterns += [path("admin/items/<int:pk>/", AdminItemView.as_view())]
urlpatterns += [path("admin/items/<int:item_id>/categories/", AdminItemCategoryRelationView.as_view())]
urlpatterns += [path("admin/items/<int:item_id>/categories/<int:category_id>/", AdminItemCategoryRelationView.as_view())]
urlpatterns += [path("admin/login/", AdminLoginView.as_view())]
urlpatterns += [path("admin/logout/", AdminLogoutView.as_view())]
urlpatterns += [path("admin/register/", AdminRegisterView.as_view())]
urlpatterns += [path("admin/egg-groups/", AdminPetEggGroupView.as_view())]
urlpatterns += [path("admin/egg-groups/<int:pk>/", AdminPetEggGroupView.as_view())]
urlpatterns += [path("admin/features/", AdminPetFeatureView.as_view())]
urlpatterns += [path("admin/features/<int:pk>/", AdminPetFeatureView.as_view())]
urlpatterns += [path("admin/generations/", AdminPetGenerationView.as_view())]
urlpatterns += [path("admin/generations/<int:pk>/", AdminPetGenerationView.as_view())]
urlpatterns += [path("admin/pets/import-csv/", AdminPokemonCsvImportView.as_view())]
urlpatterns += [path("admin/pets/", AdminPetCreateView.as_view())]
urlpatterns += [path("admin/pets/<int:pk>/", AdminPetDetailView.as_view())]
urlpatterns += [path("admin/pets/<int:pet_id>/egg-groups/", AdminPetEggGroupRelationView.as_view())]
urlpatterns += [path("admin/pets/<int:pet_id>/egg-groups/<int:egg_group_id>/", AdminPetEggGroupRelationView.as_view())]
urlpatterns += [path("admin/pets/<int:pet_id>/generations/", AdminPetGenerationRelationView.as_view())]
urlpatterns += [path("admin/pets/<int:pet_id>/generations/<int:generation_id>/", AdminPetGenerationRelationView.as_view())]
urlpatterns += [path("admin/pets/<int:pet_id>/rances/", AdminPetRanceRelationView.as_view())]
urlpatterns += [path("admin/pets/<int:pet_id>/rances/<int:rance_id>/", AdminPetRanceRelationView.as_view())]
urlpatterns += [path("admin/rances/", AdminPetRanceView.as_view())]
urlpatterns += [path("admin/rances/<int:pk>/", AdminPetRanceView.as_view())]
urlpatterns += [path("admin/skill-categories/", AdminPetSkillCategoryView.as_view())]
urlpatterns += [path("admin/skill-categories/<int:pk>/", AdminPetSkillCategoryView.as_view())]
urlpatterns += [path("admin/skills/", AdminPetSkillView.as_view())]
urlpatterns += [path("admin/skills/<int:pk>/", AdminPetSkillView.as_view())]
urlpatterns += [path("admin/tags/", AdminTagView.as_view())]
urlpatterns += [path("admin/tags/<int:pk>/", AdminTagView.as_view())]
urlpatterns += [path("egg-groups/<int:pk>/pets/", EggGroupPetsView.as_view())]
urlpatterns += [path("game-doc-categories/", GameDocCategoriesView.as_view())]
urlpatterns += [path("capture_methods/<int:pk>/", PetCaptureMethodDetailView.as_view())]
urlpatterns += [path("features/", PetFeatureListView.as_view())]
urlpatterns += [path("features/<int:pk>/", PetFeatureDetailView.as_view())]
urlpatterns += [path("pets/<int:pk>/capture_methods/", PetCaptureMethodsView.as_view())]
urlpatterns += [path("pets/<int:pk>/features/", PetFeaturesView.as_view())]
