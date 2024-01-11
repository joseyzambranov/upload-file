import csv

csv_in = csv.DictReader(open('base.csv'))
columns = ["emailAddress","unsubscribeAll"]
csv_out = csv.DictWriter(open('base2.csv','w'),columns)
csv_out.writeheader()

for row in csv_in:
   nrow = {
      "emailAddress": row["email"],
      "unsubscribeAll": "false"
   }

   csv_out.writerow(nrow)