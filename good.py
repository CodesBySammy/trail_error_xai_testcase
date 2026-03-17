def calculate_average_revenue(sales_records: list) -> float:
    """
    Calculates the average revenue from a list of sales dictionaries.
    Ignores records that do not contain a 'revenue' key.
    """
    if not sales_records:
        return 0.0
    
    total_revenue = 0.0
    valid_records = 0
    
    for record in sales_records:
        if isinstance(record, dict) and 'revenue' in record:
            total_revenue += float(record['revenue'])
            valid_records += 1
            
    if valid_records == 0:
        return 0.0
        
    return total_revenue / valid_records
