# LPRPARSER

## Educational - Experimental License Plate Reader (LPR) Data Processor

LPRPARSER is an experimental project designed to process data collected from Motorola License Plate Readers (LPR). This tool demonstrates how to extract and process data streams, including license plates, vehicle makes, models, and associated images.

### **Disclaimer**

This project is for **educational purposes only**. The authors and contributors are not responsible for any misuse or unauthorized use of this tool. Always ensure you comply with local laws and regulations when using any LPR-related technology.

---

## Table of Contents  
1. [Overview](#overview)  
2. [Getting Started](#getting-started)  
   - [Using Netcat to save stream data and later process with python](#using-netcat-for-manual-processing)  
   - [Connecting Directly to the LPR - specify IP , PORT and output paths](#connecting-directly-to-the-lpr)  
3. [Example Output](#example-output)  
4. [Contribution and Feedback](#contribution-and-feedback)  
5. [Bounty for Geolocation Assistance](#bounty-for-geolocation-assistance)  

---

## **Overview**

LPRPARSER connects to a TCP port on a Motorola LPR camera, captures binary data using `netcat`, and processes it using a Python script. The script extracts license plates, vehicle information (make and model), and associated images from the raw data. 

This project was inspired by a YouTube video from [https://www.youtube.com/@mattbrwn](@mattbrwn), particularly his exploration of license plate readers (LPRs) in his video, [https://www.youtube.com/watch?v=0dUnY1641WM&t]( Public Video and Data Feeds of Highway License Plate Readers)

In the video, Matt demonstrates how publicly accessible LPR systems can be found through a simple Censys web search, revealing a widespread lack of infrastructure and network security management. This sparked our curiosity to see just how easily data from these systems could be accessed and reverse-engineered.

Upon investigating these devices, we discovered that they not only provide live color and infrared (IR) video feeds but also stream unencrypted metadata over TCP ports. For instance, a camera’s infrared stream, labeled cam0ir, correlates with data being streamed on TCP port 5000, while cam1ir correlates with port 5001. A single IP address can host multiple camera feeds (five or more in some cases), each tied to a specific TCP port. This inherent lack of security means that anyone with the appropriate tools can connect to these cameras and retrieve sensitive data, including license plates, images, and vehicle details, without any form of encryption, password protection, or handshake verification.

The simplicity of this system turned this into an exciting challenge: how quickly could we reverse-engineer the proprietary data streams and extract meaningful information? The entire project, from discovery to functional implementation, took less than two hours. While we do not actively collect or harvest any data, this experiment highlights significant privacy concerns. It is alarming that the cameras our government agencies use to monitor traffic and public movement—visible on telephone poles and traffic lights—are left open and unsecured. This creates a gateway for malicious actors or criminal organizations to exploit these systems, harvesting sensitive information such as license plates and vehicle images. Such vulnerabilities pose serious risks, from enabling identity theft to facilitating large-scale tracking of individuals without consent.

This project underscores several critical issues: the widespread collection of personal data without adequate safeguards, the dangers of insecure Internet of Things (IoT) devices, and the lack of regard for public privacy and safety. In just a short period of experimentation, we observed live, unsecured LPR streams across several states, openly providing license plate numbers, vehicle images, and other metadata. This lack of security exposes individuals’ private information to anyone with an internet connection and basic technical knowledge.

Experiments like this are not only satisfying from a reverse-engineering perspective but also serve as a stark reminder of the vulnerabilities inherent in IoT systems. By repurposing and experimenting with these devices, we aim to bring attention to the risks posed by such insecure systems and advocate for better infrastructure management, encryption, and privacy protections.



---


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
If your camera is at `107.89.193.48` and streams data on port `5001`:

```bash
nc -v 107.89.193.48 5001 > collectedcars.bin
```

---

### **Step 2: Processing Data**

Modify the Python script `plateextract.py` to fit the paths of your data:

#### Update the Processing File Path

```python
file_path = '/test/file2.bin'  # Path to your collected data file
output_folder = '/test/reads/'  # Folder to save processed images
```

#### Activate Python Environment and Install Dependencies

```bash
python3 -m venv myenv
source myenv/bin/activate  # On macOS/Linux
myenv\Scripts\activate     # On Windows
pip install chardet
```

#### Run the Script

Execute the Python script to process the collected binary file:

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
- Infrared Stream: [http://2.3.4.5:8080/cam1ir](http://2.3.4.5:8080/cam1ir)

**Data Streaming Ports:**

- Camera 0: Port `5000`
- Camera 1: Port `5001`
- Camera 2: Port `5002`

Ensure you have permission to access and process these streams.

---

## **Example Output**

**Console Output:**

Example of plateextract.py
```plaintext
{'Plate': 'ER61033', 'ColorName': 'gray', 'MakerName': 'CHEVROLET', 'ModelName': 'IMPALA'}
{'Plate': '497088D', 'ColorName': 'black', 'MakerName': 'DODGE', 'ModelName': 'CHALLENGER'}
...

```
Example of lpr_stream_processor.py
```plaintext
[INFO] Processed vehicle data: {'Plate': '2188624', 'ColorName': 'black', 'MakerName': 'NISSAN', 'ModelName': 'MAXIMA', 'Timestamp': '010725-212304'}
[INFO] Processed vehicle data: {'Plate': 'CK55397', 'ColorName': 'black', 'MakerName': 'CHEVROLET', 'ModelName': 'SPARK', 'Timestamp': '010725-212304'}
[INFO] Processed vehicle data: {'Plate': 'DY74804', 'ColorName': 'black', 'MakerName': 'MERCEDES-BENZ', 'ModelName': 'E CLASS', 'Timestamp': '010725-212304'}
...
```

**Saved Images:**
Images will be saved in the output folder with filenames: PLATE

- `ER61033-010725-114622.jpg`
- `497088D-010725-114622.jpg`

---

## **Contribution and Feedback**

This project is experimental and open to improvements. Feel free to modify the script to fit your specific use case. Contributions, feedback, and ideas are welcome.

---

## **Disclaimer**

This tool is for **educational purposes only**. The authors are not liable for any misuse or unauthorized application of this tool. Use responsibly and ethically.
















# LPRPARSER  
**Educational - Experimental License Plate Reader (LPR) Data Processor**  

LPRPARSER is an experimental project that processes data collected from Motorola License Plate Readers (LPR). 
This tool demonstrates extracting and processing data streams, including license plates, vehicle makes, models, and associated images.

---

## Disclaimer  
This project is for educational purposes only. The authors and contributors are not responsible for the misuse or unauthorized use of this tool. 
Always ensure you comply with local laws and regulations.

---



## Overview  
LPRPARSER connects to Motorola LPR cameras to capture and process data streams. The tool supports:  
- Extracting license plates  
- Processing vehicle information (make, model, color)  
- Saving associated images  

---

## Getting Started  

### Using Netcat for Manual Processing  
In this approach, netcat is used to capture data from the LPR camera. This is ideal for experimentation and understanding the data format.

**Step 1: Collecting Data**  
Run the following command to capture raw data from the LPR camera:

```bash
nc -v <camera_ip> <camera_port> > collectedcars.bin
