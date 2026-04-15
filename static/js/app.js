/* ============================================================
   Face Recognition System — Frontend Logic
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initSidebar();
    initStudentsPage();
    initTrainPage();
    initRecognizePage();
});

/* ============================================================
   UTILITY FUNCTIONS
   ============================================================ */

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

async function apiCall(url, method = 'GET', body = null) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(url, opts);
    return res.json();
}

/* ============================================================
   CLOCK
   ============================================================ */

function initClock() {
    const clockEl = document.getElementById('live-clock');
    if (!clockEl) return;

    function update() {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
        });
    }
    update();
    setInterval(update, 1000);
}

/* ============================================================
   SIDEBAR
   ============================================================ */

function initSidebar() {
    const toggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    if (!toggle || !sidebar) return;

    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Close sidebar on outside click (mobile)
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 &&
            sidebar.classList.contains('open') &&
            !sidebar.contains(e.target) &&
            !toggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    });
}

/* ============================================================
   STUDENTS PAGE
   ============================================================ */

let selectedStudentId = null;
let selectedStudentPk = null;

function initStudentsPage() {
    const form = document.getElementById('student-form');
    if (!form) return;

    loadStudents();

    // Save
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = getFormData();
        if (!data.student_id || !data.name || !data.department) {
            showToast('Student ID, Name, and Department are required', 'error');
            return;
        }
        const res = await apiCall('/api/students', 'POST', data);
        if (res.success) {
            showToast('Student added successfully!', 'success');
            resetForm();
            loadStudents();
        } else {
            showToast(res.error || 'Failed to add student', 'error');
        }
    });

    // Update
    document.getElementById('btn-update').addEventListener('click', async () => {
        if (!selectedStudentId) return;
        const data = getFormData();
        const res = await apiCall(`/api/students/${selectedStudentId}`, 'PUT', data);
        if (res.success) {
            showToast('Student updated!', 'success');
            resetForm();
            loadStudents();
        } else {
            showToast(res.error || 'Failed to update', 'error');
        }
    });

    // Delete
    document.getElementById('btn-delete').addEventListener('click', async () => {
        if (!selectedStudentId) return;
        if (!confirm('Are you sure you want to delete this student?')) return;
        const res = await apiCall(`/api/students/${selectedStudentId}`, 'DELETE');
        if (res.success) {
            showToast('Student deleted!', 'success');
            resetForm();
            loadStudents();
        } else {
            showToast(res.error || 'Failed to delete', 'error');
        }
    });

    // Reset
    document.getElementById('btn-reset').addEventListener('click', resetForm);

    // Capture Face
    document.getElementById('btn-capture').addEventListener('click', () => {
        if (!selectedStudentPk) return;
        showToast('Starting webcam stream... Position your face in the camera.', 'info');
        const modal = document.getElementById('capture-modal');
        const feed = document.getElementById('capture-video-feed');
        feed.src = `/capture_feed/${selectedStudentPk}`;
        modal.style.display = 'flex';
    });

    // Search
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            filterTable(searchInput.value);
        });
    }
}

window.closeCaptureModal = function() {
    document.getElementById('capture-modal').style.display = 'none';
    document.getElementById('capture-video-feed').src = '';
    showToast('Capture closed', 'info');
    loadStudents();
};

function getFormData() {
    return {
        department: document.getElementById('department').value,
        course: document.getElementById('course').value,
        year: document.getElementById('year').value,
        semester: document.getElementById('semester').value,
        student_id: document.getElementById('student_id').value,
        name: document.getElementById('name').value,
        division: document.getElementById('division').value,
        roll: document.getElementById('roll').value,
        gender: document.getElementById('gender').value,
        dob: document.getElementById('dob').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value,
        teacher: document.getElementById('teacher').value,
    };
}

function resetForm() {
    const form = document.getElementById('student-form');
    if (form) form.reset();
    selectedStudentId = null;
    selectedStudentPk = null;

    document.getElementById('btn-update').disabled = true;
    document.getElementById('btn-delete').disabled = true;
    document.getElementById('btn-capture').disabled = true;
    document.getElementById('student_id').readOnly = false;

    // Remove selected row highlight
    document.querySelectorAll('#students-tbody tr.selected').forEach(r => r.classList.remove('selected'));
}

