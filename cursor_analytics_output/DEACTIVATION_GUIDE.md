# 🔐 User Deactivation Guide

**Complete guide to deactivating Cursor AI users while preserving all historical data**

---

## 📋 **Quick Start**

### Initialize the Deactivation System
```bash
cd /Users/whighley/cursor_analytics_project
python3 deactivate_user.py list
```

This creates the `user_deactivations` table if it doesn't exist.

---

## 🎯 **Common Tasks**

### 1. Deactivate a Single User
```bash
python3 deactivate_user.py deactivate jdoe@insulet.com "Never used license" "William Highley"
```

**With optional notes:**
```bash
python3 deactivate_user.py deactivate jdoe@insulet.com "Minimal usage" "William Highley" "Last active Oct 9, only 2 days total"
```

### 2. Bulk Deactivate from CSV
```bash
python3 deactivate_user.py bulk cursor_analytics_output/recoverable_licenses.csv "License optimization Q4 2025" "William Highley"
```

### 3. List All Deactivated Users
```bash
python3 deactivate_user.py list
```

### 4. Check User Info
```bash
python3 deactivate_user.py info jdoe@insulet.com
```

### 5. Reactivate a User
```bash
python3 deactivate_user.py reactivate jdoe@insulet.com "User rejoined team"
```

---

## 🏗️ **How It Works**

### What Happens When You Deactivate
1. ✅ **Sets `has_license = 0`** in ALL historical records for that user
2. ✅ **Records deactivation** in `user_deactivations` table with:
   - Deactivation date
   - Reason
   - Who deactivated them
   - Their final usage stats
   - Optional notes
3. ✅ **Preserves ALL historical data**:
   - `daily_usage_records` - untouched
   - `team_members_history` - untouched except `has_license` flag
   - All other tables - untouched

### What Is Preserved
```
✅ All daily activity records
✅ All lines of code generated
✅ All requests (agent, chat, composer)
✅ All cost center history
✅ Team member snapshot history
✅ Contribution to team totals
✅ Historical reports and trends
```

### What Changes
```
❌ has_license flag set to 0
❌ Won't count in "Current Active Licenses"
❌ Shows as "Deactivated" in reports
```

---

## 📊 **Database Schema**

### New Table: `user_deactivations`

```sql
CREATE TABLE user_deactivations (
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(100),
    email VARCHAR(200),
    name VARCHAR(200),
    deactivation_date DATE,
    deactivation_reason VARCHAR(500),
    cost_center VARCHAR(100),
    total_active_days INTEGER,
    total_ai_lines INTEGER,
    last_activity_date DATE,
    deactivated_by VARCHAR(200),
    notes TEXT,
    created_at DATETIME
)
```

### Updated Field: `team_members_history.has_license`
- `1` = Active license
- `0` = Deactivated (no license)

---

## 🔍 **Useful SQL Queries**

### Count Active vs Deactivated Licenses
```sql
SELECT 
    has_license,
    CASE 
        WHEN has_license = 1 THEN 'Active'
        ELSE 'Deactivated'
    END as status,
    COUNT(DISTINCT user_id) as user_count
FROM team_members_history
WHERE (user_id, snapshot_date) IN (
    SELECT user_id, MAX(snapshot_date)
    FROM team_members_history
    GROUP BY user_id
)
GROUP BY has_license;
```

### Get Deactivation Summary by Cost Center
```sql
SELECT 
    d.cost_center,
    COUNT(*) as deactivated_count,
    SUM(d.total_active_days) as total_active_days,
    SUM(d.total_ai_lines) as total_ai_lines,
    GROUP_CONCAT(d.email, ', ') as users
FROM user_deactivations d
INNER JOIN team_members_history tm ON d.user_id = tm.user_id
WHERE tm.has_license = 0
    AND (tm.user_id, tm.snapshot_date) IN (
        SELECT user_id, MAX(snapshot_date)
        FROM team_members_history
        GROUP BY user_id
    )
GROUP BY d.cost_center
ORDER BY deactivated_count DESC;
```

