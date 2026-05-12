from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import ItemCategory, Items, ItemsItemCategory
from pocket_api.result import Result
from pocket_api.serializers import (
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
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = Items.objects.all().order_by("-id")
        serializer = AdminItemSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminItemSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Result.created(
            data=AdminItemSerializer(item).data, msg="创建成功"
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
                msg="该物品已被分类关联，不能删除",
            ).to_response()

        data = AdminItemSerializer(item).data
        item.delete()
        return Result.success(data=data, msg="删除成功").to_response()

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
            data=AdminItemSerializer(item).data, msg="修改成功"
        ).to_response()


class AdminItemCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            category = get_object_or_404(ItemCategory, pk=pk)
            serializer = AdminItemCategorySerializer(category)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = ItemCategory.objects.all().order_by("-id")
        serializer = AdminItemCategorySerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminItemCategorySerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Result.created(
            data=AdminItemCategorySerializer(category).data, msg="创建成功"
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
                msg="该物品分类已被物品关联，不能删除",
            ).to_response()

        data = AdminItemCategorySerializer(category).data
        category.delete()
        return Result.success(data=data, msg="删除成功").to_response()

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
            data=AdminItemCategorySerializer(category).data, msg="修改成功"
        ).to_response()
