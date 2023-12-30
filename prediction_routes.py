from flask import Blueprint, request, jsonify
import pandas as pd
from RandomForestModel import RandomForestModel
import pickle

prediction_routes = Blueprint("prediction_routes", __name__)

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)


@prediction_routes.route("/api/predict", methods=["POST"])
def predict_price():
    try:
        # Your payload data
        payload = request.get_json()

        # Convert the payload to a DataFrame
        data = pd.DataFrame([payload])

        # Define a mapping from payload columns to dataset columns
        column_mapping = {
            # "location": "CITY",
            "land_area": "LA_N",
            "road_access": "RA_N",
            "built_year": "BY_N",
            "floor": "FLOOR",
            "bedroom": "BEDROOM",
            "bathroom": "BATHROOM",
            "facing": "FACING_N",
        }

        # Rename the columns in the data DataFrame
        data.rename(columns=column_mapping, inplace=True)

        # Define a mapping from facing directions to numbers
        facing_mapping = {
            "East": 1,
            "North": 1.1,
            "NorthEast": 1.1,
            "SouthEast": 2,
            "NorthWest": 2,
            "West": 2.1,
            "SouthWest": 3,
            "South": 3,
        }

        # Convert facing directions to numbers
        data["FACING_N"] = data["FACING_N"].map(facing_mapping)

        # Convert columns to numeric where appropriate
        numeric_cols = [
            "LA_N",
            "RA_N",
            "BY_N",
            "FLOOR",
            "BEDROOM",
            "BATHROOM",
            "FACING_N",
        ]
        data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric)
        prediction = model.predict(data)
        prediction_list = [float(val) for val in prediction]
        return jsonify({"prediction": prediction_list})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Error occured during prediction"})
