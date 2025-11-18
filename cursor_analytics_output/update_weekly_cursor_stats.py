import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Paths
DATA_PATH = Path(__file__).parent
KPI_FILE = DATA_PATH / "ultimate_cursor_kpis_data.json"
COMP_FILE = DATA_PATH / "comprehensive_cursor_data.json"
REPORT_FILE = DATA_PATH / "weekly_cursor_extended_stats_report.md"

# Load data
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def get_week_ranges(start, end):
    # Returns list of (week_start, week_end) tuples
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    weeks = []
    curr = start_dt
    while curr < end_dt:
        week_end = min(curr + timedelta(days=6), end_dt)
        weeks.append((curr, week_end))
        curr = week_end + timedelta(days=1)
    return weeks

def parse_daily_records(comp_data):
    # Extract daily usage records from admin_api > daily_usage > data
    try:
        return comp_data['admin_api']['daily_usage']['data']
    except Exception:
        # fallback: flatten all lists in the dict (legacy behavior)
        daily = []
        for k, v in comp_data.items():
            if isinstance(v, list):
                daily.extend(v)
            elif isinstance(v, dict):
                for vv in v.values():
                    if isinstance(vv, list):
                        daily.extend(vv)
        return daily

def aggregate_weekly_stats(daily, week_start, week_end):
    # Filter records for this week
    week_users = set()
    dau = defaultdict(set)
    dau_weekdays = defaultdict(set)  # Track weekdays only (Mon-Fri)
    feature_counts = defaultdict(int)
    lang_counts = defaultdict(int)
    proj_counts = defaultdict(int)
    accepts = rejects = lines_accepted = ai_requests = 0
    tabs_shown = tabs_accepted = 0
    composer_requests = chat_requests = agent_requests = 0
    tab_accept_rate = None
    # Convert week_start and week_end to datetime objects
    week_start_dt = datetime.strptime(week_start, "%Y-%m-%d")
    week_end_dt = datetime.strptime(week_end, "%Y-%m-%d")
    for rec in daily:
        day = rec.get('day') or rec.get('date')
        if day is None:
            continue  # skip records with missing date
        # Convert day to datetime object
        if isinstance(day, int):
            # Assume ms timestamp
            day_dt = datetime.utcfromtimestamp(day/1000)
        else:
            try:
                day_dt = datetime.strptime(day, "%Y-%m-%d")
            except Exception:
                continue  # skip if date format is not as expected
        if not (week_start_dt <= day_dt <= week_end_dt):
            continue
        uid = rec.get('userId')
        
        # Check if user has AI activity (same logic as weekly_users_report)
        has_ai_activity = (
            rec.get('acceptedLinesAdded', 0) > 0 or
            rec.get('totalAccepts', 0) > 0 or
            rec.get('totalTabsAccepted', 0) > 0 or
            rec.get('composerRequests', 0) > 0 or
            rec.get('chatRequests', 0) > 0 or
            rec.get('agentRequests', 0) > 0
        )
        
        # Only count users with AI activity for DAU/WAU
        if has_ai_activity:
            week_users.add(uid)
            dau[day].add(uid)
            # Track weekdays separately (Monday=0, Sunday=6)
            if day_dt.weekday() < 5:  # Monday (0) through Friday (4)
                dau_weekdays[day].add(uid)
        accepts += rec.get('totalAccepts', 0)
        rejects += rec.get('totalRejects', 0)
        lines_accepted += rec.get('acceptedLinesAdded', 0)
        ai_requests += sum([rec.get('agentRequests', 0), rec.get('composerRequests', 0), rec.get('chatRequests', 0)])
        tabs_shown += rec.get('totalTabsShown', 0)
        tabs_accepted += rec.get('totalTabsAccepted', 0)
        composer_requests += rec.get('composerRequests', 0)
        chat_requests += rec.get('chatRequests', 0)
        agent_requests += rec.get('agentRequests', 0)
        lang = rec.get('applyMostUsedExtension')
        if lang:
            lang_counts[lang] += 1
        proj = rec.get('tabMostUsedExtension')
        if proj:
            proj_counts[proj] += 1
        # Feature usage
        if rec.get('agentRequests', 0):
            feature_counts['Agent'] += 1
        if rec.get('composerRequests', 0):
            feature_counts['Composer'] += 1
        if rec.get('chatRequests', 0):
            feature_counts['Chat'] += 1
        if rec.get('totalTabsAccepted', 0):
            feature_counts['Tab'] += 1
        # Try to get tab accept rate if present
        if rec.get('tabAcceptRate') is not None:
            tab_accept_rate = rec.get('tabAcceptRate')
    dau_count = [len(users) for users in dau.values()]
    dau_weekdays_count = [len(users) for users in dau_weekdays.values()]
    
    # Calculate Tabs Rejected and Total Tabs
    # If tab_accept_rate is not available, estimate from tabs_shown and tabs_accepted
    if tab_accept_rate is None:
        tab_accept_rate = (tabs_accepted / tabs_shown) if tabs_shown else 0
    total_tabs = int(round(tabs_accepted / tab_accept_rate)) if tab_accept_rate else tabs_accepted
    tabs_rejected = total_tabs - tabs_accepted
    return {
        'DAU_7day': sum(dau_count) // len(dau_count) if dau_count else 0,
        'DAU_5day': sum(dau_weekdays_count) // len(dau_weekdays_count) if dau_weekdays_count else 0,
        'WAU': len(week_users),
        'Accepts': accepts,
        'Rejects': rejects,
        'LinesAccepted': lines_accepted,
        'AIRequests': ai_requests,
        'TabsShown': tabs_shown,
        'TabsAccepted': tabs_accepted,
        'TabsRejected': tabs_rejected,
        'TotalTabs': total_tabs,
        'ComposerRequests': composer_requests,
        'ChatRequests': chat_requests,
        'AgentRequests': agent_requests,
        'FeatureUsage': dict(feature_counts),
        'LangBreakdown': dict(lang_counts),
        'ProjBreakdown': dict(proj_counts),
    }

