import pandas as pd
import re


# Function to convert price to numerical value
def convert_price(price, area):
    if not isinstance(price, str):
        return price
    try:
        price = price.replace("Rs. ", "")
        per_unit_area = False
        if "/dhur" in price:
            price = price.replace("/dhur", "")
            per_unit = 182.25  # 1 dhur = 182.25 sqft
            per_unit_area = True
        elif "/kattha" in price:
            price = price.replace("/kattha", "")
            per_unit = 3645  # 1 kattha = 3645 sqft
            per_unit_area = True
        elif "/bigha" in price:
            price = price.replace("/bigha", "")
            per_unit = 72900  # 1 bigha = 72900 sqft
            per_unit_area = True
        elif "/dam" in price:
            price = price.replace("/dam", "")
            per_unit = 21.39  # 1 dam = 21.39 sqft
            per_unit_area = True
        elif "/paisa" in price:
            price = price.replace("/paisa", "")
            per_unit = 85.56  # 1 paisa = 85.56 sqft
            per_unit_area = True
        elif "/aana" in price:
            price = price.replace("/aana", "")
            per_unit = 342.25  # 1 aana = 342.25 sqft
            per_unit_area = True
        elif "/ropani" in price:
            price = price.replace("/ropani", "")
            per_unit = 5476  # 1 ropani = 5476 sqft
            per_unit_area = True
        elif "/sq. ft" in price:
            price = price.replace("/sqft", "")
            per_unit = 1
            per_unit_area = True
        elif "/sq. m" in price:
            price = price.replace("/sq. m", "")
            per_unit = 10.764  # 1 meter = 10.764 sq ft
            per_unit_area = True
        elif "/m" in price:
            price = price.replace("/m", "")
            per_unit = 10.764  # 1 meter = 10.764 sq ft
            per_unit_area = True
        if "Cr" in price:
            price = float(price.replace("Cr", "").replace(",", "")) * 10000000
        elif "Lac" in price:
            price = float(price.replace("Lac", "").replace(",", "")) * 100000
        else:
            price = float(price.replace(",", ""))
        if per_unit_area:
            price = price * per_unit * area
        return price
    except ValueError:
        return None


# Function to convert area to numerical value
def convert_area(area):
    try:
        if isinstance(area, str):
            if "aana" in area:
                area = (
                    float(area.lower().replace(" aana", "").strip()) * 342.25
                )  # 1 aana = 342.25 sq ft
            elif "kattha" in area:
                area = (
                    float(area.lower().replace(" kattha", "").strip()) * 3645
                )  # 1 kathha = 3645 sq ft
            elif "sq. mtr" in area:
                area = (
                    float(area.lower().replace(" sq. mtr", "").strip()) * 10.764
                )  # 1 meter = 10.764 sq ft
            elif "sq. m" in area:
                area = (
                    float(area.lower().replace(" sq. m", "").strip()) * 10.764
                )  # 1 meter = 10.764 sq ft
            elif "sq. ft" in area:
                area = float(area.lower().replace(" sq. ft", "").strip())
            else:
                area = float(area.lower().strip())
        return area
    except ValueError:
        return None


# Function to convert road access to numerical value
def convert_road_access(value):
    # Check if the value is not null
    if pd.isna(value):
        return value
    # Extract number from string
    try:
        numbers = re.findall(r"\d+", value)
        numbers = [float(num) for num in numbers]
    except:
        return None
    # Check if the value is in meter
    if "Meter" in value:
        numbers = [num * 3.28084 for num in numbers]  # 1 meter = 3.28084 feet
    # Return the average of all the numbers
    return sum(numbers) / len(numbers)


# Function to convert built year to numerical value
def convert_built_year(value):
    # Check if the value is not null
    if pd.isna(value):
        return value
    # Extract year from string
    try:
        year = re.findall(r"\d+", value)[0]
        return int(year)
    except:
        return None
