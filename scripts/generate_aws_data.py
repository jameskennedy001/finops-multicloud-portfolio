import pandas as pd
import numpy as np
from datetime import datetime
from aws_pricing import AWS_PRICING, TEAM_AWS_USAGE

np.random.seed(42)

print("="*50)
print("GENERATING AWS DATA - FINOPS TRANSFORMATION")
print("TechCorp: $3M cloud spend, 40% revenue growth")
print("="*50)

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='D')

teams = ['Engineering', 'DataScience', 'Marketing', 'Finance', 'DevOps', 'IT']
environments = ['Production', 'Development', 'Staging']
BASE_SCALE = 1.0

def get_monthly_growth_factor(date, start_date):
    """Realistic monthly growth with organic growth, strategic events, and FinOps impact"""
    year = date.year
    month = date.month
    days = (date - start_date).days
    
    months_elapsed = days / 30.4
    organic_growth = 1.0 + (months_elapsed * 0.028)
    
    if year == 2023:
        if month <= 3:
            seasonal = 0.94
        elif month <= 6:
            seasonal = 0.98
        elif month <= 9:
            seasonal = 1.00
        else:
            seasonal = 1.06
        
        if month == 5:
            seasonal *= 1.15
        if month == 8:
            seasonal *= 1.08
        
        return organic_growth * seasonal
    
    else:
        if month <= 3:
            seasonal = 0.96
        elif month <= 6:
            seasonal = 1.02
        elif month <= 9:
            seasonal = 1.04
        else:
            seasonal = 1.08
        
        if month <= 3:
            finops_efficiency = 0.97
        elif month <= 6:
            finops_efficiency = 0.92
        elif month <= 9:
            finops_efficiency = 0.88
        else:
            finops_efficiency = 0.86
        
        strategic = 1.0
        if month in [4, 5]:
            strategic = 1.25
        if month == 6:
            strategic = 1.10
        if month == 8:
            strategic = 1.12
        if month == 10:
            strategic = 1.18
        if month == 12:
            strategic = 0.94
        
        return organic_growth * seasonal * finops_efficiency * strategic

def get_tagging_status(date, start_date):
    days = (date - start_date).days
    if days < 365:
        if np.random.random() < 0.30:
            return ('untagged', 'v1.0')
        elif np.random.random() < 0.55:
            return ('partial', 'v1.0')
        else:
            return ('compliant', 'v1.0')
    elif days < 455:
        progress = (days - 365) / 90
        untagged_rate = 0.30 - (0.05 * progress)
        partial_rate = 0.30 + (0.10 * progress)
        if np.random.random() < untagged_rate:
            return ('untagged', 'v2.0')
        elif np.random.random() < (untagged_rate + partial_rate):
            return ('partial', 'v2.0')
        else:
            return ('compliant', 'v2.0')
    elif days < 640:
        progress = (days - 455) / 185
        untagged_rate = 0.25 - (0.10 * progress)
        partial_rate = 0.40 - (0.15 * progress)
        if np.random.random() < untagged_rate:
            return ('untagged', 'v2.0')
        elif np.random.random() < (untagged_rate + partial_rate):
            return ('partial', 'v2.0')
        else:
            return ('compliant', 'v2.0')
    else:
        progress = min(1.0, (days - 640) / 90)
        untagged_rate = 0.15 - (0.05 * progress)
        partial_rate = 0.25 - (0.10 * progress)
        if np.random.random() < untagged_rate:
            return ('untagged', 'v2.2')
        elif np.random.random() < (untagged_rate + partial_rate):
            return ('partial', 'v2.2')
        else:
            return ('compliant', 'v2.2')

def get_efficiency_multiplier(date, start_date, team):
    days = (date - start_date).days
    base_efficiency = 0.92 if team == 'DevOps' else 1.0
    if days < 365:
        return base_efficiency
    elif days < 455:
        improvement = (days - 365) / 90 * 0.05
        return base_efficiency - improvement
    elif days < 545:
        improvement = 0.05 + ((days - 455) / 90 * 0.08)
        return base_efficiency - improvement
    elif days < 640:
        improvement = 0.13 + ((days - 545) / 95 * 0.05)
        return base_efficiency - improvement
    else:
        return base_efficiency - 0.18