def get_dynamic_weeks(daily):
    """Get dynamic week ranges based on actual data, matching weekly_users_report logic."""
    # Find min and max dates
    dates = []
    for rec in daily:
        day = rec.get('day') or rec.get('date')
        if day is None:
            continue
        if isinstance(day, int):
            day_dt = datetime.utcfromtimestamp(day/1000)
        else:
            try:
                day_dt = datetime.strptime(day, "%Y-%m-%d")
            except:
                continue
        dates.append(day_dt)
    
    if not dates:
        return []
    
    min_date = min(dates)
    max_date = max(dates)
    
    # Calculate 7-day periods
    weeks = []
    current_start = min_date
    week_num = 1
    
    while current_start <= max_date:
        current_end = min(current_start + timedelta(days=6), max_date)
        weeks.append({
            'week_num': week_num,
            'start': current_start,
            'end': current_end
        })
        current_start = current_end + timedelta(days=1)
        week_num += 1
    
    # Reverse to show most recent first
    return list(reversed(weeks))

def load_historical_data():
    """Load historical weekly extended stats data."""
    historical_file = DATA_PATH / "weekly_extended_stats_historical.json"
    if historical_file.exists():
        try:
            with open(historical_file, 'r') as f:
                data = json.load(f)
                print(f"📚 Loaded {len(data)} historical weeks from cache")
                return data
        except Exception as e:
            print(f"⚠️  Could not load historical data: {e}")
    return []

def save_historical_data(rows):
    """Save weekly extended stats data for historical tracking."""
    historical_file = DATA_PATH / "weekly_extended_stats_historical.json"
    try:
        with open(historical_file, 'w') as f:
            json.dump(rows, f, indent=2)
        print(f"💾 Saved {len(rows)} weeks to historical cache")
    except Exception as e:
        print(f"⚠️  Could not save historical data: {e}")

