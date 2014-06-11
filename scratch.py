#!/usr/bin/env python
from app import db
from app.models import System, Reservation
from datetime import date, time, datetime, timedelta

#b118 = System.query.get(1)
#b120 = System.query.get(2)
#b122 = System.query.get(3)
#
#start_d = date(2014, 06, 10)
#time = time(17)

#print b118.reservations.filter(Reservation.start_date == start_d).all()

#print Reservation.query.all()

#print b118.is_reserved(date=start_d, time=time)

systems = System.query.all()
hour_list = []
start_t = datetime.combine(date.today(), time(hour=18))
for hr in range(24):
    new_t = start_t + timedelta(hours=hr)
    hour_list.append(new_t.time())

#print hour_list

matrix = []
for h in hour_list:
    h_row = [h.strftime("%H:%M %p")]
    for sys in systems:
        res = sys.is_reserved(date=date(2014, 6, 10), time=h)
        if res is not None:
            h_row.append(res)
        else:
            h_row.append(None)
    h_row.append(h.strftime("%H:%M %p"))
    matrix.append(h_row)

for row in matrix:
    print ' '.join(row)