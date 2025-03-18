import os
from pdf2image import convert_from_path

# Define the path to the PDF file
pdf_path = 'Face Vitals.pdf'  # Replace with your PDF file path
output_folder = 'images'

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Convert PDF to images
images = convert_from_path(pdf_path)

# Save images to the output folder
for i, image in enumerate(images):
    image.save(os.path.join(output_folder, f'page_{i + 1}.png'), 'PNG')

print(f'Converted {len(images)} pages to images and saved in "{output_folder}".')
