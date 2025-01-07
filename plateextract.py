import re
import os
from datetime import datetime

def extract_vehicle_data_and_save_images(file_path, output_folder):
    jpeg_start = b'\xFF\xD8'  # JPEG file header
    jpeg_end = b'\xFF\xD9'    # JPEG file footer

    with open(file_path, 'rb') as f:
        binary_content = f.read()

    # Find all LP Image positions
    segments = []
    start_pos = 0
    while start_pos < len(binary_content):
        start_idx = binary_content.find(jpeg_start, start_pos)
        if start_idx == -1:
            break
        end_idx = binary_content.find(jpeg_end, start_idx)
        if end_idx == -1:
            break
        segments.append((start_idx, end_idx + len(jpeg_end)))
        start_pos = end_idx + len(jpeg_end)

    # Grab the Time now for processing
    timestamp = datetime.now().strftime("%m%d%y-%H%M%S")

    # Extract and process data around each Plate Image
    results = []
    for idx, (start, end) in enumerate(segments):
        # Grab the OCR processed readable plate before the image
        pre_image_data = binary_content[:start].decode('utf-8', errors='ignore')
        plate_match = re.search(r'\b[A-Z0-9]{6,7}\b', pre_image_data[::-1])  # Reverse search
        plate = plate_match.group(0)[::-1] if plate_match else f"UnknownPlate-{idx}"

        # Grab the Make and Model info after the plate image
        next_start = segments[idx + 1][0] if idx + 1 < len(segments) else len(binary_content)
        post_image_data = binary_content[end:next_start].decode('utf-8', errors='ignore')
        details = re.findall(r'"(ColorName|MakerName|ModelName)":\s*"([^"]+)"', post_image_data)

        vehicle_info = {"Plate": plate}
        for key, value in details:
            vehicle_info[key] = value
        results.append(vehicle_info)

        # Save the License Plate Image
        image_filename = os.path.join(output_folder, f"{plate}-{timestamp}.jpg")
        with open(image_filename, 'wb') as img_file:
            img_file.write(binary_content[start:end])

    return results

# Processing File
file_path = '/test/collectedcars.bin'

# Folder to output plate images
output_folder = '/test/reads/'
os.makedirs(output_folder, exist_ok=True)

vehicle_data = extract_vehicle_data_and_save_images(file_path, output_folder)
for vehicle in vehicle_data:
    print(vehicle)

