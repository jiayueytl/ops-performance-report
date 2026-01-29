S1_PERFORMANCE_REPORT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Aptos', 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
            font-size: 12pt;
            color: #333;
            line-height: 1.4;
        }
        .header-title { 
            font-weight: bold; 
            font-size: 12pt; 
            margin-bottom: 30px; 
        }
        
        table {
            width: 100%;
            border-collapse: collapse; 
            margin-bottom: 20px;
        }
        
        th, td {
            border: 1px solid #000;
            padding: 8px;
        }

        th {
            background-color: #f2f2f2;
            font-weight: bold;
            text-align: center;
            font-size: 12pt;
        }

        .summary-title {
            font-weight: bold;
            margin-top: 50px; /* Large space above table */
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .total-row { background-color: #f2f2f2; font-weight: bold; }
        .footer { margin-top: 60px; }
        .sig-line { margin-top: 60px; border-top: 1px solid #000; width: 250px; }
    </style>

    <body>
        <div class="header-title">
            YTL AI LABS DATA ANNOTATION PROJECT<br>
            ANNOTATION TASK PERFORMANCE REPORT
        </div>

        <table>
            <tr><td width="25%" style="background-color: #f9f9f9; font-weight: bold;">Report ID</td><td>{{ report_id }}</td></tr>
            <tr><td style="background-color: #f9f9f9; font-weight: bold;">Date of Report</td><td>{{ report_date }}</td></tr>
            <tr><td style="background-color: #f9f9f9; font-weight: bold;">Task Period</td><td>{{ task_period }}</td></tr>
            <tr><td style="background-color: #f9f9f9; font-weight: bold;">Annotator</td><td>{{ name }}</td></tr>
        </table>

        <p><b>Package Rate: RM0.80 (PER APPROVED IMAGE)</b></p>

        <div class="summary-title">Summary of Quality Assurance Review</div>
        
        <table>
            <thead>
                <tr>
                    <th rowspan="2" style="width: 25%;">Project Name</th>
                    <th rowspan="2" style="width: 15%;">Total Submitted<br>(Uncorrupted)</th>
                    <th colspan="2" style="width: 30%;">Total Valid Format</th>
                    <th rowspan="2" style="width: 15%;">Total Invalid<br>Format</th>
                    <th rowspan="2" style="width: 15%;">Fee (RM)</th>
                </tr>
                <tr>
                    <th>Total Pass</th>
                    <th>Total Fail</th>
                </tr>
            </thead>
            <tbody>
                {% for row in projects %}
                <tr>
                    <td>{{ row['project_name'] }}</td>
                    <td style="text-align: center;">{{ row['Sum of total_submitted_uncorrupted'] }}</td>
                    <td style="text-align: center;">{{ row['Sum of total_valid_pass_count'] }}</td>
                    <td style="text-align: center;">{{ row['Sum of total_valid_fail_count'] }}</td>
                    <td style="text-align: center;">{{ row['Sum of total_invalid_format'] }}</td>
                    <td style="text-align: right;">{{ "%.2f"|format(row['total_eligible_payment']|float) }}</td>
                </tr>
                {% endfor %}
                <tr class="total-row">
                    <td colspan="5" style="text-align: right;">Total Fee (RM)</td>
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