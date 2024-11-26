$(document).ready(function () {
    $('#user-select').select2({
        placeholder: "Pick a Employee",
        allowClear: true,
        ajax: {
            url: '/api/user/users/search/', 
            dataType: 'json',
            delay: 250, 
            data: function (params) {
                return {
                    q: params.term 
                }
            },
            processResults: function (data) {
                return {
                    results: data.map(user => ({
                        id: user.id,
                        text: `${user.first_name} ${user.last_name}`
                    }))
                }
            },
            cache: true
        },
        minimumInputLength: 2 
    })

$('#takenAnnualLeave').on('submit', function (e) {
    e.preventDefault()
    const form = e.target
    let selectedUserId = $('#user-select').val()
    if (!selectedUserId) {
        alert('Pick an Employee')
        return
    }
    const leaveDuration = document.getElementById("leave_duration").value
    const description = document.getElementById("description").value

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    fetch(`/api/user/taken-annual-leave-admin/${selectedUserId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            leave_duration: leaveDuration,
            description: description,
            is_approved: true
        })
    })
        .then(response => {
            var data = response.json()
            if (response.ok) {
                alert("Annual Leave assigned successfully!")
                form.reset()
            } else {
                alert("Error: " + JSON.stringify(data.error))
            }})
        .catch(error => {
            console.error("Error:", error)
        })
    })
})