import os
import random
from locust import HttpUser, constant, task
import json

class QuickstartUser(HttpUser):
    # Define the folder containing the images
    image_folder = 'images'
    wait_time = constant(3)
    @task
    def hello_world(self):
        # List all PDF files in the image folder
        pdf_files = [f for f in os.listdir(self.image_folder)]
        
        # Select a random PDF file
        if pdf_files:
            selected_pdf = random.choice(pdf_files)
            file_path = os.path.join(self.image_folder, "page_2.png")
            
            files = {
                "file": self._get_image_part(file_path),
            }
            r = self.client.post("/ocr", files=files, verify=False)
            print(r.status_code)
            assert r.status_code == 200
            
            # Remove the encoding argument
            rData = json.loads(r.text)
            print(f"Processed {selected_pdf}")
        else:
            print("No PDF files found in the images directory.")

    def _get_image_part(self, file_path):
        # Read the file content in binary mode
        with open(file_path, 'rb') as f:
            return f.read()
