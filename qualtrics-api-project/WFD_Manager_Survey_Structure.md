# WFD Manager Survey - Qualtrics Build Guide

## URGENT: Complete by 5:00 PM PDT Today (July 28, 2025)

---

## SURVEY TITLE: WFD Manager Organizational Readiness Assessment

### BLOCK 1: PROGRAM IDENTIFICATION

**Q1. Which program area do you manage?** (Single choice)

- Community Services
- Interim Housing

*[SET SKIP LOGIC: This determines which program-specific questions appear later]*

---

### BLOCK 2: ORIC-12 VALIDATED INSTRUMENT

*Instructions: Please indicate how much you agree or disagree with each statement about implementing the new data dashboard system at WFD.*

**Scale for all ORIC-12 items:**
1 = Disagree
2 = Somewhat Disagree  
3 = Neither Agree nor Disagree
4 = Somewhat Agree
5 = Agree

**Change Efficacy Items (Questions 2-7):**

**Q2.** People who work here feel confident that the organization can get people invested in implementing this change.

**Q3.** People who work here feel confident that they can keep track of progress in implementing this change.

**Q4.** People who work here feel confident that the organization can support people as they adjust to this change.

**Q5.** People who work here feel confident that they can keep the momentum going in implementing this change.

**Q6.** People who work here feel confident that they can handle the challenges that might arise in implementing this change.

**Q7.** People who work here feel confident that they can coordinate tasks so that implementation goes smoothly.

**Change Commitment Items (Questions 8-13):**

**Q8.** People who work here are committed to implementing this change.

**Q9.** People who work here will do whatever it takes to implement this change.

**Q10.** People who work here want to implement this change.

**Q11.** People who work here are determined to implement this change.

**Q12.** People who work here are motivated to implement this change.

**Q13.** People who work here will persist through challenges to implement this change.

---

### BLOCK 3: CURRENT DATA PRACTICES (All Managers)

**Q14. How often do you currently use data to make decisions in your program?**

- Never
- Rarely (once a month or less)
- Sometimes (weekly)
- Often (several times a week)
- Daily

**Q15. What are your biggest challenges with using data? (Select all that apply)**

- [ ] Don't have time to look at data
- [ ] Don't know where to find the data I need
- [ ] Data isn't relevant to my daily work
- [ ] Don't feel confident interpreting data
- [ ] Current systems are too complicated
- [ ] Data isn't accurate or up-to-date
- [ ] Other: _________

**Q16. How comfortable are you with the following? (1=Very Uncomfortable, 5=Very Comfortable)**

- Reading data reports
- Creating charts or graphs
- Identifying trends in data
- Using data to tell a story
- Making decisions based on data

**Q17. What data would be MOST helpful for managing your program? (Open text)**

---

### BLOCK 4A: COMMUNITY SERVICES SPECIFIC

*[ONLY SHOW IF Q1 = Community Services]*

**Q18. For Community Services, which metrics are most important to track? (Rank top 3)**

- Client engagement hours
- Service referrals made
- Case note completion rates
- Client goal achievement
- Resource utilization
- Staff productivity
- Other: _________

**Q19. How often do you currently review client progress data?**

- Never
- Monthly
- Weekly
- Daily
- As needed

**Q20. What would help you use client data more effectively? (Open text)**

---

### BLOCK 4B: INTERIM HOUSING SPECIFIC

*[ONLY SHOW IF Q1 = Interim Housing]*

**Q21. For Interim Housing, which metrics are most important to track? (Rank top 3)**

- Bed utilization rates
- Length of stay
- Housing placement success
- Incident reports
- Maintenance requests
- Staff coverage
- Other: _________

**Q22. How often do you currently review occupancy and operations data?**

- Never
- Monthly
- Weekly
- Daily
- As needed

**Q23. What would help you use housing data more effectively? (Open text)**

---

### BLOCK 5: READINESS FOR CHANGE

**Q24. What excites you most about having a data dashboard?** (Open text)

**Q25. What concerns you most about implementing a data dashboard?** (Open text)

**Q26. On a scale of 1-10, how ready is your team to start using data regularly?**
(1 = Not ready at all, 10 = Completely ready)

---

### BLOCK 6: CLOSING

**Q27. Would you like to receive a summary of these survey results?**

- Yes
- No

**Thank You Message:**
"Thank you for completing this assessment. Your responses will help us design a data dashboard that truly meets your needs. You'll receive information about the August 13 Data Club session where we'll review these results and begin implementation planning."

---

## QUALTRICS SETUP CHECKLIST

### ✓ Survey Flow

1. Block 1: Program ID (with branching)
2. Block 2: ORIC-12 (all respondents)
3. Block 3: Data Practices (all respondents)
4. Block 4A OR 4B: Program-specific (based on Q1)
5. Block 5: Readiness (all respondents)
6. Block 6: Closing

### ✓ Skip Logic

- If Q1 = "Community Services" → Show Block 4A, Hide Block 4B
- If Q1 = "Interim Housing" → Show Block 4B, Hide Block 4A

### ✓ Survey Options

- Anonymous responses: YES
- Back button: YES
- Progress bar: YES
- Survey expiration: None (ongoing)

### ✓ Custom Scoring

- ORIC Change Efficacy Score = Average(Q2-Q7)
- ORIC Change Commitment Score = Average(Q8-Q13)
- Overall ORIC Score = Average(Q2-Q13)
