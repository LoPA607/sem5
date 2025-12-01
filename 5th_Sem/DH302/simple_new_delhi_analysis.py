#!/usr/bin/env python3
"""
Simple New Delhi Dengue Analysis
Cases vs Temperature, Precipitation, and LAI over Time
"""

import matplotlib.pyplot as plt
import csv
from datetime import datetime

def load_data():
    """Load New Delhi dengue data"""
    data = []
    with open("Final_data .csv", 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row.get('district') == 'New Delhi' and 
                'dengue' in str(row.get('Disease', '')).lower()):
                try:
                    cases = float(row.get('Cases', 0))
                    preci = float(row.get('preci', 0))
                    temp = float(row.get('Temp', 273.15)) - 273.15  # Convert to Celsius
                    lai = float(row.get('LAI', 0)) if row.get('LAI') else None
                    year = int(row.get('year', 2013))
                    month = int(row.get('mon', 1))
                    day = int(row.get('day', 1))
                    
                    try:
                        date = datetime(year, month, day)
                    except:
                        date = datetime(year, 1, 1)
                    
                    data.append({
                        'date': date,
                        'cases': cases,
                        'temp': temp,
                        'preci': preci,
                        'lai': lai
                    })
                except:
                    continue
    
    data.sort(key=lambda x: x['date'])
    print(f"Loaded {len(data)} records from {data[0]['date'].year} to {data[-1]['date'].year}")
    return data