def get_ri_coverage(date, start_date, resource_type):
    days = (date - start_date).days
    if not resource_type.startswith(('t3', 'm5', 'rds')):
        return 1.0
    if days < 365:
        if np.random.random() < 0.10:
            return 0.65
        return 1.0
    elif days < 455:
        if np.random.random() < 0.10:
            return 0.65
        return 1.0
    elif days < 545:
        progress = (days - 455) / 90
        coverage = 0.10 + (0.15 * progress)
        if np.random.random() < coverage:
            return 0.65
        return 1.0
    elif days < 640:
        if np.random.random() < 0.30:
            return 0.65
        return 1.0
    else:
        if np.random.random() < 0.35:
            return 0.65
        return 1.0

def get_strategic_investment(date, start_date, team):
    days = (date - start_date).days
    multiplier = 1.0
    justification = None
    if team == 'Engineering' and 590 <= days < 620:
        multiplier = 2.1
        justification = "AI analytics feature launch"
    elif team == 'Marketing' and date.year == 2024 and date.month >= 10:
        multiplier = 1.6
        justification = "Q4 pipeline campaign"
    elif team == 'Finance' and date.year == 2024 and 7 <= date.month <= 9:
        multiplier = 1.4
        justification = "SOC2 Type II preparation"
    elif team == 'DevOps' and date.year == 2024 and 4 <= date.month <= 6:
        multiplier = 1.8
        justification = "CI/CD velocity improvement"
    elif team == 'DataScience' and date.year == 2024 and date.month >= 7:
        multiplier = 1.3
        justification = "ML experimentation budget"
    return multiplier, justification

def generate_aws_costs(date_range, teams):
    records = []
    for date in date_range:
        monthly_factor = get_monthly_growth_factor(date, start_date)
        for team in teams:
            resources = TEAM_AWS_USAGE[team]
            efficiency_mult = get_efficiency_multiplier(date, start_date, team)
            strategic_mult, justification = get_strategic_investment(date, start_date, team)
            
            for resource_type in resources:
                tagging_status, standard_version = get_tagging_status(date, start_date)
                
                if resource_type.startswith(('t3', 'm5', 'c5', 'p3')):
                    service = 'EC2'
                    unit = 'Hours'
                    base_usage = np.random.uniform(20, 24)
                    usage = base_usage * efficiency_mult * strategic_mult
                    unit_cost = AWS_PRICING[resource_type]
                    ri_discount = get_ri_coverage(date, start_date, resource_type)
                    unit_cost *= ri_discount
                    
                elif resource_type.startswith('s3'):
                    service = 'S3'
                    unit = 'GB-Month'
                    base_storage = 1000 if team == 'DataScience' else 200
                    growth_factor = 1 + (date - start_date).days / 730
                    if (date - start_date).days >= 455:
                        growth_factor *= 0.93
                    usage = base_storage * growth_factor * np.random.uniform(0.9, 1.1) * strategic_mult
                    unit_cost = AWS_PRICING[resource_type] / 30
                    
                elif resource_type.startswith('rds'):
                    service = 'RDS'
                    unit = 'Hours'
                    usage = 24 * strategic_mult
                    unit_cost = AWS_PRICING[resource_type]
                    ri_discount = get_ri_coverage(date, start_date, resource_type)
                    unit_cost *= ri_discount
                    
                else:
                    continue
                
                daily_cost = usage * unit_cost * BASE_SCALE * monthly_factor
                environment = np.random.choice(environments, p=[0.6, 0.25, 0.15])
                
                if tagging_status == 'untagged':
                    team_tag = 'Untagged'
                    env_tag = 'Untagged'
                    costcenter_tag = 'Untagged'
                elif tagging_status == 'partial':
                    team_tag = team
                    env_tag = environment if np.random.random() > 0.5 else 'Untagged'
                    costcenter_tag = 'Untagged'
                else:
                    team_tag = team
                    env_tag = environment
                    costcenter_tag = f"CC-{team[:3].upper()}"
                
                records.append({
                    'Date': date,
                    'Cloud': 'AWS',
                    'Service': service,
                    'ResourceType': resource_type,
                    'Team': team_tag,
                    'Environment': env_tag,
                    'CostCenter': costcenter_tag,
                    'Usage': round(usage, 2),
                    'Unit': unit,
                    'UnitCost': round(unit_cost, 4),
                    'DailyCost': round(daily_cost, 2),
                    'TaggingStatus': tagging_status,
                    'TagStandard': standard_version,
                    'HasRI': ri_discount < 1.0,
                    'BusinessJustification': justification if justification else '',
                })
    return pd.DataFrame(records)

