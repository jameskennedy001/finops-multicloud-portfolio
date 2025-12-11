# GCP Pricing (us-central1)
GCP_PRICING = {
    # Compute (per hour)
    'e2-micro': 0.0084,
    'e2-small': 0.0168,
    'e2-medium': 0.0336,
    'n2-standard-2': 0.0971,
    'n2-standard-4': 0.1942,
    'a2-highgpu-1g': 3.673,  # GPU
    
    # Storage (per GB-month)
    'standard_storage': 0.020,
    'nearline_storage': 0.010,
    'coldline_storage': 0.004,
    
    # Database (per hour)
    'cloudsql_small': 0.0413,
    'cloudsql_medium': 0.0825,
    'cloudsql_large': 0.165,
    
    # Data transfer (per GB)
    'egress': 0.085,
}

TEAM_GCP_USAGE = {
    'Engineering': ['n2-standard-2', 'n2-standard-4', 'cloudsql_medium', 'standard_storage'],
    'DataScience': ['a2-highgpu-1g', 'n2-standard-4', 'standard_storage', 'coldline_storage'],
    'Marketing': ['e2-medium', 'standard_storage', 'cloudsql_small'],
    'Finance': ['e2-small', 'cloudsql_small', 'nearline_storage'],
    'DevOps': ['n2-standard-2', 'e2-medium', 'standard_storage'],
    'IT': ['e2-medium', 'n2-standard-2', 'cloudsql_small', 'standard_storage'],
}