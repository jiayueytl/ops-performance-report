import pandas as pd
from datetime import datetime

def process_data(df):
    """Cleans columns and identifies unique annotators."""
    df.columns = df.columns.str.strip()
    return df, df['name'].unique()

def get_performance_context(df, name, task_period):
    """Prepares context for the Performance Report."""
    person_df = df[df['name'] == name]

    sortable_keys = ['project_name', 'date']

    if set(sortable_keys).issubset(person_df.columns):
        person_df = person_df.sort_values(by=sortable_keys, ascending=[True, True])
        
    person_df = person_df[person_df['total_completed']>0] if 'total_completed' in person_df.columns else person_df
    
    safe_name = str(name).upper()
    return {
        "ctx": {
            "report_id": f"{safe_name.replace(' ', '_')}_Performance_{datetime.now().strftime('%Y%m%d')}",
            "report_date": datetime.now().strftime("%d-%b-%Y"),
            "task_period": task_period,
            "name": safe_name,
            "projects": person_df.to_dict('records'),
            "grand_total_fee": person_df['total_eligible_payment'].sum()
        },
        "filename": f"{safe_name}_Performance_Report.pdf"
    }

def get_invoice_context(df, name, task_period):
    """Prepares context for the Invoice Template."""
    person_df = df[df['name'] == name]
    # Pulls S1-Assignee for the ID format: INV/USERNAME/JAN26
    username = str(person_df['username'].iloc[0]).upper()
    total_payable = person_df['total_eligible_payment'].sum()
    safe_name = str(name).upper().replace(' ', '_')
    
    current_month_year = datetime.now().strftime("%b%y").upper() 
    
    return {
        "ctx": {
            "invoice_id": f"INV/{username}/{current_month_year}",
            "report_date": datetime.now().strftime("%d-%b-%Y"),
            "task_period": task_period,
            "name": safe_name,
            "grand_total_fee": total_payable
        },
        "filename": f"{safe_name}_Invoice_{current_month_year}.pdf"
    }