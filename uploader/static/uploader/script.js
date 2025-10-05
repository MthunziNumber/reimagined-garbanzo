document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const userId = document.getElementById('userId').value;
    const year = document.getElementById('year').value;
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`/api/financial/upload/${userId}/${year}/`, {
        method: 'POST',
        body: formData
    });

    const result = await response.json();


    let msg = result.message || result.error || '';
    if (!msg && result.file && Array.isArray(result.file)) {
        msg = result.file[0];
    }
    document.getElementById('message').textContent = msg;

    if (response.ok) {
        fetchData(userId, year);
    }
});

async function fetchData(userId, year) {
    const response = await fetch(`/api/finances/${userId}/${year}/`);
    const data = await response.json();


    const tbody = document.querySelector('#dataTable tbody');
    tbody.innerHTML = '';
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${row.month}</td><td>${row.amount}</td>`;
        tbody.appendChild(tr);
    });


    const ctx = document.getElementById('barChart').getContext('2d');
    if (window.barChartInstance) window.barChartInstance.destroy();
    window.barChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(r => `Month ${r.month}`),
            datasets: [{
                label: 'Amount',
                data: data.map(r => r.amount),
                backgroundColor: '#4e73df'
            }]
        }
    });
}