# Admin Panel Guide
**V-Mart AI Agent - Complete User Management & Access Control System**

## 📋 Table of Contents
1. [Overview](#overview)
2. [Super Admin Privileges](#super-admin-privileges)
3. [User Management](#user-management)
4. [Access Control Levels](#access-control-levels)
5. [Email Verification Workflow](#email-verification-workflow)
6. [Force-Stop Capability](#force-stop-capability)
7. [Admin Dashboard Usage](#admin-dashboard-usage)
8. [API Reference](#api-reference)

---

## 🎯 Overview

The Admin Panel provides comprehensive user management and data access control for the V-Mart AI Agent. It implements a **three-tier security model**:

### Key Features
- ✅ **Email Whitelist** - Pre-approval required before signup
- ✅ **Super Admin Protection** - 3 privileged emails bypass all restrictions
- ✅ **Force-Stop Capability** - Immediate access revocation for delisted users
- ✅ **10-Level Data Hierarchy** - Granular access control from HO to Article
- ✅ **Email Verification** - Secure token-based user activation
- ✅ **Activity Logging** - Complete audit trail of all admin actions
- ✅ **Role-Based Access** - Super Admin, Admin, and User roles

### Architecture
```
User Registration → Email Verification → Admin Approval → Access Policy Assignment → Chatbot Access
                                                                                    ↓
                                    Force-Stop (except Super Admins) ← User Delisting/Suspension
```

---

## 👑 Super Admin Privileges

### Protected Emails (No Restrictions)
Three emails have **unrestricted access** and **cannot be suspended or delisted**:

1. **dinesh.srivastava@vmart.co.in**
2. **ds.250474@gmail.com**
3. **dineshsrivastava07@gmail.com**

### Super Admin Capabilities
- ✅ **Full Data Access** - Access all stores, warehouses, zones, regions, etc.
- ✅ **User Management** - Approve, suspend, reactivate, or delist any user
- ✅ **Policy Creation** - Define 10-level access policies for users
- ✅ **Activity Monitoring** - View all user activity logs
- ✅ **Bypass Force-Stop** - Continue using chatbot even if delisted (protection mechanism)
- ✅ **No Email Verification** - Automatically approved on signup

### Super Admin Login
```bash
# Super admins can login directly at:
http://localhost:8000/admin/dashboard

# Or access chatbot immediately:
http://localhost:8000/ai-chat/
```

---

## 👥 User Management

### User Lifecycle States

| Status | Description | Can Access Chatbot? | Next Action |
|--------|-------------|-------------------|-------------|
| **Pending** | Registered but email not verified | ❌ No | User clicks email verification link |
| **Verified** | Email verified, awaiting admin approval | ❌ No | Admin approves or rejects |
| **Approved** | Admin approved, full access granted | ✅ Yes | User can use chatbot (subject to policies) |
| **Suspended** | Temporarily blocked | ❌ No | Admin can reactivate |
| **Delisted** | Permanently removed | ❌ No | Cannot be reactivated (except super admins) |

### User Approval Workflow

#### 1. User Registers
```
POST /admin/register
{
  "email": "user@vmart.co.in",
  "name": "John Doe",
  "password": "SecurePassword123"
}
```

**Response:**
- ✅ Success: Verification email sent
- ❌ Error: Email not in whitelist

#### 2. User Verifies Email
User clicks link in email → Token validated → Status: **Pending** → **Verified**

#### 3. Admin Approves
Admin dashboard → Pending Approvals tab → **Approve** button

**Actions:**
- `Approve` - Grant access, assign policies
- `Reject` - Deny access, optionally provide reason

#### 4. User Accesses Chatbot
Once approved, user can login and use AI chatbot with assigned data access policies.

---

## 🔐 Access Control Levels

### 10-Level Data Hierarchy

The admin panel supports **granular data access control** at 10 levels:

| Level | Description | Example Values |
|-------|-------------|----------------|
| **HO** | Head Office access | `["Delhi_HO", "Mumbai_HO"]` |
| **Warehouse** | Warehouse-level access | `["WH001", "WH002", "WH003"]` |
| **Zone** | Geographic zone | `["North", "South", "East", "West"]` |
| **Store** | Individual stores | `["VM_DL_001", "VM_MH_002"]` |
| **Region** | Regional access | `["NCR", "Maharashtra", "Karnataka"]` |
| **City** | City-level access | `["Delhi", "Mumbai", "Bangalore"]` |
| **State** | State-wide access | `["Delhi", "Maharashtra", "Karnataka"]` |
| **Division** | Product division | `["Apparel", "Footwear", "Accessories"]` |
| **Department** | Department access | `["Menswear", "Womenswear", "Kids"]` |
| **Article** | Specific articles | `["SHIRT_001", "TROUSER_002"]` |

### Policy Configuration

Each policy includes:
- **Access Level** - Which level to apply (Store, Zone, etc.)
- **Access Values** - Specific IDs/names for that level
- **Permissions** - What actions are allowed:
  - `can_view_data` - View data in chatbot responses
  - `can_upload_files` - Upload files to File Browser
  - `can_use_data_catalogue` - Access Data Catalogue feature
  - `can_export_data` - Export data to CSV/Excel
  - `can_view_analytics` - View analytics dashboards

### Example: Store-Level Policy

**Scenario:** User should only access 3 stores in Delhi

```json
{
  "user_id": 42,
  "access_level": "store",
  "access_values": {
    "stores": ["VM_DL_001", "VM_DL_002", "VM_DL_003"]
  },
  "can_view_data": true,
  "can_upload_files": true,
  "can_use_data_catalogue": true,
  "can_export_data": false,
  "can_view_analytics": true
}
```

**Result:** 
- User sees data only for these 3 Delhi stores
- Can upload files and use catalogue
- Cannot export data
- Can view analytics for these stores

### Example: Multi-Level Policy

**Scenario:** Regional Manager for North zone, all departments

```json
{
  "user_id": 42,
  "access_level": "zone",
  "access_values": {
    "zones": ["North"],
    "divisions": ["Apparel", "Footwear"],
    "departments": ["Menswear", "Womenswear", "Kids"]
  },
  "can_view_data": true,
  "can_upload_files": true,
  "can_use_data_catalogue": true,
  "can_export_data": true,
  "can_view_analytics": true
}
```

**Result:**
- Full access to all stores in North zone
- Only Apparel & Footwear divisions
- All departments within those divisions
- Can export data

---

## ✉️ Email Verification Workflow

### 1. Verification Email Sent
When admin approves a user:

```html
Subject: Verify Your Email - V-Mart AI Agent

Hello John Doe,

Please verify your email to activate your account:

https://vmart-ai.com/admin/verify-email?token=abc123xyz789...

This link expires in 24 hours.

Best regards,
V-Mart AI Agent Team
```

### 2. Token Structure
```python
{
  "token": "32-character secure random string",
  "user_id": 42,
  "created_at": "2025-11-12T10:00:00Z",
  "expires_at": "2025-11-13T10:00:00Z"  # 24 hours
}
```

### 3. Verification Process
```
User clicks link → Token validated → User status updated → Access granted
```

### 4. Token Validation Rules
- ✅ Token must exist in database
- ✅ Token must not be expired (< 24 hours old)
- ✅ Token must not be already used
- ❌ Invalid/expired token → Show error, option to request new token

---

## 🚫 Force-Stop Capability

### Immediate Access Revocation

When an admin **delists or suspends** a user, their access is **immediately revoked**:

### How Force-Stop Works

#### 1. Admin Action
```
Admin Dashboard → User Management → Select User → Suspend/Delist
```

#### 2. Database Update
```python
user.status = UserStatus.SUSPENDED  # or DELISTED
user.force_logout = True
db.session.commit()
```

#### 3. Middleware Check (Every Request)
```python
@AccessControl.check_user_access
def chatbot_endpoint():
    # Check runs before every chatbot request
    user = AccessControl.get_current_user()
    
    if not user:
        return {"error": "Unauthorized"}, 401
    
    if user.get("status") == "suspended":
        return {"error": "Your account has been suspended"}, 403
    
    if user.get("status") == "delisted":
        return {"error": "Your account has been removed"}, 403
    
    # ... proceed with request
```

#### 4. User Experience
```
User attempts to use chatbot →
Middleware checks status →
Status is SUSPENDED/DELISTED →
Return 403 Forbidden →
User sees: "Your account has been suspended. Contact admin."
```

### Super Admin Exception

**Super admins CANNOT be force-stopped:**

```python
def check_user_status(email):
    # Super admin check FIRST
    if email in SUPER_ADMINS:
        return True  # Always allow
    
    # Check regular users
    user = get_user(email)
    if user.status in [SUSPENDED, DELISTED]:
        return False
    
    return True
```

### Suspend vs. Delist

| Action | Reversible? | Use Case |
|--------|-------------|----------|
| **Suspend** | ✅ Yes (Reactivate button) | Temporary block, investigation, policy violation |
| **Delist** | ❌ No (Permanent) | Security threat, terminated employee, severe violation |

---

## 💻 Admin Dashboard Usage

### Accessing Admin Dashboard

**URL:** `http://localhost:8000/admin/dashboard`

**Authentication Required:**
- Login with admin or super admin account
- Regular users cannot access admin panel

### Dashboard Tabs

#### 1. **Users Tab** (Default)
View all users with filtering:

**Columns:**
- Email
- Name
- Role (User, Admin, Super Admin)
- Status (Pending, Verified, Approved, Suspended, Delisted)
- Email Verified (✓/✗)
- Created Date
- Actions (Approve, Suspend, Delist, Reactivate, Policies)

**Actions:**
- **Filter by Status** - Dropdown to show only specific status
- **Approve** - Grant access to verified users
- **Reject** - Deny access with optional reason
- **Suspend** - Temporarily block user
- **Reactivate** - Restore suspended user
- **Delist** - Permanently remove user (⚠️ irreversible)
- **Policies** - Assign/manage data access policies

#### 2. **Pending Approvals Tab**
Quick view of users awaiting approval:

**Shows:**
- Email
- Name
- Created Date
- Email Verification Status
- Quick Actions (Approve, Reject)

#### 3. **Logs Tab**
Activity monitoring:

**Columns:**
- Timestamp
- User Email
- Action (Login, Approve User, Suspend User, etc.)
- Resource (Which user/policy affected)
- Status (Success ✓ / Failed ✗)

**Filter Options:**
- Date range
- User email
- Action type
- Success/failure

### Statistics Panel

Top of dashboard shows:
- **Total Users** - All registered users
- **Pending** - Awaiting approval
- **Approved** - Active users
- **Suspended** - Temporarily blocked users

---

## 📡 API Reference

### Authentication Endpoints

#### Register New User
```http
POST /admin/register
Content-Type: application/json

{
  "email": "user@vmart.co.in",
  "name": "John Doe",
  "password": "SecurePassword123"
}

Response: 201 Created
{
  "success": true,
  "message": "Registration successful. Please check your email for verification."
}
```

#### Verify Email
```http
GET /admin/verify-email?token=abc123xyz789...

Response: 302 Redirect → /admin/dashboard
Or: 200 OK with error message
```

### User Management Endpoints (Admin Only)

#### Get All Users
```http
GET /admin/users
Query Params:
  - status (optional): pending, verified, approved, suspended, delisted

Response: 200 OK
{
  "users": [
    {
      "id": 1,
      "email": "user@vmart.co.in",
      "name": "John Doe",
      "role": "user",
      "status": "verified",
      "email_verified": true,
      "is_super_admin": false,
      "created_at": "2025-11-12T10:00:00Z"
    }
  ]
}
```

#### Approve User
```http
POST /admin/users/{user_id}/approve

Response: 200 OK
{
  "success": true,
  "message": "User approved successfully"
}
```

#### Suspend User
```http
POST /admin/users/{user_id}/suspend
Content-Type: application/json

{
  "reason": "Policy violation"
}

Response: 200 OK
{
  "success": true,
  "message": "User suspended"
}
```

#### Delist User (Permanent)
```http
POST /admin/users/{user_id}/delist
Content-Type: application/json

{
  "reason": "Security threat"
}

Response: 200 OK
{
  "success": true,
  "message": "User permanently delisted. Access revoked immediately."
}
```

#### Reactivate User
```http
POST /admin/users/{user_id}/reactivate

Response: 200 OK
{
  "success": true,
  "message": "User reactivated"
}
```

### Policy Management Endpoints

#### Get User Policies
```http
GET /admin/users/{user_id}/policies

Response: 200 OK
{
  "policies": [
    {
      "id": 1,
      "access_level": "store",
      "access_values": {
        "stores": ["VM_DL_001", "VM_DL_002"]
      },
      "can_view_data": true,
      "can_upload_files": true,
      "can_use_data_catalogue": true,
      "can_export_data": false,
      "can_view_analytics": true,
      "is_active": true
    }
  ]
}
```

#### Create Policy
```http
POST /admin/users/{user_id}/policies
Content-Type: application/json

{
  "access_level": "store",
  "access_values": {
    "stores": ["VM_DL_001", "VM_DL_002", "VM_DL_003"]
  },
  "can_view_data": true,
  "can_upload_files": true,
  "can_use_data_catalogue": true,
  "can_export_data": false,
  "can_view_analytics": true
}

Response: 201 Created
{
  "success": true,
  "policy_id": 42
}
```

#### Delete Policy
```http
DELETE /admin/policies/{policy_id}

Response: 200 OK
{
  "success": true,
  "message": "Policy deleted"
}
```

### Activity Logs

#### Get Logs
```http
GET /admin/logs
Query Params:
  - limit (optional): Number of logs to return (default 100)
  - user_email (optional): Filter by user email
  - action (optional): Filter by action type

Response: 200 OK
{
  "logs": [
    {
      "timestamp": "2025-11-12T10:15:30Z",
      "user_email": "admin@vmart.co.in",
      "action": "approve_user",
      "resource": "user@vmart.co.in",
      "success": true,
      "ip_address": "192.168.1.100"
    }
  ]
}
```

---

## 🛡️ Security Best Practices

### For Super Admins
1. ✅ **Protect Super Admin Emails** - Never share credentials
2. ✅ **Use Strong Passwords** - At least 12 characters, mixed case, numbers, symbols
3. ✅ **Regular Audits** - Review activity logs weekly
4. ✅ **Immediate Action** - Suspend suspicious accounts immediately

### For Regular Admins
1. ✅ **Verify User Identity** - Confirm email domain matches company
2. ✅ **Assign Least Privilege** - Grant minimum required access
3. ✅ **Document Changes** - Add reasons when suspending/delisting
4. ✅ **Monitor Activity** - Watch for unusual patterns

### For Users
1. ✅ **Secure Passwords** - Use password manager
2. ✅ **Don't Share Accounts** - Each user needs own login
3. ✅ **Report Issues** - Contact admin if access denied
4. ✅ **Respect Policies** - Stay within assigned access levels

---

## 📊 Monitoring & Reporting

### Key Metrics to Track

1. **User Growth**
   - New registrations per week
   - Approval rate
   - Active users

2. **Security Events**
   - Failed login attempts
   - Suspended accounts
   - Policy violations

3. **Access Patterns**
   - Most accessed stores
   - Data export frequency
   - Feature usage (File Browser, Data Catalogue, Analytics)

4. **Performance**
   - Average approval time
   - Support tickets
   - User satisfaction

---

## 🚨 Troubleshooting

### Common Issues

#### 1. User Cannot Access Chatbot
**Symptoms:** Error "Unauthorized" or "Access Denied"

**Check:**
- ✅ User status is "Approved"
- ✅ Email is verified
- ✅ At least one active policy assigned
- ✅ User not suspended/delisted

**Fix:** Admin dashboard → Users → Find user → Check status → Approve if needed

#### 2. Super Admin Being Blocked
**Should Never Happen!** Super admins bypass all checks.

**If Occurs:**
- Check `SUPER_ADMINS` list in `src/admin/models.py`
- Verify email matches exactly (case-insensitive)
- Check server logs for errors

#### 3. Verification Email Not Received
**Causes:**
- Email in spam folder
- Email service not configured
- Token expired

**Fix:**
- Check spam folder
- Admin can manually approve: Skip verification step
- Request new verification email

#### 4. Force-Stop Not Working
**Check:**
- User status updated in database
- User is not a super admin
- Session cleared (user should re-login)

**Fix:** Admin updates status → User clears browser cache → User re-login

---

## 📞 Support

### For Super Admins
- **Email:** dinesh.srivastava@vmart.co.in
- **Backup:** ds.250474@gmail.com
- **Emergency:** dineshsrivastava07@gmail.com

### For Regular Users
- Contact your admin for access issues
- Check email for verification links
- Review assigned policies in user profile

---

## 🔄 Updates & Changelog

### Version 1.0 (Current)
- ✅ Complete admin panel
- ✅ Super admin protection
- ✅ 10-level data hierarchy
- ✅ Force-stop capability
- ✅ Email verification
- ✅ Activity logging

### Planned Features
- 🔜 Bulk user import
- 🔜 Policy templates
- 🔜 Advanced analytics
- 🔜 Mobile app admin panel

---

**Developed by:** DSR  
**Powered by:** Gemini AI  
**Last Updated:** November 12, 2025
