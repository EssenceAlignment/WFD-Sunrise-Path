# Recovery Compass: Zero Surprises Action Plan

## ⚠️ Core Assumption: Everything Breaks

This plan assumes:
- Every script has a half-life measured in weeks
- Every compliance deadline will be missed without active monitoring
- Every revenue projection is wrong by 2-5x
- Every system will fail at the worst possible moment

## 🚨 Immediate Actions (Next 72 Hours)

### Hour 1-4: Stop the Bleeding
```bash
# 1. Verify MCP is working RIGHT NOW
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Screenshot all working configs (paper backup)
# 3. Print this document
# 4. Set phone reminders for every deadline below
```

### Day 1: California AG Compliance
```
TASK: File CT-1 Registration
URL: https://oag.ca.gov/charities/initial-reg
DEADLINE: TODAY (you're already late)
DOCS NEEDED:
- IRS determination letter
- Articles of incorporation
- Bylaws
- $25 fee
FAIL STATE: "Delinquent" public status, fundraising frozen
```

### Day 2: D&O Insurance
```
TASK: Bind $1M D&O policy
PROVIDERS: 
- Nonprofits Insurance Alliance
- Philadelphia Insurance
- Great American
COST: $600-1,200/year
FAIL STATE: Board members personally liable
```

### Day 3: Nonprofit CPA
```
TASK: Engage CPA with 501(c)(3) expertise
INTERVIEW QUESTIONS:
- How many 990s filed last year?
- UBIT experience?
- Cost for quarterly reviews?
BUDGET: $5,000-10,000/year
FAIL STATE: IRS revocation, UBIT penalties
```

## 📊 Real Numbers (Not Fantasies)

### Year 1 Cash Flow Reality
```
MONTH 1-3: -$10,000 (setup costs)
MONTH 4-6: +$5,000 (friends/family)
MONTH 7-9: +$15,000 (small foundation)
MONTH 10-12: +$25,000 (year-end giving)
TOTAL YEAR 1: $35,000 revenue, $50,000 expenses
RUNWAY REQUIRED: 12 months personal savings
```

### True Cost Per Dollar Raised
```
Direct Mail: $1.25 per $1 (Year 1)
Digital Ads: $1.50 per $1 (Year 1)
Events: $0.75 per $1
Grants: $0.25 per $1 (80-200 hours)
Major Gifts: $0.10 per $1 (relationships)
```

### UBIT Risk Matrix (Conservative)
```
Monthly Giving: SAFE (0% UBIT)
Foundation Grants: SAFE (0% UBIT)
Everything Else: ASSUME 35% TAX
```

## 🛠️ Technical Drift Monitoring

### Daily Automated Checks
```bash
#!/bin/bash
# Add to crontab: 0 9 * * * /path/to/daily-check.sh

# Check if configs exist
test -f ~/.zshrc || echo "ALERT: .zshrc missing"
test -f "$HOME/Library/Application Support/Claude/claude_desktop_config.json" || echo "ALERT: MCP config missing"

# Check if aliases work
zsh -ic 'type recovery-setup' || echo "ALERT: Aliases broken"

# Email results
mail -s "Recovery Compass Daily Check" you@example.com < results.log
```

### Weekly Manual Verification
- [ ] MCP servers connect in Claude
- [ ] All API keys accessible
- [ ] Bank balance > 6 months runway
- [ ] No AG/IRS notices
- [ ] Board insurance current

## 📅 Compliance Calendar (Set Reminders NOW)

### Monthly
- Day 1: Bank reconciliation
- Day 5: Donor acknowledgments complete
- Day 10: Board packet distributed
- Day 15: Compliance checklist review
- Day 20: Cash flow update
- Day 30: 990 preparation check

### Quarterly
- CPA UBIT review
- Board meeting (documented)
- Insurance premium payment
- SAM.gov renewal check

### Annual
- January: 1099s issued
- February: W-2s filed
- May 15: 990 deadline (extended)
- November: RRF-1 (CA renewal)
- December: Audit planning

## 🔥 When Things Break (Not If)

### MCP Breaks
```bash
# Manual recovery (memorize this)
mkdir -p "$HOME/Library/Application Support/Claude"
echo '{"mcpServers":{"filesystem":{"command":"npx","args":["-y","@modelcontextprotocol/server-filesystem","/Users/ericjones/Documents"]}}}' > "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
```

### Aliases Disappear
```bash
# Re-add to .zshrc manually
echo 'alias recovery-setup="source ~/.recovery_compass_setup.sh"' >> ~/.zshrc
echo 'alias fix-mcp="~/.fix_mcp.sh"' >> ~/.zshrc
source ~/.zshrc
```

### Compliance Emergency
```
1. STOP all operations
2. Call nonprofit attorney
3. Document everything
4. Prepare for audit
5. Notify insurance carrier
```

## 💰 Survival Budget (Realistic)

### Minimum Monthly Burn
```
Compliance/Legal: $1,500
Insurance: $300
Accounting: $500
Operations: $500
Total: $2,800/month minimum

Annual Minimum: $33,600
Add Programs: Double it
Add Staff: Triple it
```

### Funding Sources (Ranked by Reality)
1. **Your savings** (100% reliable)
2. **Board giving** (75% reliable)
3. **Friends/family** (50% reliable)
4. **Local foundations** (10% chance)
5. **Earned revenue** (UBIT nightmare)
6. **Federal grants** (3% chance, Year 3+)

## ✅ Success Metrics (Survival Mode)

Track daily:
- Days of cash remaining
- Days since last filing
- Number of active donors
- Compliance checklist %

Ignore:
- Social media followers
- Website traffic  
- Press mentions
- Award applications

## 🎯 The Brutal Truth

**Year 1**: You'll lose money. Budget for it.
**Year 2**: You might break even. Maybe.
**Year 3**: Sustainable if you survive.
**Year 5**: Growth possible. Not guaranteed.

**Failure points**:
- 30% fail by Year 10 (sector average)
- 50% of those fail on compliance
- 30% fail on cash flow
- 20% fail on board/leadership

## 📋 Print This Section

### Emergency Contacts
- Nonprofit Attorney: ________________
- CPA: ________________
- Insurance Agent: ________________
- Board Chair: ________________
- Major Donor: ________________

### Critical Passwords (Store Separately)
- IRS: ________________
- CA AG: ________________
- SAM.gov: ________________
- Bank: ________________

### If You're Reading This in Crisis
1. Check bank balance
2. Check compliance calendar
3. Call your attorney
4. Document everything
5. Don't panic (but move fast)

---

**Remember**: Optimism founded the nonprofit. Paranoia will keep it alive.

Last Updated: January 29, 2025
Next Update: When something breaks (probably next week)
Print Date: _____________
