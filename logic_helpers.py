import pandas as pd
from datetime import datetime

def process_data(df):
    """Cleans columns and identifies unique annotators."""
    df.columns = df.columns.str.strip()
    # FIX: your CSV uses 'annotator', not 'name'
    if 'annotator' in df.columns and 'name' not in df.columns:
        df['name'] = df['annotator']
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

    # FIX: Calculate grand total safely by checking both possible column names
    if 'Total_paid' in person_df.columns:
        grand_total = float(person_df['Total_paid'].sum())
    elif 'total_eligible_payment' in person_df.columns:
        grand_total = float(person_df['total_eligible_payment'].sum())
    else:
        grand_total = 0.0

    return {
        "ctx": {
            "report_id": f"{safe_name.replace(' ', '_')}_Performance_{datetime.now().strftime('%Y%m%d')}",
            "report_date": datetime.now().strftime("%d-%b-%Y"),
            "task_period": task_period,
            "name": safe_name,
            "projects": person_df.to_dict('records'),
            "grand_total_fee": grand_total,
            "unit_price": 2.00,
            "quantity": int(round(grand_total / 2.00)) if grand_total else 0
        },
        "filename": f"{safe_name}_Performance_Report_{current_month_year}.pdf"
    }

def get_invoice_context(df, name, ui_task_period):
    """Prepares context for the Invoice / Quotation Template."""
    now = datetime.now()
    current_month_year = now.strftime("%b%y").upper()

    person_df = df[df['name'] == name].copy()
    safe_name = get_safe_name(name)
    UNIT_PRICE = 2.00
    
    # FIX: Even if data is empty, we must pass unit_price so Jinja doesn't crash
    if person_df.empty:
        return {
            "ctx": {
                "name": safe_name,
                "unit_price": UNIT_PRICE,
                "quantity": 0,
                "grand_total_fee": 0.0,
                "total_paid": 0.0,
                "report_date": now.strftime("%d-%b-%Y"),
                "task_period": ui_task_period
            }, 
            "filename": f"{safe_name}_Quotation_{current_month_year}.pdf"
        }

    def get_val(col_name, default):
        if col_name in person_df.columns:
            val = person_df[col_name].iloc[0]
            return val if pd.notnull(val) and val != "" else default
        return default

    # Identity
    username = str(get_val('username', name)).upper()

    # Invoice / Quotation IDs
    invoice_id       = get_val('invoice_id', f"INV/{username}/{current_month_year}")
    quotation_number = get_val('quotation_number', f"{username}/46124")

    # Task info
    task_period  = get_val('task_period', ui_task_period)
    project_name = get_val('project_name', "Data Annotation Task")
    task_type    = get_val('task_type', "Data Annotation Task")

    # Payment — uses Total_paid column; falls back to total_eligible_payment
    try:
        if 'Total_paid' in person_df.columns:
            total_payable = float(person_df['Total_paid'].iloc[0] or 0)
        elif 'total_eligible_payment' in person_df.columns:
            total_payable = float(person_df['total_eligible_payment'].sum() or 0)
        else:
            total_payable = 0.0
    except (ValueError, TypeError):
        total_payable = 0.0

    # Quotation line-item breakdown
    quantity   = int(round(total_payable / UNIT_PRICE)) if total_payable else 0

    return {
        "ctx": {
            # Annotator identity
            "name"            : safe_name,
            "email"           : get_val('email', ''),
            "phone_number"    : get_val('tel', ''),
            "address"         : get_val('address', ''),

            # Invoice / quotation meta
            "invoice_id"         : invoice_id,
            "quotation_number"   : quotation_number,
            "report_date"        : "12-May-2026",
            "task_period"        : task_period,
            "current_month_year" : current_month_year,

            # Task details
            "project_name"    : project_name,
            "task_type"       : task_type,
            "task_description": "Prompt and Responses evaluation", 

            # Line-item figures
            "unit_price"      : 2.00,
            "quantity"        : quantity, # <--- FIXED THIS LINE (replaced hardcoded 1)
            "grand_total_fee" : total_payable,   # used by old templates
            "total_paid"      : total_payable,   # used by new quotation template

            # Bank details
            "bank_acc_holder" : get_val('bank_acc_holder', '(Your Full Name of Account Holder)'),
            "bank_name"       : get_val('bank_name', '(Your Bank name)'),
            "bank_acc_num"    : get_val('bank_acc_num', '(Your Bank account number)'),
        },
        "filename": f"{safe_name}_Invoice_{current_month_year}.pdf"
    }