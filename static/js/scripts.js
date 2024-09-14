document.getElementById('host_image').addEventListener('change', function(event) {
    previewImage(event, 'host_image_preview');
});

document.getElementById('watermark').addEventListener('change', function(event) {
    previewImage(event, 'watermark_preview');
});

function previewImage(event, previewId) {
    const reader = new FileReader();
    reader.onload = function() {
        const output = document.createElement('img');
        output.src = reader.result;
        const previewDiv = document.getElementById(previewId);
        previewDiv.innerHTML = '';
        previewDiv.appendChild(output);
    };
    reader.readAsDataURL(event.target.files[0]);
}
