import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_headmaster_user():
    user = User.objects.create_user(
        username="hm", password="pass", role="headmaster"
    )
    assert user.username == "hm"
    assert user.role == "headmaster"
    assert user.check_password("pass")
