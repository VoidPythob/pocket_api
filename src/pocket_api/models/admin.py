from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class AdminUserManager(BaseUserManager):
    use_in_migrations = False

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: object
    ) -> "AdminUser":
        if not email:
            raise ValueError("邮箱不能为空")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: object
    ) -> "AdminUser":
        return self.create_user(email=email, password=password, **extra_fields)


class AdminUser(AbstractBaseUser):
    email = models.CharField(max_length=50, unique=True, db_comment="邮箱")
    last_login_ip = models.CharField(
        max_length=50, blank=True, null=True, db_comment="上次登录ip"
    )
    last_login = models.DateTimeField(
        db_column="last_login_time",
        blank=True,
        null=True,
        db_comment="上次登录时间",
    )
    last_logout_time = models.DateTimeField(
        blank=True, null=True, db_comment="上次登出时间"
    )
    create_at = models.DateTimeField(blank=True, null=True, db_comment="创建时间")
    objects = AdminUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        managed = False
        db_table = "admin_user"
        db_table_comment = "管理员用户"

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self) -> bool:
        return True

    def has_perm(self, perm: str, obj: object | None = None) -> bool:
        return True

    def has_module_perms(self, app_label: str) -> bool:
        return True
