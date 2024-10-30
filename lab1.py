import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://clevershop.mk/product-category/mobilni-laptopi-i-tableti/page/{}"

products_data = []


def get_last_page():
    response = requests.get(base_url.format(1)) 
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        page_numbers = soup.select('.page-numbers')
        last_page = max([int(page.text) for page in page_numbers if page.text.isdigit()])
        return last_page
    else:
        print("Failed to retrieve the first page to determine last page.")
        return 1 

def scrape_page(page_num):
    response = requests.get(base_url.format(page_num))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.select('.product')
        
        for product in products:
            title = product.select_one('.wd-entities-title').text.strip()
            
            price_elements = product.select('.woocommerce-Price-amount')
            regular_price = price_elements[0].text.strip() if price_elements else None
            discount_price = price_elements[1].text.strip() if len(price_elements) > 1 else None
            
            product_url = product.select_one('.wd-entities-title a')['href']
            
            add_to_cart_button = product.select_one('.add_to_cart_button')
            add_to_cart_url = add_to_cart_button['href'] if add_to_cart_button else None
            
            products_data.append({
                'Title': title,
                'Regular Price': regular_price,
                'Discount Price': discount_price,
                'Product URL': product_url,
                'Add to Cart URL': add_to_cart_url
            })
    else:
        print(f"Failed to retrieve page {page_num}, status code: {response.status_code}")


last_page = get_last_page()
print(f"Total pages to scrape: {last_page}")

for page_num in range(1, last_page + 1):
    scrape_page(page_num)
    time.sleep(1) 

df = pd.DataFrame(products_data)
df.to_csv("products.csv", index=False)

print("Scraping completed and data saved to 'products.csv'")
