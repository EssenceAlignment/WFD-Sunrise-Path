import React from 'react';

export const MedicalReport = () => {
  return (
    <div className="medical-report">
      <style jsx>{`
        .medical-report {
          font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
          line-height: 1.5;
          color: #000000;
          background: white;
          padding: 20px;
        }

        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          border-bottom: 3px solid #990000;
          padding-bottom: 24px;
          margin-bottom: 32px;
        }

        .logo-section {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .keck-logo {
          width: 60px;
          height: 60px;
          background: #990000;
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          font-size: 28px;
          font-family: 'Georgia', 'Times New Roman', serif;
          border-radius: 4px;
        }

        .hospital-name {
          font-size: 28px;
          font-weight: 500;
          color: #990000;
          letter-spacing: -0.02em;
        }

        .report-date {
          text-align: right;
          font-size: 14px;
          color: #767676;
        }

        .report-date strong {
          font-weight: 600;
          color: #000000;
        }

        .patient-info {
          background: #F5F5F5;
          padding: 32px;
          border-radius: 8px;
          margin-bottom: 32px;
          border: 1px solid #E5E5E5;
        }

        .patient-info h2 {
          margin: 0 0 24px 0;
          color: #990000;
          font-size: 22px;
          font-family: 'Georgia', 'Times New Roman', serif;
          font-weight: normal;
        }

        .info-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 16px;
        }

        .info-item {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .info-label {
          font-weight: 600;
          font-size: 12px;
          color: #767676;
          text-transform: uppercase;
          letter-spacing: 0.08em;
        }

        .info-value {
          font-size: 16px;
          font-weight: 500;
          color: #000000;
        }

        .section {
          margin-bottom: 32px;
        }

        .section-title {
          background: #990000;
          color: white;
          padding: 8px 24px;
          font-size: 18px;
          font-weight: 500;
          margin-bottom: 16px;
          letter-spacing: 0.02em;
        }

        .results-table {
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 15px;
        }

        .results-table th {
          background: #F5F5F5;
          font-weight: 600;
          color: #767676;
          font-size: 14px;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          padding: 8px 16px;
          text-align: left;
          border-bottom: 1px solid #E5E5E5;
        }

        .results-table td {
          padding: 8px 16px;
          border-bottom: 1px solid #E5E5E5;
          font-size: 14px;
        }

        .results-table tr:hover {
          background: #F5F5F5;
        }

        .result-value {
          font-weight: 600;
          color: #000000;
        }

        .abnormal {
          color: #F26178;
          font-weight: 600;
        }

        .flag {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 24px;
          height: 24px;
          font-weight: bold;
          font-size: 12px;
          border-radius: 4px;
          margin-left: 8px;
        }

        .high {
          background: #F26178;
          color: white;
        }

        .low {
          background: #FFCC00;
          color: #000000;
        }

        .clinical-notes {
          background: #FFF2BF;
          border-left: 4px solid #FFCC00;
          padding: 32px;
          margin-top: 32px;
          border-radius: 6px;
        }

        .clinical-notes h3 {
          margin: 0 0 16px 0;
          color: #990000;
          font-size: 18px;
          font-family: 'Georgia', 'Times New Roman', serif;
          font-weight: normal;
        }

        .clinical-notes p {
          margin-bottom: 16px;
          line-height: 1.75;
        }

        .clinical-notes strong {
          font-weight: 600;
          color: #000000;
        }

        .footer {
          margin-top: 64px;
          padding-top: 32px;
          border-top: 2px solid #E5E5E5;
          font-size: 14px;
          color: #767676;
          text-align: center;
          line-height: 1.75;
        }

        @media print {
          body {
            padding: 0;
          }
        }
      `}</style>

      <div className="header">
        <div className="logo-section">
          <div className="keck-logo">K</div>
          <div className="hospital-name">Keck Medicine of USC</div>
        </div>
        <div className="report-date">
          <strong>Report Date:</strong> 24/07/2025<br />
          <strong>Collection Date:</strong> 22/07/2025
        </div>
      </div>

      <div className="patient-info">
        <h2>Patient Information</h2>
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Name</span>
            <span className="info-value">Sayegh, Nuha</span>
          </div>
          <div className="info-item">
            <span className="info-label">MRN</span>
            <span className="info-value">KM-2024-0823</span>
          </div>
          <div className="info-item">
            <span className="info-label">DOB</span>
            <span className="info-value">03/15/1985</span>
          </div>
          <div className="info-item">
            <span className="info-label">Age</span>
            <span className="info-value">39 years</span>
          </div>
          <div className="info-item">
            <span className="info-label">Physician</span>
            <span className="info-value">Dr. Sarah Chen, MD</span>
          </div>
          <div className="info-item">
            <span className="info-label">Diagnosis</span>
            <span className="info-value">Stage IV Ovarian CA w/ Lymphangitic Carcinomatosis</span>
          </div>
        </div>
      </div>

      <div className="section">
        <div className="section-title">Tumor Markers</div>
        <table className="results-table">
          <thead>
            <tr>
              <th>Test</th>
              <th>Result</th>
              <th>Reference Range</th>
              <th>Flag</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>CA-125</td>
              <td className="result-value abnormal">1,847 U/mL</td>
              <td>0-35 U/mL</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>HE4</td>
              <td className="result-value abnormal">892 pmol/L</td>
              <td>0-140 pmol/L</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>CEA</td>
              <td className="result-value abnormal">28.4 ng/mL</td>
              <td>0-3.0 ng/mL</td>
              <td><span className="flag high">H</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="section">
        <div className="section-title">Complete Blood Count (CBC)</div>
        <table className="results-table">
          <thead>
            <tr>
              <th>Test</th>
              <th>Result</th>
              <th>Reference Range</th>
              <th>Flag</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>WBC</td>
              <td className="result-value abnormal">14.2 K/uL</td>
              <td>4.5-11.0 K/uL</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>RBC</td>
              <td className="result-value abnormal">3.2 M/uL</td>
              <td>4.2-5.4 M/uL</td>
              <td><span className="flag low">L</span></td>
            </tr>
            <tr>
              <td>Hemoglobin</td>
              <td className="result-value abnormal">8.9 g/dL</td>
              <td>12.0-16.0 g/dL</td>
              <td><span className="flag low">L</span></td>
            </tr>
            <tr>
              <td>Hematocrit</td>
              <td className="result-value abnormal">26.8%</td>
              <td>36.0-46.0%</td>
              <td><span className="flag low">L</span></td>
            </tr>
            <tr>
              <td>Platelets</td>
              <td className="result-value">187 K/uL</td>
              <td>150-400 K/uL</td>
              <td></td>
            </tr>
            <tr>
              <td>Neutrophils %</td>
              <td className="result-value abnormal">78%</td>
              <td>50-70%</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>Lymphocytes %</td>
              <td className="result-value abnormal">12%</td>
              <td>20-40%</td>
              <td><span className="flag low">L</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="section">
        <div className="section-title">Comprehensive Metabolic Panel</div>
        <table className="results-table">
          <thead>
            <tr>
              <th>Test</th>
              <th>Result</th>
              <th>Reference Range</th>
              <th>Flag</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Glucose</td>
              <td className="result-value">98 mg/dL</td>
              <td>70-99 mg/dL</td>
              <td></td>
            </tr>
            <tr>
              <td>BUN</td>
              <td className="result-value abnormal">28 mg/dL</td>
              <td>7-20 mg/dL</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>Creatinine</td>
              <td className="result-value abnormal">1.4 mg/dL</td>
              <td>0.6-1.2 mg/dL</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>eGFR</td>
              <td className="result-value abnormal">48 mL/min</td>
              <td>&gt;60 mL/min</td>
              <td><span className="flag low">L</span></td>
            </tr>
            <tr>
              <td>Sodium</td>
              <td className="result-value">138 mmol/L</td>
              <td>136-145 mmol/L</td>
              <td></td>
            </tr>
            <tr>
              <td>Potassium</td>
              <td className="result-value">4.2 mmol/L</td>
              <td>3.5-5.1 mmol/L</td>
              <td></td>
            </tr>
            <tr>
              <td>Chloride</td>
              <td className="result-value">102 mmol/L</td>
              <td>98-107 mmol/L</td>
              <td></td>
            </tr>
            <tr>
              <td>CO2</td>
              <td className="result-value">24 mmol/L</td>
              <td>22-29 mmol/L</td>
              <td></td>
            </tr>
            <tr>
              <td>Calcium</td>
              <td className="result-value abnormal">11.2 mg/dL</td>
              <td>8.5-10.2 mg/dL</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>Total Protein</td>
              <td className="result-value abnormal">5.8 g/dL</td>
              <td>6.3-8.2 g/dL</td>
              <td><span className="flag low">L</span></td>
            </tr>
            <tr>
              <td>Albumin</td>
              <td className="result-value abnormal">2.9 g/dL</td>
              <td>3.5-5.0 g/dL</td>
              <td><span className="flag low">L</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="section">
        <div className="section-title">Liver Function Tests</div>
        <table className="results-table">
          <thead>
            <tr>
              <th>Test</th>
              <th>Result</th>
              <th>Reference Range</th>
              <th>Flag</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>ALT</td>
              <td className="result-value abnormal">68 U/L</td>
              <td>7-56 U/L</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>AST</td>
              <td className="result-value abnormal">82 U/L</td>
              <td>10-40 U/L</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>Alkaline Phosphatase</td>
              <td className="result-value abnormal">178 U/L</td>
              <td>44-147 U/L</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>Total Bilirubin</td>
              <td className="result-value">1.1 mg/dL</td>
              <td>0.1-1.2 mg/dL</td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="section">
        <div className="section-title">Pulmonary Function Indicators</div>
        <table className="results-table">
          <thead>
            <tr>
              <th>Test</th>
              <th>Result</th>
              <th>Reference Range</th>
              <th>Flag</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>D-Dimer</td>
              <td className="result-value abnormal">2.8 μg/mL</td>
              <td>&lt;0.5 μg/mL</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>LDH</td>
              <td className="result-value abnormal">412 U/L</td>
              <td>140-280 U/L</td>
              <td><span className="flag high">H</span></td>
            </tr>
            <tr>
              <td>Arterial pH</td>
              <td className="result-value">7.38</td>
              <td>7.35-7.45</td>
              <td></td>
            </tr>
            <tr>
              <td>pO2</td>
              <td className="result-value abnormal">68 mmHg</td>
              <td>80-100 mmHg</td>
              <td><span className="flag low">L</span></td>
            </tr>
            <tr>
              <td>pCO2</td>
              <td className="result-value">38 mmHg</td>
              <td>35-45 mmHg</td>
              <td></td>
            </tr>
            <tr>
              <td>O2 Saturation</td>
              <td className="result-value abnormal">91%</td>
              <td>95-100%</td>
              <td><span className="flag low">L</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="clinical-notes">
        <h3>Clinical Notes</h3>
        <p><strong>Summary:</strong> 39-year-old female with Stage IV ovarian adenocarcinoma diagnosed August 2024, now with progression to lymphangitic carcinomatosis. Laboratory findings consistent with advanced malignancy including marked elevation of tumor markers (CA-125: 1,847 U/mL), moderate anemia (Hgb: 8.9 g/dL), mild renal insufficiency, and hypoxemia. Mild hypercalcemia and hypoalbuminemia noted.</p>

        <p><strong>Interpretation:</strong> Results indicate disease progression with multisystem involvement. Elevated CA-125 and HE4 consistent with active ovarian malignancy. CBC shows anemia of chronic disease with mild leukocytosis. Metabolic panel reveals mild renal dysfunction and hypercalcemia. Pulmonary parameters suggest impaired gas exchange consistent with lymphangitic spread.</p>

        <p><strong>Recommendations:</strong> Continue current chemotherapy regimen. Consider palliative radiotherapy for symptom control. Monitor renal function and calcium levels closely. Supportive care with oxygen therapy as needed. Nutritional support for hypoalbuminemia. Follow-up in 2 weeks or sooner if symptoms worsen.</p>
      </div>

      <div className="footer">
        <p>Keck Medicine of USC | 1975 Zonal Avenue, Los Angeles, CA 90033<br />
        Phone: (323) 442-8000 | Lab Results Hotline: (323) 442-8100<br />
        This report is confidential and intended solely for the use of the patient and authorized healthcare providers.</p>
      </div>
    </div>
  );
};
