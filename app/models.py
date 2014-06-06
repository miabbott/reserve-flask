from app import db

class System(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    host_name = db.Column(db.String, index = True)
    host_type = db.Column(db.String, index = True)
    host_ip = db.Column(db.String(15), index = True)
    host_location = db.Column(db.String)
    sp_name = db.Column(db.String, index = True)
    sp_ip = db.Column(db.String(15), index = True)
    console_cmd = db.Column(db.String)
    console_name = db.Column(db.String, index = True)
    apc_url = db.Column(db.String)
    apc_user = db.Column(db.String)
    apc_passwd = db.Column(db.String)
    reservations = db.relationship('Reservation', backref = 'device', lazy = 'dynamic')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_date = db.Column(db.Date)
    end_time = db.Column(db.Time)
    reserved_by = db.Column(db.String, index = True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'))