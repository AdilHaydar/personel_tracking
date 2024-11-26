$(document).ready(function () {
    $('#datatable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/api/user/login-logs/',
            method: 'GET',
            data: function (d) {
                return {
                    length: d.length,                       
                    start: Math.floor(d.start / d.length) + 1,
                }
            },
            dataSrc: 'data'
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