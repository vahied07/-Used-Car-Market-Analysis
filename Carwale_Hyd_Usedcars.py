import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.maximize_window()


base_url = "https://www.carwale.com/used/hyderabad/page{}/"


all_cars = []


def scroll_page():
    ini_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Increased wait time
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == ini_height:
            break
        ini_height = new_height

# ✅ Function to extract data from each page
def extract_data():
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")


    cars = [car.text.strip() for car in soup.find_all('div', class_="o-bS o-co o-cC o-c6 o-C o-kY ctofvW")]
    all_cars.extend(cars)

# ✅ Loop through first 5 pages
for page in range(1, 4):  # Adjust as needed
    url = base_url.format(page)
    print(f"🔄 Scraping: {url}")
    browser.get(url)
    time.sleep(10)

    scroll_page()
    extract_data()


browser.quit()


print(len(all_cars))



# ✅ Lists to store cleaned extracted data
car_names = []
brands = []
model_names = []
model_years = []
km_driven = []
fuel_types = []
transmissions = []
locations = []
prices = []
emis = []

# ✅ Data Cleaning & Extraction
for car in all_cars:
    car = car.replace("\xa0\xa0|\xa0\xa0", "|").strip()


    name_match = re.match(r"^(.*?)(?=\d{1,3},\d{3} km)", car)
    car_name = name_match.group(1).strip() if name_match else "N/A"


    brand = car_name.split()[1] if len(car_name.split()) > 1 else "N/A"


    model_name = car_name.replace(brand, "").strip() if brand != "N/A" else "N/A"


    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", car)
    model_year = year_match.group(1) if year_match else "N/A"


    km_match = re.search(r"(\d{1,3},\d{3} km)", car)
    km_value = km_match.group(1) if km_match else "N/A"


    fuel_match = re.search(r"(Petrol|Diesel|CNG|Electric|Hybrid)", car)
    fuel_type = fuel_match.group(1) if fuel_match else "N/A"


    transmission = "Automatic" if re.search(r"\b(AMT|CVT|AT|DCT|DSG)\b", car_name, re.IGNORECASE) else "Manual"


    location_match = re.search(r"(?:Petrol|Diesel|CNG|Electric|Hybrid)\s*\|\s*(.*?)(?=Rs\.|$)", car)
    location = location_match.group(1).strip() if location_match else "N/A"


    price_match = re.search(r"(Rs\.\s?[\d.,]+ [A-Za-z]+)", car)
    price = price_match.group(1).replace("EMI", "").strip() if price_match else "N/A"


    emi_match = re.search(r"EMI at Rs\.?\s*([\d.,]+)", car)
    emi = f"Rs. {emi_match.group(1)}" if emi_match else "N/A"

    # ✅ Store Data
    car_names.append(car_name)
    brands.append(brand)
    model_names.append(model_name)
    model_years.append(model_year)
    km_driven.append(km_value)
    fuel_types.append(fuel_type)
    transmissions.append(transmission)
    locations.append(location)
    prices.append(price)
    emis.append(emi)


df = pd.DataFrame({
    "Car Name": car_names,
    "Brand": brands,
    "Model Name": model_names,
    "Model Year": model_years,
    "KM Driven": km_driven,
    "Fuel Type": fuel_types,
    "Transmission": transmissions,
    "Location": locations,
    "Price": prices,
    "EMI": emis
})

# ✅ Save to CSV
df.to_csv(r"C:\Users\jagad\OneDrive\Documents\cleaned_car_data_finall.csv", index=False)

# ✅ Print First 5 Rows
#print(df.head())