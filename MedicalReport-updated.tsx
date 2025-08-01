import React from 'react';

const MedicalReport = () => {
  return (
    <div className="min-h-screen bg-white p-8 print:p-0">
      {/* Header */}
      <div className="flex items-center justify-between border-b-4 border-[#990000] pb-6 mb-8">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-[#990000] text-white flex items-center justify-center font-bold text-3xl rounded">
            K
          </div>
          <h1 className="text-3xl font-medium text-[#990000]">Keck Medicine of USC</h1>
        </div>
        <div className="text-right text-sm text-gray-600">
          <p><strong className="text-black">Report Date:</strong> 24/07/2025</p>
          <p><strong className="text-black">Collection Date:</strong> 22/07/2025</p>
        </div>
      </div>

      {/* Patient Information */}
      <div className="bg-gray-50 p-8 rounded-lg mb-8 border border-gray-200">
        <h2 className="text-2xl text-[#990000] mb-6 font-serif">Patient Information</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-gray-600 uppercase tracking-wider font-semibold">Name</p>
            <p className="text-base font-medium">Sayegh, Nuha</p>
          </div>
          <div>
            <p className="text-xs text-gray-600 uppercase tracking-wider font-semibold">MRN</p>
            <p className="text-base font-medium">KM-2024-0823</p>
          </div>
          <div>
            <p className="text-xs text-gray-600 uppercase tracking-wider font-semibold">DOB</p>
            <p className="text-base font-medium">03/15/1985</p>
          </div>
          <div>
            <p className="text-xs text-gray-600 uppercase tracking-wider font-semibold">Age</p>
            <p className="text-base font-medium">39 years</p>
          </div>
          <div>
            <p className="text-xs text-gray-600 uppercase tracking-wider font-semibold">Physician</p>
            <p className="text-base font-medium">Dr. Sarah Chen, MD</p>
          </div>
          <div>
            <p className="text-xs text-gray-600 uppercase tracking-wider font-semibold">Diagnosis</p>
            <p className="text-base font-medium text-[#990000]">Stage IV Ovarian CA w/ Lymphangitic Carcinomatosis</p>
          </div>
        </div>
      </div>

      {/* Tumor Markers */}
      <div className="mb-8">
        <div className="bg-[#990000] text-white px-6 py-2 text-lg font-medium mb-4">
          Tumor Markers
        </div>
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Result</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Reference Range</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Flag</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">CA-125</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">1,847 U/mL</td>
              <td className="px-4 py-2">0-35 U/mL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">HE4</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">892 pmol/L</td>
              <td className="px-4 py-2">0-140 pmol/L</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">CEA</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">28.4 ng/mL</td>
              <td className="px-4 py-2">0-3.0 ng/mL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Complete Blood Count */}
      <div className="mb-8">
        <div className="bg-[#990000] text-white px-6 py-2 text-lg font-medium mb-4">
          Complete Blood Count (CBC)
        </div>
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Result</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Reference Range</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Flag</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">WBC</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">14.2 K/uL</td>
              <td className="px-4 py-2">4.5-11.0 K/uL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">RBC</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">3.2 M/uL</td>
              <td className="px-4 py-2">4.2-5.4 M/uL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Hemoglobin</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">8.9 g/dL</td>
              <td className="px-4 py-2">12.0-16.0 g/dL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Hematocrit</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">26.8%</td>
              <td className="px-4 py-2">36.0-46.0%</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Platelets</td>
              <td className="px-4 py-2 font-semibold">187 K/uL</td>
              <td className="px-4 py-2">150-400 K/uL</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Neutrophils %</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">78%</td>
              <td className="px-4 py-2">50-70%</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Lymphocytes %</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">12%</td>
              <td className="px-4 py-2">20-40%</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Comprehensive Metabolic Panel */}
      <div className="mb-8">
        <div className="bg-[#990000] text-white px-6 py-2 text-lg font-medium mb-4">
          Comprehensive Metabolic Panel
        </div>
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Result</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Reference Range</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Flag</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Glucose</td>
              <td className="px-4 py-2 font-semibold">98 mg/dL</td>
              <td className="px-4 py-2">70-99 mg/dL</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">BUN</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">28 mg/dL</td>
              <td className="px-4 py-2">7-20 mg/dL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Creatinine</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">1.4 mg/dL</td>
              <td className="px-4 py-2">0.6-1.2 mg/dL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">eGFR</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">48 mL/min</td>
              <td className="px-4 py-2">&gt;60 mL/min</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Sodium</td>
              <td className="px-4 py-2 font-semibold">138 mmol/L</td>
              <td className="px-4 py-2">136-145 mmol/L</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Potassium</td>
              <td className="px-4 py-2 font-semibold">4.2 mmol/L</td>
              <td className="px-4 py-2">3.5-5.1 mmol/L</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Chloride</td>
              <td className="px-4 py-2 font-semibold">102 mmol/L</td>
              <td className="px-4 py-2">98-107 mmol/L</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">CO2</td>
              <td className="px-4 py-2 font-semibold">24 mmol/L</td>
              <td className="px-4 py-2">22-29 mmol/L</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Calcium</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">11.2 mg/dL</td>
              <td className="px-4 py-2">8.5-10.2 mg/dL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Total Protein</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">5.8 g/dL</td>
              <td className="px-4 py-2">6.3-8.2 g/dL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Albumin</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">2.9 g/dL</td>
              <td className="px-4 py-2">3.5-5.0 g/dL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Liver Function Tests */}
      <div className="mb-8">
        <div className="bg-[#990000] text-white px-6 py-2 text-lg font-medium mb-4">
          Liver Function Tests
        </div>
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Result</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Reference Range</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Flag</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">ALT</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">68 U/L</td>
              <td className="px-4 py-2">7-56 U/L</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">AST</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">82 U/L</td>
              <td className="px-4 py-2">10-40 U/L</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Alkaline Phosphatase</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">178 U/L</td>
              <td className="px-4 py-2">44-147 U/L</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Total Bilirubin</td>
              <td className="px-4 py-2 font-semibold">1.1 mg/dL</td>
              <td className="px-4 py-2">0.1-1.2 mg/dL</td>
              <td className="px-4 py-2"></td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Pulmonary Function Indicators */}
      <div className="mb-8">
        <div className="bg-[#990000] text-white px-6 py-2 text-lg font-medium mb-4">
          Pulmonary Function Indicators
        </div>
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Result</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Reference Range</th>
              <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Flag</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">D-Dimer</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">2.8 μg/mL</td>
              <td className="px-4 py-2">&lt;0.5 μg/mL</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">LDH</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">412 U/L</td>
              <td className="px-4 py-2">140-280 U/L</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#F26178] text-white text-xs font-bold rounded">H</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">Arterial pH</td>
              <td className="px-4 py-2 font-semibold">7.38</td>
              <td className="px-4 py-2">7.35-7.45</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">pO2</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">68 mmHg</td>
              <td className="px-4 py-2">80-100 mmHg</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">pCO2</td>
              <td className="px-4 py-2 font-semibold">38 mmHg</td>
              <td className="px-4 py-2">35-45 mmHg</td>
              <td className="px-4 py-2"></td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">O2 Saturation</td>
              <td className="px-4 py-2 font-semibold text-[#F26178]">91%</td>
              <td className="px-4 py-2">95-100%</td>
              <td className="px-4 py-2">
                <span className="inline-flex items-center justify-center w-6 h-6 bg-[#FFCC00] text-black text-xs font-bold rounded">L</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Clinical Notes */}
      <div className="bg-[#FFF2BF] border-l-4 border-[#FFCC00] p-8 rounded-md mb-8">
        <h3 className="text-lg text-[#990000] font-serif mb-4">Clinical Notes</h3>
        <div className="space-y-4 text-sm">
          <p>
            <strong className="text-black">Summary:</strong> 39-year-old female with Stage IV ovarian adenocarcinoma diagnosed August 2024,
            now with progression to lymphangitic carcinomatosis. Laboratory findings consistent with advanced malignancy including marked
            elevation of tumor markers (CA-125: 1,847 U/mL), moderate anemia (Hgb: 8.9 g/dL), mild renal insufficiency, and hypoxemia.
            Mild hypercalcemia and hypoalbuminemia noted.
          </p>
          <p>
            <strong className="text-black">Interpretation:</strong> Results indicate disease progression with multisystem involvement.
            Elevated CA-125 and HE4 consistent with active ovarian malignancy. CBC shows anemia of chronic disease with mild leukocytosis.
            Metabolic panel reveals mild renal dysfunction and hypercalcemia. Pulmonary parameters suggest impaired gas exchange consistent
            with lymphangitic spread.
          </p>
          <p>
            <strong className="text-black">Recommendations:</strong> Continue current chemotherapy regimen. Consider palliative radiotherapy
            for symptom control. Monitor renal function and calcium levels closely. Supportive care with oxygen therapy as needed.
            Nutritional support for hypoalbuminemia. Follow-up in 2 weeks or sooner if symptoms worsen.
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t-2 border-gray-200 pt-8 mt-16 text-center text-sm text-gray-600">
        <p>Keck Medicine of USC | 1975 Zonal Avenue, Los Angeles, CA 90033</p>
        <p>Phone: (323) 442-8000 | Lab Results Hotline: (323) 442-8100</p>
        <p className="mt-2">This report is confidential and intended solely for the use of the patient and authorized healthcare providers.</p>
      </div>
    </div>
  );
};

export default MedicalReport;
