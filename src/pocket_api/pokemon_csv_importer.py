from __future__ import annotations

import ast
import csv
import io
import re
from pathlib import Path

from django.db import transaction
from django.utils import timezone

from pocket_api.models import (
    Attribute,
    PetFeature,
    PetGeneration,
    PetGuide,
    PetRance,
    Pets,
    PetsAttribute,
    PetsPetFeature,
    PetsPetGeneration,
    PetsPetRance,
    PetsTag,
    Tag,
)

DEFAULT_POKEMON_CSV_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "pokemon.csv"
)

TYPE_NAME_MAP = {
    "normal": "\u4e00\u822c",
    "fire": "\u706b",
    "water": "\u6c34",
    "electric": "\u7535",
    "grass": "\u8349",
    "ice": "\u51b0",
    "fighting": "\u683c\u6597",
    "poison": "\u6bd2",
    "ground": "\u5730\u9762",
    "flying": "\u98de\u884c",
    "psychic": "\u8d85\u80fd\u529b",
    "bug": "\u866b",
    "rock": "\u5ca9\u77f3",
    "ghost": "\u5e7d\u7075",
    "dragon": "\u9f99",
    "dark": "\u6076",
    "steel": "\u94a2",
    "fairy": "\u5996\u7cbe",
}

GENERATION_NAME_MAP = {
    1: "\u7b2c\u4e00\u4e16\u4ee3",
    2: "\u7b2c\u4e8c\u4e16\u4ee3",
    3: "\u7b2c\u4e09\u4e16\u4ee3",
    4: "\u7b2c\u56db\u4e16\u4ee3",
    5: "\u7b2c\u4e94\u4e16\u4ee3",
    6: "\u7b2c\u516d\u4e16\u4ee3",
    7: "\u7b2c\u4e03\u4e16\u4ee3",
}

LEGENDARY_TAG_NAME = "\u4f20\u8bf4"
LEGENDARY_TAG_COLOR = "#f59e0b"


def load_builtin_pokemon_csv_rows() -> list[dict[str, str]]:
    with DEFAULT_POKEMON_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def load_uploaded_pokemon_csv_rows(uploaded_file) -> list[dict[str, str]]:
    content = uploaded_file.read()
    if isinstance(content, str):
        text = content
    else:
        text = content.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def import_pokemon_csv(
    *,
    rows: list[dict[str, str]],
    admin_user_id: int,
    overwrite_existing: bool,
) -> dict[str, object]:
    importer = PokemonCsvImporter(
        rows=rows,
        admin_user_id=admin_user_id,
        overwrite_existing=overwrite_existing,
    )
    return importer.run()


