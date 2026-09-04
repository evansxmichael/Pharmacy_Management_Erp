import datetime
from django.core.management.base import BaseCommand
from store.models import Medicine, Stock, Supplier

# Master catalog: Name, Category, Pack Size, GST%, MRP, Purchase Cost
MEDICINE_DATA = [
    ("Anonymous", "General", "1 Unit", 12, 50.00, 35.00),
    ("Dulcoflex", "Laxative", "10 Tabs", 12, 12.38, 8.50),
    ("Sabgol", "Digestive", "100 g Pack", 5, 120.00, 90.00),
    ("ENO", "Antacid", "1 × 5 g Sachet", 12, 10.00, 7.50),
    ("Hajmola", "Digestive", "10 Tabs", 12, 5.84, 4.00),
    ("Pudin Hara", "Digestive", "10 Caps", 12, 35.00, 24.00),
    ("Cotton Roll", "First Aid", "50 g Roll", 12, 45.00, 28.00),
    ("Hansaplast", "First Aid", "10 Strips", 12, 23.40, 15.00),
    ("Band Aid", "First Aid", "10 Strips", 12, 25.00, 16.00),
    ("Savlon", "Antiseptic", "100 ml Bottle", 18, 58.00, 42.00),
    ("Dettol Antiseptic", "Antiseptic", "60 ml Bottle", 18, 45.63, 33.00),
    ("Burnol", "Ointment", "20 g Tube", 12, 98.00, 70.00),
    ("Soframycin", "Antibacterial", "30 g Tube", 12, 53.53, 38.00),
    ("Candid Cream", "Antifungal", "20 g Tube", 12, 96.00, 68.00),
    ("Azee 500", "Antibiotic", "5 Tabs", 12, 253.42, 180.00),
    ("Clavam 625", "Antibiotic", "10 Tabs", 12, 196.73, 140.00),
    ("Vicks Action 500", "Cold & Flu", "10 Tabs", 12, 64.00, 45.00),
    ("Koflet", "Cough Lozenges", "10 Lozenges", 12, 23.00, 15.00),
    ("Tixylix", "Cough Syrup", "100 ml Bottle", 12, 146.69, 105.00),
    ("Alex Syrup", "Cough Syrup", "100 ml Bottle", 12, 158.43, 115.00),
    ("Honitus Syrup", "Ayurvedic Cough", "100 ml Bottle", 12, 130.00, 95.00),
    ("Avil", "Antiallergic", "10 Tabs", 12, 9.55, 6.50),
    ("Levocetirizine", "Antiallergic", "10 Tabs", 12, 37.50, 22.00),
    ("Montair LC", "Antiallergic", "10 Tabs", 12, 279.86, 200.00),
    ("Ecosprin AV", "Cardiac", "10 Caps", 12, 41.31, 28.00),
    ("Atorvastatin", "Cholesterol", "10 Tabs", 12, 53.43, 35.00),
    ("Rosuvastatin", "Cholesterol", "10 Tabs", 12, 28.00, 18.00),
    ("Eltroxin", "Thyroid", "10 Tabs", 12, 9.50, 6.00),
    ("Thyronorm 50", "Thyroid", "10 Tabs", 12, 11.07, 7.50),
    ("Eldoper", "Antidiarrheal", "10 Caps", 12, 73.10, 50.00),
    ("Norflox TZ", "Antibiotic", "10 Tabs", 12, 116.96, 80.00),
    ("Electral Powder", "ORS", "10 Sachets", 12, 46.80, 32.00),
    ("Domstal", "Antiemetic", "10 Tabs", 12, 24.82, 16.00),
    ("Ondem", "Antiemetic", "10 Tabs", 12, 54.85, 36.00),
    ("Cefpodoxime", "Antibiotic", "10 Tabs", 12, 120.00, 85.00),
    ("Levofloxacin", "Antibiotic", "10 Tabs", 12, 80.00, 55.00),
    ("Ofloxacin", "Antibiotic", "10 Tabs", 12, 55.00, 35.00),
    ("Moxikind CV", "Antibiotic", "10 Tabs", 12, 184.14, 130.00),
    ("Taxim O", "Antibiotic", "10 Tabs", 12, 105.11, 72.00),
    ("Volini Gel", "Pain Relief", "30 g Tube", 12, 160.00, 110.00),
    ("Ultracet", "Pain Relief", "10 Tabs", 12, 115.00, 80.00),
    ("Nise", "Pain Relief", "10 Tabs", 12, 42.00, 28.00),
    ("Aceclofenac", "Pain Relief", "10 Tabs", 12, 45.00, 30.00),
    ("Zerodol SP", "Pain Relief", "10 Tabs", 12, 150.85, 105.00),
    ("Livogen", "Iron Supplement", "10 Tabs", 12, 75.00, 50.00),
    ("Dexorange Syrup", "Iron Tonic", "200 ml Bottle", 12, 217.30, 155.00),
    ("Feronia XT", "Iron Supplement", "10 Tabs", 12, 168.94, 120.00),
    ("Supradyn", "Multivitamin", "15 Tabs", 12, 50.00, 35.00),
    ("Limcee", "Vitamin C", "15 Tabs", 12, 30.00, 18.00),
    ("Evion 400", "Vitamin E", "10 Caps", 12, 38.00, 25.00),
    ("Pan D", "Gastro", "10 Caps", 12, 115.00, 75.00),
    ("Montek LC", "Antiallergic", "10 Tabs", 12, 120.00, 82.00),
    ("Augmentin", "Antibiotic", "10 Tabs", 12, 195.30, 140.00),
    ("Calpol Syrup", "Analgesic", "60 ml Bottle", 12, 65.00, 42.00),
    ("Allegra", "Antiallergic", "10 Tabs", 12, 225.00, 160.00),
    ("Otrivin Nasal Drops", "Nasal Decongestant", "10 ml Bottle", 12, 60.00, 40.00),
    ("Strepsils", "Lozenges", "8 Lozenges", 12, 68.00, 45.00),
    ("Cofsils", "Lozenges", "10 Lozenges", 12, 35.00, 22.00),
    ("Liv 52", "Hepatic Care", "60 Tabs Bottle", 12, 40.00, 26.00),
    ("Vicks Vaporub", "Cold Relief", "25 g Jar", 12, 50.00, 32.00),
    ("Moov Cream", "Pain Relief", "25 g Tube", 12, 75.00, 50.00),
    ("Volini Spray", "Pain Relief", "55 g Can", 12, 175.00, 120.00),
    ("Neurobion Forte", "Vitamin B", "10 Tabs", 12, 45.00, 30.00),
    ("Zincovit", "Multivitamin", "15 Tabs", 12, 115.00, 78.00),
    ("Becosules", "Vitamin B-Complex", "20 Caps", 12, 38.00, 25.00),
    ("Clopidogrel", "Cardiovascular", "10 Tabs", 12, 50.00, 32.00),
    ("Ecosprin", "Blood Thinner", "14 Tabs", 12, 15.00, 9.50),
    ("Atenolol", "Antihypertensive", "14 Tabs", 12, 22.50, 14.00),
    ("Telmisartan", "Antihypertensive", "10 Tabs", 12, 45.00, 28.00),
    ("Amlodipine", "Antihypertensive", "10 Tabs", 12, 22.50, 14.00),
    ("Januvia", "Antidiabetic", "7 Tabs", 12, 600.00, 450.00),
    ("Insulin Human Mixtard", "Insulin", "1 Cartridge (100 IU/ml)", 5, 250.00, 190.00),
    ("Glycomet", "Antidiabetic", "10 Tabs", 12, 22.50, 14.00),
    ("Glimepiride", "Antidiabetic", "10 Tabs", 12, 30.00, 18.00),
    ("Metformin", "Antidiabetic", "10 Tabs", 12, 18.00, 10.00),
    ("Gelusil", "Antacid", "10 Tabs", 12, 38.00, 24.00),
    ("Rantac", "Antacid", "10 Tabs", 12, 28.00, 17.00),
    ("Corex DX", "Cough Syrup", "100 ml Bottle", 12, 115.00, 78.00),
    ("Betadine", "Antiseptic", "100 ml Bottle", 12, 125.00, 85.00),
    ("ORS", "Electrolyte", "1 × 21.8 g Sachet", 12, 45.00, 30.00),
    ("Revital", "Nutritional", "10 Caps", 12, 120.00, 82.00),
    ("Shelcal", "Calcium Supplement", "15 Tabs", 12, 115.00, 78.00),
    ("Digene", "Antacid", "15 Tabs", 12, 28.00, 18.00),
    ("Ciprofloxacin", "Antibiotic", "10 Tabs", 12, 45.00, 28.00),
    ("Amoxicillin", "Antibiotic", "10 Caps", 12, 45.00, 28.00),
    ("Azithromycin", "Antibiotic", "3 Tabs", 12, 125.00, 85.00),
    ("Ibuprofen", "Pain Relief", "10 Tabs", 12, 22.50, 14.00),
    ("Combiflam", "Pain Relief", "20 Tabs", 12, 42.00, 27.00),
    ("Crocin", "Antipyretic", "15 Tabs", 12, 25.00, 16.00),
    ("Dolo 650", "Antipyretic", "15 Tabs", 12, 32.00, 20.00),
    ("Paracetamol", "Antipyretic", "10 Tabs", 12, 18.00, 10.00),
    ("Omeprazole", "Antacid", "15 Caps", 12, 30.00, 18.00),
    ("Pantoprazole", "Antacid", "10 Tabs", 12, 45.00, 28.00),
    ("Insulin", "Insulin", "1 Vial (10 ml)", 5, 350.00, 260.00),
    ("Cetirizine", "Antiallergic", "10 Tabs", 12, 22.50, 14.00),
    ("Sinarest", "Cold Relief", "10 Tabs", 12, 38.00, 24.00),
    ("Ascoril", "Cough Syrup", "100 ml Bottle", 12, 125.00, 85.00),
    ("Corex Syrup", "Cough Syrup", "100 ml Bottle", 12, 115.00, 78.00),
    ("Benadryl Syrup", "Cough Syrup", "100 ml Bottle", 12, 115.00, 78.00),
    ("Doxycycline", "Antibiotic", "10 Caps", 12, 45.00, 28.00),
    ("Cefixime", "Antibiotic", "10 Tabs", 12, 75.00, 50.00),
]