async function loadStudents() {
    const tbody = document.getElementById('students-tbody');
    if (!tbody) return;

    try {
        const res = await apiCall('/api/students');
        if (!res.success) {
            tbody.innerHTML = `<tr class="empty-row"><td colspan="9">
                <div class="empty-state"><p>Error loading data: ${res.error}</p></div>
            </td></tr>`;
            return;
        }

        const students = res.students;
        if (students.length === 0) {
            tbody.innerHTML = `<tr class="empty-row"><td colspan="9">
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                    </svg>
                    <p>No students found. Add your first student above!</p>
                </div>
            </td></tr>`;
            return;
        }

        tbody.innerHTML = students.map(s => `
            <tr data-id="${s.student_id}" onclick="selectStudent(this, ${JSON.stringify(s).replace(/"/g, '&quot;')})">
                <td>${s.student_id}</td>
                <td>${s.name}</td>
                <td>${s.department}</td>
                <td>${s.course}</td>
                <td>${s.roll || '-'}</td>
                <td>${s.gender || '-'}</td>
                <td>${s.email || '-'}</td>
                <td>${s.phone || '-'}</td>
                <td><span class="photo-badge ${s.photo_sample === 'Yes' ? 'yes' : 'no'}">${s.photo_sample || 'No'}</span></td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = `<tr class="empty-row"><td colspan="9">
            <div class="empty-state"><p>Cannot connect to database. Please check your Supabase connection.</p></div>
        </td></tr>`;
    }
}

function selectStudent(row, student) {
    // Highlight row
    document.querySelectorAll('#students-tbody tr.selected').forEach(r => r.classList.remove('selected'));
    row.classList.add('selected');

    // Fill form
    selectedStudentId = student.student_id;
    selectedStudentPk = student.id;
    document.getElementById('department').value = student.department || '';
    document.getElementById('course').value = student.course || '';
    document.getElementById('year').value = student.year || '';
    document.getElementById('semester').value = student.semester || '';
    document.getElementById('student_id').value = student.student_id || '';
    document.getElementById('name').value = student.name || '';
    document.getElementById('division').value = student.division || '';
    document.getElementById('roll').value = student.roll || '';
    document.getElementById('gender').value = student.gender || '';
    document.getElementById('dob').value = student.dob || '';
    document.getElementById('email').value = student.email || '';
    document.getElementById('phone').value = student.phone || '';
    document.getElementById('address').value = student.address || '';
    document.getElementById('teacher').value = student.teacher || '';

    // Enable buttons
    document.getElementById('btn-update').disabled = false;
    document.getElementById('btn-delete').disabled = false;
    document.getElementById('btn-capture').disabled = false;
    document.getElementById('student_id').readOnly = true;
}

function filterTable(query) {
    const rows = document.querySelectorAll('#students-tbody tr:not(.empty-row)');
    const q = query.toLowerCase();

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? '' : 'none';
    });
}

/* ============================================================
   TRAIN PAGE
   ============================================================ */

function initTrainPage() {
    const btn = document.getElementById('btn-train');
    if (!btn) return;

    btn.addEventListener('click', async () => {
        btn.disabled = true;
        const progress = document.getElementById('training-progress');
        const result = document.getElementById('training-result');

        progress.style.display = 'block';
        result.style.display = 'none';

        try {
            const res = await apiCall('/api/train', 'POST');
            progress.style.display = 'none';

            if (res.success) {
                result.style.display = 'block';
                document.getElementById('result-message').textContent = 'Training Complete!';
                document.getElementById('result-detail').textContent = res.message;
                showToast('Model trained successfully!', 'success');
                
                // Update the status UI explicitly
                const statValue = document.querySelector('.train-stat-value:last-of-type');
                if(statValue) {
                    statValue.textContent = '✓';
                    statValue.style.color = 'var(--accent-green)';
                }
            } else {
                showToast(res.error || 'Training failed', 'error');
            }
        } catch (err) {
            progress.style.display = 'none';
            showToast('Training failed: ' + err.message, 'error');
        }

        btn.disabled = false;
    });
}

/* ============================================================
   RECOGNIZE PAGE
   ============================================================ */

function initRecognizePage() {
    const startBtn = document.getElementById('btn-start-recognition');
    const stopBtn = document.getElementById('btn-stop-recognition');
    if (!startBtn) return;

    startBtn.addEventListener('click', () => {
        const feed = document.getElementById('video-feed');
        const placeholder = document.getElementById('video-placeholder');
        const liveBadge = document.getElementById('live-badge');

        feed.src = '/video_feed?' + new Date().getTime();
        feed.style.display = 'block';
        placeholder.style.display = 'none';
        liveBadge.style.display = 'inline-flex';

        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-flex';
    });

    stopBtn.addEventListener('click', () => {
        const feed = document.getElementById('video-feed');
        const placeholder = document.getElementById('video-placeholder');
        const liveBadge = document.getElementById('live-badge');

        feed.src = '';
        feed.style.display = 'none';
        placeholder.style.display = 'flex';
        liveBadge.style.display = 'none';

        stopBtn.style.display = 'none';
        startBtn.style.display = 'inline-flex';
    });
}
