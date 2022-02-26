from csv import csv,DictWriter, DictReader

FILEPATHDATA = "data/products.csv"
FILEPATH = "app/products/products.csv"

def write_product_in_csv():
    with open(FILEPATHDATA, "r") as csv_infile:
        csv_products = csv.DictReader(csv_infile, delimiter=',')
        fieldnames = csv_products.fieldnames

        with open(FILEPATH, "w") as csv_outfile:

            writer = DictWriter(csv_outfile, fieldnames)

            writer.writeheader()
            writer.writerows(list(csv_products))


write_product_in_csv()