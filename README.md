# LPRPARSER

## Educational - Experimental License Plate Reader (LPR) Data Processor

LPRPARSER is an experimental project designed to process data collected from Motorola License Plate Readers (LPR). This tool demonstrates how to extract and process data streams, including license plates, vehicle makes, models, and associated images.

### **Disclaimer**

This project is for **educational purposes only**. The authors and contributors are not responsible for any misuse or unauthorized use of this tool. Always ensure you comply with local laws and regulations when using any LPR-related technology.

---

## Table of Contents  
1. [Overview](#overview)  
2. [Getting Started](#getting-started)  
   - [Using Netcat for Manual Processing](#using-netcat-for-manual-processing)  
   - [Connecting Directly to the LPR](#connecting-directly-to-the-lpr)  
3. [Example Output](#example-output)  
4. [Accessing LPR Cameras](#accessing-lpr-cameras)  
5. [Contribution and Feedback](#contribution-and-feedback)  
6. [Bounty for Geolocation Assistance](#bounty-for-geolocation-assistance)  

---

## **Overview**

LPRPARSER connects to a TCP port on a Motorola LPR camera, captures binary data using `netcat`, and processes it using a Python script. The script extracts license plates, vehicle information (make and model), and associated images from the raw data.

This project was inspired by a YouTube video from [@mattbrwn](https://www.youtube.com/@mattbrwn), particularly his exploration of license plate readers (LPRs) in his video, [Public Video and Data Feeds of Highway License Plate Readers](https://www.youtube.com/watch?v=0dUnY1641WM&t).

In the video, Matt demonstrates how publicly accessible LPR systems can be found through a simple Censys web search, revealing a widespread lack of infrastructure and network security management. This sparked our curiosity to see just how easily data from these systems could be accessed and reverse-engineered.

Upon investigating these devices, we discovered that they not only provide live color and infrared (IR) video feeds but also stream unencrypted metadata over TCP ports. For instance, a camera’s infrared stream, labeled `cam0ir`, correlates with data being streamed on TCP port 5000, while `cam1ir` correlates with port 5001. A single IP address can host multiple camera feeds (five or more in some cases), each tied to a specific TCP port. This inherent lack of security means that anyone with the appropriate tools can connect to these cameras and retrieve sensitive data, including license plates, images, and vehicle details, without any form of encryption, password protection, or handshake verification.

The simplicity of this system turned this into an exciting challenge: how quickly could we reverse-engineer the proprietary data streams and extract meaningful information? The entire project, from discovery to functional implementation, took less than two hours. While we do not actively collect or harvest any data, this experiment highlights significant privacy concerns. It is alarming that the cameras our government agencies use to monitor traffic and public movement—visible on telephone poles and traffic lights—are left open and unsecured. This creates a gateway for malicious actors or criminal organizations to exploit these systems, harvesting sensitive information such as license plates and vehicle images. Such vulnerabilities pose serious risks, from enabling identity theft to facilitating large-scale tracking of individuals without consent.

This project underscores several critical issues: the widespread collection of personal data without adequate safeguards, the dangers of insecure Internet of Things (IoT) devices, and the lack of regard for public privacy and safety. In just a short period of experimentation, we observed live, unsecured LPR streams across several states, openly providing license plate numbers, vehicle images, and other metadata. This lack of security exposes individuals’ private information to anyone with an internet connection and basic technical knowledge.

Experiments like this are not only satisfying from a reverse-engineering perspective but also serve as a stark reminder of the vulnerabilities inherent in IoT systems. By repurposing and experimenting with these devices, we aim to bring attention to the risks posed by such insecure systems and advocate for better infrastructure management, encryption, and privacy protections.

---

## **Getting Started**

### **Prerequisites**

- Python 3.x installed on your system.
- Access to an LPR camera that streams data over TCP.

### **Using Netcat for Manual Processing**

#### Step 1: Collecting Data

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

#### Update the Processing File Path

Modify the bottom of the Python script `plateextract.py` to fit the paths of your data:

```python
file_path = '/test/collectedcars.bin'  # Path to your collected data file
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
2. Save associated images with filenames in the format: `PLATE-DATE-TIME.jpg`
   - **Example:** `ER61033-010725-114622.jpg`
3. Print extracted vehicle details in the console.

---

### **Connecting Directly to the LPR**

This approach directly connects to the LPR, streams data, and processes it in real-time.

#### Running the Streaming Processor

Run the following script to connect directly to the LPR and process data on the fly:

```bash
python3 lpr_stream_processor.py
```

You will be prompted to enter the following:  
- **IP Address**: Default: `1.2.3.4`.  
- **Port Number**: Default: `5001`.  
- **Output Folder for Images**: Default: `/test/plates`.  
- **Output File for Records**: Default: `/test/plates.txt`.  

**What It Does:**  
- Extracts and processes license plates, make, model, and color in real-time.  
- Saves images with filenames in the format: `PLATE-DATE-TIME.jpg`.  
- Outputs processed data to the specified records file with timestamps.  

**Example Output File Entry:**

```json
{'Plate': 'ER61033', 'ColorName': 'gray', 'MakerName': 'CHEVROLET', 'ModelName': 'IMPALA', 'Timestamp': '010725-114622'}
```

---

## **Example Output**

**Console Output:**

Example of `plateextract.py`:
```plaintext
{'Plate': 'ER61033', 'ColorName': 'gray', 'MakerName': 'CHEVROLET', 'ModelName': 'IMPALA'}
{'Plate': '497088D', 'ColorName': 'black', 'MakerName': 'DODGE', 'ModelName': 'CHALLENGER'}
...
```

Example of `lpr_stream_processor.py`:
```plaintext
[INFO] Processed vehicle data: {'Plate': '2188624', 'ColorName': 'black', 'MakerName': 'NISSAN', 'ModelName': 'MAXIMA', 'Timestamp': '010725-212304'}
[INFO] Processed vehicle data: {'Plate': 'CK55397', 'ColorName': 'black', 'MakerName': 'CHEVROLET', 'ModelName': 'SPARK', 'Timestamp': '010725-212304'}
[INFO] Processed vehicle data: {'Plate': 'DY74804', 'ColorName': 'black', 'MakerName': 'MERCEDES-BENZ', 'ModelName': 'E CLASS', 'Timestamp': '010725-212304'}
...
```

**Saved Images:**
Images will be saved in the output folder with filenames: `PLATE-DATE-TIME.jpg`

- `ER61033-010725-114622.jpg`
- `497088D-010725-114622.jpg`

---

## **Accessing LPR Cameras**

Motorola LPR cameras can be accessed at the following example URLs:

- Color Stream: [http://1.2.3.4:8080/cam1color](http://1.2.3.4:8080/cam1color)
- Infrared Stream: [http://2.3.4.5:8080/cam1ir](http://2.3.4.5:8080/cam1ir)

**Data Streaming Ports:**

- Camera 0: Port `5000`
- Camera 1: Port `5001`
- Camera 2: Port `5002`

Ensure you have permission to access and process these streams.

---

## **Contribution and Feedback**

This project is experimental and open to improvements. Feel free to modify the script to fit your specific use case. Contributions, feedback, and ideas are welcome.

---

## **Bounty for Geolocation Assistance**

I have observed references to GPS accuracy (e.g., `NumSatellitesGPS`) in the data stream. This suggests geolocation data such as latitude and longitude may also be embedded.  

Challenge for anyone who can extract the geo data from the stream.

