from django.db import models


class Attribute(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "attribute"


class GameDocs(models.Model):
    p_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "game_docs"


class ItemCategory(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "item_category"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "tag"


class Items(models.Model):
    name = models.CharField(max_length=100)
    jp_name = models.CharField(max_length=100, blank=True, null=True)
    en_name = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.CharField(max_length=100, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "items"


class ItemsItemCategory(models.Model):
    pk = models.CompositePrimaryKey("item_id", "category_id")
    item_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "items_item_category"


class PetCaptureMethod(models.Model):
    pet_region_id = models.IntegerField(blank=True, null=True)
    method = models.CharField(max_length=100, blank=True, null=True)
    detail = models.CharField(max_length=20, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_capture_method"


class PetEggGroup(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_egg_group"


class PetFeature(models.Model):
    introduction = models.CharField(max_length=100, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_feature"


class PetGeneration(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_generation"


class PetGuide(models.Model):
    pet_id = models.IntegerField(primary_key=True)
    detail = models.CharField(max_length=50, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_guide"


class PetImage(models.Model):
    pet_id = models.IntegerField()
    image_url = models.CharField(max_length=255)
    sort = models.IntegerField()
    is_cover = models.IntegerField()
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_image"
        unique_together = (("pet_id", "image_url"),)


class PetRance(models.Model):
    p_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    hp = models.IntegerField(blank=True, null=True)
    attack = models.IntegerField(blank=True, null=True)
    defense = models.IntegerField(blank=True, null=True)
    special_attack = models.IntegerField(blank=True, null=True)
    special_defense = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    is_delete = models.IntegerField()
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_rance"


class PetRegion(models.Model):
    p_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_region"


class PetSkill(models.Model):
    learn_type = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    attribute_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.CharField(max_length=100, blank=True, null=True)
    detail = models.CharField(max_length=100, blank=True, null=True)
    damage = models.IntegerField(blank=True, null=True)
    aim = models.IntegerField(blank=True, null=True)
    pp = models.IntegerField(blank=True, null=True)
    cost_time = models.IntegerField(blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_skill"


class PetSkillAffected(models.Model):
    pet_skill_id = models.IntegerField(primary_key=True)
    is_touch = models.IntegerField(blank=True, null=True)
    defense = models.IntegerField(blank=True, null=True)
    magic_reflect = models.IntegerField(blank=True, null=True)
    learn_speech = models.IntegerField(blank=True, null=True)
    proof_of_king = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_skill_affected"


class PetSkillAttribute(models.Model):
    pk = models.CompositePrimaryKey("pet_skill_id", "attribute_id")
    pet_skill_id = models.IntegerField()
    attribute_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pet_skill_attribute"


class PetSkillCategory(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pet_skill_category"


class Pets(models.Model):
    name = models.CharField(unique=True, max_length=100)
    jp_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    weight = models.IntegerField()
    gender_male_ratio = models.IntegerField(blank=True, null=True)
    base_point_type = models.IntegerField(blank=True, null=True)
    base_point_value = models.IntegerField(blank=True, null=True)
    capture_probability = models.IntegerField(blank=True, null=True)
    egg_hatching_steps = models.IntegerField(blank=True, null=True)
    create_by = models.IntegerField()
    modified_by = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pets"


class PetsAttribute(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "attribute_id")
    pet_id = models.IntegerField()
    attribute_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_attribute"


class PetsEggGroup(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "egg_group_id")
    pet_id = models.IntegerField()
    egg_group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_egg_group"


class PetsPetFeature(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "feature_id")
    pet_id = models.IntegerField()
    feature_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_pet_feature"


class PetsPetGeneration(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "generation_id")
    pet_id = models.IntegerField()
    generation_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_pet_generation"


class PetsPetGuide(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "guide_id")
    pet_id = models.IntegerField()
    guide_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_pet_guide"


class PetsPetRance(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "rance_id")
    pet_id = models.IntegerField()
    rance_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_pet_rance"


class PetsPetRegion(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "region_id")
    pet_id = models.IntegerField()
    region_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_pet_region"


class PetsPetSkill(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "skill_id")
    pet_id = models.IntegerField()
    skill_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_pet_skill"


class PetsTag(models.Model):
    pk = models.CompositePrimaryKey("pet_id", "tag_id")
    pet_id = models.IntegerField()
    tag_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pets_tag"
