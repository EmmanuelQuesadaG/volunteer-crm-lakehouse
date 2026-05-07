# ============================================
# VIDA CRM Lakehouse
# Script 01: Synthetic Data Generation
# Author: Emmanuel Quesada Gómez
# ============================================

from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os

fake = Faker('en_US')
random.seed(42)

# ============================================
# dim_volunteer
# ============================================

def generate_volunteers(n=8000):
    volunteers = []
    for i in range(1, n + 1):
        volunteers.append({
            "volunteer_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "gender": random.choice(["Male", "Female", "Non-binary"]),
            "nationality": fake.country() if random.random() > 0.95 else "United States",
            "birth_date": fake.date_of_birth(minimum_age=22, maximum_age=35).strftime("%Y-%m-%d"),
            "start_date": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Completed", "Early Terminated"]),
            "education_level": random.choice(["Bachelor's", "Master's", "PhD"]),
        })
    return pd.DataFrame(volunteers)

# ============================================
# dim_geography
# ============================================

COUNTRIES = [
    ("Costa Rica", "Central America", "San José"),
    ("Guatemala", "Central America", "Guatemala City"),
    ("Honduras", "Central America", "Tegucigalpa"),
    ("Nicaragua", "Central America", "Managua"),
    ("Panama", "Central America", "Panama City"),
    ("Peru", "South America", "Lima"),
    ("Bolivia", "South America", "La Paz"),
    ("Ecuador", "South America", "Quito"),
    ("Paraguay", "South America", "Asunción"),
    ("Senegal", "West Africa", "Dakar"),
    ("Ghana", "West Africa", "Accra"),
    ("Uganda", "East Africa", "Kampala"),
    ("Tanzania", "East Africa", "Dodoma"),
    ("Morocco", "North Africa", "Rabat"),
    ("Nepal", "Asia", "Kathmandu"),
    ("Philippines", "Asia", "Manila"),
    ("Cambodia", "Asia", "Phnom Penh"),
]

def generate_geography(n=250):
    geographies = []
    for i in range(1, n + 1):
        country, region, capital = random.choice(COUNTRIES)
        geographies.append({
            "geography_id": i,
            "country": country,
            "region": region,
            "capital_city": capital,
            "city": fake.city(),
            "rural_urban": random.choice(["Rural", "Urban", "Peri-urban"]),
        })
    return pd.DataFrame(geographies)

# ============================================
# dim_organization
# ============================================

ORG_TYPES = ["NGO", "Government", "Community Group", "School", "Health Center", "Cooperative"]

def generate_organizations(n=800):
    organizations = []
    for i in range(1, n + 1):
        organizations.append({
            "organization_id": i,
            "organization_name": fake.company(),
            "org_type": random.choice(ORG_TYPES),
            "geography_id": random.randint(1, 250),
            "founded_year": random.randint(1980, 2020),
            "active": random.choice([True, True, True, False]),
            "contact_email": fake.email(),
        })
    return pd.DataFrame(organizations)

# ============================================
# dim_project
# ============================================

PROJECT_TYPES = [
    "Education", "Health", "Agriculture",
    "Environment", "Economic Development",
    "Community Development", "Technology"
]

STATUS = ["Active", "Completed", "On Hold", "Cancelled"]

def generate_projects(n=400):
    projects = []
    for i in range(1, n + 1):
        start = fake.date_between(start_date="-10y", end_date="-1y")
        end = start + timedelta(days=random.randint(180, 730))
        projects.append({
            "project_id": i,
            "project_name": f"{random.choice(PROJECT_TYPES)} Initiative {fake.word().capitalize()}",
            "project_type": random.choice(PROJECT_TYPES),
            "geography_id": random.randint(1, 250),
            "organization_id": random.randint(1, 800),
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "budget_usd": round(random.uniform(5000, 500000), 2),
            "status": random.choice(STATUS),
        })
    return pd.DataFrame(projects)

# ============================================
# dim_date
# ============================================

def generate_dates(start="2015-01-01", end="2024-12-31"):
    dates = []
    current = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    i = 1
    while current <= end_date:
        dates.append({
            "date_id": i,
            "full_date": current.strftime("%Y-%m-%d"),
            "year": current.year,
            "quarter": (current.month - 1) // 3 + 1,
            "month": current.month,
            "month_name": current.strftime("%B"),
            "week": current.isocalendar()[1],
            "day_of_week": current.strftime("%A"),
            "is_weekend": current.weekday() >= 5,
        })
        current += timedelta(days=1)
        i += 1
    return pd.DataFrame(dates)

# ============================================
# fact_volunteer_activity
# ============================================

ACTIVITY_TYPES = [
    "Training", "Field Visit", "Community Meeting",
    "Report Submission", "Workshop", "Health Campaign",
    "Agricultural Support", "School Program", "Monitoring"
]

OUTCOMES = ["Successful", "Partially Successful", "Unsuccessful", "Pending"]

def generate_fact_activities(n=800000):
    activities = []
    for i in range(1, n + 1):
        activities.append({
            "activity_id": i,
            "volunteer_id": random.randint(1, 8000),
            "project_id": random.randint(1, 400),
            "organization_id": random.randint(1, 800),
            "geography_id": random.randint(1, 250),
            "date_id": random.randint(1, 3653),
            "activity_type": random.choice(ACTIVITY_TYPES),
            "hours_logged": round(random.uniform(1, 8), 1),
            "beneficiaries_reached": random.randint(0, 500),
            "outcome": random.choice(OUTCOMES),
        })
    return pd.DataFrame(activities)

# ============================================
# Main — Generate and export all tables
# ============================================

if __name__ == "__main__":
    output_path = "data/raw"
    os.makedirs(output_path, exist_ok=True)

    print("Generating dim_volunteer...")
    df_volunteers = generate_volunteers()
    df_volunteers.to_csv(f"{output_path}/dim_volunteer.csv", index=False)
    print(f"dim_volunteer: {len(df_volunteers)} records")

    print("Generating dim_geography...")
    df_geography = generate_geography()
    df_geography.to_csv(f"{output_path}/dim_geography.csv", index=False)
    print(f"dim_geography: {len(df_geography)} records")

    print("Generating dim_organization...")
    df_organizations = generate_organizations()
    df_organizations.to_csv(f"{output_path}/dim_organization.csv", index=False)
    print(f"dim_organization: {len(df_organizations)} records")

    print("Generating dim_project...")
    df_projects = generate_projects()
    df_projects.to_csv(f"{output_path}/dim_project.csv", index=False)
    print(f"dim_project: {len(df_projects)} records")

    print("Generating dim_date...")
    df_dates = generate_dates()
    df_dates.to_csv(f"{output_path}/dim_date.csv", index=False)
    print(f"dim_date: {len(df_dates)} records")

    print("Generating fact_volunteer_activity...")
    df_fact = generate_fact_activities()
    df_fact.to_csv(f"{output_path}/fact_volunteer_activity.csv", index=False)
    print(f"fact_volunteer_activity: {len(df_fact)} records")

    print("\nAll tables generated successfully")