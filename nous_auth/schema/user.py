from marshmallow import fields, Schema, post_load, post_dump, ValidationError
from trafaret import DataError

from ..validation.user import (
    REGISTER,
    phone_validation,
    authorization_validation,
)


class Account(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(dump_only=True)
    password = fields.Str(dump_only=True)
    username = fields.Str(dump_only=True)
    phone = fields.Int(dump_only=True)
    create_date = fields.Int(dump_only=True)
    vip = fields.Int(dump_only=True)
    blocked = fields.Int(dump_only=True)
    role = fields.Int(dump_only=True)
    country = fields.Int(dump_only=True)


class GetAccount(Account):
    @post_dump
    def rm_pass(self, data, **kwargs):
        try:
            data.pop('password')
        except KeyError:
            pass
        try:
            data.pop('id')
        except KeyError:
            pass

        return data


class AccountReg(Account):
    email = fields.Str(required=False)
    password = fields.Str(required=True)
    username = fields.Str(required=False)
    phone = fields.Int(required=False)
    country = fields.Int(required=False)

    @post_load
    def validation(self, data, **kwargs):
        try:
            phone_validation(
                phone=data.get('phone'),
                country=data.get('country')
            )
            REGISTER.check(data)

            if not data.get('email') and (not data.get('phone')
                                          and not data.get('country')):
                raise DataError(
                    error='For registration require email or phone + country.'
                )
        except DataError as err:
            raise ValidationError(message=f'{err}')
        return data


class AccountAuth(AccountReg):
    @post_load
    def validation(self, data, **kwargs):
        authorization_validation(data)
        return data
