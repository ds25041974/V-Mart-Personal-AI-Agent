/**
 * Admin Dashboard JavaScript
 * Handles user management, approval workflows, and access control
 */

let currentUser = null;
let allUsers = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadUsers();
    loadStats();
});

// Tab Management
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active from all tabs
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
            
            // Add active to clicked tab
            tab.classList.add('active');
            const tabName = tab.getAttribute('data-tab');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Load data for tab
            if (tabName === 'pending') {
                loadPendingUsers();
            } else if (tabName === 'logs') {
                loadLogs();
            }
        });
    });
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/admin/users');
        const data = await response.json();
        
        if (data.users) {
            const stats = {
                total: data.users.length,
                pending: data.users.filter(u => u.status === 'pending' || u.status === 'verified').length,
                approved: data.users.filter(u => u.status === 'approved').length,
                suspended: data.users.filter(u => u.status === 'suspended').length
            };
            
            document.getElementById('stat-total').textContent = stats.total;
            document.getElementById('stat-pending').textContent = stats.pending;
            document.getElementById('stat-approved').textContent = stats.approved;
            document.getElementById('stat-suspended').textContent = stats.suspended;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load all users
async function loadUsers() {
    const tbody = document.getElementById('users-tbody');
    tbody.innerHTML = '<tr><td colspan="7" class="loading">Loading users...</td></tr>';
    
    try {
        const statusFilter = document.getElementById('status-filter').value;
        const url = statusFilter === 'all' ? '/admin/users' : `/admin/users?status=${statusFilter}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (!data.users || data.users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No users found</td></tr>';
            return;
        }
        
        allUsers = data.users;
        tbody.innerHTML = '';
        
        data.users.forEach(user => {
            const row = createUserRow(user);
            tbody.appendChild(row);
        });
        
        loadStats();
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="7" class="alert alert-error">Error loading users</td></tr>';
        console.error('Error:', error);
    }
}

// Create user table row
function createUserRow(user) {
    const tr = document.createElement('tr');
    
    const statusBadge = `<span class="badge badge-${user.status}">${user.status.toUpperCase()}</span>`;
    const roleBadge = user.is_super_admin 
        ? '<span class="badge badge-super">SUPER ADMIN</span>'
        : `<span class="badge">${user.role.toUpperCase()}</span>`;
    const verifiedBadge = user.email_verified 
        ? '<span style="color: #10b981;">✓</span>' 
        : '<span style="color: #ef4444;">✗</span>';
    
    let actions = '';
    if (user.is_super_admin) {
        actions = '<span style="color: #6b7280; font-size: 0.75rem;">Protected</span>';
    } else {
        actions = '<div class="action-buttons">';
        
        if (user.status === 'verified' || user.status === 'pending') {
            actions += `<button class="btn btn-success btn-sm" onclick="approveUser(${user.id})">✓ Approve</button>`;
            actions += `<button class="btn btn-danger btn-sm" onclick="showRejectModal(${user.id})">✗ Reject</button>`;
        }
        
        if (user.status === 'approved') {
            actions += `<button class="btn btn-warning btn-sm" onclick="suspendUser(${user.id})">⏸ Suspend</button>`;
            actions += `<button class="btn btn-danger btn-sm" onclick="showDelistModal(${user.id})">🚫 Delist</button>`;
        }
        
        if (user.status === 'suspended') {
            actions += `<button class="btn btn-success btn-sm" onclick="reactivateUser(${user.id})">▶ Reactivate</button>`;
        }
        
        actions += `<button class="btn btn-secondary btn-sm" onclick="showPolicyModal(${user.id})">🔐 Policies</button>`;
        actions += '</div>';
    }
    
    const createdDate = new Date(user.created_at).toLocaleDateString();
    
    tr.innerHTML = `
        <td>${user.email}</td>
        <td>${user.name || '-'}</td>
        <td>${roleBadge}</td>
        <td>${statusBadge}</td>
        <td>${verifiedBadge}</td>
        <td>${createdDate}</td>
        <td>${actions}</td>
    `;
    
    return tr;
}

// Load pending users
async function loadPendingUsers() {
    const tbody = document.getElementById('pending-tbody');
    tbody.innerHTML = '<tr><td colspan="5" class="loading">Loading pending users...</td></tr>';
    
    try {
        const response = await fetch('/admin/users?status=verified');
        const data = await response.json();
        
        if (!data.users || data.users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No pending approvals</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        
        data.users.forEach(user => {
            const tr = document.createElement('tr');
            const verifiedBadge = user.email_verified 
                ? '<span style="color: #10b981;">✓ Verified</span>' 
                : '<span style="color: #ef4444;">✗ Not Verified</span>';
            const createdDate = new Date(user.created_at).toLocaleString();
            
            tr.innerHTML = `
                <td>${user.email}</td>
                <td>${user.name || '-'}</td>
                <td>${createdDate}</td>
                <td>${verifiedBadge}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-success btn-sm" onclick="approveUser(${user.id})">✓ Approve</button>
                        <button class="btn btn-danger btn-sm" onclick="showRejectModal(${user.id})">✗ Reject</button>
                    </div>
                </td>
            `;
            
            tbody.appendChild(tr);
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="5" class="alert alert-error">Error loading pending users</td></tr>';
        console.error('Error:', error);
    }
}

// Load activity logs
async function loadLogs() {
    const tbody = document.getElementById('logs-tbody');
    tbody.innerHTML = '<tr><td colspan="5" class="loading">Loading logs...</td></tr>';
    
    try {
        const response = await fetch('/admin/logs?limit=100');
        const data = await response.json();
        
        if (!data.logs || data.logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No activity logs</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        
        data.logs.forEach(log => {
            const tr = document.createElement('tr');
            const timestamp = new Date(log.timestamp).toLocaleString();
            const status = log.success 
                ? '<span style="color: #10b981;">✓</span>' 
                : '<span style="color: #ef4444;">✗</span>';
            
            tr.innerHTML = `
                <td>${timestamp}</td>
                <td>${log.user_email}</td>
                <td>${log.action}</td>
                <td>${log.resource || '-'}</td>
                <td>${status}</td>
            `;
            
            tbody.appendChild(tr);
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="5" class="alert alert-error">Error loading logs</td></tr>';
        console.error('Error:', error);
    }
}

// Approve user
async function approveUser(userId) {
    if (!confirm('Approve this user?')) return;
    
    try {
        const response = await fetch(`/admin/users/${userId}/approve`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('User approved successfully!', 'success');
            loadUsers();
            loadPendingUsers();
        } else {
            showAlert(data.error || 'Failed to approve user', 'error');
        }
    } catch (error) {
        showAlert('Error approving user', 'error');
        console.error('Error:', error);
    }
}

// Show reject modal
function showRejectModal(userId) {
    const reason = prompt('Reason for rejection (optional):');
    if (reason !== null) {
        rejectUser(userId, reason);
    }
}

// Reject user
async function rejectUser(userId, reason) {
    try {
        const response = await fetch(`/admin/users/${userId}/reject`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({reason: reason || 'Not specified'})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('User rejected', 'success');
            loadUsers();
            loadPendingUsers();
        } else {
            showAlert(data.error || 'Failed to reject user', 'error');
        }
    } catch (error) {
        showAlert('Error rejecting user', 'error');
        console.error('Error:', error);
    }
}

// Suspend user
async function suspendUser(userId) {
    const reason = prompt('Reason for suspension:');
    if (!reason) return;
    
    try {
        const response = await fetch(`/admin/users/${userId}/suspend`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({reason})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('User suspended', 'success');
            loadUsers();
        } else {
            showAlert(data.error || 'Failed to suspend user', 'error');
        }
    } catch (error) {
        showAlert('Error suspending user', 'error');
        console.error('Error:', error);
    }
}

// Show delist modal
function showDelistModal(userId) {
    if (!confirm('⚠️ PERMANENTLY DELIST this user?\n\nThis will:\n• Immediately revoke all access\n• Force logout\n• Cannot be undone\n\nAre you sure?')) {
        return;
    }
    
    const reason = prompt('Reason for delisting (required):');
    if (!reason) return;
    
    delistUser(userId, reason);
}

// Delist user
async function delistUser(userId, reason) {
    try {
        const response = await fetch(`/admin/users/${userId}/delist`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({reason})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('User delisted. Access immediately revoked.', 'success');
            loadUsers();
        } else {
            showAlert(data.error || 'Failed to delist user', 'error');
        }
    } catch (error) {
        showAlert('Error delisting user', 'error');
        console.error('Error:', error);
    }
}

// Reactivate user
async function reactivateUser(userId) {
    if (!confirm('Reactivate this user?')) return;
    
    try {
        const response = await fetch(`/admin/users/${userId}/reactivate`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('User reactivated', 'success');
            loadUsers();
        } else {
            showAlert(data.error || 'Failed to reactivate user', 'error');
        }
    } catch (error) {
        showAlert('Error reactivating user', 'error');
        console.error('Error:', error);
    }
}

// Show policy modal
async function showPolicyModal(userId) {
    const modal = document.getElementById('policy-modal');
    const content = document.getElementById('policy-content');
    
    content.innerHTML = '<div class="loading">Loading policies...</div>';
    modal.classList.add('show');
    
    try {
        const response = await fetch(`/admin/users/${userId}/policies`);
        const data = await response.json();
        
        currentUser = allUsers.find(u => u.id === userId);
        
        content.innerHTML = `
            <div class="alert alert-info">
                Managing policies for: <strong>${currentUser.email}</strong>
            </div>
            
            <div class="form-group">
                <button class="btn btn-primary" onclick="showAddPolicyForm(${userId})">+ Add Policy</button>
            </div>
            
            <h4 style="margin: 1.5rem 0 1rem;">Current Policies:</h4>
            <div id="policies-list">
                ${data.policies.length === 0 ? '<p class="empty-state">No policies assigned</p>' : ''}
            </div>
        `;
        
        if (data.policies.length > 0) {
            const policiesList = document.getElementById('policies-list');
            data.policies.forEach(policy => {
                const policyCard = createPolicyCard(policy);
                policiesList.appendChild(policyCard);
            });
        }
    } catch (error) {
        content.innerHTML = '<div class="alert alert-error">Error loading policies</div>';
        console.error('Error:', error);
    }
}

// Create policy card
function createPolicyCard(policy) {
    const div = document.createElement('div');
    div.className = 'card';
    div.style.marginBottom = '1rem';
    
    const accessValues = JSON.stringify(policy.access_values, null, 2);
    const isActive = policy.is_active ? '<span style="color: #10b981;">✓ Active</span>' : '<span style="color: #6b7280;">Inactive</span>';
    
    div.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <strong>Level:</strong> ${policy.access_level.toUpperCase()}<br>
                <strong>Status:</strong> ${isActive}<br>
                <strong>Values:</strong> <pre style="background: #f3f4f6; padding: 0.5rem; margin: 0.5rem 0; border-radius: 0.25rem; font-size: 0.75rem;">${accessValues}</pre>
                <strong>Permissions:</strong><br>
                ${policy.can_view_data ? '✓' : '✗'} View Data<br>
                ${policy.can_upload_files ? '✓' : '✗'} Upload Files<br>
                ${policy.can_use_data_catalogue ? '✓' : '✗'} Use Data Catalogue<br>
                ${policy.can_export_data ? '✓' : '✗'} Export Data<br>
                ${policy.can_view_analytics ? '✓' : '✗'} View Analytics
            </div>
            <button class="btn btn-danger btn-sm" onclick="deletePolicy(${policy.id})">Delete</button>
        </div>
    `;
    
    return div;
}

// Close policy modal
function closePolicyModal() {
    document.getElementById('policy-modal').classList.remove('show');
}

// Show alert
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.position = 'fixed';
    alert.style.top = '2rem';
    alert.style.right = '2rem';
    alert.style.zIndex = '10000';
    alert.style.minWidth = '300px';
    alert.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Status filter change
document.getElementById('status-filter').addEventListener('change', loadUsers);

// Close modal on outside click
document.getElementById('policy-modal').addEventListener('click', (e) => {
    if (e.target.id === 'policy-modal') {
        closePolicyModal();
    }
});
