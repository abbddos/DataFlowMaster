import requests
import json
import random
import time
from datetime import datetime, timedelta
import sys

API_URL = "http://localhost:5000/api/v1/RefugeeRegistrations"

camps = ["Camp Alpha", "Camp Beta", "Camp Gamma", "Camp Delta"]
first_names_male = ["Omar", "Ahmed", "Mohammed", "Khalid", "Youssef"]
first_names_female = ["Amina", "Fatima", "Leyla", "Zainab", "Nour"] 
last_names = ["Al-Masri", "Hassan", "Ibrahim", "Abdullah", "Khalil"]
ethnicities = ['Arab', 'Armenian', 'Caucase', 'Kurd', 'Turkmen', 'Other']
religions = ['Sumni', 'Shiaa', 'Christian', 'Jewish', 'Yazidi', 'Druz', 'Ismaili', 'Alawite', 'Murshidi', 'Other']
places = ['Damascus', 'Rural Damascus', 'Qunaitara', 'Daraa', 'Sweidaa', 'Homs', 'Tartous', 'Hama', 'Lattakia', 'Idlib', 'Aleppo', 'Raqqa', 'Deir Ezzor', 'Hasakeh']

def generate_refugee():
    is_male = random.choice([True, False])
    first_name = random.choice(first_names_male) if is_male else random.choice(first_names_female)
    
    return {
        "camp": random.choice(camps),
        "firstName": first_name,
        "middleName": random.choice([None, "Ali", "Khalid", "Mohammed"]),
        "lastName": random.choice(last_names),
        "sex": "Male" if is_male else "Female",
        "dateOfBirth": (datetime.now() - timedelta(days=random.randint(18*365, 70*365))).strftime("%Y-%m-%d"),
        "placeOfBirth": random.choice(places),
        "nationality": "Syrian",
        "ethnicity": random.choice(ethnicities),
        "religion": random.choice(religions),
        "householdSize": random.randint(1, 8),
        "householdHasDisability": random.random() < 0.1,  # 10% chance
        "disabilityType": random.choice([None, "Mobility impairment", "Visual impairment"]),
        "householdHasInfants": random.random() < 0.25,  # 25% chance
        "numOfInfants": random.randint(1, 3) if random.random() < 0.25 else 0,
        "householdHasElderly": random.random() < 0.2,  # 20% chance
        "numOfElderly": random.randint(1, 2) if random.random() < 0.2 else 0,
        "hasDocumentation": random.random() < 0.33,  # 33% chance
        "documentationType": random.choice([None, "Passport", "ID", "Family Booklet"]),
        "documentationNumber": f"DOC{random.randint(1000, 9999)}" if random.random() < 0.33 else None
    }

def main():
    print("Starting refugee data generator...")
    
    while True:
        try:
            refugee = generate_refugee()
            response = requests.post(API_URL, json=refugee)
            
            if response.status_code == 201:
                print(f"✅ Created: {refugee['firstName']} {refugee['lastName']} - {refugee['placeOfBirth']} - {refugee['ethnicity']} {refugee['religion']}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                
            time.sleep(0.5)  # Send every 5 seconds
            
        except KeyboardInterrupt:
            print("\n🛑 Generator stopped by user")
            sys.exit(0)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)
            
        
            

if __name__ == "__main__":
    main()