document.addEventListener('DOMContentLoaded', function() {
    const drawButton = document.getElementById('drawButton');
    const flowerImage = document.getElementById('flowerImage');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const buttonText = document.querySelector('.button-text');
    const buttonLoader = document.querySelector('.button-loader');
    const errorMessage = document.getElementById('errorMessage');

    drawButton.addEventListener('click', async function() {
        // Show loading state
        drawButton.disabled = true;
        buttonText.style.opacity = '0.5';
        buttonLoader.style.display = 'inline-block';
        flowerImage.style.display = 'none';
        loadingSpinner.style.display = 'block';
        errorMessage.style.display = 'none';

        try {
            const response = await fetch('/draw-flower');
            const data = await response.json();

            if (data.status === 'success') {
                flowerImage.src = `data:image/png;base64,${data.image}`;
                flowerImage.style.display = 'block';
            } else {
                throw new Error(data.message || 'Failed to draw flower');
            }
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Oops! Something went wrong. Please try again.';
            errorMessage.style.display = 'block';
        } finally {
            // Reset loading state
            drawButton.disabled = false;
            buttonText.style.opacity = '1';
            buttonLoader.style.display = 'none';
            loadingSpinner.style.display = 'none';
        }
    });
});
