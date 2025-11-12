# Admin Panel Quick Start Guide

## 🚀 Quick Access

### Super Admin Login (Instant Access)
If you're one of the 3 super admins, you can access the admin panel immediately:

**Protected Emails:**
- dinesh.srivastava@vmart.co.in
- ds.250474@gmail.com
- dineshsrivastava07@gmail.com

**Access URL:** http://localhost:8000/admin/dashboard

---

## 📋 Common Tasks

### 1. Approve a New User

**Steps:**
1. Open admin dashboard: http://localhost:8000/admin/dashboard
2. Click **"Pending Approvals"** tab
3. Find the user in the list
4. Click **"✓ Approve"** button
5. User receives verification email
6. User clicks email link → Account activated

### 2. Suspend a User (Temporary Block)

**Steps:**
1. Go to **"Users"** tab
2. Find the user
3. Click **"⏸ Suspend"** button
4. Enter reason for suspension
5. Click "Confirm"
6. User immediately blocked from chatbot

**Effect:** User sees "Your account has been suspended" message

### 3. Delist a User (Permanent Removal)

**⚠️ WARNING: This action is IRREVERSIBLE**

**Steps:**
1. Go to **"Users"** tab
2. Find the user
3. Click **"🚫 Delist"** button
4. Confirm the warning
5. Enter reason for delisting
6. User permanently removed

**Effect:** User cannot access chatbot, cannot be reactivated

### 4. Assign Data Access Policy

**Example: Give user access to 3 stores**

**Steps:**
1. Find user in **"Users"** tab
2. Click **"🔐 Policies"** button
3. Click **"+ Add Policy"**
4. Configure policy:
   ```json
   Access Level: Store
   Stores: VM_DL_001, VM_DL_002, VM_DL_003
   
   Permissions:
   ✓ View Data
   ✓ Upload Files
   ✓ Use Data Catalogue
   ✗ Export Data
   ✓ View Analytics
   ```
5. Click **"Save Policy"**

**Effect:** User can only see data for these 3 stores in chatbot

### 5. Reactivate Suspended User

**Steps:**
1. Filter users by **"Suspended"** status
2. Find the user
3. Click **"▶ Reactivate"** button
4. Confirm reactivation
5. User can login again

---

## 🔐 Access Levels Explained

### Simple Use Cases

#### Store Manager
**Access:** 1 store only
```
Level: Store
Values: ["VM_DL_001"]
```

#### Regional Manager
**Access:** All stores in North zone
```
Level: Zone
Values: {"zones": ["North"]}
```

#### Category Manager
**Access:** All stores, only Apparel division
```
Level: HO
Values: {
  "divisions": ["Apparel"],
  "departments": ["Menswear", "Womenswear"]
}
```

#### City Manager
**Access:** All stores in Delhi
```
Level: City
Values: {"cities": ["Delhi"]}
```

---

## ⚡ Quick Actions

### Bulk Operations

#### Approve All Verified Users
1. **Pending Approvals** tab
2. Select all users (Ctrl+A)
3. Click **"Approve Selected"** (future feature)

#### Export User List
1. **Users** tab
2. Click **"Export CSV"** button
3. Opens in Excel

---

## 🛠️ Troubleshooting

### User Can't Login
**Check:**
- [ ] Email verified?
- [ ] Admin approved?
- [ ] Not suspended/delisted?
- [ ] At least one active policy?

**Fix:** Go to Users tab → Check user status → Take appropriate action

### Super Admin Blocked
**Should NEVER happen!** Super admins bypass all checks.

**If it does:**
1. Check server logs
2. Verify email matches SUPER_ADMINS list exactly
3. Restart server

### Email Not Received
**Check:**
- Spam folder
- SMTP configured correctly
- Email service running

**Workaround:** Admin manually approves (skip email verification)

---

## 📊 Dashboard Overview

