# 🔐 Dashboard Authentication Guide

The interactive dashboard now includes admin authentication to protect sensitive user details.

---

## 🎯 Features

### Protected Content
- ✅ **User Activity Summary Table** - Shows individual user statistics
- ✅ User names, emails, activity levels, and detailed metrics
- ✅ All sortable columns with personal information

### Public Content (No Login Required)
- ✅ Overall team metrics (AI %, Agent Edits, Tab Completions, Messages)
- ✅ Aggregate charts and trends
- ✅ Time range filters
- ✅ High-level analytics

---

## 🔑 Default Credentials

**Default Password:** `admin123`

⚠️ **Important:** Change this password before sharing the dashboard!

---

## 🔄 How to Change Password

### Option 1: Automated (Recommended)

```bash
python3 change_dashboard_password.py
```

This interactive script will:
1. Prompt for your new password
2. Generate a secure hash
3. Automatically update the dashboard generator
4. Remind you to regenerate the dashboard

### Option 2: Manual

1. Generate your password hash:

```python
import hashlib
password = "your_new_password"
hash = hashlib.sha1(password.encode()).hexdigest()
print(hash)
```

2. Edit `generate_interactive_dashboard.py` (around line 1035):

```javascript
const AUTH_CONFIG = {
    passwordHash: 'YOUR_NEW_HASH_HERE',  // Replace this
    sessionKey: 'cursor_dashboard_auth',
    sessionTimeout: 8 * 60 * 60 * 1000
};
```

3. Regenerate the dashboard:

```bash
python3 generate_interactive_dashboard.py
```

---

## 🚀 Using the Dashboard

### First Time Access

1. Open the dashboard in your browser
2. You'll see a login screen with the lock icon 🔐
3. Enter the admin password (default: `admin123`)
4. Click "Login"

### After Login

- ✅ User details table will appear
- ✅ Admin badge (🔐 Admin Only) will be visible
- ✅ Logout button in the top-right corner
- ✅ Session persists for 8 hours

### To Logout

- Click the "🔓 Logout" button in the header
- Your session will be cleared
- Login screen will reappear

---

## 🛡️ Security Features

### Session Management
- **Duration:** 8 hours (28,800 seconds)
- **Storage:** Browser sessionStorage (cleared when tab closes)
- **Auto-expire:** Session automatically expires after timeout

### Password Security
- Passwords are hashed using SHA-1
- Original password is never stored
- Hash is compared client-side

### Best Practices

1. **Change Default Password Immediately**
   ```bash
   python3 change_dashboard_password.py
   ```

2. **Use Strong Passwords**
   - At least 12 characters
   - Mix of letters, numbers, symbols
   - Avoid common words

3. **Share Securely**
   - Send password through secure channel (not email)
   - Use password manager to share with team
   - Consider unique passwords per environment

4. **Regular Updates**
   - Change password periodically (every 90 days)
   - Change if team member leaves
   - Change if password may be compromised

---

## 🔧 Advanced Configuration

### Change Session Timeout

Edit `generate_interactive_dashboard.py` (around line 1037):

```javascript
sessionTimeout: 4 * 60 * 60 * 1000  // 4 hours instead of 8
```

Then regenerate the dashboard.

### Disable Authentication (Not Recommended)

If you need to disable authentication temporarily:

1. Comment out the login check in `generate_interactive_dashboard.py`
2. Or remove the `.protected-content` class from the user table

---

## 📊 What Users See

### Without Login
```
🎯 Cursor Analytics Dashboard
📅 Sept 3, 2025 to Nov 7, 2025 (65 days)

[Metrics Cards - Public]
🤖 AI Share of Code: 23.4%
✏️ Agent Edits: 12,345
⚡ Tab Completions: 45,678
💬 Messages Sent: 8,901

[Charts - Public]
[Interactive charts showing aggregate trends]

[Login Prompt Required for User Details]
```

### With Login
```
🎯 Cursor Analytics Dashboard        [🔓 Logout]
📅 Sept 3, 2025 to Nov 7, 2025 (65 days)

[All public content above, PLUS...]

👥 User Activity Summary 🔐 Admin Only
[Full sortable table with all user details]
```

---

## 🐛 Troubleshooting

### Can't Login / Forgot Password

1. Check console for errors (F12 → Console tab)
2. Verify password hash in the HTML source
3. Reset to default:
   - Edit `generate_interactive_dashboard.py`
   - Find line with `passwordHash`
   - Replace with: `'e38ad214943daad1d64c102faec29de4afe9da3d'`
   - Regenerate dashboard
   - Default password `admin123` will work

### Session Keeps Expiring

- Check your browser's sessionStorage settings
- Some privacy extensions block sessionStorage
- Try a different browser

### Login Screen Not Appearing

- Clear browser cache
- Regenerate the dashboard from scratch
- Check browser console for JavaScript errors

---

## 📝 Files Modified

- `generate_interactive_dashboard.py` - Added authentication system
- `change_dashboard_password.py` - New password management tool
- `cursor_analytics_output/interactive_dashboard.html` - Generated with auth

---

## 🎨 Next Steps

1. **Change the password:**
   ```bash
   python3 change_dashboard_password.py
   ```

2. **Test the login:**
   ```bash
   open cursor_analytics_output/interactive_dashboard.html
   ```

3. **Share with team:**
   - Send dashboard HTML file
   - Share password securely
   - Document where to find updates

---

**Created:** November 7, 2025  
**Dashboard Version:** v2.0 (with authentication)  
**Security Level:** Client-side authentication (suitable for internal tools)

