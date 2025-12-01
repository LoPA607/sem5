#!/usr/bin/env python3
"""
Extract New Delhi Dengue Data
============================
Filters and saves New Delhi dengue data to a separate CSV file
"""

import csv

def extract_new_delhi_dengue():
    """Extract New Delhi dengue data and save to CSV"""
    print("Extracting New Delhi dengue data...")
    
    new_delhi_data = []
    
    # Read the original file
    with open("Final_data .csv", 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        
        for row in reader:
            # Filter for New Delhi dengue cases
            if (row.get('district') == 'New Delhi' and 
                'dengue' in str(row.get('Disease', '')).lower()):
                new_delhi_data.append(row)
    
    print(f"Found {len(new_delhi_data)} New Delhi dengue records")
    
    # Save to new CSV file
    output_file = "new_delhi_dengue_data.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        if new_delhi_data:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(new_delhi_data)
    
    print(f"✅ Saved to: {output_file}")
    
    # Show summary
    if new_delhi_data:
        print("\n📊 SUMMARY:")
        total_cases = sum([float(row['Cases']) if row['Cases'] else 0 for row in new_delhi_data])
        years = sorted(list(set([row['year'] for row in new_delhi_data])))
        weeks = sorted(list(set([row['week_of_outbreak'] for row in new_delhi_data])))
        
        print(f"Total cases: {total_cases:,}")
        print(f"Years: {', '.join(years)}")
        print(f"Weeks: {len(weeks)} unique weeks")
        print(f"First week: {weeks[0]}")
        print(f"Last week: {weeks[-1]}")
        
        # Show first few records
        print(f"\n📋 FIRST 3 RECORDS:")
        for i, row in enumerate(new_delhi_data[:3]):
            print(f"{i+1}. Week: {row['week_of_outbreak']}, Cases: {row['Cases']}, Year: {row['year']}")

def main():
    print("🎯 NEW DELHI DENGUE DATA EXTRACTOR")
    print("="*50)
    extract_new_delhi_dengue()

if __name__ == "__main__":
    main()
