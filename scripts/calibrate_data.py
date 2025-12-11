import pandas as pd

print("="*50)
print("CALIBRATING TO $3M TARGET")
print("="*50)

df_aws = pd.read_csv('../data/aws_costs.csv')
df_azure = pd.read_csv('../data/azure_costs.csv')
df_gcp = pd.read_csv('../data/gcp_costs.csv')

df_aws['Date'] = pd.to_datetime(df_aws['Date'])
df_azure['Date'] = pd.to_datetime(df_azure['Date'])
df_gcp['Date'] = pd.to_datetime(df_gcp['Date'])

aws_2023 = df_aws[df_aws['Date'].dt.year == 2023]['DailyCost'].sum()
aws_2024 = df_aws[df_aws['Date'].dt.year == 2024]['DailyCost'].sum()
azure_2023 = df_azure[df_azure['Date'].dt.year == 2023]['DailyCost'].sum()
azure_2024 = df_azure[df_azure['Date'].dt.year == 2024]['DailyCost'].sum()
gcp_2023 = df_gcp[df_gcp['Date'].dt.year == 2023]['DailyCost'].sum()
gcp_2024 = df_gcp[df_gcp['Date'].dt.year == 2024]['DailyCost'].sum()

total_2023 = aws_2023 + azure_2023 + gcp_2023
total_2024 = aws_2024 + azure_2024 + gcp_2024

print(f"\nCurrent: 2023=${total_2023:,.0f} | 2024=${total_2024:,.0f}")

target_2023 = 3_000_000
target_2024 = 3_600_000

aws_target_2023 = target_2023 * 0.40
azure_target_2023 = target_2023 * 0.32
gcp_target_2023 = target_2023 * 0.28
aws_target_2024 = target_2024 * 0.40
azure_target_2024 = target_2024 * 0.32
gcp_target_2024 = target_2024 * 0.28

aws_scale = (aws_target_2023 + aws_target_2024) / (aws_2023 + aws_2024)
azure_scale = (azure_target_2023 + azure_target_2024) / (azure_2023 + azure_2024)
gcp_scale = (gcp_target_2023 + gcp_target_2024) / (gcp_2023 + gcp_2024)

print(f"Scale: AWS={aws_scale:.2f}x | Azure={azure_scale:.2f}x | GCP={gcp_scale:.2f}x")

df_aws['DailyCost'] = df_aws['DailyCost'] * aws_scale
df_azure['DailyCost'] = df_azure['DailyCost'] * azure_scale
df_gcp['DailyCost'] = df_gcp['DailyCost'] * gcp_scale

df_aws.to_csv('../data/aws_costs.csv', index=False)
df_azure.to_csv('../data/azure_costs.csv', index=False)
df_gcp.to_csv('../data/gcp_costs.csv', index=False)

aws_2023_new = df_aws[df_aws['Date'].dt.year == 2023]['DailyCost'].sum()
aws_2024_new = df_aws[df_aws['Date'].dt.year == 2024]['DailyCost'].sum()
azure_2023_new = df_azure[df_azure['Date'].dt.year == 2023]['DailyCost'].sum()
azure_2024_new = df_azure[df_azure['Date'].dt.year == 2024]['DailyCost'].sum()
gcp_2023_new = df_gcp[df_gcp['Date'].dt.year == 2023]['DailyCost'].sum()
gcp_2024_new = df_gcp[df_gcp['Date'].dt.year == 2024]['DailyCost'].sum()

print(f"\n{'='*50}")
print("FINAL CALIBRATED RESULTS")
print(f"{'='*50}")
print(f"2023: AWS=${aws_2023_new:,.0f} | Azure=${azure_2023_new:,.0f} | GCP=${gcp_2023_new:,.0f}")
print(f"      Total: ${aws_2023_new + azure_2023_new + gcp_2023_new:,.0f}")
print(f"\n2024: AWS=${aws_2024_new:,.0f} | Azure=${azure_2024_new:,.0f} | GCP=${gcp_2024_new:,.0f}")
print(f"      Total: ${aws_2024_new + azure_2024_new + gcp_2024_new:,.0f}")
print(f"\nGrowth: {((aws_2024_new + azure_2024_new + gcp_2024_new)/(aws_2023_new + azure_2023_new + gcp_2023_new)-1)*100:+.1f}%")
print(f"\n✓ Data calibrated to $3M baseline")
print("="*50)