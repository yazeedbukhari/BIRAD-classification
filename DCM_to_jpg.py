import os
import numpy as np
import pydicom
from PIL import Image
from pydicom.pixel_data_handlers.util import apply_voi_lut

def dicom_to_jpeg(dicom_file_path, output_folder):
    # Load the DICOM file
    dicom = pydicom.dcmread(dicom_file_path)

    # Apply VOI LUT if present
    data = apply_voi_lut(dicom.pixel_array, dicom)

    # Convert to uint8 (if necessary)
    if dicom.pixel_array.dtype != np.uint8:
        data = data - np.min(data)
        data = data / np.max(data)
        data = (data * 255).astype(np.uint8)

    # Convert to PIL Image
    image = Image.fromarray(data)

    # Save the image as JPEG
    jpeg_file_path = os.path.join(output_folder, os.path.basename(dicom_file_path).replace('.dcm', '.jpg'))
    image.save(jpeg_file_path)
    print(f'Converted {dicom_file_path} to {jpeg_file_path}')

# Directory containing DICOM files
dicom_directory = 'Sorted/5'

# Directory to save JPEG files
output_directory = 'Sorted/BIRAD5-INbreast'

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Convert all DICOM files in the directory
for filename in os.listdir(dicom_directory):
    if filename.endswith('.dcm'):
        dicom_file_path = os.path.join(dicom_directory, filename)
        dicom_to_jpeg(dicom_file_path, output_directory)
