from server.db import orm, sa, Base


class Device(Base):
    __tablename__ = 'devices'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(20), nullable=False)
    interface = sa.Column(sa.String(10), nullable=False)
    mac = sa.Column(sa.String(17), nullable=False)
    active = sa.Column(sa.Boolean, default=True)
    scripts = orm.relationship('Script', backref='owner', lazy=True)

    def __repr__(self):
        return "User<name={}, mac={}>".format(self.name, self.mac)


class Script(Base):
    __tablename__ = 'scripts'
    id = sa.Column(sa.Integer, primary_key=True)
    command = sa.Column(sa.String, nullable=False)
    device_id = sa.Column(sa.Integer, sa.ForeignKey(
        'devices.id'), nullable=False)

    def __repr__(self):
        return "Script({} | {})".format(self.device_id, self.command)
