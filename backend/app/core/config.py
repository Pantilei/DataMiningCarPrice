import os

PROJECT_NAME = "car_prices_analysis"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

API_V1_STR = "/api/v1"
