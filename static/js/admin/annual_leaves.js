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
            };
        },
        dataSrc: 'data'
    },
    columns: [
        { 
            data: 'user',
            title: 'Requested Employee',
            render: function (data) {
                return `${data.first_name} ${data.last_name}`
            }
        },
        { data: 'leave_duration', title: 'Requested Day' },
        { data: 'description', title: 'Description' },
        { data: 'created_at', title: 'Created At' },
        { 
            data: null, 
            title: 'Actions',
            render: function (data, type, row) {
                return `
                    <button class="btn btn-success btn-action" data-id="${row.id}" data-action="accept" data-leave-duration="${row.leave_duration}">Accept</button>
                    <button class="btn btn-danger btn-action" data-id="${row.id}" data-action="decline" data-leave-duration="${row.leave_duration}">Decline</button>
                `;
            }
        }
    ]
});

$('#datatable').on('click', '.btn-action', function () {
    const leaveId = $(this).data('id')
    const action = true ? $(this).data('action') === 'accept' : false
    const leaveDuration = $(this).data('leave-duration')
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    $.ajax({
        url: `/api/user/taken-annual-leave/${leaveId}/`,
        method: 'PATCH',
        data: { 
            leave_duration: leaveDuration,
            is_approved: action
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {
            alert(` ${response.user.first_name} ${response.user.last_name} Annual Leave ${action ? 'Accepted' : 'Declined'}`);
            $('#datatable').DataTable().ajax.reload()
        },
        error: function (xhr, status, error) {
            alert('An error occurred: ' + error)
        }
    })
})