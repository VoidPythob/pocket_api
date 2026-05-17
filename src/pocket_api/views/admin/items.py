from __future__ import annotations

from typing import Any

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import ItemCategory, Items, ItemsItemCategory
from pocket_api.result import Result
from pocket_api.serializers import (
    AdminItemCategoryRelationCreateSerializer,
    AdminItemCategoryRelationUpdateSerializer,
    AdminItemCategorySerializer,
    AdminItemSerializer,
)


class AdminItemView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            item = get_object_or_404(Items, pk=pk)
            serializer = AdminItemSerializer(item)
            return Result.success(data=serializer.data, msg="success").to_response()

        queryset = Items.objects.all().order_by("-id")
        serializer = AdminItemSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="success").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminItemSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Result.created(
            data=AdminItemSerializer(item).data,
            msg="created",
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        item = get_object_or_404(Items, pk=kwargs["pk"])
        if ItemsItemCategory.objects.filter(item_id=item.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="item is referenced by item categories",
            ).to_response()

        data = AdminItemSerializer(item).data
        item.delete()
        return Result.success(data=data, msg="deleted").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        item = get_object_or_404(Items, pk=kwargs["pk"])
        serializer = AdminItemSerializer(
            item,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Result.success(
            data=AdminItemSerializer(item).data,
            msg="updated",
        ).to_response()


class AdminItemCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            category = get_object_or_404(ItemCategory, pk=pk)
            serializer = AdminItemCategorySerializer(category)
            return Result.success(data=serializer.data, msg="success").to_response()

        queryset = ItemCategory.objects.all().order_by("-id")
        serializer = AdminItemCategorySerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="success").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminItemCategorySerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Result.created(
            data=AdminItemCategorySerializer(category).data,
            msg="created",
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        category = get_object_or_404(ItemCategory, pk=kwargs["pk"])
        if ItemsItemCategory.objects.filter(category_id=category.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="item category is referenced by items",
            ).to_response()

        data = AdminItemCategorySerializer(category).data
        category.delete()
        return Result.success(data=data, msg="deleted").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        category = get_object_or_404(ItemCategory, pk=kwargs["pk"])
        serializer = AdminItemCategorySerializer(
            category,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Result.success(
            data=AdminItemCategorySerializer(category).data,
            msg="updated",
        ).to_response()


class AdminItemCategoryRelationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        item = self._get_item(kwargs["item_id"])
        relations = list(ItemsItemCategory.objects.filter(item_id=item.id))
        category_ids = [relation.category_id for relation in relations]
        category_map = {
            category.id: category
            for category in ItemCategory.objects.filter(id__in=category_ids)
        }
        data = {
            "item_id": item.id,
            "item_name": item.name,
            "categories": [
                self._build_category_payload(item, category_map[relation.category_id])
                for relation in relations
                if relation.category_id in category_map
            ],
        }
        return Result.success(data=data, msg="success").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        item = self._get_item(kwargs["item_id"])
        serializer = AdminItemCategoryRelationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = self._get_category(serializer.validated_data["category_id"])

        if ItemsItemCategory.objects.filter(
            item_id=item.id,
            category_id=category.id,
        ).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="item category relation already exists",
            ).to_response()

        ItemsItemCategory.objects.create(item_id=item.id, category_id=category.id)
        return Result.created(
            data=self._build_category_payload(item, category),
            msg="created",
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        item = self._get_item(kwargs["item_id"])
        old_category = self._get_item_relation_category(item.id, kwargs["category_id"])
        serializer = AdminItemCategoryRelationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_category = self._get_category(serializer.validated_data["new_category_id"])

        if old_category.id == new_category.id:
            return Result.success(
                data=self._build_category_payload(item, old_category),
                msg="updated",
            ).to_response()

        if ItemsItemCategory.objects.filter(
            item_id=item.id,
            category_id=new_category.id,
        ).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="item category relation already exists",
            ).to_response()

        with transaction.atomic():
            ItemsItemCategory.objects.filter(
                item_id=item.id,
                category_id=old_category.id,
            ).delete()
            ItemsItemCategory.objects.create(
                item_id=item.id,
                category_id=new_category.id,
            )

        return Result.success(
            data=self._build_category_payload(item, new_category),
            msg="updated",
        ).to_response()

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        item = self._get_item(kwargs["item_id"])
        category = self._get_item_relation_category(item.id, kwargs["category_id"])
        ItemsItemCategory.objects.filter(
            item_id=item.id,
            category_id=category.id,
        ).delete()
        return Result.success(
            data=self._build_category_payload(item, category),
            msg="deleted",
        ).to_response()

    @staticmethod
    def _get_item(pk: int) -> Items:
        return get_object_or_404(Items, pk=pk)

    @staticmethod
    def _get_category(pk: int) -> ItemCategory:
        return get_object_or_404(ItemCategory, pk=pk)

    def _get_item_relation_category(
        self, item_id: int, category_id: int
    ) -> ItemCategory:
        relation = get_object_or_404(
            ItemsItemCategory,
            item_id=item_id,
            category_id=category_id,
        )
        return self._get_category(relation.category_id)

    @staticmethod
    def _build_category_payload(item: Items, category: ItemCategory) -> dict[str, Any]:
        return {
            "item_id": item.id,
            "item_name": item.name,
            "category_id": category.id,
            "category_name": category.name,
        }