### Statistics Panel (Top)
- **Total Users**: All registered
- **Pending**: Awaiting approval
- **Approved**: Active users
- **Suspended**: Temporarily blocked

### Users Tab
**Columns:**
- Email
- Name
- Role (User/Admin/Super Admin)
- Status (Badge color-coded)
- Email Verified (✓/✗)
- Created Date
- Actions (Buttons)

**Filters:**
- All
- Pending
- Verified
- Approved
- Suspended
- Delisted

### Pending Approvals Tab
**Quick view of users awaiting approval**

Shows only:
- Users with status "Verified"
- Quick approve/reject actions

### Logs Tab
**Activity monitoring**

Shows:
- All admin actions
- User logins
- Policy changes
- Suspensions/reactivations

**Filters:**
- Date range
- User email
- Action type

---

## 🎯 Best Practices

### For Super Admins

1. **Review Pending Users Daily**
   - Check pending approvals tab every morning
   - Verify email domains match company

2. **Assign Least Privilege**
   - Only grant necessary access
   - Start with minimal permissions
   - Expand as needed

3. **Monitor Suspicious Activity**
   - Check logs weekly
   - Watch for failed login attempts
   - Investigate unusual data access

4. **Document Actions**
   - Always provide reasons when suspending
   - Add notes to delisting actions
   - Maintain audit trail

5. **Regular Policy Review**
   - Review user policies quarterly
   - Remove inactive users
   - Update access as roles change

### For Regular Admins

1. **Verify Before Approving**
   - Confirm user identity
   - Check email domain
   - Verify role/department

2. **Use Suspend First**
   - Don't delist unless absolutely necessary
   - Suspend for investigation
   - Reactivate if resolved

3. **Clear Communication**
   - Inform users of suspension reasons
   - Provide reactivation timeline
   - Document decisions

---

## 📞 Quick Reference

### URLs
- **Admin Dashboard:** http://localhost:8000/admin/dashboard
- **User Registration:** http://localhost:8000/admin/register
- **API Docs:** See docs/ADMIN_PANEL_GUIDE.md

### Super Admins
- dinesh.srivastava@vmart.co.in
- ds.250474@gmail.com
- dineshsrivastava07@gmail.com

### Status Meanings
- **Pending:** Registered, email not verified
- **Verified:** Email verified, awaiting admin approval
- **Approved:** Active, can use chatbot
- **Suspended:** Temporarily blocked (reversible)
- **Delisted:** Permanently removed (irreversible)

### Common Actions
- **Approve:** Grant access
- **Reject:** Deny access
- **Suspend:** Temporary block
- **Reactivate:** Restore access
- **Delist:** Permanent removal

---

## ⚙️ Configuration

### Email Service (Optional)
If you want to send verification emails:

1. Edit `.env` file:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

2. Restart server

### Database Backup
```bash
# Backup admin database
cp src/admin/data/admin.db src/admin/data/admin.db.backup

# Restore from backup
cp src/admin/data/admin.db.backup src/admin/data/admin.db
```

---

## 🆘 Emergency Procedures

### Reset All Users (Nuclear Option)
```bash
cd "/Users/dineshsrivastava/Ai Chatbot for Gemini LLM/V-Mart Personal AI Agent"
rm src/admin/data/admin.db
python main.py
# Database recreated, all users cleared except super admins
```

### Unlock Suspended User via Database
```bash
python -c "
from src.admin.database import get_admin_db
from src.admin.models import User, UserStatus

db = get_admin_db()
session = db.get_session()

user = session.query(User).filter(User.email == 'user@example.com').first()
user.status = UserStatus.APPROVED
user.force_logout = False
session.commit()
print('User unlocked!')
"
```

---

**Need Help?**
- 📖 Full Guide: docs/ADMIN_PANEL_GUIDE.md
- 📧 Contact: dinesh.srivastava@vmart.co.in
- 🐛 Report Issues: GitHub Issues

**Version:** 1.0  
**Last Updated:** November 12, 2025
