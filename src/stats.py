import pandas as pd
import matplotlib.pyplot as plt

def generate_management_statistics(patients):
    print("\nGenerating key statistics reports...\n")

    # Collect all visit data in a list of dictionaries
    visit_data = []

    for patient in patients.values():
        for visit in patient.records:
            visit_data.append({
                "visit_time": visit.visit_time,
                "insurance": visit.insurance,
                "age": visit.age,
                "race": visit.race,
                "gender": visit.gender,
                "ethnicity": visit.ethnicity
            })

    # Convert list to pandas DataFrame
    df = pd.DataFrame(visit_data)

    # Make sure visit_date is in datetime format
    # https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
    df['visit_time'] = pd.to_datetime(df['visit_time'], errors='coerce')

    # Remove any rows with bad/missing dates
    df = df.dropna(subset=['visit_time'])

    # Extract Year and Month
    df['year'] = df['visit_time'].dt.year
    df['month'] = df['visit_time'].dt.month

    # Total visits per Year
    yearly_visits = df.groupby('year').size().sort_index()
    yearly_visits.plot(kind='bar', title="Total Visits per Year", figsize=(15, 5))
    plt.xlabel("Year")
    plt.ylabel("Number of Visits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("total_visits_per_year.png")  # Save the plot
    plt.show()

    # Visits by insurance type
    insurance_trend = df.groupby(['year', 'insurance']).size().unstack()
    insurance_trend.plot(kind='line', stacked=True, title="Visits by Insurance Over Time (Yearly)", figsize=(12, 5))
    plt.xlabel("Year")
    plt.ylabel("Number of Visits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("visits_by_insurance_yearly.png")  # Save the plot
    plt.show()

    # Demographics (race, gender, ethnicity)
    for category in ['race', 'gender', 'ethnicity']:
        demo_trend = df.groupby(['year', category]).size().unstack().fillna(0)
        demo_trend.plot(title="Visits by "+ category.capitalize()+" Over Time (Yearly)", figsize=(15, 5))
        plt.xlabel("Year")
        plt.ylabel("Number of Visits")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("visits_by_"+ category +"_yearly.png")  # Save the plot
        plt.show()

    print("\nManagement statistics generated and saved as figures.\n")
