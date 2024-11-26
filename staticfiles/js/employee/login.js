$(document).ready(function () {
    $('#loginForm').on('submit', function (event) {
        event.preventDefault(); 
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        const formData = $(this).serialize(); 

        $.ajax({
            url: '/api/user/login/employee/', 
            method: 'POST',
            data: formData, 
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (response) {
                console.log('Giriş başarılı:', response);
                localStorage.setItem('auth_token', response.key);
                window.location.href = '/u/main/employee/'; 
            },
            error: function (xhr, status, error) {
                console.error('Hata:', xhr.responseText);
                alert('Login failed. Please check your credentials.');
            }
        });
    });
});