class PokemonCsvImporter:
    def __init__(
        self,
        *,
        rows: list[dict[str, str]],
        admin_user_id: int,
        overwrite_existing: bool,
    ) -> None:
        self.rows = rows
        self.admin_user_id = admin_user_id
        self.overwrite_existing = overwrite_existing
        self.now = timezone.now()
        self.summary: dict[str, object] = {
            "total_rows": len(rows),
            "created_pets": 0,
            "updated_pets": 0,
            "skipped_pets": 0,
            "created_generations": 0,
            "created_attributes": 0,
            "created_features": 0,
            "created_tags": 0,
            "created_rances": 0,
            "created_guides": 0,
            "linked_generations": 0,
            "linked_attributes": 0,
            "linked_features": 0,
            "linked_tags": 0,
        }

    def run(self) -> dict[str, object]:
        normalized_rows = [
            self._normalize_row(row, row_number=index)
            for index, row in enumerate(self.rows, start=2)
        ]

        with transaction.atomic():
            for row in normalized_rows:
                self._import_row(row)

        return self.summary

    def _import_row(self, row: dict[str, object]) -> None:
        pet, pet_created = self._upsert_pet(row)
        if pet is None:
            self.summary["skipped_pets"] = int(self.summary["skipped_pets"]) + 1
            return

        if pet_created:
            self.summary["created_pets"] = int(self.summary["created_pets"]) + 1
        else:
            self.summary["updated_pets"] = int(self.summary["updated_pets"]) + 1

        generation = self._upsert_generation(int(row["generation"]))
        if self._replace_single_relation(
            model=PetsPetGeneration,
            pet_id=pet.id,
            field_name="generation_id",
            target_id=generation.id,
        ):
            self.summary["linked_generations"] = (
                int(self.summary["linked_generations"]) + 1
            )

        attribute_ids = [
            self._upsert_attribute(type_name).id
            for type_name in row["types"]  # type: ignore[index]
        ]
        if self._replace_relation_set(
            model=PetsAttribute,
            pet_id=pet.id,
            field_name="attribute_id",
            target_ids=attribute_ids,
        ):
            self.summary["linked_attributes"] = (
                int(self.summary["linked_attributes"]) + len(attribute_ids)
            )

        feature_ids = [
            self._upsert_feature(ability_name).id
            for ability_name in row["abilities"]  # type: ignore[index]
        ]
        if self._replace_relation_set(
            model=PetsPetFeature,
            pet_id=pet.id,
            field_name="feature_id",
            target_ids=feature_ids,
        ):
            self.summary["linked_features"] = (
                int(self.summary["linked_features"]) + len(feature_ids)
            )

        rance = self._upsert_rance(pet=pet, row=row)
        self._replace_single_relation(
            model=PetsPetRance,
            pet_id=pet.id,
            field_name="rance_id",
            target_id=rance.id,
        )

        self._upsert_guide(
            pet_id=pet.id,
            classification=str(row["classification"]),
        )
        self._sync_legendary_tag(
            pet_id=pet.id,
            is_legendary=bool(row["is_legendary"]),
        )

    def _upsert_pet(self, row: dict[str, object]) -> tuple[Pets | None, bool]:
        en_name = str(row["en_name"])
        pet = Pets.objects.filter(en_name=en_name).first()
        if pet is None:
            pet = Pets.objects.filter(name=en_name).first()

        if pet is not None and not self.overwrite_existing:
            return None, False

        defaults = {
            "jp_name": str(row["jp_name"]),
            "en_name": en_name,
            "weight": int(row["weight"]),
            "gender_male_ratio": row["gender_male_ratio"],
            "capture_probability": row["capture_probability"],
            "egg_hatching_steps": row["egg_hatching_steps"],
        }

        if pet is None:
            return (
                Pets.objects.create(
                    name=en_name,
                    jp_name=defaults["jp_name"],
                    en_name=defaults["en_name"],
                    weight=defaults["weight"],
                    gender_male_ratio=defaults["gender_male_ratio"],
                    base_point_type=None,
                    base_point_value=None,
                    capture_probability=defaults["capture_probability"],
                    egg_hatching_steps=defaults["egg_hatching_steps"],
                    create_by=self.admin_user_id,
                    create_at=self.now,
                ),
                True,
            )

        if not pet.name or pet.name == pet.en_name:
            pet.name = en_name
        pet.jp_name = defaults["jp_name"]
        pet.en_name = defaults["en_name"]
        pet.weight = defaults["weight"]
        pet.gender_male_ratio = defaults["gender_male_ratio"]
        pet.capture_probability = defaults["capture_probability"]
        pet.egg_hatching_steps = defaults["egg_hatching_steps"]
        pet.modified_by = self.admin_user_id
        pet.modified_at = self.now
        pet.save()
        return pet, False

    def _upsert_generation(self, generation_number: int) -> PetGeneration:
        generation = PetGeneration.objects.filter(pk=generation_number).first()
        generation_name = GENERATION_NAME_MAP.get(
            generation_number,
            f"\u7b2c{generation_number}\u4e16\u4ee3",
        )
        if generation is None:
            self.summary["created_generations"] = (
                int(self.summary["created_generations"]) + 1
            )
            return PetGeneration.objects.create(
                id=generation_number,
                name=generation_name,
                create_by=self.admin_user_id,
                create_at=self.now,
            )

        if generation.name != generation_name:
            generation.name = generation_name
            generation.modified_by = self.admin_user_id
            generation.modified_at = self.now
            generation.save(update_fields=["name", "modified_by", "modified_at"])
        return generation

    def _upsert_attribute(self, type_name: str) -> Attribute:
        display_name = TYPE_NAME_MAP.get(type_name.lower(), type_name)
        attribute = Attribute.objects.filter(name=display_name).first()
        if attribute is not None:
            return attribute

        self.summary["created_attributes"] = (
            int(self.summary["created_attributes"]) + 1
        )
        return Attribute.objects.create(
            name=display_name,
            create_by=self.admin_user_id,
            create_at=self.now,
        )

    def _upsert_feature(self, ability_name: str) -> PetFeature:
        feature = PetFeature.objects.filter(introduction=ability_name).first()
        if feature is not None:
            return feature

        self.summary["created_features"] = (
            int(self.summary["created_features"]) + 1
        )
        return PetFeature.objects.create(
            introduction=ability_name,
            detail="Imported from pokemon.csv",
            create_by=self.admin_user_id,
            create_at=self.now,
        )

    def _upsert_rance(self, *, pet: Pets, row: dict[str, object]) -> PetRance:
        pokedex_number = int(row["pokedex_number"])
        rance = PetRance.objects.filter(p_id=pokedex_number, is_delete=0).first()
        if rance is None:
            self.summary["created_rances"] = int(self.summary["created_rances"]) + 1
            return PetRance.objects.create(
                p_id=pokedex_number,
                name=pet.name,
                hp=int(row["hp"]),
                attack=int(row["attack"]),
                defense=int(row["defense"]),
                special_attack=int(row["sp_attack"]),
                special_defense=int(row["sp_defense"]),
                speed=int(row["speed"]),
                total=int(row["base_total"]),
                is_delete=0,
                create_by=self.admin_user_id,
                create_at=self.now,
            )

        rance.name = pet.name
        rance.hp = int(row["hp"])
        rance.attack = int(row["attack"])
        rance.defense = int(row["defense"])
        rance.special_attack = int(row["sp_attack"])
        rance.special_defense = int(row["sp_defense"])
        rance.speed = int(row["speed"])
        rance.total = int(row["base_total"])
        rance.modified_by = self.admin_user_id
        rance.modified_at = self.now
        rance.save()
        return rance

    def _upsert_guide(self, *, pet_id: int, classification: str) -> None:
        guide = PetGuide.objects.filter(pet_id=pet_id).first()
        if guide is None:
            self.summary["created_guides"] = int(self.summary["created_guides"]) + 1
            PetGuide.objects.create(
                pet_id=pet_id,
                detail=classification[:50],
                create_by=self.admin_user_id,
                create_at=self.now,
            )
            return

        guide.detail = classification[:50]
        guide.modified_by = self.admin_user_id
        guide.modified_at = self.now
        guide.save(update_fields=["detail", "modified_by", "modified_at"])

    def _sync_legendary_tag(self, *, pet_id: int, is_legendary: bool) -> None:
        tag = Tag.objects.filter(name=LEGENDARY_TAG_NAME).first()
        if is_legendary and tag is None:
            self.summary["created_tags"] = int(self.summary["created_tags"]) + 1
            tag = Tag.objects.create(
                name=LEGENDARY_TAG_NAME,
                color=LEGENDARY_TAG_COLOR,
                create_by=self.admin_user_id,
                create_at=self.now,
            )

        if tag is None:
            return

        relation = PetsTag.objects.filter(pet_id=pet_id, tag_id=tag.id)
        if is_legendary:
            if not relation.exists():
                PetsTag.objects.create(pet_id=pet_id, tag_id=tag.id)
                self.summary["linked_tags"] = int(self.summary["linked_tags"]) + 1
            return

        relation.delete()

    @staticmethod
    def _replace_single_relation(*, model, pet_id: int, field_name: str, target_id: int) -> bool:
        current_ids = list(
            model.objects.filter(pet_id=pet_id).values_list(field_name, flat=True)
        )
        if current_ids == [target_id]:
            return False

        model.objects.filter(pet_id=pet_id).delete()
        model.objects.create(pet_id=pet_id, **{field_name: target_id})
        return True

    @staticmethod
    def _replace_relation_set(
        *, model, pet_id: int, field_name: str, target_ids: list[int]
    ) -> bool:
        normalized_target_ids = list(dict.fromkeys(target_ids))
        current_ids = list(
            model.objects.filter(pet_id=pet_id)
            .order_by(field_name)
            .values_list(field_name, flat=True)
        )
        if current_ids == sorted(normalized_target_ids):
            return False

        model.objects.filter(pet_id=pet_id).delete()
        if normalized_target_ids:
            model.objects.bulk_create(
                [
                    model(pet_id=pet_id, **{field_name: target_id})
                    for target_id in normalized_target_ids
                ]
            )
        return True

    def _normalize_row(self, row: dict[str, str], *, row_number: int) -> dict[str, object]:
        en_name = self._require_value(row, "name", row_number)
        types = [
            value
            for value in [
                self._clean_text(row.get("type1")),
                self._clean_text(row.get("type2")),
            ]
            if value
        ]
        abilities = self._parse_abilities(row.get("abilities", ""))
        if not types:
            raise ValueError(f"row {row_number}: type1/type2 is empty")
        if not abilities:
            raise ValueError(f"row {row_number}: abilities is empty")

        return {
            "en_name": en_name,
            "jp_name": self._extract_japanese_name(
                self._clean_text(row.get("japanese_name")) or en_name
            ),
            "pokedex_number": self._parse_required_int(
                row.get("pokedex_number"),
                "pokedex_number",
                row_number,
            ),
            "generation": self._parse_required_int(
                row.get("generation"),
                "generation",
                row_number,
            ),
            "weight": self._parse_weight(row.get("weight_kg"), row_number),
            "gender_male_ratio": self._parse_optional_percent(
                row.get("percentage_male")
            ),
            "capture_probability": self._parse_optional_int(row.get("capture_rate")),
            "egg_hatching_steps": self._parse_optional_int(row.get("base_egg_steps")),
            "classification": self._clean_text(row.get("classfication")) or "",
            "hp": self._parse_required_int(row.get("hp"), "hp", row_number),
            "attack": self._parse_required_int(row.get("attack"), "attack", row_number),
            "defense": self._parse_required_int(
                row.get("defense"),
                "defense",
                row_number,
            ),
            "sp_attack": self._parse_required_int(
                row.get("sp_attack"),
                "sp_attack",
                row_number,
            ),
            "sp_defense": self._parse_required_int(
                row.get("sp_defense"),
                "sp_defense",
                row_number,
            ),
            "speed": self._parse_required_int(row.get("speed"), "speed", row_number),
            "base_total": self._parse_required_int(
                row.get("base_total"),
                "base_total",
                row_number,
            ),
            "types": list(dict.fromkeys(types)),
            "abilities": list(dict.fromkeys(abilities)),
            "is_legendary": self._parse_optional_int(row.get("is_legendary")) == 1,
        }

    @staticmethod
    def _require_value(row: dict[str, str], field_name: str, row_number: int) -> str:
        value = PokemonCsvImporter._clean_text(row.get(field_name))
        if not value:
            raise ValueError(f"row {row_number}: {field_name} is required")
        return value

    @staticmethod
    def _clean_text(value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @staticmethod
    def _parse_required_int(value: str | None, field_name: str, row_number: int) -> int:
        parsed = PokemonCsvImporter._parse_optional_int(value)
        if parsed is None:
            raise ValueError(f"row {row_number}: invalid {field_name}")
        return parsed

    @staticmethod
    def _parse_optional_int(value: str | None) -> int | None:
        cleaned = PokemonCsvImporter._clean_text(value)
        if cleaned is None:
            return None

        match = re.search(r"\d+(?:\.\d+)?", cleaned)
        if match is None:
            return None
        return int(float(match.group(0)))

    @staticmethod
    def _parse_optional_percent(value: str | None) -> int | None:
        cleaned = PokemonCsvImporter._clean_text(value)
        if cleaned is None:
            return None

        try:
            return int(float(cleaned))
        except ValueError:
            return None

    @staticmethod
    def _parse_weight(value: str | None, row_number: int) -> int:
        cleaned = PokemonCsvImporter._clean_text(value)
        if cleaned is None:
            return 0

        try:
            return int(round(float(cleaned) * 10))
        except ValueError as exc:
            raise ValueError(f"row {row_number}: invalid weight_kg") from exc

    @staticmethod
    def _parse_abilities(value: str) -> list[str]:
        cleaned = value.strip()
        if not cleaned:
            return []

        try:
            parsed = ast.literal_eval(cleaned)
        except (SyntaxError, ValueError):
            parsed = [item.strip(" '\"") for item in cleaned.strip("[]").split(",")]

        if not isinstance(parsed, list):
            return []
        return [str(item).strip() for item in parsed if str(item).strip()]

    @staticmethod
    def _extract_japanese_name(value: str) -> str:
        match = re.search(r"([^\x00-\x7F]+)$", value)
        if match is not None:
            return match.group(1)
        return value
