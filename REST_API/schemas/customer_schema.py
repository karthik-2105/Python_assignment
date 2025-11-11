from marshmallow import Schema, fields, validate

class CustomerSchema(Schema):
    CustomerID = fields.Str(required=True)
    CustomerName = fields.Str(required=True, validate=validate.Length(min=3))
    Address = fields.Str(required=True)
    City = fields.Str(required=True)
    PostalCode = fields.Str(required=True, validate=validate.Length(equal=6))
    Country = fields.Str(required=True)

   
