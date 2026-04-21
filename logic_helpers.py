import pandas as pd
from datetime import datetime

def process_data(df):
    """Cleans columns and identifies unique annotators."""
    df.columns = df.columns.str.strip()

    # Rename new CSV columns to match internal logic variables
    df = df.rename(columns={
        'Annotators': 'name',
        'amount': 'total_eligible_payment'
    })

    # Ensure payment is a numeric value
    if 'total_eligible_payment' in df.columns:
        df['total_eligible_payment'] = pd.to_numeric(df['total_eligible_payment'], errors='coerce').fillna(0.0)

    return df, df['name'].dropna().unique()

def get_safe_name(name):
    safe_name = str(name).upper()
    safe_name = safe_name.replace('/', '')
    return safe_name

def get_performance_context(df, name, task_period):
    """Prepares context for the Performance Report (S1/S2)."""
    person_df = df[df['name'] == name]

    sortable_keys = ['project_name', 'date']
    if set(sortable_keys).issubset(person_df.columns):
        person_df = person_df.sort_values(by=sortable_keys, ascending=[True, True])

    if 'total_completed' in person_df.columns:
        person_df = person_df[person_df['total_completed'] > 0]

    safe_name = get_safe_name(name)
    current_month_year = datetime.now().strftime("%b%y").upper()

    return {
        "ctx": {
            "report_id":       f"{safe_name.replace(' ', '_')}_Performance_{datetime.now().strftime('%Y%m%d')}",
            "report_date":     datetime.now().strftime("%d-%b-%Y"),
            "task_period":     task_period,
            "name":            safe_name,
            "projects":        person_df.to_dict('records'),
            "grand_total_fee": person_df['total_eligible_payment'].sum() if 'total_eligible_payment' in person_df.columns else 0,
        },
        "filename": f"{safe_name}_Performance_Report_{current_month_year}.pdf"
    }

def get_invoice_context(df, name, task_period):
    """Prepares context for the Invoice templates, grouping multiple tasks."""
    person_df = df[df['name'] == name]

    username     = str(name).upper() if not person_df.empty else "UNKNOWN"
    total_payable = person_df['total_eligible_payment'].sum() if not person_df.empty and 'total_eligible_payment' in person_df.columns else 0

    safe_name          = get_safe_name(name)
    current_month_year = datetime.now().strftime("%b%y").upper()

    # Build a list of tasks for the Jinja loop
    tasks = []
    for _, row in person_df.iterrows():
        tasks.append({
            "project": row.get("project", "Unknown Project"),
            "period": row.get("period", task_period),
            "amount": row.get("total_eligible_payment", 0.0)
        })

    return {
        "ctx": {
            "invoice_id":        f"INV/{username}/{current_month_year}",
            "report_date":       datetime.now().strftime("%d-%b-%Y"),
            "name":              safe_name,
            "tasks":             tasks,             # NEW: Passes the grouped rows
            "grand_total_fee":   total_payable      # NEW: Passes the sum
        },
        "filename": f"{safe_name}_Invoice_{current_month_year}.pdf"
    }