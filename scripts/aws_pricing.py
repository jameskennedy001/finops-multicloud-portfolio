# AWS Pricing (us-east-1, per hour unless noted)
AWS_PRICING = {
    # Compute (per hour)
    't3.micro': 0.0104,
    't3.small': 0.0208,
    't3.medium': 0.0416,
    't3.large': 0.0832,
    'm5.large': 0.096,
    'm5.xlarge': 0.192,
    'm5.2xlarge': 0.384,
    'c5.2xlarge': 0.34,
    'p3.2xlarge': 3.06,  # GPU
    
    # Storage (per GB-month)
    's3_standard': 0.023,
    's3_ia': 0.0125,
    's3_glacier': 0.004,
    
    # Database (per hour)
    'rds_t3.small': 0.034,
    'rds_t3.medium': 0.068,
    'rds_m5.large': 0.188,
    'rds_m5.xlarge': 0.376,
    
    # Data transfer (per GB)
    'data_transfer_out': 0.09,
    'data_transfer_in': 0.0,
}

# Team resource allocations (which teams use what)
TEAM_AWS_USAGE = {
    'Engineering': ['t3.large', 'm5.xlarge', 'rds_m5.large', 's3_standard'],
    'DataScience': ['p3.2xlarge', 'm5.2xlarge', 's3_standard', 's3_glacier'],
    'Marketing': ['t3.medium', 's3_standard', 'rds_t3.small'],
    'Finance': ['t3.small', 'rds_t3.medium', 's3_ia'],
    'DevOps': ['t3.large', 'c5.2xlarge', 's3_standard'],
    'IT': ['t3.medium', 'm5.large', 'rds_t3.small', 's3_standard'],
}