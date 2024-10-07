import pandas as pd
df = pd.read_csv("car.csv")
unique_values = df["Make"].unique()
print(unique_values)


# ['Ford' 'Mercury' 'Hyundai' 'Lexus' 'Mercedes-Benz' 'Toyota' 'Volkswagen'
#  'Honda' 'Dodge' 'Chevrolet' 'MINI' 'Nissan' 'Ram' 'Jeep' 'Isuzu' 'Kia'
#  'GMC' 'Audi' 'Geo' 'Acura' 'Porsche' 'Lincoln' 'INFINITI' 'Pontiac'
#  'Suzuki' 'Land Rover' 'Plymouth' 'Chrysler' 'Mitsubishi' 'MAZDA' 'BMW'
#  'Scion' 'Bentley' 'Subaru' 'Saab' 'Maserati' 'Cadillac' 'Ferrari'
#  'HUMMER' 'smart' 'Oldsmobile' 'Alfa Romeo' 'Lamborghini' 'Buick' 'Jaguar'
#  'Freightliner' 'Volvo' 'Aston Martin' 'Daewoo' 'FIAT' 'Maybach' 'Saturn'
#  'Eagle' 'Lotus' 'Polestar' 'Genesis' 'Rolls-Royce' 'McLaren' 'Tesla'
#  'Rivian' 'Daihatsu' 'Panoz' 'Fisker' 'SRT']