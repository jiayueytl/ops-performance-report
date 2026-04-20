import pandas as pd
from datetime import datetime

def process_data(df):
    """Cleans columns and identifies unique annotators."""
    df.columns = df.columns.str.strip()

    # Fill empty numeric cells with 0 to prevent float conversion
    cols_to_fix = ['PASS', 'FAIL', 'Grand Total', 'Requested volume']
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Map Grand Total to the necessary template keys
    if 'Grand Total' in df.columns:
        df['Sum of total_invalid_format'] = df['Grand Total']
        df['Sum of grand_total'] = df['Grand Total']

    # Rename all CSV columns to match template field names
    df = df.rename(columns={
        'Image Collectors':      'name',
        'Total Eligible Amount': 'total_eligible_payment',
        'Requested volume':      'Sum of total_submitted_uncorrupted',
        'PASS':                  'Sum of total_valid_pass_count',
        'FAIL':                  'Sum of total_valid_fail_count',
        'Passing rate':          'passing_rate',
    })

    # Ensure Invalid Format (Grand Total) exists
    if 'Sum of total_invalid_format' not in df.columns:
        df['Sum of total_invalid_format'] = 0

    # Inject fixed project name
    df['project_name'] = 'KuihLapis 2.0(Image Collection)'

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
    """Prepares context for the Invoice templates."""
    person_df = df[df['name'] == name]

    username     = str(name).upper() if not person_df.empty else "UNKNOWN"
    total_payable = person_df['total_eligible_payment'].sum() if not person_df.empty and 'total_eligible_payment' in person_df.columns else 0

    safe_name          = get_safe_name(name)
    current_month_year = datetime.now().strftime("%b%y").upper()

    def _get(col, cast=str):
        if not person_df.empty and col in person_df.columns:
            val = person_df[col].iloc[0]
            try:
                return cast(val)
            except Exception:
                return val
        return 0 if cast in (int, float) else "—"

    return {
        "ctx": {
            "invoice_id":        f"INV/{username}/{current_month_year}",
            "report_date":       datetime.now().strftime("%d-%b-%Y"),
            "task_period":       task_period,
            "name":              safe_name,
            "grand_total_fee":   total_payable,
            "requested_volume":  _get('Sum of total_submitted_uncorrupted', int),
            "pass_count":        _get('Sum of total_valid_pass_count', int),
            "fail_count":        _get('Sum of total_valid_fail_count', int),
            "invalid_format":    _get('Sum of total_invalid_format', int),
            "grand_total_count": _get('Sum of grand_total', int),
            "passing_rate":      _get('passing_rate', str),
        },
        "filename": f"{safe_name}_Invoice_{current_month_year}.pdf"
    }