### Recently Deactivated (Last 30 Days)
```sql
SELECT 
    name,
    email,
    cost_center,
    deactivation_date,
    deactivation_reason,
    total_active_days,
    total_ai_lines,
    deactivated_by
FROM user_deactivations
WHERE deactivation_date >= date('now', '-30 days')
ORDER BY deactivation_date DESC;
```

### Users Deactivated But Still in API (Need Portal Removal)
```sql
SELECT 
    tm.name,
    tm.email,
    tm.cost_center,
    d.deactivation_date,
    d.deactivation_reason
FROM team_members_history tm
INNER JOIN user_deactivations d ON tm.user_id = d.user_id
WHERE tm.has_license = 0
    AND tm.snapshot_date = (SELECT MAX(snapshot_date) FROM team_members_history)
    AND tm.is_active = 1  -- Still appearing in API responses
ORDER BY d.deactivation_date;
```

### Calculate Monthly Savings from Deactivations
```sql
SELECT 
    strftime('%Y-%m', deactivation_date) as month,
    COUNT(*) as users_deactivated,
    COUNT(*) * 360 as annual_savings,
    COUNT(*) * 30 as monthly_savings
FROM user_deactivations
GROUP BY month
ORDER BY month DESC;
```

### Deactivation Reasons Breakdown
```sql
SELECT 
    deactivation_reason,
    COUNT(*) as count,
    ROUND(AVG(total_active_days), 1) as avg_active_days,
    ROUND(AVG(total_ai_lines), 0) as avg_ai_lines
FROM user_deactivations
GROUP BY deactivation_reason
ORDER BY count DESC;
```

---

## 📈 **Updated Dashboard Queries**

### Current Active License Count (Excluding Deactivated)
```sql
SELECT COUNT(DISTINCT user_id) as active_licenses
FROM team_members_history
WHERE (user_id, snapshot_date) IN (
    SELECT user_id, MAX(snapshot_date)
    FROM team_members_history
    GROUP BY user_id
)
AND has_license = 1;
```

### Cost Center License Breakdown (Active Only)
```sql
SELECT 
    COALESCE(cost_center, 'Unassigned') as cost_center,
    COUNT(DISTINCT user_id) as licensed_users
FROM team_members_history
WHERE (user_id, snapshot_date) IN (
    SELECT user_id, MAX(snapshot_date)
    FROM team_members_history
    GROUP BY user_id
)
AND has_license = 1
GROUP BY cost_center
ORDER BY licensed_users DESC;
```

---

## 🔄 **Workflow for License Recovery**

### Phase 1: Mark Users for Deactivation (Database)
```bash
# Deactivate 26 never-used licenses
python3 deactivate_user.py bulk tier1_never_used.csv "Never used - License recovery Q4 2025" "William Highley"

# Deactivate 15 minimal usage licenses
python3 deactivate_user.py bulk tier2_minimal.csv "Minimal usage - Last active before Nov 1" "William Highley"
```

### Phase 2: Remove from Cursor Portal
1. Log into cursor.com/settings
2. Navigate to Team Management
3. For each deactivated user:
   - Click user name
   - Click "Remove from Team"
   - Confirm removal

### Phase 3: Verify Deactivation
```bash
# List all deactivated users
python3 deactivate_user.py list

# Check they're marked correctly
sqlite3 cursor_analytics.db "SELECT name, email, deactivation_date FROM user_deactivations WHERE deactivation_date = date('now');"
```

### Phase 4: Generate Reports
```bash
# Regenerate dashboard (will show updated license counts)
python3 generate_interactive_dashboard.py

# Check savings
sqlite3 cursor_analytics.db "SELECT COUNT(*) * 360 as annual_savings FROM user_deactivations WHERE deactivation_date >= date('now', '-7 days');"
```

---

## 📊 **Reporting Examples**

