from uuid import uuid4

from django.db.models import BooleanField, DateTimeField, Model, UUIDField


class DefaultModel(Model):
    created_at = DateTimeField(
        auto_created=True, editable=False, auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class BaseUUIDModel(Model):
    id = UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = DateTimeField(
        auto_created=True, editable=False, auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True, db_index=True)
    is_deleted = BooleanField(null=True, blank=True, default=False)

    class Meta:
        abstract = True
