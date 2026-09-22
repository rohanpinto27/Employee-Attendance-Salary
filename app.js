// Employee Attendance & Salary Management System - Frontend JS

document.addEventListener('DOMContentLoaded', () => {
    // State variables
    let employeesData = [];
    let salaryChartInstance = null;
    let attendanceChartInstance = null;

    // DOM Elements
    const tabBtnDirectory = document.getElementById('tabBtnDirectory');
    const tabBtnCalculator = document.getElementById('tabBtnCalculator');
    const tabBtnAnalytics = document.getElementById('tabBtnAnalytics');

    const tabContentDirectory = document.getElementById('tabContentDirectory');
    const tabContentCalculator = document.getElementById('tabContentCalculator');
    const tabContentAnalytics = document.getElementById('tabContentAnalytics');

    const employeeTableBody = document.getElementById('employeeTableBody');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');

    // KPI Card Elements
    const statTotalEmployees = document.getElementById('statTotalEmployees');
    const statTotalPayroll = document.getElementById('statTotalPayroll');
    const statOvertimeShare = document.getElementById('statOvertimeShare');
    const statAvgAttendance = document.getElementById('statAvgAttendance');
    const statLowAttendance = document.getElementById('statLowAttendance');

    // Modal Elements
    const employeeModal = document.getElementById('employeeModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalForm = document.getElementById('modalForm');
    const modalEmployeeId = document.getElementById('modalEmployeeId');
    const modalName = document.getElementById('modalName');
    const modalBasic = document.getElementById('modalBasic');
    const modalOtRate = document.getElementById('modalOtRate');
    const modalTotalDays = document.getElementById('modalTotalDays');
    const modalPresentDays = document.getElementById('modalPresentDays');
    const modalOtHours = document.getElementById('modalOtHours');
    const btnOpenAddModal = document.getElementById('btnOpenAddModal');
    const btnCloseModal = document.getElementById('btnCloseModal');
    const btnCancelModal = document.getElementById('btnCancelModal');

    // Modal Live Preview elements
    const modalEstAttendance = document.getElementById('modalEstAttendance');
    const modalEstOtPay = document.getElementById('modalEstOtPay');
    const modalEstFinalSalary = document.getElementById('modalEstFinalSalary');

    // Quick Calculator Inputs
    const calcName = document.getElementById('calcName');
    const calcBasic = document.getElementById('calcBasic');
    const calcOtRate = document.getElementById('calcOtRate');
    const calcTotalDays = document.getElementById('calcTotalDays');
    const calcPresentDays = document.getElementById('calcPresentDays');
    const calcOtHours = document.getElementById('calcOtHours');
    const btnSaveFromCalc = document.getElementById('btnSaveFromCalc');

    // Quick Calculator Results
    const resCalcName = document.getElementById('resCalcName');
    const resCalcBasic = document.getElementById('resCalcBasic');
    const resCalcAttendance = document.getElementById('resCalcAttendance');
    const resCalcOvertime = document.getElementById('resCalcOvertime');
    const resCalcFinal = document.getElementById('resCalcFinal');
    const calcStatusBadge = document.getElementById('calcStatusBadge');

    // --- INITIALIZATION ---
    fetchSummary();
    fetchEmployees();

    // --- TAB SWITCHING ---
    function switchTab(activeTabBtn, activeTabContent) {
        [tabBtnDirectory, tabBtnCalculator, tabBtnAnalytics].forEach(btn => {
            btn.classList.remove('border-brand-600', 'text-brand-600');
            btn.classList.add('border-transparent', 'text-slate-500');
        });
        [tabContentDirectory, tabContentCalculator, tabContentAnalytics].forEach(content => {
            content.classList.add('hidden');
        });

        activeTabBtn.classList.remove('border-transparent', 'text-slate-500');
        activeTabBtn.classList.add('border-brand-600', 'text-brand-600');
        activeTabContent.classList.remove('hidden');

        if (activeTabContent === tabContentAnalytics) {
            renderCharts();
        }
    }

    tabBtnDirectory.addEventListener('click', () => switchTab(tabBtnDirectory, tabContentDirectory));
    tabBtnCalculator.addEventListener('click', () => switchTab(tabBtnCalculator, tabContentCalculator));
    tabBtnAnalytics.addEventListener('click', () => switchTab(tabBtnAnalytics, tabContentAnalytics));

    // --- API FETCH FUNCTIONS ---
    async function fetchSummary() {
        try {
            const res = await fetch('/api/summary');
            const data = await res.json();
            if (data.success) {
                const s = data.summary;
                statTotalEmployees.textContent = s.total_employees;
                statTotalPayroll.textContent = `Rs. ${s.total_payroll.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
                statOvertimeShare.textContent = `OT: Rs. ${s.total_overtime_pay.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
                statAvgAttendance.textContent = `${s.avg_attendance.toFixed(1)}%`;
                statLowAttendance.textContent = s.low_attendance_count;
            }
        } catch (err) {
            console.error('Failed to fetch summary:', err);
        }
    }

    async function fetchEmployees() {
        try {
            const search = searchInput.value.trim();
            const status = statusFilter.value;
            const url = new URL('/api/employees', window.location.origin);
            if (search) url.searchParams.append('search', search);
            if (status) url.searchParams.append('status', status);

            const res = await fetch(url);
            const data = await res.json();
            if (data.success) {
                employeesData = data.employees;
                renderEmployeeTable(employeesData);
                if (!tabContentAnalytics.classList.contains('hidden')) {
                    renderCharts();
                }
            }
        } catch (err) {
            console.error('Failed to fetch employees:', err);
            showToast('Failed to load employee list', 'error');
        }
    }

    // --- TABLE RENDERING ---
    function renderEmployeeTable(employees) {
        if (!employees || employees.length === 0) {
            employeeTableBody.innerHTML = `
                <tr>
                    <td colspan="8" class="text-center py-8 text-slate-400">
                        <i class="fa-solid fa-folder-open text-3xl mb-2 text-slate-300 block"></i>
                        No employee records found matching criteria.
                    </td>
                </tr>
            `;
            return;
        }

        employeeTableBody.innerHTML = employees.map(emp => {
            const isOk = emp.attendance_status === 'Attendance OK';
            const badgeClass = isOk ? 'badge-ok' : 'badge-warning';
            const statusIcon = isOk ? 'fa-check' : 'fa-triangle-exclamation';

            return `
                <tr class="hover:bg-slate-50 transition duration-150">
                    <td class="px-5 py-4 text-xs font-semibold text-slate-500">#${emp.id}</td>
                    <td class="px-5 py-4 font-semibold text-slate-900">${escapeHtml(emp.name)}</td>
                    <td class="px-5 py-4 text-slate-700">Rs. ${emp.basic_salary.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
                    <td class="px-5 py-4">
                        <div class="flex items-center space-x-2">
                            <span class="font-bold ${isOk ? 'text-slate-800' : 'text-amber-700'}">${emp.attendance_percentage.toFixed(2)}%</span>
                            <span class="text-xs text-slate-400">(${emp.present_days}/${emp.total_working_days} days)</span>
                        </div>
                    </td>
                    <td class="px-5 py-4 text-slate-700">
                        <div>${emp.overtime_hours} hrs</div>
                        <div class="text-xs text-emerald-600 font-medium">+Rs. ${emp.overtime_pay.toLocaleString('en-IN', {minimumFractionDigits: 2})}</div>
                    </td>
                    <td class="px-5 py-4 font-extrabold text-slate-900">Rs. ${emp.final_salary.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
                    <td class="px-5 py-4">
                        <span class="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${badgeClass}">
                            <i class="fa-solid ${statusIcon} text-xs"></i>
                            <span>${emp.attendance_status}</span>
                        </span>
                    </td>
                    <td class="px-5 py-4 text-right space-x-2">
                        <button onclick="editEmployee(${emp.id})" class="text-slate-500 hover:text-brand-600 p-1.5 rounded-lg hover:bg-slate-100 transition" title="Edit">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                        <button onclick="deleteEmployee(${emp.id}, '${escapeJsString(emp.name)}')" class="text-slate-500 hover:text-red-600 p-1.5 rounded-lg hover:bg-slate-100 transition" title="Delete">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    }

    // Filter Listeners
    let searchTimeout;
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(fetchEmployees, 250);
    });

    statusFilter.addEventListener('change', fetchEmployees);

    // --- QUICK CALCULATOR LOGIC ---
    function updateQuickCalculator() {
        const name = calcName.value.trim() || 'John Doe';
        const basic = parseFloat(calcBasic.value) || 0;
        const otRate = parseFloat(calcOtRate.value) || 250;
        const totalDays = parseInt(calcTotalDays.value) || 0;
        const presentDays = parseInt(calcPresentDays.value) || 0;
        const otHours = parseFloat(calcOtHours.value) || 0;

        const attPct = totalDays > 0 ? (presentDays / totalDays) * 100 : 0;
        const otPay = otHours * otRate;
        const finalSal = basic + otPay;
        const isOk = attPct >= 75.0;

        resCalcName.textContent = name;
        resCalcBasic.textContent = `Rs. ${basic.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
        resCalcAttendance.textContent = `${attPct.toFixed(2)}%`;
        resCalcOvertime.textContent = `Rs. ${otPay.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
        resCalcFinal.textContent = `Rs. ${finalSal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

        if (isOk) {
            calcStatusBadge.className = 'bg-emerald-500/20 text-emerald-300 px-2.5 py-1 rounded-full text-xs font-semibold border border-emerald-500/30';
            calcStatusBadge.textContent = 'Attendance OK';
        } else {
            calcStatusBadge.className = 'bg-amber-500/20 text-amber-300 px-2.5 py-1 rounded-full text-xs font-semibold border border-amber-500/30';
            calcStatusBadge.textContent = 'Below Threshold';
        }
    }

    [calcName, calcBasic, calcOtRate, calcTotalDays, calcPresentDays, calcOtHours].forEach(input => {
        input.addEventListener('input', updateQuickCalculator);
    });

    btnSaveFromCalc.addEventListener('click', async () => {
        const empData = {
            name: calcName.value.trim() || 'John Doe',
            basic_salary: parseFloat(calcBasic.value) || 0,
            overtime_rate: parseFloat(calcOtRate.value) || 250,
            total_working_days: parseInt(calcTotalDays.value) || 0,
            present_days: parseInt(calcPresentDays.value) || 0,
            overtime_hours: parseFloat(calcOtHours.value) || 0
        };

        try {
            const res = await fetch('/api/employees', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(empData)
            });
            const data = await res.json();
            if (data.success) {
                showToast(`Employee '${empData.name}' saved successfully!`, 'success');
                fetchSummary();
                fetchEmployees();
                switchTab(tabBtnDirectory, tabContentDirectory);
            } else {
                showToast(data.error || 'Error saving record', 'error');
            }
        } catch (err) {
            showToast('Failed to connect to backend server', 'error');
        }
    });

    // --- MODAL DIALOG HANDLERS ---
    function openModal(isEdit = false, emp = null) {
        employeeModal.classList.remove('hidden');
        if (isEdit && emp) {
            modalTitle.textContent = `Edit Employee #${emp.id}`;
            modalEmployeeId.value = emp.id;
            modalName.value = emp.name;
            modalBasic.value = emp.basic_salary;
            modalOtRate.value = emp.overtime_rate;
            modalTotalDays.value = emp.total_working_days;
            modalPresentDays.value = emp.present_days;
            modalOtHours.value = emp.overtime_hours;
        } else {
            modalTitle.textContent = 'Add New Employee';
            modalEmployeeId.value = '';
            modalForm.reset();
            modalOtRate.value = 250;
            modalTotalDays.value = 22;
            modalPresentDays.value = 20;
            modalOtHours.value = 0;
        }
        updateModalPreview();
    }

    function closeModal() {
        employeeModal.classList.add('hidden');
    }

    function updateModalPreview() {
        const basic = parseFloat(modalBasic.value) || 0;
        const otRate = parseFloat(modalOtRate.value) || 250;
        const totalDays = parseInt(modalTotalDays.value) || 0;
        const presentDays = parseInt(modalPresentDays.value) || 0;
        const otHours = parseFloat(modalOtHours.value) || 0;

        const attPct = totalDays > 0 ? (presentDays / totalDays) * 100 : 0;
        const otPay = otHours * otRate;
        const finalSal = basic + otPay;

        modalEstAttendance.textContent = `${attPct.toFixed(2)}%`;
        modalEstOtPay.textContent = `Rs. ${otPay.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
        modalEstFinalSalary.textContent = `Rs. ${finalSal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
    }

    [modalBasic, modalOtRate, modalTotalDays, modalPresentDays, modalOtHours].forEach(input => {
        input.addEventListener('input', updateModalPreview);
    });

    btnOpenAddModal.addEventListener('click', () => openModal(false));
    btnCloseModal.addEventListener('click', closeModal);
    btnCancelModal.addEventListener('click', closeModal);

    modalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = modalEmployeeId.value;
        const payload = {
            name: modalName.value.trim(),
            basic_salary: parseFloat(modalBasic.value) || 0,
            overtime_rate: parseFloat(modalOtRate.value) || 250,
            total_working_days: parseInt(modalTotalDays.value) || 0,
            present_days: parseInt(modalPresentDays.value) || 0,
            overtime_hours: parseFloat(modalOtHours.value) || 0
        };

        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/employees/${id}` : '/api/employees';

        try {
            const res = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.success) {
                showToast(data.message || 'Operation successful', 'success');
                closeModal();
                fetchSummary();
                fetchEmployees();
            } else {
                showToast(data.error || 'Error saving employee', 'error');
            }
        } catch (err) {
            showToast('Failed to save record', 'error');
        }
    });

    // Global Edit & Delete functions attached to window
    window.editEmployee = (id) => {
        const emp = employeesData.find(e => e.id === id);
        if (emp) openModal(true, emp);
    };

    window.deleteEmployee = async (id, name) => {
        if (!confirm(`Are you sure you want to delete employee '${name}' (#${id})?`)) return;

        try {
            const res = await fetch(`/api/employees/${id}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                showToast(`Employee #${id} deleted`, 'success');
                fetchSummary();
                fetchEmployees();
            } else {
                showToast(data.error || 'Failed to delete employee', 'error');
            }
        } catch (err) {
            showToast('Error connecting to server', 'error');
        }
    };

    // --- CHARTS VISUALIZATION ---
    function renderCharts() {
        if (!employeesData || employeesData.length === 0) return;

        // Chart 1: Salary Breakdown
        const labels = employeesData.map(e => e.name);
        const basicSalaries = employeesData.map(e => e.basic_salary);
        const overtimePays = employeesData.map(e => e.overtime_pay);

        const ctxSalary = document.getElementById('chartSalaryBreakdown').getContext('2d');
        if (salaryChartInstance) salaryChartInstance.destroy();

        salaryChartInstance = new Chart(ctxSalary, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Basic Salary (Rs.)',
                        data: basicSalaries,
                        backgroundColor: '#3b82f6',
                        borderRadius: 6
                    },
                    {
                        label: 'Overtime Pay (Rs.)',
                        data: overtimePays,
                        backgroundColor: '#10b981',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { stacked: true },
                    y: { stacked: true, beginAtZero: true }
                }
            }
        });

        // Chart 2: Attendance Status Breakdown
        const okCount = employeesData.filter(e => e.attendance_status === 'Attendance OK').length;
        const lowCount = employeesData.filter(e => e.attendance_status === 'Below Attendance Threshold').length;

        const ctxAttendance = document.getElementById('chartAttendanceStatus').getContext('2d');
        if (attendanceChartInstance) attendanceChartInstance.destroy();

        attendanceChartInstance = new Chart(ctxAttendance, {
            type: 'doughnut',
            data: {
                labels: ['Attendance OK (>=75%)', 'Below Threshold (<75%)'],
                datasets: [{
                    data: [okCount, lowCount],
                    backgroundColor: ['#22c55e', '#f59e0b'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    // --- TOAST NOTIFICATION UTILITY ---
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        const isSuccess = type === 'success';
        const isError = type === 'error';

        const bgClass = isSuccess ? 'bg-emerald-800 text-white' : (isError ? 'bg-red-800 text-white' : 'bg-slate-800 text-white');
        const icon = isSuccess ? 'fa-circle-check' : (isError ? 'fa-circle-xmark' : 'fa-circle-info');

        toast.className = `toast-slide px-4 py-3 rounded-lg shadow-lg ${bgClass} text-sm font-medium flex items-center space-x-2.5 max-w-sm`;
        toast.innerHTML = `<i class="fa-solid ${icon}"></i><span>${escapeHtml(message)}</span>`;

        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.remove();
        }, 3500);
    }

    // Helper sanitizers
    function escapeHtml(str) {
        return String(str).replace(/[&<>"']/g, match => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        })[match]);
    }

    function escapeJsString(str) {
        return String(str).replace(/'/g, "\\'");
    }
});
