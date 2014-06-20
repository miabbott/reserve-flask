from datetime import date, datetime
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

    def __repr__(self):
        return '<System %s>' % (self.host_name)

    def get_reservations(self, date=None, time=None):
        if date is None:
            date = datetime.today().date()
        
        if time is None:
            hour = datetime.today().hour
            time = datetime.time(hour=hour)
    
        return reservations.filter(Reservation.start_date == date, Reservation.start_time == time).all()
    
    def get_all_reservations(self):
        return reservations.all()
    
    def is_reserved(self, res_datetime=None):        
        res = self.reservations.filter(Reservation.res_datetime == res_datetime).all()

        if len(res) == 0:
            return None

        return res[0]

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    res_datetime = db.Column(db.DateTime, index=True)
    reserved_by = db.Column(db.String, index = True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'))
    
    def __repr__(self):
        return '<Reservation - ID: %s; DateTime: %s; ReservedBy: %s; Device: %s>' % (self.id, self.res_datetime, self.reserved_by, self.device)