document.addEventListener('DOMContentLoaded', () => {
    // Sortable tables
    const tables = document.querySelectorAll('table.sortable');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            header.addEventListener('click', () => {
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                const isAscending = header.dataset.sort !== 'asc';
                header.dataset.sort = isAscending ? 'asc' : 'desc';

                rows.sort((a, b) => {
                    const aText = a.cells[index].textContent.trim();
                    const bText = b.cells[index].textContent.trim();
                    if (!isNaN(aText) && !isNaN(bText)) {
                        return isAscending ? aText - bText : bText - aText;
                    }
                    return isAscending
                        ? aText.localeCompare(bText)
                        : bText.localeCompare(aText);
                });

                const tbody = table.querySelector('tbody');
                tbody.innerHTML = '';
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });

    // Toast notification function
    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // Example: Show a welcome toast on Faculty dashboard load
    if (document.querySelector('h2')?.textContent === 'Faculty Dashboard') {
        showToast('Welcome to the Faculty Dashboard!', 'success');
    }

    // Toggle date fields for submit modal
    window.toggleDateFields = function() {
        const oneDayDiv = document.getElementById('one-day-date');
        const multiDayDiv = document.getElementById('multi-day-dates');
        const oneDayRadio = document.getElementById('one_day');
        const eventDateInput = document.getElementById('event_date');
        const fromDateInput = document.getElementById('from_date');
        const toDateInput = document.getElementById('to_date');

        if (oneDayRadio.checked) {
            oneDayDiv.style.display = 'block';
            multiDayDiv.style.display = 'none';
            eventDateInput.required = true;
            fromDateInput.required = false;
            toDateInput.required = false;
        } else {
            oneDayDiv.style.display = 'none';
            multiDayDiv.style.display = 'block';
            eventDateInput.required = false;
            fromDateInput.required = true;
            toDateInput.required = true;
        }
    };

    // Toggle date fields for update modal
    window.toggleUpdateDateFields = function() {
        const oneDayDiv = document.getElementById('update-one-day-date');
        const multiDayDiv = document.getElementById('update-multi-day-dates');
        const oneDayRadio = document.getElementById('update_one_day');
        const eventDateInput = document.getElementById('update_event_date');
        const fromDateInput = document.getElementById('update_from_date');
        const toDateInput = document.getElementById('update_to_date');

        if (oneDayRadio.checked) {
            oneDayDiv.style.display = 'block';
            multiDayDiv.style.display = 'none';
            eventDateInput.required = true;
            fromDateInput.required = false;
            toDateInput.required = false;
        } else {
            oneDayDiv.style.display = 'none';
            multiDayDiv.style.display = 'block';
            eventDateInput.required = false;
            fromDateInput.required = true;
            toDateInput.required = true;
        }
    };

    // Open update modal and pre-fill form
    window.openUpdateModal = function(reportId, authorType, reportType, category, fromDate, toDate, department, reportData) {
        const modal = document.getElementById('update-report-modal');
        const form = document.getElementById('update-report-form');
        form.action = `/update_annual_report/${reportId}`;
        document.getElementById('update_report_id').value = reportId;
        document.getElementById('update_author_type').value = authorType;
        document.getElementById('update_report_type').value = reportType;
        document.getElementById('update_category').value = category;
        document.getElementById('update_department').value = department;
        document.getElementById('update_report_data').value = reportData;

        // Set date fields based on duration
        const oneDayRadio = document.getElementById('update_one_day');
        const multiDayRadio = document.getElementById('update_multi_day');
        const eventDateInput = document.getElementById('update_event_date');
        const fromDateInput = document.getElementById('update_from_date');
        const toDateInput = document.getElementById('update_to_date');

        if (fromDate === toDate) {
            oneDayRadio.checked = true;
            eventDateInput.value = fromDate;
            toggleUpdateDateFields();
        } else {
            multiDayRadio.checked = true;
            fromDateInput.value = fromDate;
            toDateInput.value = toDate;
            toggleUpdateDateFields();
        }

        modal.style.display = 'flex';
    };
});