from .docs import AdminGameDocsView
from .files import AdminFileUploadView
from .generations import AdminPetGenerationView
from .items import AdminItemCategoryView, AdminItemView
from .pets import (
    AdminPetCreateView,
    AdminPetEggGroupRelationView,
    AdminPetEggGroupView,
    AdminPetFeatureView,
    AdminPetGenerationRelationView,
    AdminPetRanceRelationView,
)
from .pet_detail import AdminPetDetailView
from .pokemon_import import AdminPokemonCsvImportView
from .rances import AdminPetRanceView
from .register import AdminRegisterView
from .skills import AdminPetSkillCategoryView, AdminPetSkillView
from .tags import AdminTagView

__all__ = [
    "AdminGameDocsView",
    "AdminFileUploadView",
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
