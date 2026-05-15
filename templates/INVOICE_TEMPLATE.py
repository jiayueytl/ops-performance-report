INVOICE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: Arial, sans-serif;
    font-size: 11px;
    color: #000;
    background: #fff;
    padding: 30px 40px;
  }

  h1.title {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 20px;
    text-decoration: underline;
  }

  /* ── Header block ── */
  .header-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
  }
  .header-grid .block { line-height: 1.7; }
  .header-grid .block .label { font-weight: bold; }

  /* ── Att / Tel / Email row ── */
  .contact-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
    line-height: 1.8;
  }

  /* ── Quotation meta (right side of contact row) ── */
  .meta-table { width: 100%; border-collapse: collapse; }
  .meta-table td { padding: 1px 4px; vertical-align: top; }
  .meta-table td:first-child { font-weight: normal; white-space: nowrap; }
  .meta-table td:nth-child(2) { text-align: center; width: 10px; }

  /* ── Line-items table ── */
  .items-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 0;
  }
  .items-table thead tr {
    background-color: #222;
    color: #fff;
  }
  .items-table thead th {
    padding: 6px 8px;
    text-align: center;
    font-weight: bold;
    font-size: 11px;
  }
  .items-table tbody tr td {
    padding: 6px 8px;
    border: 1px solid #ccc;
    text-align: center;
    vertical-align: top;
  }
  .items-table tbody tr td:nth-child(2) { text-align: left; }

  /* Empty rows to pad the table like the original */
  .items-table tbody tr.empty td { height: 22px; }

  /* ── Totals block ── */
  .totals-wrap {
    display: flex;
    justify-content: flex-end;
    border-top: none;
  }
  .totals-table {
    width: 260px;
    border-collapse: collapse;
    border: 1px solid #ccc;
  }
  .totals-table td {
    padding: 4px 8px;
    border: 1px solid #ccc;
    font-size: 11px;
  }
  .totals-table td:first-child { text-align: right; font-weight: bold; }
  .totals-table td:last-child  { text-align: right; }
  .totals-table tr:last-child td { font-weight: bold; }

  /* ── Terms ── */
  .terms { margin-top: 20px; font-size: 10.5px; line-height: 1.6; }
  .terms h3 { font-size: 11px; margin-top: 10px; margin-bottom: 2px; }
  .terms p, .terms li { margin-bottom: 2px; }
  .terms ul { padding-left: 0; list-style: none; }
  .terms ul li::before { content: "• "; }
  .terms .bold { font-weight: bold; }

  /* ── Signatures ── */
  .signatures {
    display: grid;
    grid-template-columns: 1fr 1fr;
    margin-top: 40px;
    text-align: center;
    font-size: 11px;
  }
</style>
</head>
<body>

<h1 class="title">QUOTATION</h1>

<!-- ── TOP HEADER ── -->
<div class="header-grid">
  <!-- LEFT: To -->
  <div class="block">
    <span class="label">To &nbsp;: &nbsp; YTL AI LABS SDN BHD</span>
    &nbsp;&nbsp;<span style="font-size:9.5px;">(Formerly Known as FrogAsia Sdn Bhd)</span><br>
    Company No: 201101004050519 (968641-K)<br>
    15th Floor, Menara YTL<br>
    205 Jalan Bukit Bintang<br>
    55100 Kuala Lumpur
  </div>

  <!-- RIGHT: From -->
  <div class="block">
    <span class="label">From: &nbsp; {{ annotator }}</span><br>
    {{ address_line1 | default('') }}<br>
    {{ address_line2 | default('') }}<br>
    {{ address_line3 | default('') }}<br>
    Tel: &nbsp; {{ tel | default('') }}
  </div>
</div>

<!-- ── ATT / QUOTATION META ── -->
<div class="contact-row">
  <!-- LEFT: Att / Tel / Email -->
  <div>
    Att &nbsp;&nbsp;: &nbsp; Yeong Keat Mei<br>
    Tel &nbsp;&nbsp;: &nbsp; 018 799 7979<br>
    Email : &nbsp; <span style="color:#00f;">team.data@ytlailabs.com</span>
  </div>

  <!-- RIGHT: Quotation Number / Date / Validity -->
  <div>
    <table class="meta-table">
      <tr>
        <td>Quotation Number</td><td>:</td>
        <td>{{ quotation_number | default('QUO-' ~ annotator | upper | replace(' ','') ~ '/' ~ task_period | replace(' ','')) }}</td>
      </tr>
      <tr>
        <td>Quotation Date</td><td>:</td>
        <td>{{ task_period }}</td>
      </tr>
      <tr>
        <td>Quotation Validity</td><td>:</td>
        <td>60 Days</td>
      </tr>
    </table>
  </div>
</div>

<!-- ── LINE ITEMS TABLE ── -->
<table class="items-table">
  <thead>
    <tr>
      <th style="width:40px;">No</th>
      <th>Item Description</th>
      <th style="width:80px;">Quantity</th>
      <th style="width:50px;">Unit</th>
      <th style="width:90px;">Unit Price<br>(RM)</th>
      <th style="width:90px;">Total<br>(RM)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>{{ task_description | default('Data Annotation Task') }}</td>
      <td>{{ quantity }}</td>
      <td>Tasks</td>
      <td>{{ "%.2f"|format(unit_price) }}</td>
      <td>{{ "%.2f"|format(total_paid) }}</td>
    </tr>
    <!-- Empty padding rows -->
    <tr class="empty"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr class="empty"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr class="empty"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  </tbody>
</table>

<!-- ── TOTALS ── -->
<div class="totals-wrap">
  <table class="totals-table">
    <tr>
      <td>Subtotal :</td>
      <td>{{ "%.2f"|format(total_paid) }}</td>
    </tr>
    <tr>
      <td>Total :</td>
      <td>{{ "%.2f"|format(total_paid) }}</td>
    </tr>
  </table>
</div>

<!-- ── TERMS & CONDITIONS ── -->
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
    <li>
      <span class="bold">Confidentiality:</span> &nbsp; Both parties agree to maintain strict confidentiality regarding all information exchanged. Any sensitive information
      concerning YTL AI Labs or its operations must be protected and used solely to fulfill the agreed work duties. Such information shall not
      be disclosed to third parties unless required by law or authorized in writing by YTL AI Labs.
    </li>
    <li>
      <span class="bold">Intellectual Property:</span> &nbsp; All Intellectual Property conceived, originated, or developed specifically for this Project shall vest exclusively
      in YTL AI Labs as the sole beneficial owner.
    </li>
  </ul>
</div>

<!-- ── SIGNATURES ── -->
<div class="signatures">
  <div>Issued by,</div>
  <div>Accepted by,</div>
</div>

</body>
</html>
"""