def main(update_current_only=True, week_start_str=None, week_end_str=None):
    kpi = load_json(KPI_FILE)
    comp = load_json(COMP_FILE)
    daily = parse_daily_records(comp)
    
    # Get dynamic week ranges matching weekly_users_report
    weeks = get_dynamic_weeks(daily)
    
    # Load historical data if updating current week only
    historical_rows = []
    if update_current_only:
        historical_rows = load_historical_data()
    
    rows = []
    
    if update_current_only and historical_rows and len(weeks) > 0:
        # Determine which week to update
        if week_start_str and week_end_str:
            # Use custom week dates
            week_start_dt = datetime.strptime(week_start_str, '%Y-%m-%d')
            week_end_dt = datetime.strptime(week_end_str, '%Y-%m-%d')
            
            # Find matching week or create custom week
            current_week = None
            for week in weeks:
                if week['start'] == week_start_dt and week['end'] == week_end_dt:
                    current_week = week
                    break
            
            # If no exact match, create a custom week entry
            if current_week is None:
                current_week = {
                    'week_num': 0,  # Custom week
                    'start': week_start_dt,
                    'end': week_end_dt
                }
                print(f"🔄 Updating custom week: {week_start_dt.strftime('%Y-%m-%d')} to {week_end_dt.strftime('%Y-%m-%d')}")
            else:
                print(f"🔄 Updating week {current_week['week_num']}: {week_start_dt.strftime('%Y-%m-%d')} to {week_end_dt.strftime('%Y-%m-%d')}")
        else:
            # Use the most recent week (first in list)
            current_week = weeks[0]
            print(f"🔄 Updating current week only: {current_week['start'].strftime('%Y-%m-%d')} to {current_week['end'].strftime('%Y-%m-%d')}")
        
        start = current_week['start'].strftime("%Y-%m-%d")
        end = current_week['end'].strftime("%Y-%m-%d")
        label = f"{current_week['start'].strftime('%b %d')} - {current_week['end'].strftime('%b %d, %Y')}"
        
        stats = aggregate_weekly_stats(daily, start, end)
        current_row = {
            'Dates': label,
            'DAU_5day': stats['DAU_5day'],
            'DAU_7day': stats['DAU_7day'],
            'WAU': stats['WAU'],
            'Accepts': stats['Accepts'],
            'Rejects': stats['Rejects'],
            'Lines Accepted': stats['LinesAccepted'],
            'AI Requests Total': stats['AIRequests'],
            'TabsShown': stats['TabsShown'],
            'TabsAccepted': stats['TabsAccepted'],
            'TabsRejected': stats['TabsRejected'],
            'TotalTabs': stats['TotalTabs'],
            'ComposerRequests': stats['ComposerRequests'],
            'ChatRequests': stats['ChatRequests'],
            'AgentRequests': stats['AgentRequests'],
            'Feature Usage Breakdown': stats['FeatureUsage'],
            'Requests/Accepts by Language': stats['LangBreakdown'],
            'Requests/Accepts by Project': stats['ProjBreakdown'],
        }
        
        # Add current week
        rows.append(current_row)
        
        # Add historical weeks (excluding current week if it exists)
        for hist_row in historical_rows:
            if hist_row['Dates'] != label:
                rows.append(hist_row)
        
    else:
        # Calculate all weeks (original behavior)
        print("📊 Calculating all weeks from scratch...")
        for week in weeks:
            start = week['start'].strftime("%Y-%m-%d")
            end = week['end'].strftime("%Y-%m-%d")
            label = f"{week['start'].strftime('%b %d')} - {week['end'].strftime('%b %d, %Y')}"
            
            stats = aggregate_weekly_stats(daily, start, end)
            # Fill in all fields for the report row
            row = {
                'Dates': label,
                'DAU_5day': stats['DAU_5day'],
                'DAU_7day': stats['DAU_7day'],
                'WAU': stats['WAU'],
                'Accepts': stats['Accepts'],
                'Rejects': stats['Rejects'],
                'Lines Accepted': stats['LinesAccepted'],
                'AI Requests Total': stats['AIRequests'],
                'TabsShown': stats['TabsShown'],
                'TabsAccepted': stats['TabsAccepted'],
                'TabsRejected': stats['TabsRejected'],
                'TotalTabs': stats['TotalTabs'],
                'ComposerRequests': stats['ComposerRequests'],
                'ChatRequests': stats['ChatRequests'],
                'AgentRequests': stats['AgentRequests'],
                'Feature Usage Breakdown': stats['FeatureUsage'],
                'Requests/Accepts by Language': stats['LangBreakdown'],
                'Requests/Accepts by Project': stats['ProjBreakdown'],
                # Add more fields as needed
            }
            rows.append(row)
    
    # Save historical data
    if update_current_only:
        save_historical_data(rows)
    # Output to markdown
    with open(REPORT_FILE, 'w') as f:
        f.write("# 📊 Weekly Cursor AI Extended Stats (Auto-Updated)\n\n")
        f.write("*Generated on: " + datetime.now().strftime("%Y-%m-%d") + "*\n\n")
        f.write("| Dates | DAU (5-day) | DAU (7-day) | WAU | Accepts | Rejects | Lines Accepted | AI Requests Total | Tabs Shown | Tabs Accepted | Tabs Rejected | Total Tabs | Composer Requests | Chat Requests | Agent Requests | Feature Usage Breakdown | Requests/Accepts by Language | Requests/Accepts by Project |\n")
        f.write("|-------|-------------|-------------|-----|---------|---------|----------------|-------------------|------------|---------------|--------------|------------|------------------|--------------|---------------|------------------------|-----------------------------|-----------------------------|\n")
        for row in rows:
            f.write(f"| {row['Dates']} | {row['DAU_5day']} | {row['DAU_7day']} | {row['WAU']} | {row['Accepts']} | {row['Rejects']} | {row['Lines Accepted']} | {row['AI Requests Total']} | {row['TabsShown']} | {row['TabsAccepted']} | {row['TabsRejected']} | {row['TotalTabs']} | {row['ComposerRequests']} | {row['ChatRequests']} | {row['AgentRequests']} | {row['Feature Usage Breakdown']} | {row['Requests/Accepts by Language']} | {row['Requests/Accepts by Project']} |\n")
        
        # Add field definitions
        f.write("\n## 📋 Field Definitions (Extended)\n")
        f.write("- **DAU (5-day)**: Average daily active AI users during **workweek only** (Monday-Friday). This provides a more accurate measure of business day activity.\n")
        f.write("- **DAU (7-day)**: Average daily active AI users across **all 7 days** (including weekends). Useful for seeing overall engagement.\n")
        f.write("- **WAU (Weekly Active AI Users)**: The total number of unique users with AI activity at least once during the week. This matches 'AI Users' in other reports.\n")
        f.write("- **Accepts**: Total number of AI suggestions accepted\n")
        f.write("- **Rejects**: Total number of AI suggestions rejected\n")
        f.write("- **Lines Accepted**: Total lines of code accepted from AI suggestions\n")
        f.write("- **AI Requests Total**: Total AI requests (Agent + Composer + Chat)\n")
        f.write("- **Tabs Shown**: Total tab completions shown to users\n")
        f.write("- **Tabs Accepted**: Total tab completions accepted by users\n")
        f.write("- **Tabs Rejected**: Total tab completions rejected (Tabs Shown - Tabs Accepted)\n")
        f.write("- **Total Tabs**: Total tab completion events\n")
        f.write("- **Composer/Chat/Agent Requests**: Breakdown of AI requests by feature type\n")
        f.write("- **Feature Usage Breakdown**: Count of users using each AI feature\n")
        f.write("- **Requests/Accepts by Language**: Breakdown by programming language file extension\n")
        f.write("- **Requests/Accepts by Project**: Breakdown by project or file type\n")
        f.write("\n### Notes:\n")
        f.write("- **AI Activity** includes: tab completions, composer requests, chat requests, agent requests, or code acceptance\n")
        f.write("- **5-day DAU** typically shows higher numbers than 7-day DAU since it excludes low-activity weekends\n")
        f.write("- **5-day DAU** is recommended for business metrics and comparing against team productivity\n")
        f.write("- DAU/WAU now match the 'AI Users' metric in the Weekly Users Report\n")
        f.write("- Week ranges are calculated dynamically from available data\n")
        f.write("\n---\n\n")
        f.write("*This report uses the same 7-day increments and AI activity definition as the Weekly Users Report.*\n")

if __name__ == "__main__":
    import sys
    # Check for --recalculate-all flag
    recalculate_all = '--recalculate-all' in sys.argv
    
    # Check for custom week dates
    week_start = None
    week_end = None
    for i, arg in enumerate(sys.argv):
        if arg == '--week-start' and i + 1 < len(sys.argv):
            week_start = sys.argv[i + 1]
        elif arg == '--week-end' and i + 1 < len(sys.argv):
            week_end = sys.argv[i + 1]
    
    main(update_current_only=not recalculate_all, week_start_str=week_start, week_end_str=week_end)
