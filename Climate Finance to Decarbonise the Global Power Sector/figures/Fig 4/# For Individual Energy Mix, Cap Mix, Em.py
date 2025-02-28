# For Individual Energy Mix, Cap Mix, Emi Mix
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

def format_value(value, metric):
    if metric == 'capacity':
        gw_value = value / 1000
        return f'{gw_value:.1f}\nGW'
    elif metric == 'activity':
        twh_value = value / 1_000_000
        return f'{twh_value:.1f}\nTWh'
    else:  
        gt_value = value / 1000
        return f'{gt_value:.3f}\nGt'

def create_visualization_block(df, title, mask, is_group=False):
    fig, axes = plt.subplots(1, 3, figsize=(6, 2))  # Using your smaller figure size
    if is_group:
        fig.suptitle(title, fontsize=12, fontweight='bold', y=1.15)
    else:
        fig.suptitle(title, fontsize=12, fontweight='bold', y=1.15)
    
    subsectors = ['Coal', 'Gas', 'Oil', 'Solar', 'Wind', 'Hydropower', 
                 'Geothermal', 'Nuclear', 'Bioenergy']
    metrics = ['capacity', 'activity', 'annualco2tyear']
    titles = ['Installed\nCapacity', 'Electricity\nGenerated', 'Emissions']
    
    for ax, metric, title in zip(axes, metrics, titles):
        data = df[mask].groupby('subsector')[metric].sum()
        data = data.reindex(subsectors).fillna(0)
        total_value = data.sum()
        
        if total_value > 0:
            wedges, _ = ax.pie(data, wedgeprops=dict(width=0.4), startangle=90)  # Using your wider donut
            ax.text(0, 0, format_value(total_value, metric),
                   ha='center', va='center', fontsize=10)
        
        ax.set_title(title, pad=0, fontsize=10)  # Using your zero padding
        ax.axis('equal')
    
    plt.show()
    plt.close()

def create_visualizations(df):
    plt.style.use(['science', 'nature', 'light'])
    
    plt.rcParams.update({
        'font.size': 10,
        'font.family': 'DejaVu Sans',
        'axes.linewidth': 0.5,
        'grid.linewidth': 0.5,
        'lines.linewidth': 1,
        'lines.markersize': 3,
        'text.usetex': False,
    })
    
    # First create group visualizations
    groups = [
        ('Global', lambda x: x['status'] == 'operating'),
        ('Developed Countries', lambda x: (x['status'] == 'operating') & (x['unfccc_group'] == 'Developed Financiers')),
        ('Developing Countries', lambda x: (x['status'] == 'operating') & (x['unfccc_group'] == 'Developing Recipients'))
    ]
    
    for title, mask in groups:
        create_visualization_block(df, title, mask, is_group=True)
    
    # Then create country visualizations
    countries = [
        ('IN', 'India'), ('ID', 'Indonesia'), ('ZA', 'South Africa'),
        ('MX', 'Mexico'), ('VN', 'Vietnam'), ('IR', 'Iran'),
        ('TH', 'Thailand'), ('EG', 'Egypt')
    ]
    
    for code, name in countries:
        mask = (df['status'] == 'operating') & (df['asset_location'] == code)
        create_visualization_block(df, name, mask, is_group=False)

def main():
    df = pd.read_csv('/Users/yukthabhadane/Documents/Climate Finance Thesis/Data/v3_power_Forward_Analytics2024.csv')
    unfccc_df = pd.read_excel('/Users/yukthabhadane/Documents/Climate Finance Thesis/Policy Brief/UNFCCC classification.xlsx')
    
    location_to_group = dict(zip(unfccc_df['asset_location'], unfccc_df['group']))
    df['unfccc_group'] = df['asset_location'].map(location_to_group)
    
    create_visualizations(df)

if __name__ == "__main__":
    main()