### Monthly Deactivation Report
```sql
SELECT 
    strftime('%Y-%m', d.deactivation_date) as month,
    COUNT(DISTINCT d.user_id) as users_deactivated,
    SUM(d.total_ai_lines) as ai_lines_lost,
    COUNT(*) * 30 as monthly_savings_dollars,
    GROUP_CONCAT(DISTINCT d.deactivation_reason) as reasons
FROM user_deactivations d
WHERE d.deactivation_date >= date('now', '-90 days')
GROUP BY month
ORDER BY month DESC;
```

### Cost Center Impact Analysis
```sql
SELECT 
    d.cost_center,
    COUNT(*) as deactivations,
    COUNT(*) * 360 as annual_savings,
    ROUND(AVG(d.total_active_days), 1) as avg_usage_before_deactivation,
    MAX(d.deactivation_date) as most_recent
FROM user_deactivations d
GROUP BY d.cost_center
ORDER BY annual_savings DESC;
```

---

## ⚠️ **Important Notes**

### Before Deactivating
- ✅ Export user data (CSV already created)
- ✅ Notify the user (email templates provided)
- ✅ Get manager approval if required
- ✅ Document reason clearly

### After Deactivating
- ✅ Remove from Cursor portal within 1 week
- ✅ Update any access lists or documentation
- ✅ Keep deactivation list for audit purposes
- ✅ Regenerate dashboard to show updated counts

### Reversing Deactivation
- ✅ Use `python3 deactivate_user.py reactivate <email>`
- ✅ Re-invite user in Cursor portal
- ✅ User gets fresh invitation email
- ✅ All historical data still intact

---

## 🎯 **Best Practices**

### Deactivation Reasons (Standardized)
Use consistent reasons for easy reporting:
- `"Never used license"`
- `"Minimal usage - inactive 30+ days"`
- `"Role change - no longer developing"`
- `"Left company"`
- `"Duplicate account"`
- `"License optimization Q4 2025"`

### Tracking
- Document who approved the deactivation
- Include last activity date in notes
- Note any special circumstances
- Keep CSV of bulk operations

### Timing
- Deactivate in database immediately after decision
- Remove from portal within 1 week
- Savings start next billing cycle
- Keep records for 1 year minimum

---

## 🔧 **Troubleshooting**

### "User not found"
- Check email spelling
- Verify user exists: `python3 deactivate_user.py info <email>`
- Check if user is in `team_members_history` table

### "User already deactivated"
- Check status: `python3 deactivate_user.py list`
- User may have been deactivated earlier
- Use reactivate command if needed

### Bulk operation failing
- Verify CSV has `email` column
- Check CSV format (UTF-8, comma-separated)
- Run individual test first
- Check terminal output for specific errors

---

## 📞 **Quick Reference**

| Command | Purpose |
|---------|---------|
| `deactivate <email> <reason> <name>` | Deactivate single user |
| `bulk <csv> <reason> <name>` | Deactivate multiple users |
| `reactivate <email>` | Restore user license |
| `list` | Show all deactivated users |
| `info <email>` | Get user details |

---

## 💰 **Financial Tracking**

### Calculate Total Savings
```bash
# Since specific date
sqlite3 cursor_analytics.db "SELECT COUNT(*) || ' users = $' || (COUNT(*) * 360) || '/year' FROM user_deactivations WHERE deactivation_date >= '2025-11-01';"

# All time
sqlite3 cursor_analytics.db "SELECT COUNT(*) || ' users = $' || (COUNT(*) * 360) || '/year' FROM user_deactivations;"
```

### Monthly Savings Trend
```bash
sqlite3 cursor_analytics.db -header -column "SELECT strftime('%Y-%m', deactivation_date) as month, COUNT(*) as users, '$' || (COUNT(*) * 30) as monthly_savings FROM user_deactivations GROUP BY month ORDER BY month;"
```

---

**Last Updated:** November 18, 2025  
**Database:** cursor_analytics.db  
**Script:** deactivate_user.py

