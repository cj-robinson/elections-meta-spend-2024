import requests
import csv
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

# Configuration
base_url = 'https://ad-archive.nexxxt.cloud/adsbypage/{}?offset={}'
limit = 100  # Number of ads per request (keep this for pagination)
output_directory = 'ad_data_plus_body_110324'

# List of page IDs with their names as comments
page_ids = [
    # Metric media outlets
    '107188720968827',  # Peach Tree Times
    '101380274600494',  # Old North News
    '103902317946785',  # The Sconi
    '103936177693945',  # Grand Canyon Times
    '110199357322201',  # Central Bucks Today
    '110870006973319',  # Great Lakes Wire
    '102937951392349',  # Altoona Times
    '118375432886638',  # Durham Reporter
    '103220924789843',  # Silver State Times
    '115829333162253',  # Tuscon Standard
    '102066598144632',  # Southeast South Dakota News
    '105928717748894',  # Centennial State News
    '104944811154618',  # Empire State Today
    '107420874140846',  # Houston Republic
    '104334391239228',  # Old Dominion News
    '104205461233963',  # Maryland State Wire
    '108367200712125',  # Ft Worth Times
    '102661127957543',  # San Antonio Standard
    '102317521440744',  # Madison Reporter
    '101826427907463',  # PHX Reporter
    '110991080301105',  # North Charlotte News

    # Courier newsroom
    '106487520883333',  # Cardinal & Pine
    '102540204580217',  # UpNorthNews
    '110746996993983',  # The Gander Newsroom
    '1509209726034350',  # Iowa Starting Line
    '114971076538782',  # The Keystone
    '344690446467832',   # The Copper Courier
    '113595901816074', # The Nevadan
    '126485960550562', # Granite Post

    # Star Spangled Media
    '271334569394073', # The Morning Mirror

    # Star News
    "295961613606996", # Olean Star

    # American Independent
    "101364989314326", # Penn Ind
    "105070129182164", # Wisconsin Ind
    "253770764485550", # Montanta Ind
    "343992762133104", # Nebraska
    "129615950227850" #Michigan
]

def get_ads_by_page_id(page_id: str, offset: int = 0) -> Optional[List[Dict[Any, Any]]]:
    """
    Get ads for a specific page ID with proper pagination handling.
    """
    url = base_url.format(page_id, offset)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        if not isinstance(data, list):
            print(f"Unexpected response format for page ID '{page_id}' at offset {offset}")
            return None
            
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ads for page ID '{page_id}' at offset {offset}: {str(e)}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON for page ID '{page_id}' at offset {offset}: {str(e)}")
        return None
    
def write_to_csv(ads: List[Dict], page_id: str):
    """
    Write ads to a CSV file with page ID and timestamp in filename.
    Splits spend and impressions into low and high bounds.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_directory}/page_{page_id}_{timestamp}.csv'
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id', '_last_updated', 'ad_creation_time',
            'ad_creative_bodies',
            'ad_delivery_start_time', 'ad_delivery_end_time', 'page_name',
            'publisher_platforms', 'bylines', 'currency', 'delivery_by_region',
            'demographic_distribution', 'estimated_audience_size', 
            'low_spend', 'high_spend', 
            'low_impressions', 'high_impressions', 
            'page_id'
        ])

        for ad in ads:
            # Extract spend bounds
            spend_bounds = ad.get('spend', {})
            low_spend = get_field(spend_bounds, 'lower_bound')
            high_spend = get_field(spend_bounds, 'upper_bound')

            # Extract impressions bounds
            impressions_bounds = ad.get('impressions', {})
            low_impressions = get_field(impressions_bounds, 'lower_bound')
            high_impressions = get_field(impressions_bounds, 'upper_bound')

            writer.writerow([
                get_field(ad, '_id'),
                get_field(ad, '_last_updated'),
                get_field(ad, 'ad_creation_time'),
                ";".join(ad.get('ad_creative_bodies', [])),
                get_field(ad, 'ad_delivery_start_time'),
                get_field(ad, 'ad_delivery_stop_time'),
                get_field(ad, 'page_name'),
                ";".join(ad.get('publisher_platforms', [])),
                get_field(ad, 'bylines'),
                get_field(ad, 'currency'),
                get_field(ad, 'delivery_by_region'),
                get_field(ad, 'demographic_distribution'),
                get_field(ad, 'estimated_audience_size'),
                low_spend,
                high_spend,
                low_impressions,
                high_impressions,
                page_id
            ])
    
    print(f"Written {len(ads)} records to {filename}")

def get_field(ad: Dict, field_name: str) -> str:
    """
    Helper function to safely get field values.
    Handles nested dictionaries and returns an empty string if not found.
    """
    return str(ad.get(field_name, "") if not isinstance(ad, dict) else ad.get(field_name, ""))

def fetch_ads_for_page(page_id: str) -> List[Dict]:
    """
    Fetch all available ads for a single page ID.
    """
    all_ads = []
    current_offset = 0
    
    print(f"\nFetching ads for page ID: '{page_id}'")
    
    while True:
        print(f"Fetching records {current_offset + 1}-{current_offset + limit}")
        
        ads = get_ads_by_page_id(page_id, current_offset)
        
        if ads is None or len(ads) == 0:
            print(f"No more ads available for page ID '{page_id}' after {len(all_ads)} records")
            break
            
        all_ads.extend(ads)
        
        if len(ads) < limit:
            print(f"Reached end of available ads for page ID '{page_id}' at {len(all_ads)} records")
            break
        
        current_offset += limit
    
    return all_ads

def main():
    print(f"Starting ad fetch for {len(page_ids)} page IDs")
    print("Will fetch all available records for each page")
    
    for page_id in page_ids:
        ads = fetch_ads_for_page(page_id)
        if ads:
            write_to_csv(ads, page_id)
            print(f"Completed fetching {len(ads)} ads for page ID '{page_id}'")
        else:
            print(f"No ads found for page ID '{page_id}'")
    
    print("\nProcess complete!")

if __name__ == "__main__":
    main()