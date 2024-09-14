Secure and Imperceptible Blind Medical Image Watermarking for IoMT Applications
Overview
This project focuses on the development of a secure and imperceptible blind medical image watermarking system designed for Internet of Medical Things (IoMT) applications. 
The system embeds a watermark into medical images to ensure authenticity and ownership without compromising diagnostic quality.
It also includes functionality to extract the watermark and evaluate its quality.
Features
Image Upload: Users can upload a host image and a watermark image through a web interface.
Watermark Embedding: The system embeds the watermark into the host image using discrete wavelet transform (DWT) and discrete cosine transform (DCT).
Watermark Extraction: The watermark can be extracted from the watermarked image.
Evaluation Metrics: The quality of watermarked images and extracted watermarks is assessed using Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM).
Python: Core programming language for image processing and watermarking algorithms.
OpenCV: Used for image manipulation and processing.
PyWavelets: For discrete wavelet transform operations.
SciPy: For discrete cosine transform.
Flask: Web framework for building the web interface.
HTML/CSS/JavaScript: For front-end user interface.
Docker: For containerizing the application (optional, if used).
Installation
Clone the repository:
Copy code
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
Set up a virtual environment:
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:
Copy code
pip install -r requirements.txt
Run the application:
Copy code
python app.py
The application will be available at http://127.0.0.1:5000/
Usage
Navigate to the web interface.
Upload the host image and watermark image.
Submit the form to embed the watermark.
View and download the results, including the watermarked image and extracted watermark.
Evaluation Metrics
The quality of the watermarked images and extracted watermarks is evaluated using:
Peak Signal-to-Noise Ratio (PSNR): Measures the quality of the watermarked image compared to the original host image.
Structural Similarity Index (SSIM): Assesses the visual similarity between the watermarked image and the original.
Drawback :
A noted drawback of the proposed method is that while the watermark remains imperceptible, slight differences may exist between the 
extracted watermark and the original to ensure minimal impact on the host image's quality.
Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.
Contact
For any questions or feedback, please reach out to yaserbarkaath7@gmail.com


