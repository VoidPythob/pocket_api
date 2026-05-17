from .docs import AdminGameDocsView
from .egg_groups import AdminPetEggGroupView
from .feature_views import AdminPetFeatureView
from .files import AdminFileUploadView
from .generations import AdminPetGenerationView
from .items import (
    AdminItemCategoryRelationView,
    AdminItemCategoryView,
    AdminItemView,
)
from .pets import (
    AdminPetCreateView,
    AdminPetEggGroupRelationView,
    AdminPetGenerationRelationView,
    AdminPetRanceRelationView,
)
from .pet_detail import AdminPetDetailView
from .pokemon_import import AdminPokemonCsvImportView
from .rances import AdminPetRanceView
from .register import AdminRegisterView
from .skill_views import AdminPetSkillCategoryView, AdminPetSkillView
from .tags import AdminTagView

__all__ = [
    "AdminGameDocsView",
    "AdminFileUploadView",
    "AdminItemCategoryRelationView",
    "AdminItemCategoryView",
    "AdminItemView",
    "AdminPetCreateView",
    "AdminPetDetailView",
    "AdminPokemonCsvImportView",
    "AdminPetEggGroupRelationView",
    "AdminPetEggGroupView",
    "AdminPetFeatureView",
    "AdminPetGenerationRelationView",
    "AdminPetGenerationView",
    "AdminPetRanceRelationView",
    "AdminPetRanceView",
    "AdminPetSkillCategoryView",
    "AdminPetSkillView",
    "AdminRegisterView",
    "AdminTagView",
]
