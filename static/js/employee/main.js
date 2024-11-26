document.getElementById("takenAnnualLeave").addEventListener("submit", function (e) {
    e.preventDefault()

    const form = e.target
    const leaveDuration = document.getElementById("leave_duration").value
    const description = document.getElementById("description").value

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    fetch("/api/user/taken-annual-leave/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            leave_duration: leaveDuration,
            description: description
        })
    })
        .then(response => {
            var data = response.json()
            if (response.ok) {
                alert("Leave request submitted successfully!")
                form.reset()
            } else {
                alert("Error: " + JSON.stringify(data.error))
            }})
        .catch(error => {
            console.error("Error:", error)
        })
    })


document.getElementById("logoutId").addEventListener("submit", function (e) {
    e.preventDefault()
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    fetch("/api/user/logout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        }
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "/u/login/employee/"
            } else {
                alert("Error: " + response.error)
            }
        })
        .catch(error => {
            console.error("Error:", error)
        })
})