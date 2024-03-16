import os
import json
import re
import requests
from bs4 import BeautifulSoup

def scrape_and_save(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles_list = []

        # Find all parent tags
        parent_tags = soup.find_all(class_="uwU81")

        # Iterate through parent tags
        for parent_tag in parent_tags:
            # Check if the parent tag has a child with class "fHv_i"
            article = parent_tag.find(class_="fHv_i")
            if article:
                title = article.text
                paragraph_elem = parent_tag.find(class_="oxXSK")
                paragraph = paragraph_elem.text if paragraph_elem else "No description available"

                # Check if the title contains specific words
                keywords = ["earthquake", "forest fire", "tsunami", "cyclone", "pandemic", "epidemic", "drought", "flood"]
                for keyword in keywords:
                    if keyword.lower() in title.lower():
                        articles_list.append({"title": title, "paragraph": paragraph})
                        break

        # Create JSON structure
        data = {"articles": articles_list}

        # Write data to JSON file
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)

        print("Scraping completed and data saved to", output_file)
    else:
        print("Failed to fetch data from the webpage")

# Example usage
current_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(current_dir, "sample.json")
scrape_and_save("https://timesofindia.indiatimes.com/topic/disaster-alert", output_file)
