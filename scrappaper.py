import csv
import requests
from bs4 import BeautifulSoup
import re
import sys

def get_full_text(pubmed_id):
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    url = base_url + str(pubmed_id)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        abstract = soup.find("div", class_="abstract-content")
        if abstract:
            return abstract.get_text(strip=True)
    return None

def identify_primers(text):
    # Regular expression to match DNA sequences
    pattern = re.compile(r'[ACGTacgt]{18,30}')

    matches = pattern.findall(text)
    return matches

def identify_orientation(primer_text):
    # Assuming Fw, FW, or forward in the primer indicates a forward primer, and similar for reverse
    if 'Fw' in primer_text or 'FW' in primer_text or 'forward' in primer_text:
        return 'Forward'
    elif 'Rev' in primer_text or 'Rv' in primer_text or 'reverse' in primer_text:
        return 'Reverse'
    else:
        return 'Unknown'

def write_to_tsv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerow(['PubMedID', 'PrimerSequence', 'Orientation'])
        writer.writerows(data)

def process_csv(input_file, output_file):
    data = []

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pubmed_id = row['PubMedID']
            full_text = get_full_text(pubmed_id)
            if full_text:
                primers = identify_primers(full_text)
                for primer in primers:
                    orientation = identify_orientation(full_text)
                    data.append([pubmed_id, primer, orientation])

    write_to_tsv(data, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_csv(input_file, output_file)
