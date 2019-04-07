import csv
from weddingRegistry.models import User
from weddingRegistry import db


with open('list_of_users.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    for row in csv_reader:
        user = User(name = row[0],
                    email = row[1].lower(),
                    password = None,
                    phone_number = row[2],
                    guests = row[3],
                    guests_names = row[4],
                    guests_confirmed = None,
                    total_guests = 0,
                    is_RSVP = False,
                    date_RSVP = None,
                    update_date_RSVP = None,
                    update_times = 0)
        db.session.add(user)
    db.session.commit()
        #print(f"Name: {row[0]} email: {(row[1]).lower()} tel: {row[2]} p: {row[3]} n: {row[4]}")
        # row[0], row[1], row[2], row[3], row[4])
