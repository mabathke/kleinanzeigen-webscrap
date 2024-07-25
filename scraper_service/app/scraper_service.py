from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Setzt die Headers der Anfrage (Den User-Agent), damit Ebay-Kleinanzeigen die Anfrage nicht blockt.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}


def get_total_pages(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            pagination = soup.find('div', class_='pagination')
            if pagination:
                pages = pagination.find_all('a')
                total_pages = int(pages[-2].text.strip())  # Get the second to last page number
                return total_pages
        return 1
    except Exception as e:
        print(f'Error in get_total_pages: {e}')
        return 1

def get_listing_details(listing_url):
    try:
        response = requests.get(listing_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            details = {}

            # Extract ID from the URL
            listing_id = listing_url.rstrip('/').split('/')[-1]
            details['ID'] = listing_id

            # Extract details
            details['Title'] = soup.find('h1', id='viewad-title').text.strip() if soup.find('h1', id='viewad-title') else 'N/A'
            details['Price'] = soup.find('h2', id='viewad-price').text.strip() if soup.find('h2', id='viewad-price') else 'N/A'
            details['Location'] = soup.find('span', id='viewad-locality').text.strip() if soup.find('span', id='viewad-locality') else 'N/A'
            details['Date'] = soup.find('div', id='viewad-extra-info').find('span').text.strip() if soup.find('div', id='viewad-extra-info') else 'N/A'
            details['Description'] = soup.find('p', class_='aditem-main--middle--description').text.strip() if soup.find('p', class_='aditem-main--middle--description') else 'N/A'

            # Extract additional features
            feature_list = soup.find_all('li', class_='addetailslist--detail')
            for feature in feature_list:
                key = feature.contents[0].strip()
                value = feature.find('span', class_='addetailslist--detail--value').text.strip()
                details[key] = value

            return details
        return {}
    except Exception as e:
        print(f'Error in get_listing_details: {e}')
        return {}

@app.route('/scrape', methods=['POST'])
def scrape():
    base_url = request.json.get('base_url')
    print(f"Base URL: {base_url}")
    total_pages = get_total_pages(base_url.format(1))
    print(f"Total Pages: {total_pages}")
    data = []

    for page in range(1, total_pages + 1):
        url = base_url.format(page)
        print(f"Scraping URL: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = soup.find_all('article', class_='aditem')
            print(f"Found {len(listings)} listings on page {page}")

            for listing in listings:
                try:
                    listing_url = 'https://www.kleinanzeigen.de' + listing.find('a', class_='ellipsis')['href']
                    detailed_info = get_listing_details(listing_url)
                    data.append(detailed_info)
                    print(f"Scraped listing: {detailed_info}")
                except Exception as e:
                    print(f'Error processing listing: {listing}')
                    print(f'Error message: {e}')
                print(f"Scrapped {listing_url}")
        else:
            print(f'Failed to retrieve page {page}. Status code: {response.status_code}')
    
    # Check if data is empty
    if not data:
        print("No data scraped.")
    else:
        print(f"Scraped data: {data}")

    # Send data to the database service
    try:
        db_response = requests.post('http://db_service:5001/store', json={'data': data})
        print(f"DB Store Response Status Code: {db_response.status_code}")
        print(f"DB Store Response: {db_response.text}")
        return jsonify(db_response.json()), db_response.status_code
    except Exception as e:
        print(f'Error sending data to database service: {e}')
        return jsonify({'error': 'Failed to store data in the database'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
