"""
Dollar exchange
"""
import os
import requests
import argparse
from bs4 import BeautifulSoup

def scrap_web_page(url:str) -> str:
    """Scrapes the web page and returns the content as a string."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to retrieve the web page. Status code: {response.status_code}")
    
    
def get_dollar_exchange_rate(content: str) -> list:
    """Extracts the dollar exchange rate from the web page content."""
    soup = BeautifulSoup(content, 'html.parser')
    main_table = soup.find('table', id='dllsTable')
    price_list = []
    if main_table:
        rows = main_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 4:
                sell_price = cols[3].text.strip()
                buy_price = cols[2].text.strip()
                bank_name = cols[1].text.strip()
                print(bank_name)
            if len(cols) == 5:
                sell_price = cols[3].text.strip()
                buy_price = cols[4].text.strip()
                bank_name = cols[2].text.strip()
                print(bank_name)
            price_list.append((bank_name, sell_price, buy_price))
    else:
        print("Error: Could not find the main table with id 'dllsTable'.")
    return price_list

def main(args):
    """Main function to scrape the web page and save the content to a file."""
    url = args.url
    output_file = args.output_file
    try:
        content = scrap_web_page(url)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content successfully saved to {output_file}")
        price_list = get_dollar_exchange_rate(content)
        print(price_list)
        for bank_name, sell_price, buy_price in price_list:
            print(f"Bank: {bank_name}, Sell Price: {sell_price}, Buy Price: {buy_price}")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape a web page and save its content to a file.")
    parser.add_argument("url", type=str, help="URL of the web page to scrape.")
    parser.add_argument("output_file", type=str, help="Path to the output file where the content will be saved.")
    args = parser.parse_args()
    main(args)