document.getElementById('resumeForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    let fileInput = document.getElementById('resumeFile');
    if (fileInput.files.length === 0) {
        alert('Please upload a PDF file.');
        return;
    }

    let formData = new FormData();
    formData.append('resume', fileInput.files[0]);

    try {
        let response = await fetch('/parse-resume', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            let data = await response.json();
            document.getElementById('name').textContent = data.name || 'N/A';
            document.getElementById('contactNumber').textContent = data.contactNumber || 'N/A';
            document.getElementById('email').textContent = data.email || 'N/A';
            document.getElementById('skills').textContent = data.skills.length ? data.skills.join(', ') : 'N/A';
            document.getElementById('education').textContent = data.education.length ? data.education.join(', ') : 'N/A';
            document.getElementById('experience').textContent = data.experience || 'N/A'; 
        } else {
            alert('Error parsing resume.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error parsing resume.');
    }
});
