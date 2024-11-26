$(document).ready(function () {
    $('#datatable').DataTable({
        ajax: {
            url: '/api/user/login-logs/', // DRF API URL
            dataSrc: 'results' // DRF varsayılan olarak liste döner
        },
        columns: [
            { data: 'user.email' },
            { data: 'user.first_name' },
            { data: 'user.last_name' },
            { data: 'user.last_login' },
            { data: 'late_minute' }
        ]
    });
});