def create_plots(data):
    """Create the 4 requested plots + table"""
    
    fig = plt.figure(figsize=(16, 20))
    
    # Create subplots
    ax1 = plt.subplot(5, 1, 1)
    ax2 = plt.subplot(5, 1, 2)
    ax3 = plt.subplot(5, 1, 3)
    ax4 = plt.subplot(5, 1, 4)
    ax5 = plt.subplot(5, 1, 5)
    
    fig.suptitle('NEW DELHI DENGUE ANALYSIS', fontsize=16, fontweight='bold')
    
    dates = [d['date'] for d in data]
    cases = [d['cases'] for d in data]
    temps = [d['temp'] for d in data]
    precis = [d['preci'] for d in data]
    lais = [d['lai'] for d in data if d['lai'] is not None]
    lai_dates = [d['date'] for d in data if d['lai'] is not None]
    lai_cases = [d['cases'] for d in data if d['lai'] is not None]
    
    # Plot 1: Cases + Temperature vs Time
    ax1_cases = ax1
    line1 = ax1_cases.plot(dates, cases, 'ro-', linewidth=2, markersize=6, label='Cases')
    ax1_cases.set_ylabel('Cases', color='red', fontweight='bold')
    ax1_cases.tick_params(axis='y', labelcolor='red')
    
    ax1_temp = ax1_cases.twinx()
    line2 = ax1_temp.plot(dates, temps, 'g^-', linewidth=2, markersize=4, label='Temperature')
    ax1_temp.set_ylabel('Temperature (°C)', color='green', fontweight='bold')
    ax1_temp.tick_params(axis='y', labelcolor='green')
    
    ax1.set_title('Cases & Temperature vs Time', fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.grid(True, alpha=0.3)
    
    # Combined legend
    lines1 = line1 + line2
    labels1 = [l.get_label() for l in lines1]
    ax1.legend(lines1, labels1, loc='upper left')
    
    # Plot 2: Cases + Precipitation vs Time
    ax2_cases = ax2
    line3 = ax2_cases.plot(dates, cases, 'ro-', linewidth=2, markersize=6, label='Cases')
    ax2_cases.set_ylabel('Cases', color='red', fontweight='bold')
    ax2_cases.tick_params(axis='y', labelcolor='red')
    
    ax2_preci = ax2_cases.twinx()
    line4 = ax2_preci.plot(dates, precis, 'b^-', linewidth=2, markersize=4, label='Precipitation')
    ax2_preci.set_ylabel('Precipitation', color='blue', fontweight='bold')
    ax2_preci.tick_params(axis='y', labelcolor='blue')
    
    ax2.set_title('Cases & Precipitation vs Time', fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.grid(True, alpha=0.3)
    
    # Combined legend
    lines2 = line3 + line4
    labels2 = [l.get_label() for l in lines2]
    ax2.legend(lines2, labels2, loc='upper left')
    
    # Plot 3: Cases + LAI vs Time
    ax3_cases = ax3
    line5 = ax3_cases.plot(dates, cases, 'ro-', linewidth=2, markersize=6, label='Cases')
    ax3_cases.set_ylabel('Cases', color='red', fontweight='bold')
    ax3_cases.tick_params(axis='y', labelcolor='red')
    
    if lais:  # Only plot LAI if data exists
        ax3_lai = ax3_cases.twinx()
        line6 = ax3_lai.plot(lai_dates, lais, 'mo-', linewidth=2, markersize=4, label='LAI')
        ax3_lai.set_ylabel('LAI', color='magenta', fontweight='bold')
        ax3_lai.tick_params(axis='y', labelcolor='magenta')
        
        # Combined legend
        lines3 = line5 + line6
        labels3 = [l.get_label() for l in lines3]
        ax3.legend(lines3, labels3, loc='upper left')
    else:
        ax3.legend(['Cases'], loc='upper left')
    
    ax3.set_title('Cases & LAI vs Time', fontweight='bold')
    ax3.set_xlabel('Date')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Just Cases vs Time (simple plot)
    ax4.plot(dates, cases, 'ro-', linewidth=3, markersize=8, color='red')
    ax4.set_title('Number of Cases vs Time', fontweight='bold', fontsize=14)
    ax4.set_xlabel('Date', fontweight='bold')
    ax4.set_ylabel('Number of Cases', fontweight='bold', color='red')
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='y', labelcolor='red')
    
    # Add case numbers as annotations
    for date, case in zip(dates, cases):
        ax4.annotate(f'{int(case):,}', (date, case), 
                    xytext=(0, 10), textcoords='offset points',
                    ha='center', fontweight='bold', fontsize=9)
    
    # Plot 5: Data Table
    ax5.axis('off')
    
    # Prepare table data
    table_data = []
    for d in data:
        table_data.append([
            d['date'].strftime('%Y-%m-%d'),
            f"{int(d['cases']):,}",
            f"{d['temp']:.1f}°C",
            f"{d['preci']:.4f}",
            f"{d['lai']:.2f}" if d['lai'] is not None else "N/A"
        ])
    
    headers = ['Date', 'Cases', 'Temperature', 'Precipitation', 'LAI']
    
    # Create table
    table = ax5.table(cellText=table_data,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 1])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    # Color code rows by year
    for i, row in enumerate(table_data):
        year = int(row[0].split('-')[0])
        color = 'lightcoral' if year == 2015 else 'lightsalmon' if year == 2013 else 'lightblue'
        for j in range(len(headers)):
            table[(i+1, j)].set_facecolor(color)
    
    # Header styling
    for j in range(len(headers)):
        table[(0, j)].set_facecolor('lightgray')
        table[(0, j)].set_text_props(weight='bold')
    
    ax5.set_title('Data Table: All Parameters', fontweight='bold', pad=20)
    
    # Format x-axis for all time plots
    for ax in [ax1, ax2, ax3, ax4]:
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig('simple_new_delhi_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    print("NEW DELHI DENGUE: Cases vs Temp, Precipitation, LAI over Time + Table")
    print("="*70)
    
    data = load_data()
    create_plots(data)
    
    print("\n✅ Done! Generated: simple_new_delhi_analysis.png")
    print("📊 Includes: 4 plots + data table")
    print("   - Cases & Temperature vs Time")
    print("   - Cases & Precipitation vs Time") 
    print("   - Cases & LAI vs Time")
    print("   - Number of Cases vs Time")
    print("   - Complete Data Table")

if __name__ == "__main__":
    main()
