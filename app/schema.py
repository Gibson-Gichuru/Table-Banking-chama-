from marshmallow import Schema, fields, pre_load, validate

from app import ma


class RoleSchema(ma.Schema):

    Id = fields.Integer(dumps_only=True)
    Name = fields.String(required=True, validate=validate.Length(3))
    Users = fields.Nested("UserSchema", many=True)


class UserSchema(ma.Schema):

    Id = fields.Integer(dumps_only=True)
    RegisterTime = fields.DateTime(dumps_only=True)
    UserName = fields.String(required=True, validate=validate.Length(3))
    Password = fields.String(required=True, validate=validate.Length(
        8), error="Your Password Needs to be 8 chatacters long")
    PhoneNumber = fields.String(required=True, validate=validate.Regexp(
        "(\+?254|0)(7)([0-9]{8})$", error="Use 07xxxxxxx format "))
    Email = fields.String(required=True, validate=validate.Email(error="give a valide email"))

class PaymentSchema(ma.Schema):

    id = fields.Integer(dumps_only = True)
    TransId = fields.String(required=True, validate=validate.Length(4))
    TransTime = fields.String(required=True, validate=validate.Length(4))
    TransAmount = fields.String(required=True, validate=validate.Length(1))
    BussinessShortCode = fields.String(required=True, validate=validate.Length(2))
    BillRefNumber = fields.String(required=True, validate=validate.Length(4))
    OrgAccountBalance = fields.String(required=True, validate=validate.Length(4))
    ThirdPartyTransId = fields.String(required=True, validate=validate.Length(4))
    MSISDN = fields.String(required=True, validate=validate.Length(4))
    FirstName = fields.String(required=True, validate=validate.Length(1))
    MiddleName = fields.String(required=True, validate=validate.Length(1))
    LastName = fields.String(required=True, validate=validate.Length(1))







    
    
