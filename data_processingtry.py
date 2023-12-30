import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from scipy import stats
from converters import (
    convert_price,
    convert_area,
    convert_road_access,
    convert_built_year,
)
from RandomForestModel import RandomForestModel
import pickle


# Loading data
datapath = "Data/Dataset.xlsx"
df = pd.read_excel(datapath)

# Droping null values and title column
df = df.drop("TITLE", axis=1)
df = df.drop("BUILDUP AREA", axis=1)

# Spliting location column
df["LOCATION"] = df["LOCATION"].str.split(",").str[1].str.strip()

le = LabelEncoder()

# Converting location to numerical
df["LOCATION"] = le.fit_transform(df["LOCATION"])

# Converting facing to numerical
df["FACING"] = le.fit_transform(df["FACING"])

# Converting price and area to numerical
df["LAND AREA"] = df["LAND AREA"].apply(convert_area)
df["PRICE"] = df.apply(
    lambda row: convert_price(row["PRICE"], row["LAND AREA"]), axis=1
)

# Counting and printing the number of rows to be dropped
num_dropped_rows = df["LAND AREA"].isnull().sum() + df["PRICE"].isnull().sum()
print(f"Null Land Area or Price: {num_dropped_rows}")

# Removing rows with null values in LAND AREA and PRICE column
df = df.dropna(subset=["LAND AREA", "PRICE"])

# Converting road access to numerical
df["ROAD ACCESS"] = df["ROAD ACCESS"].apply(convert_road_access)

# Converting built year to numerical
df["BUILT YEAR"] = df["BUILT YEAR"].apply(convert_built_year)

# Dropping PARKING column
df = df.drop("PARKING", axis=1)

# Dropping AMENITIES column
df = df.drop("AMENITIES", axis=1)

# Calculating Z-scores for numerical columns
numerical_cols = [
    "LAND AREA",
    "PRICE",
    "ROAD ACCESS",
    "BUILT YEAR",
]
z_scores = df[numerical_cols].apply(stats.zscore)

# Define a threshold to identify an outlier
threshold = 3

# Get boolean mask where values are out of threshold
outliers = np.abs(z_scores) > threshold

# Count and print number of outliers
num_outliers = outliers.sum().sum()
print(f"Number of outliers: {num_outliers}")

# Removing outliers
df = df[~outliers.any(axis=1)]

df.columns = df.columns.str.lower().str.replace(" ", "_")

# Splitting data into features and target
X = df.drop("price", axis=1)
y = df["price"]

X = X.fillna(0)

# Splitting data into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Initializing model
model = RandomForestModel()

# Training model
model.train(X_train, y_train)

# Predicting price
y_pred = model.predict(X_test)

# Calculate the accuracy
r2 = r2_score(y_test, y_pred)

# Print the accuracy
print(f"R^2 Score: {r2}")

# Save the trained model as a pickle file
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with pd.ExcelWriter(
    datapath, engine="openpyxl", mode="a", if_sheet_exists="replace"
) as writer:
    df.to_excel(writer, sheet_name="Cleaned Data")
