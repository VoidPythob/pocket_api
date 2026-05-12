from __future__ import annotations

from typing import Any

from rest_framework import serializers
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.pokemon_csv_importer import (
    DEFAULT_POKEMON_CSV_PATH,
    import_pokemon_csv,
    load_builtin_pokemon_csv_rows,
    load_uploaded_pokemon_csv_rows,
)
from pocket_api.result import Result
from pocket_api.serializers import AdminPokemonCsvImportSerializer


class AdminPokemonCsvImportView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPokemonCsvImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uploaded_file = serializer.validated_data.get("file")
            if uploaded_file is not None:
                rows = load_uploaded_pokemon_csv_rows(uploaded_file)
                source = getattr(uploaded_file, "name", "uploaded.csv")
            else:
                rows = load_builtin_pokemon_csv_rows()
                source = str(DEFAULT_POKEMON_CSV_PATH)

            summary = import_pokemon_csv(
                rows=rows,
                admin_user_id=request.user.id,
                overwrite_existing=serializer.validated_data["overwrite_existing"],
            )
        except (FileNotFoundError, UnicodeDecodeError, ValueError) as exc:
            raise serializers.ValidationError(str(exc)) from exc

        return Result.created(
            data={
                "source": source,
                "overwrite_existing": serializer.validated_data["overwrite_existing"],
                **summary,
            },
            msg="pokemon csv import success",
        ).to_response()