class Command(BaseCommand):
    help = "Bulk updates medicine metadata including pack sizes, GST, and pricing without duplicate errors"

    def handle(self, *args, **kwargs):
        supplier, _ = Supplier.objects.get_or_create(
            name="Apollo Pharma Distributors",
            defaults={"contact_person": "Supply Desk", "phone": "9988776655", "address": "Hyderabad Central Depot"}
        )

        future_date = datetime.date.today() + datetime.timedelta(days=365)
        updated_meds = 0
        updated_batches = 0

        for name, category, pack_size, gst, mrp, cost in MEDICINE_DATA:
            # Query all matching records to tolerate duplicates safely
            existing_meds = list(Medicine.objects.filter(name__iexact=name))

            if existing_meds:
                for med in existing_meds:
                    med.category = category
                    med.pack_size = pack_size
                    med.gst_percentage = gst
                    med.minimum_stock_level = 15
                    med.save()
                    updated_meds += 1

                batches = Stock.objects.filter(medicine__in=existing_meds)
                if batches.exists():
                    for b in batches:
                        b.mrp = mrp
                        b.purchase_price = cost
                        b.save()
                        updated_batches += 1
                else:
                    Stock.objects.create(
                        medicine=existing_meds[0],
                        supplier=supplier,
                        batch_no=f"BAT-{existing_meds[0].id}01",
                        expiry_date=future_date,
                        quantity=50,
                        purchase_price=cost,
                        mrp=mrp
                    )
                    updated_batches += 1
            else:
                new_med = Medicine.objects.create(
                    name=name,
                    category=category,
                    pack_size=pack_size,
                    gst_percentage=gst,
                    minimum_stock_level=15
                )
                updated_meds += 1

                Stock.objects.create(
                    medicine=new_med,
                    supplier=supplier,
                    batch_no=f"BAT-{new_med.id}01",
                    expiry_date=future_date,
                    quantity=50,
                    purchase_price=cost,
                    mrp=mrp
                )
                updated_batches += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully synchronized {updated_meds} medicines with pack sizes and updated {updated_batches} batches!")
        )