import React from 'react';

const ConsultationReport = () => {
  return (
    <div className="min-h-screen bg-white p-8 print:p-0">
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-16 h-16 bg-usc-cardinal text-white flex items-center justify-center font-bold text-3xl rounded font-caslon">
            K
          </div>
          <div>
            <h1 className="text-3xl font-medium text-usc-cardinal font-caslon">Keck Medicine of USC</h1>
            <p className="text-lg text-gray-70k font-national">USC Norris Comprehensive Cancer Center</p>
          </div>
        </div>
        <div className="text-gray-70k font-national">
          <p>1441 Eastlake Avenue</p>
          <p>Los Angeles, CA 90089</p>
          <p>(323) 865-3000</p>
        </div>
      </div>

      {/* Report Title */}
      <div className="bg-usc-gold/20 p-6 rounded-lg mb-8">
        <h2 className="text-2xl font-caslon text-usc-cardinal text-center">
          Comprehensive Oncology Patient Consultation Report
        </h2>
      </div>

      {/* Patient Information Grid */}
      <div className="grid grid-cols-2 gap-6 mb-8 font-national">
        <div>
          <p className="text-xs text-gray-70k uppercase tracking-wider font-semibold">PATIENT NAME:</p>
          <p className="text-base font-medium">Nuha Sayegh</p>
        </div>
        <div>
          <p className="text-xs text-gray-70k uppercase tracking-wider font-semibold">DATE OF BIRTH:</p>
          <p className="text-base font-medium">04/03/1985</p>
        </div>
        <div>
          <p className="text-xs text-gray-70k uppercase tracking-wider font-semibold">MEDICAL RECORD NUMBER:</p>
          <p className="text-base font-medium">12489697</p>
        </div>
        <div>
          <p className="text-xs text-gray-70k uppercase tracking-wider font-semibold">DATE/TIME OF CONSULTATION:</p>
          <p className="text-base font-medium">07/22/2025 / 10:45:00 AM</p>
        </div>
        <div>
          <p className="text-xs text-gray-70k uppercase tracking-wider font-semibold">ONCOLOGIST:</p>
          <p className="text-base font-medium">Laila I. Muderspach, MD (Gyn Oncology)</p>
        </div>
        <div>
          <p className="text-xs text-gray-70k uppercase tracking-wider font-semibold">REFERRING PHYSICIAN:</p>
          <p className="text-base font-medium">Dr. Sarah P. Nguyen</p>
        </div>
      </div>

      {/* Clinical Background */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          CLINICAL BACKGROUND
        </div>
        <p className="text-base leading-relaxed font-national text-foreground">
          Ms. Sayegh is a 39-year-old woman initially diagnosed with Stage IIIC high-grade serous ovarian carcinoma in September 2024.
          Initial presentation included significant ascites, elevated CA-125 (2,847 U/mL), and extensive peritoneal disease on imaging.
          Molecular testing revealed BRCA1 germline mutation and homologous recombination deficiency (HRD) positive status.
        </p>
      </div>

      {/* Course to Date */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          COURSE TO DATE
        </div>
        <div className="space-y-3 font-national">
          <p className="text-base"><strong>September 2024:</strong> Neoadjuvant chemotherapy initiated with carboplatin/paclitaxel + bevacizumab.</p>
          <p className="text-base"><strong>November 2024:</strong> Excellent clinical and biochemical response. CA-125 decreased to 42 U/mL.</p>
          <p className="text-base"><strong>December 2024:</strong> Interval debulking surgery performed with optimal cytoreduction (R0 resection).</p>
          <p className="text-base"><strong>January 2025:</strong> Completed adjuvant chemotherapy. Maintenance olaparib initiated given BRCA1 status.</p>
        </div>
      </div>

      {/* Recent Clinical Change */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          RECENT CLINICAL CHANGE
        </div>
        <p className="text-base leading-relaxed font-national text-foreground">
          In March 2025, Ms. Sayegh reported new onset of progressive dyspnea, persistent dry cough, and severe fatigue.
          CA-125 has risen dramatically from nadir of 8 U/mL to current level of 1,847 U/mL over 8 weeks.
          Physical examination revealed diminished breath sounds bilaterally and mild lower extremity edema.
          Patient also reports unintentional weight loss of 15 pounds despite adequate oral intake.
        </p>
      </div>

      {/* Laboratory/Imaging Results */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          LABORATORY/IMAGING RESULTS
        </div>
        <div className="space-y-3 font-national">
          <p className="text-base"><strong>CA-125:</strong> 1,847 U/mL (↑ from 8 U/mL eight weeks ago)</p>
          <p className="text-base"><strong>CT Chest/Abdomen/Pelvis (07/15/2025):</strong> Multiple bilateral pulmonary nodules,
            diffuse interlobular septal thickening, and peribronchial thickening consistent with lymphangitic carcinomatosis.
            New moderate bilateral pleural effusions. Multiple new hepatic metastases ranging from 1.2-3.8 cm.</p>
          <p className="text-base"><strong>Complete Blood Count:</strong> Hemoglobin 8.9 g/dL (anemia), platelets 187 K/uL</p>
          <p className="text-base"><strong>Comprehensive Metabolic Panel:</strong> Albumin 2.9 g/dL, mild renal insufficiency (Cr 1.4 mg/dL)</p>
          <p className="text-base"><strong>Pulmonary Function Tests:</strong> Restrictive pattern with DLCO 45% predicted</p>
        </div>
      </div>

      {/* Updated Diagnosis */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          UPDATED DIAGNOSIS
        </div>
        <p className="text-base font-semibold text-usc-cardinal font-national">
          Stage IV Ovarian Carcinoma with Lymphangitic Carcinomatosis
        </p>
      </div>

      {/* Assessment & Discussion */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          ASSESSMENT & DISCUSSION
        </div>
        <p className="text-base leading-relaxed font-national text-foreground">
          Ms. Sayegh has experienced rapid disease progression with development of lymphangitic carcinomatosis,
          representing a significant advancement from her initial platinum-sensitive recurrence.
          The lymphangitic spread pattern indicates widespread microscopic tumor infiltration of the pulmonary lymphatic system,
          which substantially alters prognosis and treatment approach. Her declining performance status (ECOG 2-3),
          hypoxemia requiring supplemental oxygen, and nutritional deterioration are concerning indicators.
        </p>
        <p className="text-base leading-relaxed font-national text-foreground mt-4">
          Despite her young age and BRCA1 mutation status, the extent of disease progression necessitates
          a careful reassessment of treatment goals, balancing aggressive intervention with quality of life considerations.
        </p>
      </div>

      {/* Plan / Recommendations */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          PLAN / RECOMMENDATIONS
        </div>
        <ol className="list-decimal list-inside space-y-2 font-national text-foreground">
          <li>Discontinue maintenance olaparib immediately</li>
          <li>Initiate modified chemotherapy regimen with weekly paclitaxel (dose-reduced given performance status)</li>
          <li>Thoracentesis for symptomatic relief of pleural effusions</li>
          <li>Pulmonology consultation for optimization of respiratory support</li>
          <li>Initiate high-dose corticosteroids for lymphangitic inflammation</li>
          <li>Pain management consultation for comprehensive symptom control</li>
          <li>Nutritional support with consideration of parenteral nutrition if oral intake remains poor</li>
          <li>Early integration of supportive care services alongside active treatment</li>
          <li>Discussion of advance directives and goals of care in upcoming visit</li>
          <li>Family meeting scheduled to discuss treatment trajectory and expectations</li>
        </ol>
      </div>

      {/* Patient Understanding & Perspective */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          Patient Understanding & Perspective
        </div>
        <p className="text-base italic font-national text-foreground mb-4">
          "I understand that my cancer has spread to my lungs in a serious way. Dr. Muderspach explained that
          we'll try chemotherapy but also need to focus on keeping me comfortable. I'm scared about not being
          able to breathe, but I trust my team to help me through this."
        </p>
        <p className="text-base leading-relaxed font-national text-foreground">
          Ms. Sayegh demonstrates understanding of her disease progression and the gravity of lymphangitic involvement.
          She expresses primary concerns about respiratory symptoms and maintaining independence for her children,
          Talib (6) and Mia (13). She has initiated discussions with family regarding contingency planning
          but remains hopeful for meaningful response to treatment.
        </p>
        <p className="text-base leading-relaxed font-national text-foreground mt-4">
          <em>Clinical Note: Patient exhibits appropriate concern while maintaining realistic hope.
          Recommended ongoing psychological support and family counseling services.
          Social work engaged for practical support planning.</em>
        </p>
      </div>

      {/* Prognosis */}
      <div className="mb-8">
        <div className="bg-usc-cardinal text-white px-6 py-2 text-lg font-medium mb-4 font-caslon">
          PROGNOSIS
        </div>
        <p className="text-base leading-relaxed font-national text-foreground">
          Lymphangitic carcinomatosis in ovarian cancer represents an advanced disease state with limited therapeutic options.
          Current literature suggests median survival of approximately 3-6 months from diagnosis of lymphangitic spread,
          with 50% of patients surviving beyond 1.5 years being uncommon. Response to systemic therapy is variable,
          with symptom palliation often being the primary achievable goal. Her BRCA1 status may confer slightly
          improved chemosensitivity, though the lymphangitic pattern typically shows modest response rates.
        </p>
        <p className="text-base leading-relaxed font-national text-foreground mt-4">
          Focus will remain on aggressive symptom management, preservation of quality of life,
          and supporting the patient's goal of maintaining meaningful time with her young children.
        </p>
      </div>

      {/* Electronic Signature */}
      <div className="mt-16 pt-8 border-t-2 border-gray-30k">
        <div className="flex items-center justify-between font-national">
          <div>
            <p className="text-sm text-gray-70k mb-2">bizmaticsInc</p>
            <div className="border-b-2 border-gray-70k w-64 mb-2"></div>
            <p className="text-sm font-semibold">Electronic Signature</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-70k">07/22/2025 at 11:05:00 AM</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConsultationReport;
