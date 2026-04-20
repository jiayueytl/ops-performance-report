import pandas as pd
from datetime import datetime

def process_data(df):
    """Cleans columns and identifies unique annotators."""
    df.columns = df.columns.str.strip()
    
    # Map the new CSV 'Annotators' column to 'name' for the logic to work
    if 'Annotators' in df.columns:
        df = df.rename(columns={'Annotators': 'name'})
        
    # Map 'Total Eligible Amount' to 'total_eligible_payment'
    if 'Total Eligible Amount' in df.columns:
        df = df.rename(columns={'Total Eligible Amount': 'total_eligible_payment'})

    # Inject fixed project name since it's not in the new CSV
    if 'project_name' not in df.columns:
        df['project_name'] = 'KuihLapis 2.0(Image Editing And Transcription)'

    # Remove the summary "Grand Total" row from the bottom of the CSV
    df = df[df['name'] != 'Grand Total']
    df = df.dropna(subset=['name'])

    return df, df['name'].unique()

def get_safe_name(name):
    safe_name = str(name).upper()
    safe_name = safe_name.replace('/','')
    return safe_name

def get_performance_context(df, name, task_period):
    """Prepares context for the Performance Report."""
    person_df = df[df['name'] == name]

    sortable_keys = ['project_name', 'date']

    if set(sortable_keys).issubset(person_df.columns):
        person_df = person_df.sort_values(by=sortable_keys, ascending=[True, True])
        
    person_df = person_df[person_df['total_completed']>0] if 'total_completed' in person_df.columns else person_df
    
    safe_name = get_safe_name(name)
    current_month_year = datetime.now().strftime("%b%y").upper() 
    
    # Grab the dynamic payment rate for this specific annotator
    payment_rate = person_df['Payment Rate'].iloc[0] if not person_df.empty and 'Payment Rate' in person_df.columns else "0.00"

    return {
        "ctx": {
            "report_id": f"{safe_name.replace(' ', '_')}_Performance_{datetime.now().strftime('%Y%m%d')}",
            "report_date": datetime.now().strftime("%d-%b-%Y"),
            "task_period": task_period,
            "name": safe_name,
            "payment_rate": payment_rate,
            "projects": person_df.to_dict('records'),
            "grand_total_fee": person_df['total_eligible_payment'].sum() if 'total_eligible_payment' in person_df.columns else 0
        },
        "filename": f"{safe_name}_Performance_Report_{current_month_year}.pdf"
    }

def get_invoice_context(df, name, task_period):
    """Prepares context for the Invoice Template."""
    person_df = df[df['name'] == name]
    # Pulls S1-Assignee for the ID format: INV/USERNAME/JAN26
    # Check if any matching rows exist
    if not person_df.empty:
        # Revert to 'name' if username is not in the CSV
        username = str(person_df['username'].iloc[0]).upper() if 'username' in person_df.columns else str(name).upper()
    else:
        # Fallback if the person isn't found
        username = "UNKNOWN"
        
    total_payable = person_df['total_eligible_payment'].sum() if 'total_eligible_payment' in person_df.columns else 0
    safe_name = get_safe_name(name)
    
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