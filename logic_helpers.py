import pandas as pd
from datetime import datetime

def process_data(df):
    """Cleans columns and identifies unique annotators."""
    # Strip whitespace and BOM characters
    df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=False)

    # Normalize all columns to lowercase + underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False).str.replace(r'[().]', '', regex=True)

    # Rename to internal names
    df = df.rename(columns={
        'completed_task': 'total_completed',
        'completion_percentage': 'completion_percentage',
        'payment_rm80_for_full_package': 'total_eligible_payment'
    })

    if 'name' not in df.columns:
        raise ValueError(f"❌ 'name' column not found. Available columns: {df.columns.tolist()}")

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

    return {
        "ctx": {
            "report_id": f"{safe_name.replace(' ', '_')}_Performance_{datetime.now().strftime('%Y%m%d')}",
            "report_date": datetime.now().strftime("%d-%b-%Y"),
            "task_period": task_period,
            "name": safe_name,
            "projects": person_df.to_dict('records'),
            "grand_total_fee": person_df['total_eligible_payment'].sum()
        },
        "filename": f"{safe_name}_Performance_Report_{current_month_year}.pdf"
    }


from datetime import datetime
import pandas as pd

def get_invoice_context(df, name, ui_task_period):
    """Prepares context for the Invoice Template."""
    now = datetime.now()
    current_month_year = now.strftime("%b%y").upper()

    person_df = df[df['name'] == name].copy()
    
    if person_df.empty:
        return {"error": "User not found"}

    # Helper to get first value if column exists and isn't null, else return default
    def get_val(col_name, default):
        if col_name in person_df.columns:
            val = person_df[col_name].iloc[0]
            return val if pd.notnull(val) and val != "" else default
        return default

    # 1. Determine Username
    username = str(get_val('username', name)).upper()

    # 2. Invoice ID Logic: Use existing or Auto-generate
    invoice_id = get_val('invoice_id', f"INV/{username}/{current_month_year}")

    # 3. Task Period Logic
    task_period = get_val('task_period', ui_task_period)

    # 4. Project Name Logic
    project_name = get_val('project_name', "Task Review and Rewrite")
    task_type = get_val('task_type', "Task Review and Rewrite")

    # 5. Quotation Number
    quotation_number = get_val('quotation_number', "")

    # 6. Calculations and Formatting
    total_payable = person_df['total_eligible_payment'].sum() if 'total_eligible_payment' in person_df.columns else 0
    safe_name = get_safe_name(name)
    
    return {
        "ctx": {
            "email": get_val('email', 'xxx@xxx.com'),
            "phone_number": get_val('phone_number', '601X-XXXX XXXX'),
            "address_1": get_val('address_1', 'XXX,'),
            "address_2": get_val('address_2', 'XXX,'),
            "address_3": get_val('address_3', 'XXX,'),
            "invoice_id": invoice_id,
            "quotation_number": quotation_number,
            "project_name": project_name,
            "task_type": task_type,
            "report_date": now.strftime("%d-%b-%Y"),
            "task_period": task_period,
            "name": safe_name,
            "grand_total_fee": total_payable,
            "bank_acc_holder": get_val('bank_acc_holder', '(Your Full Name of Account Holder)'),
            "bank_name": get_val('bank_name', '(Your Bank name)'),
            "bank_acc_num": get_val('bank_acc_num', '(Your Bank account number)')
        },
        
        "filename": f"{safe_name}_Invoice_{current_month_year}.pdf"
    }