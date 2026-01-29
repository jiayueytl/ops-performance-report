S2_PERFORMANCE_REPORT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 1.5cm; /* Standard professional margin */
        }
        body {
            font-family: 'Aptos', 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
            font-size: 10pt; /* Reduced from 12pt for better fit */
            color: #333;
            line-height: 1.2;
            margin: 0;
            padding: 0;
        }
        .header-title { 
            font-weight: bold; 
            font-size: 11pt; 
            margin-bottom: 15px; /* Reduced from 30px */
            text-align: left;
        }
        
        table {
            width: 100%;
            border-collapse: collapse; 
            margin-bottom: 12px;
        }
        
        th, td {
            border: 1px solid #000;
            padding: 6px; /* Tightened padding */
        }

        th {
            background-color: #f2f2f2;
            font-weight: bold;
            text-align: center;
            font-size: 9pt;
        }

        .summary-title {
            font-weight: bold;
            margin-top: 15px; /* Reduced from 50px */
            margin-bottom: 8px;
            text-transform: uppercase;
            border-bottom: 1px solid #333;
            display: inline-block;
        }

        .total-row { background-color: #f2f2f2; font-weight: bold; }
        
        .footer {
            margin-top: 20px;
            font-size: 9pt;
        }
        
        .rate-box {
            margin: 10px 0;
            padding: 5px;
            
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="header-title">
        YTL AI LABS DATA ANNOTATION PROJECT<br>
        REVIEWER PERFORMANCE & PAYMENT SUMMARY
    </div>

    <table>
        <tr><td width="20%" style="background-color: #f9f9f9; font-weight: bold;">Report ID</td><td>{{ report_id }}</td></tr>
        <tr><td style="background-color: #f9f9f9; font-weight: bold;">Date of Report</td><td>{{ report_date }}</td></tr>
        <tr><td style="background-color: #f9f9f9; font-weight: bold;">Task Period</td><td>{{ task_period }}</td></tr>
        <tr><td style="background-color: #f9f9f9; font-weight: bold;">Reviewer</td><td>{{ name }}</td></tr>
    </table>

    <div class="rate-box">
        <b>Package Rate:</b> RM100 (Full Day) | RM50 (Half Day)
    </div>
    <br>
    <div class="summary-title">Summary of Quality Assurance Review</div>
    
    <table>
        <thead>
            <tr>
                <th width="30%">Project Name</th>
                <th>Date</th>
                <th>Total Completed</th>
                <th>Accuracy Rate</th>
                <th>Payment Tier</th>
                <th>Total Payable (RM)</th>
            </tr>
        </thead>
        <tbody>
            {% for row in projects %}
            <tr>
                <td>{{ row['project_name'] }}</td>
                <td style="text-align: center;">{{ row['date'] }}</td>
                <td style="text-align: center;">{{ row['total_completed'] }}</td>
                <td style="text-align: center;">{{ "%.2f"|format(row['accuracy_rate']|float) }}%</td>
                <td style="text-align: center;">{{ row['payment_tier'] }}</td>
                <td style="text-align: right;">{{ "%.2f"|format(row['total_eligible_payment']|float) }}</td>
            </tr>
            {% endfor %}
            <tr class="total-row">
                <td colspan="5" style="text-align: right;">Grand Total (RM)</td>
                <td style="text-align: right;">{{ "%.2f"|format(grand_total_fee|float) }}</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        <p>I acknowledge and agree with the reviewed performance and the corresponding fee stated above.</p>
        <p>Signed by,</p>
        <p>Full name: _______________________________<br>
           NRIC no. : _______________________________</p>
    </div>
</body>
</html>
"""