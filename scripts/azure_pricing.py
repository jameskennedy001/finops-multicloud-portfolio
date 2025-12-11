# Azure Pricing (West Europe)
AZURE_PRICING = {
    # Compute (per hour)
    'B1s': 0.0104,
    'B2s': 0.0416,
    'D2s_v3': 0.096,
    'D4s_v3': 0.192,
    'F4s_v2': 0.169,
    'NC6s_v3': 3.06,  # GPU
    
    # Storage (per GB-month)
    'blob_hot': 0.0184,
    'blob_cool': 0.01,
    'blob_archive': 0.00099,
    
    # Database (per hour)
    'sql_basic': 0.0068,
    'sql_s3': 0.102,
    'sql_p1': 0.170,
    
    # Data transfer (per GB)
    'data_out': 0.087,
}

TEAM_AZURE_USAGE = {
    'Engineering': ['D2s_v3', 'D4s_v3', 'sql_s3', 'blob_hot'],
    'DataScience': ['NC6s_v3', 'D4s_v3', 'blob_hot', 'blob_archive'],
    'Marketing': ['B2s', 'blob_hot', 'sql_basic'],
    'Finance': ['B2s', 'sql_s3', 'blob_cool'],
    'DevOps': ['D2s_v3', 'F4s_v2', 'blob_hot'],
    'IT': ['B2s', 'D2s_v3', 'sql_basic', 'blob_hot'],
}