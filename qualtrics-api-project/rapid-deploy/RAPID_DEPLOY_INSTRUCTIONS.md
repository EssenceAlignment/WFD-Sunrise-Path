# 🚨 RAPID DEPLOYMENT - GET SURVEY LIVE BY 5 PM!

## Current Time Check: 3:24 PM - You have 96 minutes!

---

## 🏃‍♂️ QUICKSTART (10 minutes)

### 1. Open Terminal and Navigate Here:
```bash
cd "/Users/ericjones/Desktop/Whittier First Day/Survey/qualtrics-api-project/rapid-deploy"
```

### 2. Install Dependencies:
```bash
npm install
```

### 3. Get Your Qualtrics API Token:
1. Log into Qualtrics
2. Go to: **Account Settings → Qualtrics IDs → API**
3. Click **Generate Token**
4. Copy the token

### 4. Update .env File:
```bash
# Edit .env and replace YOUR_API_TOKEN_HERE with your actual token
nano .env
# OR open in your text editor
```

Your .env should look like:
```
QUALTRICS_API_TOKEN=UR_1234567890abcdef
QUALTRICS_DATACENTER=yul1
```

---

## 🧪 TEST CONNECTION (2 minutes)

```bash
npm run test-connection
```

✅ If you see "Connection successful!" → Continue  
❌ If you see errors → Check your token and datacenter

---

## 🚀 OPTION A: CREATE SURVEY VIA API (15 minutes)

### Run the creation script:
```bash
npm run create-survey
```

This will:
- Create the survey
- Add ORIC-12 questions
- Set anonymous responses
- Activate the survey
- Save the Survey ID

### Then get the anonymous link:
```bash
npm run get-link
```

The link will be:
- Displayed in terminal
- Saved to `anonymous-link.txt`
- Email snippet saved to `email-snippet.txt`

---

## 🎯 OPTION B: MANUAL FALLBACK (If API fails)

1. **Create survey manually in Qualtrics UI**
   - Use `WFD_Manager_Survey_Structure.md` as guide
   - Copy all questions exactly
   - Set up skip logic on Q1

2. **Get Survey ID from URL:**
   - Look for `SV_XXXXXXXXX` in the URL
   - Example: `https://yul1.qualtrics.com/survey-builder/SV_abc123def456/edit`

3. **Get anonymous link via API:**
   ```bash
   node get-anonymous-link.js SV_XXXXXXXXX
   ```

---

## 📧 FINAL STEPS (4:45 PM)

### 1. Copy the anonymous link from terminal or `anonymous-link.txt`

### 2. Update your email:
- Open `Email_to_Donna_5PM.md`
- Replace `[INSERT QUALTRICS LINK]` with your link
- Replace other placeholders

### 3. Send to Donna by 5:00 PM!

---

## 🆘 TROUBLESHOOTING

### "API Token Invalid"
- Regenerate token in Qualtrics
- Make sure no spaces before/after token

### "Survey Creation Failed"
- Use manual option (create in UI, get link via API)
- Focus on getting link - that's what matters!

### "Can't find datacenter"
- Check your Qualtrics URL
- Common: yul1, fra1, syd1, sin1
- If unsure, try without subdomain

### Time Running Out?
1. Create survey manually in Qualtrics
2. Get Survey ID from URL
3. Run: `node get-anonymous-link.js SV_YOUR_ID`
4. Email link to Donna

---

## ⏱️ TIME CHECKS

- **3:30 PM**: Should have API connection working
- **3:45 PM**: Survey created (API or manual)
- **4:00 PM**: Have anonymous link
- **4:30 PM**: Email drafted
- **4:45 PM**: Final review
- **5:00 PM**: SEND TO DONNA

---

## 📝 BARE MINIMUM SUCCESS

If everything else fails, you need:
1. ✅ Survey created in Qualtrics (any method)
2. ✅ Anonymous link (get via API or Qualtrics UI)
3. ✅ Email sent to Donna with link

The webhook and dashboard integration can wait until tomorrow!

---

## 💡 PRO TIP

The anonymous link is what Donna needs TODAY. Everything else (webhook, dashboard, API sync) can be set up later. Focus on:

1. Getting a working survey
2. Getting the anonymous link
3. Sending the email

GO GO GO! 🚀
