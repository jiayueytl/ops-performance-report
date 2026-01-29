INVOICE_TEMPLATE_TASKREVIEW = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Aptos', 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 12pt; line-height: 1.6; }
        .invoice-header { font-size: 26pt; font-weight: bold; margin-bottom: 30px; }
        .info-table { width: 100%; border: none; margin-bottom: 40px; }
        .info-table td { border: none; vertical-align: top; }
        
        .main-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
        .main-table th, .main-table td { border: 1px solid #000; padding: 10px; text-align: left; }
        
        .bank-details { margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }
        .thank-you { margin-top: 50px; text-align: center; font-weight: bold; }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
            text-align: center;
            font-size: 12pt;
        }
    </style>
</head>
<body>
    <div class="invoice-header">INVOICE</div>

    <table class="info-table">
        <tr>
            <td width="70%">
                XXX<br>
                XXX<br>
                XXX<br>
                XXX@XXX.XXX<br>
                +60 XX-XX
            </td>
            <td width="30%" style="text-align: left;">
                <b>Invoice No:</b> {{ invoice_id }}<br>
                <b>Date:</b> {{ report_date }}<br>
                <b>To:</b><br>
                YTL AI Labs Sdn. Bhd.<br>
                15th Floor, Menara YTL,<br>
                205 Jalan Bukit Bintang,<br>
                55100 Kuala Lumpur.
            </td>
        </tr>
    </table>

    <table class="main-table">
        <thead>
            <tr>
                <th>Task Type</th>
                <th>Project Period</th>
                <th>Amount (RM)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Review and Rewriting</td>
                <td>{{ task_period }}</td>
                <td>{{ "%.2f"|format(grand_total_fee|float) }}</td>
            </tr>
        </tbody>
    </table>

    <div class="bank-details">
        <p><strong>Please make all checks payable to:</strong></p>
        <p>Full Name of Account Holder: (Your Full Name of Account Holder)</p>
        <p>Bank name: (Your Bank name)</p>
        <p>Bank account number: (Your Bank account number)</p>
    </div>

    <div class="thank-you">Thank you!</div>
</body>
</html>
"""