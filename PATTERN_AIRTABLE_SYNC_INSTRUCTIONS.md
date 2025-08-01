# Pattern → Airtable Sync Verification Instructions

## 🎯 Purpose
This script makes Pattern Registry 2.0 detections visible in your actual Airtable dashboard by updating existing records with AI-generated annotations.

## 🚀 How to Run

```bash
python scripts/pattern_to_airtable_sync.py --update-live
```

## 📊 What You'll See During Execution

```
🔍 Pattern Registry → Airtable Sync Starting...
📊 Found 61 existing records to analyze
✅ Updated: SAMHSA Recovery Community Services Program... → Pattern: mental_health_grant
✅ Updated: Conrad N. Hilton Foundation Recovery Housing... → Pattern: foundation_grant_open
✅ Updated: San Diego County Behavioral Health Services RFP... → Pattern: rfp_deadline_approaching
... (more updates)
📈 SYNC COMPLETE: X records updated with AI patterns
🔗 View changes at: https://airtable.com/appNBesu9xYl5Mvm1/tblcfetlKrhMU4p5r
📄 Verification report saved: pattern_sync_verification.txt
```

## 🔍 How to Verify in Airtable

### 1. Open your Airtable dashboard
Navigate to: https://airtable.com/appNBesu9xYl5Mvm1/tblcfetlKrhMU4p5r

### 2. Check the Following Fields for Changes:

#### **Notes Field**
- **Before**: Original notes or empty
- **After**: Original notes + new line with:
  ```
  [AI Pattern: mental_health_grant (95% confidence) - 2025-07-31 15:15:00]
  ```

#### **Priority Score Field**
- **Before**: Original score or empty
- **After**: Updated with pattern force multiplier (0-100 scale)
  - mental_health_grant: 100 (20 × 5)
  - federal_funding_announcement: 125 → 100 (capped)
  - rfp_deadline_approaching: 75 (15 × 5)

#### **External API ID Field**
- **Before**: Original ID or empty
- **After**: Pattern provenance ID:
  ```
  PR2-mental_health_grant-2025-07-31 15:15:00
  ```

### 3. Sample Expected Changes

| Row | Opportunity Name | Notes (Added) | Priority Score | External API ID |
|-----|-----------------|---------------|----------------|-----------------|
| 1 | SAMHSA Recovery Community Services | [AI Pattern: mental_health_grant (95% confidence)...] | 100 | PR2-mental_health_grant-... |
| 2 | HRSA Rural Communities Opioid Response | [AI Pattern: federal_funding_announcement (90% confidence)...] | 100 | PR2-federal_funding_announcement-... |
| 3 | San Diego County Behavioral Health RFP | [AI Pattern: rfp_deadline_approaching (85% confidence)...] | 75 | PR2-rfp_deadline_approaching-... |

## 📋 Verification Checklist

- [ ] Run the sync command
- [ ] See real-time progress in terminal
- [ ] Open/refresh Airtable dashboard
- [ ] Confirm Notes field shows AI Pattern annotations
- [ ] Confirm Priority Score updated (higher = stronger pattern match)
- [ ] Confirm External API ID shows pattern provenance
- [ ] Check pattern_sync_verification.txt for summary

## ⚠️ Important Notes

1. **Persistence**: All changes are permanent and will persist across refreshes
2. **Provenance**: Every update includes timestamp and pattern name for audit trail
3. **Non-destructive**: Existing data is preserved; AI annotations are appended
4. **Idempotent**: Running multiple times will add multiple annotations (by design for audit trail)

## 🚨 No Success Until You Confirm

**This implementation is NOT complete until Eric Brakebill Jones confirms:**
- "I see the AI Pattern annotations in my Notes field"
- "I see updated Priority Scores"
- "I see pattern provenance in External API ID"
- "The changes persist after refresh"

Only user-witnessed changes in the actual dashboard count as success.
