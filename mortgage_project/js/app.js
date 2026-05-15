let currentStep = 1;
const totalSteps = 6;
const formData = {};

// Handle Option Button Clicks
document.querySelectorAll('.option-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const field = btn.getAttribute('data-field');
        const value = btn.getAttribute('data-value');
        
        // Remove 'selected' from siblings
        btn.parentElement.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        
        formData[field] = value;
        
        // Auto-advance for option buttons
        setTimeout(nextStep, 300);
    });
});

function nextStep() {
    if (currentStep >= totalSteps) return;

    // Optional: Add validation here
    
    document.getElementById(`step-${currentStep}`).classList.remove('active');
    currentStep++;
    document.getElementById(`step-${currentStep}`).classList.add('active');
    
    updateProgress();
}

function updateProgress() {
    document.getElementById('current-step-num').innerText = currentStep;
    const percent = (currentStep / totalSteps) * 100;
    document.getElementById('progress').style.width = percent + '%';
}

async function submitForm() {
    // Collect remaining inputs
    formData.est_value = parseFloat(document.getElementById('est_value').value);
    formData.down_payment = parseFloat(document.getElementById('down_payment').value);
    formData.location_nh = document.getElementById('location_nh').value;
    formData.first_name = document.getElementById('first_name').value;
    formData.last_name = document.getElementById('last_name').value;
    formData.email = document.getElementById('email').value;
    formData.phone = document.getElementById('phone').value;

    console.log("Submitting Data:", formData);

    try {
        const response = await fetch('http://localhost:8001/submit_lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            document.getElementById(`step-${currentStep}`).classList.remove('active');
            document.getElementById('step-success').classList.add('active');
            document.getElementById('progress').style.width = '100%';
        } else {
            alert('Submission failed. Please check your connection.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Server unreachable. Ensure the backend is running.');
    }
}
