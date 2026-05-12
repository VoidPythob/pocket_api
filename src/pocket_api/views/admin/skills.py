from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import (
    PetSkill,
    PetSkillAffected,
    PetSkillAttribute,
    PetSkillCategory,
    PetsPetSkill,
)
from pocket_api.result import Result
from pocket_api.serializers import (
    AdminPetSkillCategorySerializer,
    AdminPetSkillSerializer,
)


class AdminPetSkillView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            skill = get_object_or_404(PetSkill, pk=pk)
            serializer = AdminPetSkillSerializer(skill)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = PetSkill.objects.all().order_by("-id")
        serializer = AdminPetSkillSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetSkillSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        skill = serializer.save()
        return Result.created(
            data=AdminPetSkillSerializer(skill).data, msg="创建成功"
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        skill = get_object_or_404(PetSkill, pk=kwargs["pk"])
        if PetsPetSkill.objects.filter(skill_id=skill.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该技能已被宠物关联，不能删除",
            ).to_response()
        if PetSkillAttribute.objects.filter(pet_skill_id=skill.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该技能存在属性关联，不能删除",
            ).to_response()
        if PetSkillAffected.objects.filter(pet_skill_id=skill.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该技能存在受影响配置，不能删除",
            ).to_response()

        data = AdminPetSkillSerializer(skill).data
        skill.delete()
        return Result.success(data=data, msg="删除成功").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        skill = get_object_or_404(PetSkill, pk=kwargs["pk"])
        serializer = AdminPetSkillSerializer(
            skill,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        skill = serializer.save()
        return Result.success(
            data=AdminPetSkillSerializer(skill).data, msg="修改成功"
        ).to_response()


class AdminPetSkillCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            category = get_object_or_404(PetSkillCategory, pk=pk)
            serializer = AdminPetSkillCategorySerializer(category)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = PetSkillCategory.objects.all().order_by("-id")
        serializer = AdminPetSkillCategorySerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetSkillCategorySerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Result.created(
            data=AdminPetSkillCategorySerializer(category).data, msg="创建成功"
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        category = get_object_or_404(PetSkillCategory, pk=kwargs["pk"])
        if PetSkill.objects.filter(category_id=category.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该技能分类已被技能关联，不能删除",
            ).to_response()

        data = AdminPetSkillCategorySerializer(category).data
        category.delete()
        return Result.success(data=data, msg="删除成功").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        category = get_object_or_404(PetSkillCategory, pk=kwargs["pk"])
        serializer = AdminPetSkillCategorySerializer(
            category,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Result.success(
            data=AdminPetSkillCategorySerializer(category).data, msg="修改成功"
        ).to_response()
