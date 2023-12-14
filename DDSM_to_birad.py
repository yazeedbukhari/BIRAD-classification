import os
import shutil
import pandas as pd

# Paths (you need to update these)
excel_file_path = 'INbreast.xls'  # Update this path
dicom_files_directory = 'ALL-IMGS'  # Update this path

# Read and process the Excel file
df = pd.read_excel(excel_file_path)
df = df[['File Name', 'Bi-Rads']].dropna()
df['Bi-Rads'] = df['Bi-Rads'].astype(str).str.extract('(\d)').astype(int)
df['File Name'] = df['File Name'].astype(int).astype(str)

# Create a mapping from file name to BIRAD score
file_to_birad = dict(zip(df['File Name'], df['Bi-Rads']))

# Create folders for each unique BIRAD score and an 'Others' folder
unique_birads = set(df['Bi-Rads'])
for birad_score in unique_birads:
    os.makedirs(os.path.join(dicom_files_directory, str(birad_score)), exist_ok=True)
os.makedirs(os.path.join(dicom_files_directory, 'Others'), exist_ok=True)

# Move files to respective folders
for file in os.listdir(dicom_files_directory):
    if file.endswith('.dcm'):
        file_id = file.split('_')[0]
        birad_score = file_to_birad.get(file_id)

        if birad_score in unique_birads:
            dest_folder = str(birad_score)
        else:
            dest_folder = 'Others'

        src_path = os.path.join(dicom_files_directory, file)
        dest_path = os.path.join(dicom_files_directory, dest_folder, file)
        shutil.move(src_path, dest_path)
        print(f"Moved {file} to folder {dest_folder}")

print("File sorting complete.")
