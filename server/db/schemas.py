from server.db.models import Device, Script
import marshmallow_sqlalchemy as ma


class DeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Device
        include_relationships = True


class ScriptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Script
        include_fk = True
