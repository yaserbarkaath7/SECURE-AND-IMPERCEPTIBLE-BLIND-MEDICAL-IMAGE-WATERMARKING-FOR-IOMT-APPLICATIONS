from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import numpy as np
import pywt
from scipy.fftpack import dct, idct
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULTS_FOLDER = 'static/uploads/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def apply_dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def apply_idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

def embed_watermark(image, watermark, alpha=0.1):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    watermark_gray = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)

    coeffs = pywt.dwt2(image_gray, 'haar')
    cA, (cH, cV, cD) = coeffs
    cH_dct = apply_dct2(cH)
    cV_dct = apply_dct2(cV)
    cD_dct = apply_dct2(cD)

    # Resize watermark to match coefficient block size
    watermark_resized = cv2.resize(watermark_gray, (cH_dct.shape[1], cH_dct.shape[0]))
    watermark_normalized = watermark_resized.astype(np.float32) / 255.0

    # Embed watermark in all high-frequency coefficients
    cH_dct_watermarked = cH_dct + alpha * watermark_normalized
    cV_dct_watermarked = cV_dct + alpha * watermark_normalized
    cD_dct_watermarked = cD_dct + alpha * watermark_normalized

    cH_watermarked = apply_idct2(cH_dct_watermarked)
    cV_watermarked = apply_idct2(cV_dct_watermarked)
    cD_watermarked = apply_idct2(cD_dct_watermarked)

    coeffs_watermarked = cA, (cH_watermarked, cV_watermarked, cD_watermarked)
    image_watermarked = pywt.idwt2(coeffs_watermarked, 'haar')
    image_watermarked = np.uint8(np.clip(image_watermarked, 0, 255))

    if len(image.shape) == 3:
        image_watermarked = cv2.merge([image_watermarked] * 3)
    
    return image_watermarked

def extract_watermark(original_image, watermarked_image, alpha=0.1):
    original_image_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    watermarked_image_gray = cv2.cvtColor(watermarked_image, cv2.COLOR_BGR2GRAY)

    coeffs_original = pywt.dwt2(original_image_gray, 'haar')
    cA_original, (cH_original, cV_original, cD_original) = coeffs_original
    coeffs_watermarked = pywt.dwt2(watermarked_image_gray, 'haar')
    cA_watermarked, (cH_watermarked, cV_watermarked, cD_watermarked) = coeffs_watermarked

    cH_dct_original = apply_dct2(cH_original)
    cV_dct_original = apply_dct2(cV_original)
    cD_dct_original = apply_dct2(cD_original)
    cH_dct_watermarked = apply_dct2(cH_watermarked)
    cV_dct_watermarked = apply_dct2(cV_watermarked)
    cD_dct_watermarked = apply_dct2(cD_watermarked)

    # Extract watermark from all high-frequency coefficients
    watermark_extracted_H = (cH_dct_watermarked - cH_dct_original) / alpha
    watermark_extracted_V = (cV_dct_watermarked - cV_dct_original) / alpha
    watermark_extracted_D = (cD_dct_watermarked - cD_dct_original) / alpha

    # Average the extracted watermarks
    watermark_extracted = (watermark_extracted_H + watermark_extracted_V + watermark_extracted_D) / 3
    watermark_extracted = np.uint8(np.clip(watermark_extracted * 255.0, 0, 255))

    # Resize to original watermark size if needed
    watermark_resized = cv2.resize(watermark_extracted, (256, 256))
    return watermark_resized

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed_watermark', methods=['POST'])
def embed_watermark_route():
    host_image = request.files['host_image']
    watermark_image = request.files['watermark']

    host_image_path = os.path.join(UPLOAD_FOLDER, 'host_image.png')
    watermark_image_path = os.path.join(UPLOAD_FOLDER, 'watermark.png')
    watermarked_image_path = os.path.join(RESULTS_FOLDER, 'watermarked_image.png')
    extracted_watermark_path = os.path.join(RESULTS_FOLDER, 'extracted_watermark.png')

    host_image.save(host_image_path)
    watermark_image.save(watermark_image_path)

    host_image_cv = cv2.imread(host_image_path)
    watermark_image_cv = cv2.imread(watermark_image_path)

    watermarked_image = embed_watermark(host_image_cv, watermark_image_cv)
    cv2.imwrite(watermarked_image_path, watermarked_image)

    # Extract watermark from the watermarked image
    extracted_watermark = extract_watermark(host_image_cv, watermarked_image)
    cv2.imwrite(extracted_watermark_path, extracted_watermark)

    # Calculate PSNR and SSIM
    host_image_gray = cv2.cvtColor(host_image_cv, cv2.COLOR_BGR2GRAY)
    watermarked_image_gray = cv2.cvtColor(watermarked_image, cv2.COLOR_BGR2GRAY)

    psnr_value = psnr(host_image_gray, watermarked_image_gray)
    ssim_value = ssim(host_image_gray, watermarked_image_gray)

    return render_template('results.html', 
                           psnr_value=psnr_value, 
                           ssim_value=ssim_value,
                           host_image='static/uploads/host_image.png',
                           watermark_image='static/uploads/watermark.png',
                           watermarked_image='static/uploads/results/watermarked_image.png',
                           extracted_watermark='static/uploads/results/extracted_watermark.png')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(RESULTS_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
