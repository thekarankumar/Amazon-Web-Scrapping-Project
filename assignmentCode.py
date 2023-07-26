from bs4 import BeautifulSoup
import requests
import pandas as pd

# Empty data dictionary
data_dictionary = {
    "Product Names": [],
    "Product URLs": [],
    "Product Prices": [],
    "Product Rating": [],
    "No. Of Review": [],
    "Description": [],
    "ASIN": [],
    "Manufacturer": []
}

num_pages = 20  # Set the number of pages to scrape

for i in range(1, num_pages + 1):
    URL = "https://www.amazon.in/s?k=bags&page=" + str(i)
    print(f"Currently scraping page no. {str(i)}")

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    response = requests.get(URL, headers=HEADERS)
    webpage = response.text

    soup = BeautifulSoup(webpage, "lxml")

    try:
        product_names = [name.getText().strip() for name in soup.find_all(name="span", class_="a-size-medium "
                                                                          "a-color-base a-text-normal")]
        for name in product_names:
            data_dictionary["Product Names"].append(name)
    except:
        product_names2 = [name.getText().strip() for name in soup.find_all("span", attrs={"id": "productTitle"})]
        for name2 in product_names2:
            data_dictionary["Product Names"].append(name2)

    product_prices = [price.getText().strip() for price in soup.find_all(name="span", attrs={"class": "a-price-whole"})]
    for price in product_prices:
        data_dictionary["Product Prices"].append(price)

    product_ratings = [rating.getText().strip() for rating in soup.find_all("span", class_="a-icon-alt")]
    for rating in product_ratings:
        data_dictionary["Product Rating"].append(rating)

    num_of_reviews = [review.getText().strip() for review in soup.find_all("span", class_="a-size-base s-underline-text")]
    for review in num_of_reviews:
        data_dictionary["No. Of Review"].append(review)

    for link in soup.find_all(name="a", class_="a-link-normal s-underline-text s-underline-link-text "
                                               "s-link-style a-text-normal"):
        clean_link = link.get("href").strip()
        if clean_link.startswith("https"):
            data_dictionary["Product URLs"].append(clean_link)
        else:
            data_dictionary["Product URLs"].append("https://www.amazon.in" + clean_link)

# Part 2: With the Product URLs received in the above case, hit each URL, and add below items:
# Description
# ASIN
# Manufacturer
for url in data_dictionary["Product URLs"]:
    response2 = requests.get(url, headers=HEADERS)
    webpage2 = response2.content
    soup2 = BeautifulSoup(webpage2, "lxml")

    try:
        asin_data = soup2.select_one('#detailBulletsWrapper_feature_div span:-soup-contains("ASIN") + span').text
        data_dictionary["ASIN"].append(asin_data)
    except:
        data_dictionary["ASIN"].append(None)

    try:
        manu_info = soup2.select_one('#detailBulletsWrapper_feature_div span:-soup-contains("Manufacturer") + span').text
        data_dictionary["Manufacturer"].append(manu_info)
    except:
        data_dictionary["Manufacturer"].append(None)

    try:
        desc = soup2.find("div", attrs={"id": "feature-bullets"})
        clear_desc = desc.get_text().strip()
        data_dictionary["Description"].append(clear_desc)
    except:
        data_dictionary["Description"].append(None)

# Data cleaning and formatting
data_dictionary["Product Prices"] = [float(price.replace(",", "")) for price in data_dictionary["Product Prices"]]
data_dictionary["Product Rating"] = [float(rating.split()[0]) for rating in data_dictionary["Product Rating"]]
data_dictionary["No. Of Review"] = [int(review.replace(",", "")) for review in data_dictionary["No. Of Review"]]

# Check if the lengths of all lists in data_dictionary are equal
list_lengths = [len(data) for data in data_dictionary.values()]
if len(set(list_lengths)) != 1:
    # If the lengths are not equal, find the missing data points and add placeholders
    max_length = max(list_lengths)
    for key, data_list in data_dictionary.items():
        while len(data_list) < max_length:
            data_list.append(None)

# Create a DataFrame from the data_dictionary and save to CSV
abc = pd.DataFrame(data_dictionary)
abc.to_csv("AssignmentDONE.csv", index=False)  # Set index=False to avoid saving the DataFrame index as a separate column