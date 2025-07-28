# Qualtrics Survey API Integration

This project provides a Python-based integration between Qualtrics Survey Platform and Google Sheets, with automatic ORIC (Organizational Readiness for Implementing Change) score calculation.

## Features

- **Qualtrics API Integration**: Connect to Qualtrics and export survey responses
- **ORIC Score Calculation**: Automatically calculate organizational readiness scores
- **Google Sheets Sync**: Real-time sync of survey data to Google Sheets
- **Dashboard Data**: Aggregated metrics for visualization
- **Automated Insights**: Generate actionable insights based on ORIC scores
- **Webhook Support**: Set up automatic syncing on survey completion

## Architecture Overview

This implementation follows the recommended Phase 1 approach from your architecture plan:
- Basic integration with Qualtrics API
- Google Sheets for immediate value
- ORIC score calculations
- Foundation for future scaling to other platforms

## Prerequisites

1. **Python 3.8+** installed
2. **Qualtrics Account** with API access
3. **Google Cloud Project** with Sheets API enabled
4. **Google Service Account** credentials

## Setup Instructions

### 1. Clone/Copy the Project

```bash
cd "/Users/ericjones/Desktop/Whittier First Day/Survey/qualtrics-api-project"
```

### 2. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install additional requirements
pip install -r requirements.txt
```

### 3. Configure Qualtrics API

1. Log into your Qualtrics account
2. Go to **Account Settings** > **Qualtrics IDs**
3. Note your **User ID** and **Organization ID**
4. Go to **Account Settings** > **API** > **API Token**
5. Generate a new API token

### 4. Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable the **Google Sheets API**
4. Create a **Service Account**:
   - Go to **IAM & Admin** > **Service Accounts**
   - Click **Create Service Account**
   - Download the JSON credentials file
5. Create a new Google Sheet and note its ID (from the URL)
6. Share the sheet with the service account email

### 5. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env
```

Update these values in `.env`:
```
QUALTRICS_API_TOKEN=your_actual_api_token
QUALTRICS_DATA_CENTER=https://yourdatacenter.qualtrics.com
QUALTRICS_SURVEY_ID=SV_your_survey_id
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_CREDENTIALS_FILE=/path/to/your/credentials.json
```

Data center URLs:
- US: `https://yul1.qualtrics.com`
- EU: `https://fra1.qualtrics.com`
- Singapore: `https://sin1.qualtrics.com`
- Sydney: `https://syd1.qualtrics.com`
- Washington DC: `https://iad1.qualtrics.com`
- Canada: `https://yul1.qualtrics.com`
- UK: `https://lhr1.qualtrics.com`
- Japan: `https://hnd1.qualtrics.com`

## Usage

### Test Connection

```bash
python main.py test
```

### Run ORIC Calculation Demo

```bash
python main.py demo
```

### Sync Survey to Google Sheets

```bash
# Sync configured survey
python main.py sync

# Sync specific survey
python main.py sync --survey-id SV_123456
```

### Set Up Webhook (Optional)

```bash
python main.py webhook https://your-webhook-url.com/qualtrics
```

## Project Structure

```
qualtrics-api-project/
├── .env                    # Your configuration (create from .env.example)
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
├── qualtrics_client.py   # Qualtrics API wrapper
├── oric_calculator.py    # ORIC score calculations
├── google_sheets_sync.py # Google Sheets integration
├── main.py              # Command-line interface
└── README.md            # This file
```

## Google Sheets Structure

The integration creates multiple sheets:

1. **Survey Responses**: Raw survey data with ORIC scores
   - Response ID, timestamps, status
   - Individual question responses
   - Calculated ORIC scores
   - Subscale scores

2. **Dashboard Data**: Aggregated metrics
   - Total responses
   - Average ORIC score
   - Readiness level distribution
   - Subscale averages

3. **Dashboard Data_TimeSeries**: Time-based trends
   - Daily averages
   - Trend analysis data

4. **Insights**: Generated recommendations
   - Response-level insights
   - Actionable recommendations

## Customizing ORIC Calculations

Edit `oric_calculator.py` to customize:

1. **Question Mappings**: Update `SUBSCALES` dictionary with your survey question IDs
2. **Weights**: Adjust subscale weights in the constructor
3. **Score Ranges**: Modify readiness level thresholds

Example:
```python
SUBSCALES = {
    'change_commitment': ['QID1', 'QID2', 'QID3'],  # Your actual question IDs
    'change_efficacy': ['QID4', 'QID5', 'QID6'],
    'contextual_factors': ['QID7', 'QID8', 'QID9']
}
```

## Creating a Dashboard in Google Sheets

1. Open your synced Google Sheet
2. Create a new sheet called "Dashboard"
3. Use these formulas:

```
# Average ORIC Score
=AVERAGE('Survey Responses'!G:G)

# Response Count
=COUNTA('Survey Responses'!A:A)-1

# Readiness Distribution
=COUNTIF('Survey Responses'!H:H,"high")/COUNTA('Survey Responses'!H:H)
```

4. Create charts:
   - Line chart for time series data
   - Gauge chart for current ORIC score
   - Pie chart for readiness distribution

## Troubleshooting

### API Token Issues
- Ensure token has correct permissions
- Check data center URL matches your account

### Google Sheets Access Denied
- Verify service account email has edit access
- Check credentials file path is correct

### Missing Survey Responses
- Confirm survey ID is correct
- Check survey has completed responses
- Verify date range if filtering

## Next Steps (Phase 2-3)

As outlined in your architecture plan:

1. **Advanced Analytics**
   - Predictive modeling
   - Cohort analysis
   - Manager-specific dashboards

2. **Multi-Tenant Support**
   - Organization management
   - White-label components
   - Role-based access

3. **Platform Migration Options**
   - Lovable.dev for real-time dashboards
   - Cloudflare Workers for edge computing
   - AWS Amplify for enterprise scale

## Support

For issues or questions:
1. Check Qualtrics API documentation
2. Review Google Sheets API guides
3. Examine error messages in console output

## Security Notes

- Never commit `.env` file to version control
- Keep API tokens secure
- Use webhook secrets for production
- Enable audit logging for compliance

---

Built for Whittier First Day and Recovery Compass
Strategic implementation for organizational change measurement
