import csv


with open('list_of_users.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    for row in csv_reader:
        print(f"Name: {row[0]} email: {(row[1]).lower()} tel: {row[2]} p: {row[3]} n: {row[4]}")
        # row[0], row[1], row[2], row[3], row[4])
