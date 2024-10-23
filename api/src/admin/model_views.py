from sqladmin import ModelView

from ..auth.models import User
from ..auth.models import JWTBlackList


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.steam_connected,
        User.is_superuser,
    ]
    column_details_exclude_list = [
        User.hashed_password,
    ]
    can_create = False
    form_excluded_columns = [User.created_at, User.updated_at]


class JWTBlackListAdmin(ModelView, model=JWTBlackList):
    column_list = [
        JWTBlackList.id,
        JWTBlackList.token,
    ]


def get_model_views() -> list[ModelView]:
    return [
        UserAdmin,
        JWTBlackListAdmin,
    ]
