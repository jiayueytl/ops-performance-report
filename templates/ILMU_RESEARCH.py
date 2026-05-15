ILMU_RESEARCH = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  
  /* PRIORITY FONT SETTINGS */
  body { 
    font-family: 'Aptos', 'Segoe UI', 'Helvetica', 'Arial', sans-serif; 
    font-size: 11pt; 
    line-height: 1.4;
    color: #000;
    background: #fff;
    padding: 15px 20px;
  }

  h1.title {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 20px;
    text-decoration: underline;
  }

  .header-grid { display: table; width: 100%; margin-bottom: 35px; line-height: 1.4; }
  .header-grid .col { display: table-cell; width: 50%; vertical-align: top; }

  .align-table { border-collapse: collapse; }
  .align-table td { vertical-align: top; padding-right: 5px; padding-bottom: 2px; }
  .label { font-weight: bold; }

  .contact-row { display: table; width: 100%; margin-bottom: 10px; line-height: 1.4; }
  .contact-row .col { display: table-cell; width: 50%; vertical-align: top; }

  .meta-table { border-collapse: collapse; }
  .meta-table td { padding: 3px 4px; vertical-align: top; padding-left: 0; }
  .meta-table td:first-child { white-space: nowrap; }
  .meta-table td:nth-child(2) { width: 8px; text-align: center; padding: 0; }

  .items-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
  .items-table thead tr { background-color: #f2f2f2; color: #000; }
  .items-table thead th {
    padding: 8px 10px;
    text-align: center;
    font-weight: bold;
    font-size: 11pt;
    border: 1px solid #000;
  }
  .items-table tbody td {
    padding: 8px 10px;
    border: 1px solid #000;
    text-align: center;
    vertical-align: top;
  }
  .items-table tbody td:nth-child(2) { text-align: left; }

  .items-table tfoot tr td { border: 1px solid #000; padding: 6px 10px; }
  .items-table tfoot .spacer { border: none; }
  .items-table tfoot .lbl   { text-align: right; font-weight: bold; white-space: nowrap; }
  .items-table tfoot .val { text-align: right; }
  .items-table tfoot tr:last-child .lbl,
  .items-table tfoot tr:last-child .val { font-weight: bold; }

  .terms { margin-top: 10px; font-size: 10pt; line-height: 1.4; }
  .terms h3 { font-size: 11pt; margin-top: 10px; margin-bottom: 4px; }
  .terms p  { margin-bottom: 6px; }
  .terms ul { padding-left: 0; list-style: none; }
  .terms ul li { margin-bottom: 4px; }
  .terms ul li::before { content: "• "; }
  .terms .bold { font-weight: bold; }

  /* ADDITIONAL PRIORITY STYLES */
  .invoice-header { font-size: 24pt; font-weight: bold; margin-bottom: 20px; }
  .info-table { width: 100%; border: none; margin-bottom: 20px; }
  .info-table td { border: none; vertical-align: top; }
  .main-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
  .main-table th, .main-table td { border: 1px solid #000; padding: 8px; text-align: left; }
  .bank-details { margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px; }
  .thank-you { margin-top: 30px; text-align: center; font-weight: bold; }
  th {
      background-color: #f2f2f2;
      font-weight: bold;
      text-align: center;
      font-size: 11pt;
  }
</style>
</head>
<body>

<h1 class="title">QUOTATION</h1>

<div class="header-grid">
  <div class="col">
    <table class="align-table">
        <tr>
            <td class="label">To</td>
            <td class="label">:</td>
            <td>
                <span class="label">YTL AI LABS SDN BHD</span>
                &nbsp;<span style="font-size:9.5px;">(Formerly Known as FrogAsia Sdn Bhd)</span><br>
                Company No: 20110104050519 (968641-K)<br>
                15th Floor, Menara YTL<br>
                205 Jalan Bukit Bintang<br>
                55100 Kuala Lumpur
            </td>
        </tr>
    </table>
  </div>
  <div class="col">
      <table class="align-table">
        <tr>
            <td class="label">From</td>
            <td class="label">:</td>
            <td>
                <span class="label">{{ name }}</span><br>
                {% if address and address not in ('', 'XXX') %}{{ address }}{% endif %}
            </td>
        </tr>
        {% if phone_number and phone_number not in ('', '601X-XXXX XXXX') %}
        <tr>
            <td class="label">Tel</td>
            <td class="label">:</td>
            <td>{{ phone_number }}</td>
        </tr>
        {% endif %}
    </table>
  </div>
</div>

<div class="contact-row">
  <div class="col">
    <table class="align-table">
        <tr>
            <td class="label" style="font-weight: bold;">Att</td>
            <td class="label" style="font-weight: bold;">:</td>
            <td style="font-weight: bold;">Yeong Keat Mei</td>
        </tr>
        <tr>
            <td class="label" style="font-weight: bold;">Tel</td>
            <td class="label" style="font-weight: bold;">:</td>
            <td>018 799 7979</td>
        </tr>
        <tr>
            <td class="label" style="font-weight: bold;">Email</td>
            <td class="label" style="font-weight: bold;">:</td>
            <td><span style="color:#00f;">team.data@ytlailabs.com</span></td>
        </tr>
    </table>
  </div>
  <div class="col" style="padding-left: 0;">
    <table class="meta-table">
      <tr>
        <td style="font-weight: bold;">Quotation Number</td><td>:</td>
        <td>{{ name }}/46124</td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Quotation Date</td><td>:</td>
        <td>{{ report_date }}</td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Quotation Validity</td><td>:</td>
        <td>60 Days</td>
      </tr>
    </table>
  </div>
</div>

<table class="items-table">
  <thead>
    <tr>
      <th style="width:36px;">No</th>
      <th>Item Description</th>
      <th style="width:75px;">Quantity</th>
      <th style="width:50px;">Unit</th>
      <th style="width:85px; text-align:right;">Unit Price<br>(RM)</th>
      <th style="width:85px; text-align:right;">Total<br>(RM)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Prompt and Responses evaluation</td>
      <td>1</td>
      <td>{{ quantity }}</td>
      <td style="text-align: right;">2.00</td>
      <td style="text-align: right;">{{ "%.2f"|format(grand_total_fee|float) }}</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="4" class="spacer" style="border:none;"></td>
      <td class="lbl">Subtotal :</td>
      <td class="val">{{ "%.2f"|format(grand_total_fee|float) }}</td>
    </tr>
    <tr>
      <td colspan="4" class="spacer" style="border:none;"></td>
      <td class="lbl">Total :</td>
      <td class="val">{{ "%.2f"|format(grand_total_fee|float) }}</td>
    </tr>
  </tfoot>
</table>
<div class="terms">
  <h3>Terms &amp; Condition</h3>

  <h3>1. Pricing and Taxes</h3>
  <p>All prices are quoted above are exclusive of applicable tax. Any applicable taxes will be added to the invoice at the prevailing rate at the time of billing.</p>

  <h3>2. Scope and Variations</h3>
  <p>This quotation covers only the specific scope of annotation work stated above. Any requests of extra services will be quoted and charged separately as a project variation. Service will commence upon confirmation of order.</p>

  <h3>3. Invoicing and Payment</h3>
  <ul>
    <li><span class="bold">Billing:</span> &nbsp; A single invoice will be issued upon successful project completion.</li>
    <li><span class="bold">Payment Terms:</span> &nbsp; Payment is due within 30 days from the date of invoice.</li>
  </ul>

  <h3>4. Confidentiality and Intellectual Property</h3>
  <ul>
    <li><span class="bold">Confidentiality:</span> &nbsp; Both parties agree to maintain strict confidentiality regarding all information exchanged. Any sensitive information concerning YTL AI Labs or its operations must be protected and used solely to fulfill the agreed work duties. Such information shall not be disclosed to third parties unless required by law or authorized in writing by YTL AI Labs.</li>
    <li><span class="bold">Intellectual Property:</span> &nbsp; All Intellectual Property conceived, originated, or developed specifically for this Project shall vest exclusively in YTL AI Labs as the sole beneficial owner.</li>
  </ul>
</div>

<table style="width:100%; margin-top:25px; font-size:11pt; font-family: 'Aptos', 'Segoe UI', 'Helvetica', 'Arial', sans-serif;">
  <tr>
    <td style="width:50%; text-align: left; padding-left: 5%;">
      <div style="width: 80%;">
        <div style="margin-bottom: 120px; font-weight: bold;">Issued by,</div>
        <div style="border-top: 1px solid #000;"></div>
        <div style="margin-top: 8px; font-weight: bold;">{{ name }}</div>
      </div>
    </td>
    <td style="width:50%; text-align: left; padding-left: 5%;">
      <div style="width: 80%;">
        <div style="margin-bottom: 120px; font-weight: bold;">Accepted by,</div>
        <div style="border-top: 1px solid #000;"></div>
        <div style="margin-top: 8px; font-weight: bold;">YTL AI LABS SDN BHD</div>
      </div>
    </td>
  </tr>
</table>

</body>
</html>
"""