from flask import Flask
from flask_cors import CORS
from prediction_routes import prediction_routes

# Initializing flask app
app = Flask(__name__)
CORS(app)


# Registering routes
app.register_blueprint(prediction_routes)

# Running app
if __name__ == "__main__":
    try:
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"Error occured: {str(e)}")
