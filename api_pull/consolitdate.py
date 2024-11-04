import pandas as pd
import glob
import os
from datetime import datetime

# Configuration
input_directory = 'ad_data_plus_body_110324'  # Directory containing the CSV files
output_directory = 'consolidated_body_110324'  # Directory for the consolidated file

def consolidate_csvs():
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Get list of all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_directory, '*.csv'))
    
    if not csv_files:
        print("No CSV files found in the input directory")
        return
    
    print(f"Found {len(csv_files)} CSV files to consolidate")
    
    # Read and combine all CSV files
    dfs = []
    for file in csv_files:
        print(f"Reading {os.path.basename(file)}")
        df = pd.read_csv(file)
        dfs.append(df)
    
    # Concatenate all dataframes
    consolidated_df = pd.concat(dfs, ignore_index=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_directory, f'consolidated_ads_{timestamp}.csv')
    
    # Save consolidated data
    consolidated_df.to_csv(output_file, index=False)
    
    print(f"\nConsolidation complete!")
    print(f"Total records: {len(consolidated_df)}")
    print(f"Output file: {output_file}")

if __name__ == "__main__":
    consolidate_csvs()