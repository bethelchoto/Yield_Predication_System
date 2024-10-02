import pandas as pd

# Function to load CSV and find min/max values for specific columns
def load_csv_and_find_min_max(file_path):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Define the columns you want to find min/max for
        target_columns = ['average_rain_fall_mm_per_year', 'avg_temp', 'pesticides_tonnes']
        
        # Check if the target columns exist in the DataFrame
        for col in target_columns:
            if col not in df.columns:
                print(f"Column '{col}' not found in the CSV file.")
                continue
            
            # Find the min and max for the column
            min_value = df[col].min()
            max_value = df[col].max()
            
            # Print the result
            print(f"{col}: Min = {min_value}, Max = {max_value}")
        
    except Exception as e:
        print(f"Error loading CSV file: {e}")

# Example usage
csv_file_path = 'yield_df.csv'  # Replace with the actual CSV file path
load_csv_and_find_min_max(csv_file_path)
