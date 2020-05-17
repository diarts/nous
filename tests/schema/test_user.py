import pytest

from marshmallow import ValidationError

from nous_auth.schema.user import AccountReg
from .data import RegisterAccData


@pytest.mark.schema
def test_registration():
    schema = AccountReg()

    assert schema.dump(
        RegisterAccData.correct_acc) == RegisterAccData.correct_acc
    with pytest.raises(ValidationError):
        schema.dump(RegisterAccData.missed_email_and_phone)
        schema.dump(RegisterAccData.missed_password)
        schema.dump(RegisterAccData.wrong_country)
        schema.dump(RegisterAccData.wrong_mail)
        schema.dump(RegisterAccData.wrong_phone)
