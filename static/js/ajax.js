// Function to handle AJAX deletion
function handleDelete(event) {
    event.preventDefault(); // Prevent the default form submission

    const form = event.target.closest('form');
    const url = form.getAttribute('action');
    const taskId = url.split('/').pop(); // Extract task ID from URL

    if (confirm('Are you sure you want to delete this task?')) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                '_method': 'DELETE'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const taskElement = document.getElementById(`task-${taskId}`);
                if (taskElement) {
                    taskElement.remove();
                }
                // Optionally, show a success message or alert
                alert(data.message);
            } else {
                // Optionally, show an error message or alert
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the task.');
        });
    }
}

// Attach the function to all delete forms
document.addEventListener('DOMContentLoaded', () => {
    const deleteForms = document.querySelectorAll('form[action^="/delete/"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', handleDelete);
    });
});