#!/usr/bin/env python
from app import db
from app.models import System, Reservation
from datetime import date, time, datetime, timedelta

reservation = Reservation.query.get(32)
user_id = reservation.reserved_by
system = reservation.device
date = reservation.res_datetime

search_res = True

while search_res:
    date = date + timedelta(hours=1)
    next_res = Reservation.query.filter(Reservation.res_datetime == date, Reservation.reserved_by == user_id, Reservation.device == system).all()

    if next_res:
        print next_res
    else:
        search_res = False

#b118 = System.query.get(1)
#b120 = System.query.get(2)
#b122 = System.query.get(3)
#
#start_d = date(2014, 06, 10)
#time = time(17)

#print b118.reservations.filter(Reservation.start_date == start_d).all()

#print System.query.all()
#print Reservation.query.all()

#b090 = System.query.get(2)
#print b090

#d = date.today()
#t = time(hour=18)
#dt = datetime.combine(d,t)
#
#print b090.is_reserved(res_datetime=dt)

#print b118.is_reserved(date=start_d, time=time)

#systems = System.query.all()
#hour_list = []
#start_t = datetime.combine(date.today(), time(hour=18))
#for hr in range(24):
#    new_t = start_t + timedelta(hours=hr)
#    hour_list.append(new_t.time())
#
##print hour_list
#
#matrix = {}
#for h in hour_list:
#    #h_row = [h.strftime("%H:%M %p")]
#    h_row = []
#    for sys in systems:
#        res = sys.is_reserved(date=date(2014, 6, 10), time=h)
#        if res is not None:
#            h_row.append(res)
#        else:
#            h_row.append(None)
#    #h_row.append(h.strftime("%H:%M %p"))
#    zipped = zip(systems, h_row)
#    matrix[h] = zipped
#
#for k in sorted(matrix.keys()):
#    for l in matrix[k]:
#        print l