import csv
import random
from datetime import datetime, timedelta


def generate_ev_dataset(num_rows=10000, output_filename='ev_extended_18col_dataset.csv'):
    print(f"Starting generation of {num_rows} rows...")

    manufacturers_pool = {
        'Tesla': [('Model 3', 60), ('Model Y', 75)],
        'BYD': [('Atto 3', 50), ('Seal', 82)],
        'Hyundai': [('Ioniq 5', 77), ('Kona EV', 48)],
        'Kia': [('EV6', 77), ('EV9', 100)],
        'Tata': [('Nexon EV', 40), ('Punch EV', 25)]
    }

    entities = []
    for i in range(1, 51):
        brand = random.choice(list(manufacturers_pool.keys()))
        model_info = random.choice(manufacturers_pool[brand])
        model_name = model_info[0]
        battery_capacity = model_info[1]

        entities.append({
            'Vehicle_ID': f'EV-{1000 + i}',
            'Driver_ID': f'DRV-{5000 + i}',
            'Manufacturer': brand,
            'Model': model_name,
            'Battery_Capacity_kWh': battery_capacity,
            'Registration_No': f'REG-{random.randint(10,99)}{chr(random.randint(65,90))}{chr(random.randint(65,90))}-{random.randint(1000,9999)}'
        })

    data = []
    for i in range(1, num_rows + 1):
        entity = random.choice(entities)
        status = random.choice(['Running', 'Charging', 'Garage'])
        start_time = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
        date_time = (datetime(2026, 1, 1) + timedelta(
            days=random.randint(0, 364),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )).strftime('%Y-%m-%d %H:%M:%S')

        if status == 'Running':
            battery = random.randint(15, 98)
            avg_speed = round(random.uniform(30.0, 75.0), 1)
            distance = round(random.uniform(10.0, 180.0), 2)
            revenue = round(distance * random.uniform(1.2, 2.5), 2)
            elec_cost = 0.0
            maint_cost = round(random.choices([0.0, random.uniform(10.0, 45.0)], weights=[85, 15])[0], 2)
            overspeed = random.choices([0, 1, 2, 3], weights=[80, 12, 6, 2])[0]
        elif status == 'Charging':
            battery = random.randint(5, 80)
            avg_speed = 0.0
            distance = 0.0
            revenue = 0.0
            elec_cost = round(random.uniform(8.0, 35.0), 2)
            maint_cost = 0.0
            overspeed = 0
        else:
            battery = random.randint(10, 100)
            avg_speed = 0.0
            distance = 0.0
            revenue = 0.0
            elec_cost = 0.0
            maint_cost = round(random.choices([0.0, random.uniform(80.0, 250.0)], weights=[95, 5])[0], 2)
            overspeed = 0

        expected_range = int(battery * random.uniform(3.2, 4.4))

        data.append({
            'Trip_ID': f'TRIP-{100000 + i}',
            'Vehicle_ID': entity['Vehicle_ID'],
            'Driver_ID': entity['Driver_ID'],
            'Manufacturer': entity['Manufacturer'],
            'Model': entity['Model'],
            'Registration_No': entity['Registration_No'],
            'Battery_Capacity_kWh': entity['Battery_Capacity_kWh'],
            'Current_Battery_%': battery,
            'Battery_Remaining_%': battery,
            'Expected_Range_km': expected_range,
            'Status': status,
            'Date_Time': date_time,
            'Start_Time': start_time,
            'Distance_km': distance,
            'Avg_Speed_kmph': avg_speed,
            'Revenue': revenue,
            'Electricity_Cost': elec_cost,
            'Maintenance_Cost': maint_cost,
            'Overspeed_Count': overspeed
        })

    fieldnames = [
        'Trip_ID', 'Vehicle_ID', 'Driver_ID', 'Manufacturer', 'Model', 'Registration_No',
        'Battery_Capacity_kWh', 'Current_Battery_%', 'Battery_Remaining_%', 'Expected_Range_km',
        'Status', 'Date_Time', 'Start_Time', 'Distance_km', 'Avg_Speed_kmph', 'Revenue',
        'Electricity_Cost', 'Maintenance_Cost', 'Overspeed_Count'
    ]

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Success! Saved updated dataset to file: '{output_filename}'")
    except PermissionError:
        alternative_name = f"ev_dataset_{datetime.now().strftime('%H%M%S')}.csv"
        print(f"\n⚠️ WARNING: '{output_filename}' is currently open in Excel or another app!")
        print(f"Saving to an alternative file instead: '{alternative_name}'")
        with open(alternative_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print("Success!")


if __name__ == '__main__':
    generate_ev_dataset()
