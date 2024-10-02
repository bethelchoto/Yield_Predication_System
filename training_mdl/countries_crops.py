import pandas as pd

# Function to load CSV and extract unique countries and crops
def load_csv_and_extract_countries_crops(file_path):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Assuming columns for countries and crops are named 'Country' and 'Crop'
        unique_countries = df['Area'].unique()
        unique_crops = df['Item'].unique()
        
        # Convert them to lists for easier handling
        unique_countries_list = list(unique_countries)
        unique_crops_list = list(unique_crops)
        
        print("Unique Countries:")
        print(unique_countries_list)
        
        print("\nUnique Crops:")
        print(unique_crops_list)
        
        return unique_countries_list, unique_crops_list
    except Exception as e:
        print(f"Error loading CSV file: {e}")

# Example usage
csv_file_path = 'yield_df.csv'
countries, crops = load_csv_and_extract_countries_crops(csv_file_path)