print("Generating AWS cost data...")
df_aws = generate_aws_costs(date_range, teams)

print("Adding data transfer...")
transfer_records = []
for date in date_range:
    monthly_factor = get_monthly_growth_factor(date, start_date)
    efficiency_mult = get_efficiency_multiplier(date, start_date, 'Engineering')
    tagging_status, standard_version = get_tagging_status(date, start_date)
    
    for team in teams:
        if team == 'DataScience':
            transfer_gb = np.random.uniform(500, 1500)
        else:
            transfer_gb = np.random.uniform(50, 200)
        
        if (date - start_date).days >= 545:
            transfer_gb *= 0.88
        
        transfer_cost = transfer_gb * AWS_PRICING['data_transfer_out'] * BASE_SCALE * monthly_factor
        
        if tagging_status == 'untagged':
            team_tag = 'Untagged'
            env_tag = 'Untagged'
            costcenter_tag = 'Untagged'
        elif tagging_status == 'partial':
            team_tag = team
            env_tag = 'Production'
            costcenter_tag = 'Untagged'
        else:
            team_tag = team
            env_tag = 'Production'
            costcenter_tag = f"CC-{team[:3].upper()}"
        
        transfer_records.append({
            'Date': date,
            'Cloud': 'AWS',
            'Service': 'DataTransfer',
            'ResourceType': 'Egress',
            'Team': team_tag,
            'Environment': env_tag,
            'CostCenter': costcenter_tag,
            'Usage': round(transfer_gb, 2),
            'Unit': 'GB',
            'UnitCost': AWS_PRICING['data_transfer_out'],
            'DailyCost': round(transfer_cost, 2),
            'TaggingStatus': tagging_status,
            'TagStandard': standard_version,
            'HasRI': False,
            'BusinessJustification': '',
        })

df_transfer = pd.DataFrame(transfer_records)
df_aws = pd.concat([df_aws, df_transfer], ignore_index=True)

output_path = '../data/aws_costs.csv'
df_aws.to_csv(output_path, index=False)

df_aws['Date'] = pd.to_datetime(df_aws['Date'])
year_2023 = df_aws[df_aws['Date'].dt.year == 2023]
year_2024 = df_aws[df_aws['Date'].dt.year == 2024]

print(f"\n{'='*50}")
print("AWS TRANSFORMATION SUMMARY")
print(f"{'='*50}")
print(f"Total records: {len(df_aws):,}")
print(f"\n2023 Baseline:")
print(f"  Total spend: ${year_2023['DailyCost'].sum():,.0f}")
print(f"  Untagged: {(year_2023['TaggingStatus'] == 'untagged').mean()*100:.1f}%")
print(f"  Partial: {(year_2023['TaggingStatus'] == 'partial').mean()*100:.1f}%")
print(f"  Compliant: {(year_2023['TaggingStatus'] == 'compliant').mean()*100:.1f}%")
print(f"  RI coverage: {(year_2023['HasRI'] == True).mean()*100:.1f}%")
print(f"\n2024 Transformation:")
print(f"  Total spend: ${year_2024['DailyCost'].sum():,.0f}")
print(f"  Growth: {((year_2024['DailyCost'].sum() / year_2023['DailyCost'].sum()) - 1)*100:+.1f}%")
print(f"  Untagged: {(year_2024['TaggingStatus'] == 'untagged').mean()*100:.1f}%")
print(f"  Partial: {(year_2024['TaggingStatus'] == 'partial').mean()*100:.1f}%")
print(f"  Compliant: {(year_2024['TaggingStatus'] == 'compliant').mean()*100:.1f}%")
print(f"  RI coverage: {(year_2024['HasRI'] == True).mean()*100:.1f}%")
print(f"\nSaved to {output_path}")
print("="*50)