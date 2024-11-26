$(document).ready(function () {
    $('#datatable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/api/user/taken-annual-leave/',
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
            { data: 'leave_duration' },
            { data: 'description' },
            { 
                data: 'is_approved',
                render: function(data, type, row) {
                    if (data === null) {
                        return 'Waiting'
                    } else if (data === false) {
                        return 'Declined'
                    } else if (data === true) {
                        return 'Approved'
                    }
                }
            },
        ]
    });
});