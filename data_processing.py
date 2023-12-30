import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor
import pickle


datapath = "Data/DataSet.xlsx"
df = pd.read_excel(datapath, sheet_name="FF")

heatmap_col = [
    "LA_N",
    "RA_N",
    "BY_N",
    "FLOOR",
    "BEDROOM",
    "BATHROOM",
    "FACING_N",
    "PRICE_N",
]
df1 = df[heatmap_col]
cormatrix = df[heatmap_col].corr()

plt.figure(figsize=(8, 6))
plt.title("Correlation Heatmap")
sns.heatmap(cormatrix, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 10})


X = df1.drop("PRICE_N", axis=1)
y = df1["PRICE_N"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = GradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

# Predicting on the test set
y_pred = model.predict(X_test)

# Saving the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"R^2 Score: {r2}")

# print(f"Mean Squared Error (MSE): {mse}")
# print(f"Mean Absolute Error (MAE): {mae}")
feature_imp = model.feature_importances_
print(df[heatmap_col].columns)
print(feature_imp)
print(f"GBR R-squared (R2): {r2}")
