import pandas as pd

# Load the CSV data
df = pd.read_csv("car.csv")

# Keep only relevant columns and explode models
df = df.drop(columns=["Year", "Category"]).explode("Model")

# Group by Make and get unique models as lists
grouped_models = df.groupby("Make")["Model"].unique().to_dict()

# Create a DataFrame from the grouped models
df_unique_models = pd.DataFrame(grouped_models.items(), columns=["Make", "Models"])

# Save the DataFrame as a CSV
df_unique_models.to_csv("unique_models.csv", index=False)
    # ['Ford' 'Mercury' 'Hyundai' 'Lexus' 'Mercedes-Benz' 'Toyota' 'Volkswagen'
    #  'Honda' 'Dodge' 'Chevrolet' 'MINI' 'Nissan' 'Ram' 'Jeep' 'Isuzu' 'Kia'
    #  'GMC' 'Audi' 'Geo' 'Acura' 'Porsche' 'Lincoln' 'INFINITI' 'Pontiac'
    #  'Suzuki' 'Land Rover' 'Plymouth' 'Chrysler' 'Mitsubishi' 'MAZDA' 'BMW'
    #  'Scion' 'Bentley' 'Subaru' 'Saab' 'Maserati' 'Cadillac' 'Ferrari'
    #  'HUMMER' 'smart' 'Oldsmobile' 'Alfa Romeo' 'Lamborghini' 'Buick' 'Jaguar'
    #  'Freightliner' 'Volvo' 'Aston Martin' 'Daewoo' 'FIAT' 'Maybach' 'Saturn'
    #  'Eagle' 'Lotus' 'Polestar' 'Genesis' 'Rolls-Royce' 'McLaren' 'Tesla'
    #  'Rivian' 'Daihatsu' 'Panoz' 'Fisker' 'SRT']