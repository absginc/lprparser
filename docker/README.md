# Motorola LPR Scanner Docker Guide

## Overview
This project provides a Dockerized tool to search for Motorola License Plate Reader (LPR) cameras over specified IP ranges. The tool sends HTTP requests to identify unsecured LPR cameras based on their unique response and saves the results to a specified output file.

---

## Features
- Specify IP ranges (e.g., `/24`, `/16`) to scan.
- Multi-threaded scanning for faster results.
- Results are saved in a mounted output folder.
- Use Docker Compose for managing multiple subnet scans.

---

## Launch Using Docker Run
You can run the scanner in Docker using the following command:

### Example for Scanning a Single Subnet
```bash
# Scan the 192.168.1.0/24 subnet with 10 threads and save the results
# to /tmp/lprs/found-192.168.1.0.txt

docker run -d --rm \
  -e IP_RANGE="192.168.1.0/24" \
  -e THREADS=10 \
  -e OUTPUT_FILE="/output/found-192.168.1.0.txt" \
  -v /tmp/lprs:/output \
  --name lprscan_192-168-1-0 \
  absgscott/motorola-lpr-scanner
```

**Explanation:**
- `IP_RANGE`: Subnet to scan.
- `THREADS`: Number of simultaneous connections.
- `OUTPUT_FILE`: File where found IPs will be saved.
- `/tmp/lprs`: Host directory where results will be stored.
- `--name`: Optional container name for tracking the scan.

### Example for Scanning Multiple Subnets Simultaneously
Run multiple containers in parallel for different subnets:
```bash
# Scan 4 /16 subnets with 35 threads each

docker run -d --rm -e IP_RANGE="166.146.0.0/16" -e THREADS=35 -e OUTPUT_FILE="/output/found-166.146.0.0.txt" -v /tmp/lprs:/output --name lprscan_166-146-0-0 absgscott/motorola-lpr-scanner

docker run -d --rm -e IP_RANGE="166.145.0.0/16" -e THREADS=35 -e OUTPUT_FILE="/output/found-166.145.0.0.txt" -v /tmp/lprs:/output --name lprscan_166-145-0-0 absgscott/motorola-lpr-scanner

docker run -d --rm -e IP_RANGE="166.144.0.0/16" -e THREADS=35 -e OUTPUT_FILE="/output/found-166.144.0.0.txt" -v /tmp/lprs:/output --name lprscan_166-144-0-0 absgscott/motorola-lpr-scanner

docker run -d --rm -e IP_RANGE="166.143.0.0/16" -e THREADS=35 -e OUTPUT_FILE="/output/found-166.143.0.0.txt" -v /tmp/lprs:/output --name lprscan_166-143-0-0 absgscott/motorola-lpr-scanner
```
Example Output
```bash
eff1967dd31eb71d7f05e74369d9cd764aaa6705fada08cdeb6ee3f35f3ccf49
9479dad9eadc5cdc86993b72d2ba27c6429579d25a85cfc51b0f97c6fc15c5b8
29ae16fc91e53ca02af7a06be414b3f9799f4fecd5d37d28256b7e9b08c3e697
84927ce1fb3672e283197f0e15544e0992cd732a25905c2f9609ea554161bf39

~# docker ps
CONTAINER ID   IMAGE                            COMMAND               CREATED          STATUS          PORTS     NAMES
84927ce1fb36   absgscott/motorola-lpr-scanner   "python3 search.py"   31 seconds ago   Up 30 seconds             lprscan_166-143-0-0
29ae16fc91e5   absgscott/motorola-lpr-scanner   "python3 search.py"   32 seconds ago   Up 31 seconds             lprscan_166-144-0-0
9479dad9eadc   absgscott/motorola-lpr-scanner   "python3 search.py"   33 seconds ago   Up 32 seconds             lprscan_166-145-0-0
eff1967dd31e   absgscott/motorola-lpr-scanner   "python3 search.py"   35 seconds ago   Up 34 seconds             lprscan_166-146-0-0
```
4 Containers are launched and will automatically be removed when the scan is completed, results if available are in your mounted folder.

---

## Launch Using Docker Compose
To manage multiple scans simultaneously, use Docker Compose:

### **docker-compose.yml**
```yaml
version: "3.9"
services:
  lprscan_166-146-0-0:
    image: absgscott/motorola-lpr-scanner
    container_name: lprscan_166-146-0-0
    environment:
      - IP_RANGE=166.146.0.0/16
      - THREADS=35
      - OUTPUT_FILE=/output/found-166.146.0.0.txt
    volumes:
      - /tmp/lprs:/output
    restart: "no"

  lprscan_166-145-0-0:
    image: absgscott/motorola-lpr-scanner
    container_name: lprscan_166-145-0-0
    environment:
      - IP_RANGE=166.145.0.0/16
      - THREADS=35
      - OUTPUT_FILE=/output/found-166.145.0.0.txt
    volumes:
      - /tmp/lprs:/output
    restart: "no"

  lprscan_166-144-0-0:
    image: absgscott/motorola-lpr-scanner
    container_name: lprscan_166-144-0-0
    environment:
      - IP_RANGE=166.144.0.0/16
      - THREADS=35
      - OUTPUT_FILE=/output/found-166.144.0.0.txt
    volumes:
      - /tmp/lprs:/output
    restart: "no"

  lprscan_166-143-0-0:
    image: absgscott/motorola-lpr-scanner
    container_name: lprscan_166-143-0-0
    environment:
      - IP_RANGE=166.143.0.0/16
      - THREADS=35
      - OUTPUT_FILE=/output/found-166.143.0.0.txt
    volumes:
      - /tmp/lprs:/output
    restart: "no"
```

### Running the Compose File
```bash
docker-compose up -d
```

This will launch all the services defined in the `docker-compose.yml` file.

---

## Output Files
The results for each subnet scan will be saved in the `/tmp/lprs` directory on the host machine or your mounted path. Each file is named according to the `OUTPUT_FILE` environment variable.

Example files:
```
/tmp/lprs/found-166.146.0.0.txt
/tmp/lprs/found-166.145.0.0.txt
/tmp/lprs/found-166.144.0.0.txt
/tmp/lprs/found-166.143.0.0.txt
```

---

## Troubleshooting
- Ensure Docker is installed and running.
- Verify that the `/tmp/lprs` or modified equivalent directory exists and is writable.
- Check the container logs for er
- rors using `docker logs <container_name>`. 
---

## Notes
This tool is intended for research and educational purposes only. Always adhere to ethical and legal standards when using this application.
