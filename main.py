import pandas as pd
import sys
import yaml

def readCsv(filePath):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filePath)

    # Ensure the 'division' and 'points' columns are integers
    df['division'] = df['division'].astype(int)
    df['points'] = df['points'].astype(int)

    return df

def selectTopRecords(df):
    # Sort by 'division' and 'points' in descending order and select top 3
    top_records = df.sort_values(by=['division', 'points'], ascending=[False, False]).head(3)
    return top_records

def formatYaml(df):
    # Convert the DataFrame to a list of dictionaries for YAML formatting
    yaml_output = {'records': []}
    for _, record in df.iterrows():
        entry = {
            'name': f"{record['firstname']} {record['lastname']}",
            'details': f"In division {record['division']} from {record['date']} performing {record['summary']}"
        }
        yaml_output['records'].append(entry)
    
    return yaml.dump(yaml_output, sort_keys=False)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        # Read CSV into a DataFrame
        df = readCsv(file_path)
        
        if df.empty:
            print("No valid records found in the CSV file.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Select top records
    top_records = selectTopRecords(df)

    # Format the selected records as YAML
    yaml_output = formatYaml(top_records)

    # Output the result
    print(yaml_output)
    
if __name__ == "__main__":
    main()