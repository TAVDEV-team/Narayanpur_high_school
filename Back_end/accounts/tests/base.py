import pytest

from accounts.models import User


@pytest.fixture
def headmaster(db):
    return User.objects.create_user(
        username="hm", password="pass", role="headmaster"
    )


@pytest.fixture
def student(db):
    return User.objects.create_user(
        username="stu", password="pass", role="student"
    )


class BaseAccountTest:
    pass
