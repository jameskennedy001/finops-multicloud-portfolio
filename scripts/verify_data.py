import pandas as pd
import matplotlib.pyplot as plt

print("="*50)
print("DATA VERIFICATION")
print("="*50)

# Load all data
df_aws = pd.read_csv('../data/aws_costs.csv', parse_dates=['Date'])
df_azure = pd.read_csv('../data/azure_costs.csv', parse_dates=['Date'])
df_gcp = pd.read_csv('../data/gcp_costs.csv', parse_dates=['Date'])
df_all = pd.concat([df_aws, df_azure, df_gcp], ignore_index=True)

print(f"\nTotal records: {len(df_all):,}")
print(f"Date range: {df_all['Date'].min()} to {df_all['Date'].max()}")

# Monthly spending pattern
df_all['YearMonth'] = df_all['Date'].dt.to_period('M')
monthly = df_all.groupby('YearMonth')['DailyCost'].sum()

print(f"\n{'='*50}")
print("MONTHLY SPENDING")
print(f"{'='*50}")
for ym in monthly.index:
    print(f"{ym}: ${monthly[ym]:>10,.0f}")

# Annual summary
print(f"\n{'='*50}")
print("ANNUAL SUMMARY")
print(f"{'='*50}")
for year in [2023, 2024]:
    year_data = df_all[df_all['Date'].dt.year == year]
    print(f"\n{year}:")
    print(f"  Total: ${year_data['DailyCost'].sum():,.0f}")
    print(f"  By cloud:")
    for cloud in ['AWS', 'Azure', 'GCP']:
        cloud_cost = year_data[year_data['Cloud'] == cloud]['DailyCost'].sum()
        print(f"    {cloud:6s}: ${cloud_cost:>12,.0f} ({cloud_cost/year_data['DailyCost'].sum()*100:.1f}%)")
    
    print(f"  Tagging:")
    print(f"    Untagged:  {(year_data['TaggingStatus'] == 'untagged').mean()*100:.1f}%")
    print(f"    Partial:   {(year_data['TaggingStatus'] == 'partial').mean()*100:.1f}%")
    print(f"    Compliant: {(year_data['TaggingStatus'] == 'compliant').mean()*100:.1f}%")
    
    print(f"  RI Coverage: {(year_data['HasRI'] == True).mean()*100:.1f}%")

# Strategic investments visible?
print(f"\n{'='*50}")
print("STRATEGIC INVESTMENTS CHECK")
print(f"{'='*50}")
investments = df_all[df_all['BusinessJustification'] != '']
print(f"Total records with business justification: {len(investments):,}")
print(f"\nTop justifications:")
for just in investments['BusinessJustification'].value_counts().head(5).items():
    print(f"  {just[0]}: {just[1]:,} records")

# Team breakdown
print(f"\n{'='*50}")
print("COST BY TEAM (2024)")
print(f"{'='*50}")
teams_2024 = df_all[df_all['Date'].dt.year == 2024].groupby('Team')['DailyCost'].sum().sort_values(ascending=False)
for team, cost in teams_2024.items():
    print(f"{team:15s}: ${cost:>12,.0f}")

print(f"\n✓ Verification complete")

# Create charts
print("\nGenerating charts...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Monthly spending trend
ax1 = axes[0, 0]
monthly.plot(kind='bar', ax=ax1, color=['blue']*12 + ['green']*12)
ax1.set_title('Monthly Cloud Spend (2023-2024)')
ax1.set_xlabel('Month')
ax1.set_ylabel('Spend ($)')
ax1.axvline(x=11.5, color='red', linestyle='--', label='FinOps Start')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

# 2. Tagging improvement
ax2 = axes[0, 1]
tagging_2023 = [
    (df_all[df_all['Date'].dt.year == 2023]['TaggingStatus'] == 'untagged').mean() * 100,
    (df_all[df_all['Date'].dt.year == 2023]['TaggingStatus'] == 'partial').mean() * 100,
    (df_all[df_all['Date'].dt.year == 2023]['TaggingStatus'] == 'compliant').mean() * 100
]
tagging_2024 = [
    (df_all[df_all['Date'].dt.year == 2024]['TaggingStatus'] == 'untagged').mean() * 100,
    (df_all[df_all['Date'].dt.year == 2024]['TaggingStatus'] == 'partial').mean() * 100,
    (df_all[df_all['Date'].dt.year == 2024]['TaggingStatus'] == 'compliant').mean() * 100
]
x = ['Untagged', 'Partial', 'Compliant']
width = 0.35
x_pos = range(len(x))
ax2.bar([p - width/2 for p in x_pos], tagging_2023, width, label='2023', color='red', alpha=0.7)
ax2.bar([p + width/2 for p in x_pos], tagging_2024, width, label='2024', color='green', alpha=0.7)
ax2.set_title('Tagging Compliance Improvement')
ax2.set_ylabel('Percentage')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(x)
ax2.legend()

# 3. Cloud distribution
ax3 = axes[1, 0]
cloud_2024 = df_all[df_all['Date'].dt.year == 2024].groupby('Cloud')['DailyCost'].sum()
ax3.pie(cloud_2024, labels=cloud_2024.index, autopct='%1.1f%%', startangle=90)
ax3.set_title('2024 Spend by Cloud')

# 4. Team spending (top 6)
ax4 = axes[1, 1]
teams_top = teams_2024.head(6)
teams_top.plot(kind='barh', ax=ax4, color='steelblue')
ax4.set_title('2024 Spend by Team (Top 6)')
ax4.set_xlabel('Spend ($)')

plt.tight_layout()
plt.savefig('../analysis/data_verification.png', dpi=150, bbox_inches='tight')
print("✓ Charts saved to ../analysis/data_verification.png")
plt.close()

print("="*50)