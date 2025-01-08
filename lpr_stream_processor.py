import re
import os
import socket
from datetime import datetime

def extract_vehicle_data_and_save_images(binary_content, output_folder, record_file):
    jpeg_start = b'\xFF\xD8'  # JPEG file header
    jpeg_end = b'\xFF\xD9'    # JPEG file footer

    # Find all license plate images, encoded as jpegs in the stream
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

    # Extract and process data around each license plate image
    for idx, (start, end) in enumerate(segments):
        # The Plate is BEFORE the image, the first text supplied in the data stream
        pre_image_data = binary_content[:start].decode('utf-8', errors='ignore')
        plate_match = re.search(r'\b[A-Z0-9]{6,7}\b', pre_image_data[::-1])  # Reverse search
        plate = plate_match.group(0)[::-1] if plate_match else f"UnknownPlate-{idx}"

        # The make and model are provided after the plate image
        next_start = segments[idx + 1][0] if idx + 1 < len(segments) else len(binary_content)
        post_image_data = binary_content[end:next_start].decode('utf-8', errors='ignore')
        details = re.findall(r'"(ColorName|MakerName|ModelName)":\s*"([^"]+)"', post_image_data)

        # Compile vehicle info
        vehicle_info = {"Plate": plate}
        for key, value in details:
            vehicle_info[key] = value

        # Save license plate image
        timestamp = datetime.now().strftime("%m%d%y-%H%M%S")
        image_filename = os.path.join(output_folder, f"{plate}-{timestamp}.jpg")
        with open(image_filename, 'wb') as img_file:
            img_file.write(binary_content[start:end])

        # Add timestamp to vehicle info and save to record file
        vehicle_info["Timestamp"] = timestamp
        record_file.write(f"{vehicle_info}\n")
        record_file.flush()
        print(f"[INFO] Processed vehicle data: {vehicle_info}")

def process_stream(ip, port, output_folder, output_file):
    os.makedirs(output_folder, exist_ok=True)

    with open(output_file, 'a') as record_file:
        print(f"[INFO] Connecting to {ip}:{port}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((ip, port))
                print(f"[SUCCESS] Connected to {ip}:{port}. Waiting for data stream...")

                buffer = b''
                idle_count = 0

                while True:
                    try:
                        # Receive data
                        data = s.recv(4096)
                        if not data:
                            print("[INFO] No data received. Connection may have closed.")
                            break

                        # Process data after idle packets arrive
                        if len(data) == 4:
                            idle_count += 1
                            if idle_count > 3:  # Assume 3 consecutive 4-byte packets indicate a gap
                                if buffer:
                                    print("[INFO] Processing accumulated data...")
                                    extract_vehicle_data_and_save_images(buffer, output_folder, record_file)
                                    buffer = b''  # Clear buffer after processing
                                idle_count = 0  # Reset idle counter
                            continue
                        else:
                            idle_count = 0  # Reset idle count if real data arrives

                        # Allow multiple bursts to come in
                        buffer += data
                    except KeyboardInterrupt:
                        print("[INFO] Exiting program...")
                        break
                    except Exception as e:
                        print(f"[ERROR] Error during data processing: {e}")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")

# Configure the application
if __name__ == "__main__":
    # Default values
    default_ip = "1.2.3.4"
    default_port = 5001
    default_output_folder = "/scratch/lpr/test/plates"
    default_output_file = "/scratch/lpr/test/plates.txt"

    # User inputs with defaults
    ip = input(f"Enter IP address [{default_ip}]: ").strip() or default_ip
    port = int(input(f"Enter port number [{default_port}]: ").strip() or default_port)
    output_folder = input(f"Enter output folder for images [{default_output_folder}]: ").strip() or default_output_folder
    output_file = input(f"Enter output file for records [{default_output_file}]: ").strip() or default_output_file

    # Run the stream processor
    process_stream(ip, port, output_folder, output_file)

