# LPRPARSER

## Educational - Experimental License Plate Reader (LPR) Data Processor

LPRPARSER is an experimental project designed to process data collected from Motorola License Plate Readers (LPR). This tool demonstrates how to extract and process data streams, including license plates, vehicle makes, models, and associated images.

### **Disclaimer**

This project is for **educational purposes only**. The authors and contributors are not responsible for any misuse or unauthorized use of this tool. Always ensure you comply with local laws and regulations.

---

## **Overview**

LPRPARSER connects to a TCP port on a Motorola LPR camera, captures binary data initially using `netcat`, and processes it using a Python script. The script extracts license plates, vehicle information (make and model), and associated images from the raw data.

---

## **Getting Started**

### **Prerequisites**

- Python 3.x installed on your system.
- Access to an LPR camera that streams data over TCP.

### **Step 1: Collecting Data**

Use `netcat` to capture data from the LPR camera. Each passing car generates a burst of data that includes:

- License plate information
- A JPEG image of the vehicle
- Vehicle details (make, model, color)

Run the following command to save the data stream:

```bash
nc -v <camera_ip> <camera_port> > collectedcars.bin
```

**Example:**
If your camera is at `1.2.3.4` and streams data on port `5001`:

```bash
nc -v 1.2.3.4 5001 > collectedcars.bin
```

---

### **Step 2: Processing Data**

Modify the Python script `plateextract.py` to fit the paths of your data:

#### Update the Processing File Path

```python
file_path = '/test/collectedcars.bin'  # Path to your collected data file
output_folder = '/test/reads/'  # Folder to save processed images
```

#### Activate Python Environment and Install Dependencies

```bash
python3 -m venv lprenv
source lprenv/bin/activate  # On macOS/Linux
lprenv\Scripts\activate     # On Windows
pip install chardet
```

#### Run the Script

Execute the Python script to process the collected plates:

```bash
python3 plateextract.py
```

The script will:

1. Extract license plates, vehicle makes, and models.

2. Save associated images with filenames in the format:
   `PLATE-DATE-TIME.jpg`

   **Example:** `ER61033-010725-114622.jpg`

3. Print extracted vehicle details in the console.

---

### **Step 3: Accessing LPR Cameras**

Motorola LPR cameras can be accessed at the following example URLs:

- Color Stream: [http://1.2.3.4:8080/cam1color](http://1.2.3.4:8080/cam1color)
- Infrared Stream: [http://1.2.3.4:8080/cam1ir](http://1.2.3.4:8080/cam1ir)
- Cam streams are as cam0, cam1, replace as needed for additional streams on the single IP

**Data Streaming Ports:**

- Camera 0: Port `5000`
- Camera 1: Port `5001`
- Camera 2: Port `5002`
- Camera 3: Port `5003`
- Camera 4: Port `5004`

Ensure you have permission to access and process these streams.

---

## **Example Output**

**Console Output:**

```plaintext
{'Plate': 'ER61033', 'ColorName': 'gray', 'MakerName': 'CHEVROLET', 'ModelName': 'IMPALA'}
{'Plate': '497088D', 'ColorName': 'black', 'MakerName': 'DODGE', 'ModelName': 'CHALLENGER'}
...
```

**Saved Images:**
Images will be saved in the output folder `/test/reads/` with filenames:

- `ER61033-010725-114622.jpg`
- `497088D-010725-114622.jpg`

---

## **Contribution and Feedback**

This project is experimental and open to improvements. Feel free to fork and modify the script to fit your specific use case. Contributions, feedback, and ideas are welcome.

---

## **Disclaimer**

This tool is for **educational purposes only**. The authors are not liable for any misuse or unauthorized application of this tool. Use responsibly and ethically.

