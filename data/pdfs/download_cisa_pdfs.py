#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time

def download_cisa_pdfs(max_pdfs=20):
    base_url = "https://www.cisa.gov"
    url = "https://www.cisa.gov/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find advisory links
    advisory_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/news-events/cybersecurity-advisories/' in href and href not in advisory_links:
            advisory_links.append(urljoin(base_url, href))
    
    print(f"Found {len(advisory_links)} advisory pages")
    
    pdf_count = 0
    for advisory_url in advisory_links[:max_pdfs * 2]:  # Check more pages than needed
        if pdf_count >= max_pdfs:
            break
            
        try:
            print(f"Checking: {advisory_url}")
            page_response = requests.get(advisory_url, headers=headers)
            page_soup = BeautifulSoup(page_response.content, 'html.parser')
            
            # Look for PDF links
            for link in page_soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.pdf'):
                    pdf_url = urljoin(base_url, href)
                    filename = os.path.basename(urlparse(pdf_url).path)
                    
                    if not filename.endswith('.pdf'):
                        filename += '.pdf'
                    
                    filepath = os.path.join(os.getcwd(), filename)
                    
                    if not os.path.exists(filepath):
                        print(f"Downloading: {filename}")
                        pdf_response = requests.get(pdf_url, headers=headers)
                        with open(filepath, 'wb') as f:
                            f.write(pdf_response.content)
                        pdf_count += 1
                        time.sleep(1)  # Be respectful
                        
                        if pdf_count >= max_pdfs:
                            break
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error processing {advisory_url}: {e}")
            continue
    
    print(f"Downloaded {pdf_count} PDFs")

if __name__ == "__main__":
    download_cisa_pdfs(20)
