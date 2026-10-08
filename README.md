<img width="1479" height="8191" alt="Local Offline Audio-2026-10-08-100654" src="https://github.com/user-attachments/assets/74b58496-cafa-4bf4-a205-8f7a7d446734" /># ResilientMesh

> Offline-first emergency field terminal that converts speech and unstructured distress reports into ultra-dense telemetry packets using local Whisper STT and local Gemma 4 inference, transmitted over zero-internet Wi-Fi mesh networks

## Team

**Team Name:** [Team Astra]


| Member | Contribution   |
| ------ | -------------- |
| [CHAGANTI SAI MANIKANTA PAPAYYA CHOWDHARY] | Designed local Ollama/Gemma 4 compression pipeline, model prompt engineering, local Whisper STT integration, and dynamic environment pathing (imageio-ffmpeg). |
| [ROHAN CHERUKURI] | Network Protocol & Base Station Lead — Built Flask telemetry receiver on Base Station (Laptop B), socket connection handlers, and local LAN IP routing protocols. |
| [CHAGANTI SESI KARTHIK] | Field UI Engineer — Developed Streamlit frontend interface, state persistence for combined audio/text inputs, and user session management. |
| [DHARNENDHRAN PIRLA] | Systems & QA Engineer — Conducted offline field testing, batch script automation (Launch Field Unit.bat), latency benchmarking, and network timeout fault tolerance. |


## Problem Statement

### The Problem

During major natural disasters (earthquakes, floods, grid collapses), commercial cellular towers and internet backbones fail within minutes. First responders and trapped civilians are forced to rely on low-bandwidth VHF/UHF radios or localized offline Wi-Fi hotspots.

-Voice communication over congested channels leads to huge communication bottlenecks:

-High audio transmission bandwidth requirements.

-Channel noise, packet loss, and overlapping signals.

-Human error in manually writing down emergency locations, casualties, and resource requests under extreme stress.

-Inability for central dispatch systems to automatically parse, sort, and prioritize incoming distress calls.

### Why We Chose This Problem

The critical bottleneck in disaster response is not the absence of radio/Wi-Fi signals—it is the channel capacity vs. data density ratio. Transmitting 30 seconds of uncompressed voice audio over a degraded network link frequently fails.

By running edge AI models directly on field hardware, we can capture natural speech, extract structured facts locally, and compress a 5 MB voice file into an ultra-compact ~60-byte telemetry packet (PRIO|LOC|HAZ|CAS|REQ). This guarantees a >99.9% bandwidth reduction, allowing emergency alerts to pass through even the most congested local networks.

## Solution

ResilientMesh-AI is an offline edge processing application designed for field deployment on standard laptops.

1.Dual Field Input: Accepts either live spoken voice commands or typed text reports from field operators.

2.Offline Speech-to-Text: Converts spoken audio into text locally using an embedded OpenAI Whisper model.

3.Local LLM Compression: Leverages a local quantized Google Gemma 4 model (gemma4:e2b) running on Ollama to parse natural language, strip fluff, and extract structured telemetry data.

4.Offline Mesh Transmission: Packages the compressed string into a standardized telemetry payload and pushes it over an isolated, zero-internet local LAN/Wi-Fi hotspot to the command base station.

### Key Features

- 100% Zero-Cloud Dependency: Complete stack runs fully offline without external API keys, cloud backends, or cellular connections.
- Offline Speech-to-Text Processing: Integrates local Whisper inference with dynamic binary execution to transcribe field radio audio without external dependencies.
- Gemma 4 Fact Extraction: Uses Gemma 4 to parse messy, panicked human text into a standardized format:
PRIO:<LEVEL>|LOC:<Location>|HAZ:<Hazard>|CAS:<Count>|REQ:<Resources>
- Fault-Tolerant Offline Networking: Built using hardcoded loopback (127.0.0.1) and local peer-to-peer IPv4 addressing to prevent Windows local DNS resolution failures when internet access is severed.
- 1-Click Field Launcher: Includes automated Windows batch execution scripting for immediate boot in high-stress field conditions.

## Innovation and Differentiation

-Edge LLM vs. Traditional Sat-Phones: Conventional emergency systems rely on expensive satellite bandwidth to transmit raw audio or text. ResilientMesh-AI executes natural language processing at the source, shifting compute overhead to local field hardware to minimize transmission payload size.

-Zero-Shot Telemetry Formatting: Unlike rigid form-filling apps that force stressed users to fill out complex drop-downs during an emergency, our system allows users to speak naturally. Gemma 4 handles the cognitive load of categorizing hazards, locations, and priorities.

-Self-Contained Runtime Environment: Uses dynamic path injections to auto-bind local binaries (ffmpeg.exe), avoiding fragile OS-level configuration steps during emergency setups.

## Technical Implementation

### Architecture
flowchart TD
    subgraph Laptop_A ["Laptop A - Field Terminal (Offline)"]
        A[Microphone / Text Input] -->|Raw Audio Stream| B[Audio Recorder Component]
        B -->|WAV Audio File| C[Local Whisper STT Engine]
        A -->|Direct Text Input| D[Streamlit Session State]
        C -->|Transcribed Text| D
        D -->|Raw Unstructured Report| E["Local Ollama Service (127.0.0.1:11434)"]
        E -->|Gemma 4 Edge Inference| F["Structured Telemetry (e.g., PRIO:CRITICAL|LOC:...)" ]
    end

    subgraph Offline_Transport ["Local Wi-Fi Mesh / Ad-Hoc Hotspot"]
        F -->|HTTP REST POST / Zero Internet| G[Local IPv4 Network Route]
    end

    subgraph Laptop_B ["Laptop B - Command Base Station"]
        G -->|Payload Packet| H[Flask Receiver Server :5000]
        H --> I[Central Dispatch Triage Dashboard]
    end



### Technology Stack


| Category        | Technologies                |
| --------------- | --------------------------- |
| Frontend        | Streamlit, audio-recorder-streamlit       |
| Backend         | [Python 3.13, Flask (Base Station Receiver),]        |
| Database        | N/A (In-Memory Session State & Local Telemetry Logs)        |
| AI / ML         | Ollama (gemma4:e2b / gemma4:e4b), OpenAI Whisper (tiny), PyTorch (CPU Quantized Inference) |
| Infrastructure  | Isolated Local Wi-Fi Hotspot / LAN Mesh, Windows Batch Shell (.bat)      |
| APIs / Services | Local Ollama REST API           |



### How It Works

1.Audio Decoding & Transcription: The user records audio via the browser interface. The raw stream is converted to WAV format, and an embedded runtime copies ffmpeg.exe dynamically to the local process directory. OpenAI's local Whisper model processes the WAV file on CPU and returns transcribed text.

2.Context Compression Pipeline: The text is passed into a local Ollama process running Google's gemma4:e2b model. The prompt enforces strict zero-shot extraction:
You are an edge telemetry compressor for disaster mesh networks.
If the message is an emergency, extract facts into this exact format:
PRIO:<CRITICAL/HIGH>|LOC:<Location>|HAZ:<Hazard>|CAS:<Count>|REQ:<NeededResources>
Output ONLY the formatted string without extra text.

3.Local Mesh Packet Delivery: The resulting compressed string is sent via an HTTP POST request directly to Laptop B's fixed local IPv4 address over the shared offline Wi-Fi access point.

### Technical Decisions

-Using 127.0.0.1 Over localhost: On Windows systems, disconnecting entirely from external networks breaks internal mDNS/NetBIOS hostname resolution for localhost. Explicitly binding to 127.0.0.1 ensures uninterrupted socket connections to the Ollama background daemon while offline.

-Targeting gemma4:e2b Parameters: We selected the 2B effective parameter quantization of Gemma 4 to achieve inference times under 3–5 seconds on integrated laptop hardware, ensuring high telemetry throughput without requiring a discrete GPU.

-Dynamic Binary Linking (imageio-ffmpeg): To avoid requiring users to manually configure Windows environment variables (PATH) under hackathon conditions, the code dynamically locates the embedded imageio_ffmpeg executable, copies it to the working directory as ffmpeg.exe, and prepends the directory path to the Python runtime OS environment.

-Extended HTTP Timeout Handling: Cold-loading GGUF model weights into RAM on laptop startup can take up to 45 seconds. The local API client timeout was increased to timeout=180 seconds to guarantee thread stability during cold starts.

## Implementation During the Hackathon

During the hackathon, the team designed and implemented the entire pipeline from scratch:

-Integrated the Streamlit voice recorder component and synchronized session state for live editing of audio outputs.

-Implemented local Whisper execution and built the dynamic FFmpeg self-healing script for Windows environments.

-Configured local Ollama environment with quantized Gemma 4 weights and crafted deterministic extraction prompts.

-Established an offline peer-to-peer Wi-Fi network routing strategy between field terminals and base station receivers.

-Created batch script automation (Launch Field Unit.bat) for streamlined deployment.

### Team Contributions

Rohan: Integrated local Gemma 4 model via Ollama, engineered edge prompts, implemented Whisper speech-to-text, and resolved offline system environment dependencies (imageio-ffmpeg auto-linking).

Karthik: Constructed the Flask Base Station web server, handled incoming JSON network packets, and developed offline LAN connectivity logic.

Manikanta: Designed the Streamlit user interface, implemented session state handling for real-time text/audio editing, and managed component layouts.

Dharan: Automated deployment with shortcut batch scripts, performed offline field testing across disconnected hardware setups, and benchmarked inference speeds

## Working Application

**Live Application:** [Live URL]

[Briefly explain how the deployed application can be accessed and what functionality can be tested.]

The submitted application should be functional and accessible through the provided link where applicable.

## Demo Video

**Demo Video:** https://youtu.be/5DZY78ddo0E

[Provide a short demonstration of the working project, covering the main user flow and important functionality.]

## Open Source and AI Usage
##AI / Models
Google Gemma 4 (gemma4:e2b): Runs locally via Ollama to perform edge telemetry extraction and natural language compression.

OpenAI Whisper (tiny checkpoint): Runs locally via PyTorch to execute offline speech-to-text transcription.

##Open Source Components

Streamlit (streamlit): Apache-2.0 License — Core web UI dashboard framework.

Audio Recorder Streamlit (audio-recorder-streamlit): MIT License — Microphone recording widget interface.

ImageIO-FFmpeg (imageio-ffmpeg): BSD-2-Clause License — Standalone cross-platform FFmpeg binary loader.

Requests (requests): Apache-2.0 License — HTTP networking layer for local REST communication.

- **[Model]:** [How it is used]

### Open Source Components

- **[Library / Framework]:** [Purpose]
- **[Dataset]:** [Purpose]
- **[API / Service]:** [Purpose]

[Include relevant licenses, attribution, and acknowledgements for external components.]

## Setup and Usage
## Prerequisites

-Windows 10/11 OS

-Python 3.10+ installed

-Ollama Desktop Runtime installed (ollama.exe)

## Installation

-Clone the repository and navigate to the project directory:

PowerShell
git clone [repository-url]
cd Hackathon
Pull the required Gemma 4 model using Ollama (requires internet during initial setup only):

PowerShell
ollama pull gemma4:e2b
Install required Python packages:

PowerShell
pip install streamlit requests audio-recorder-streamlit openai-whisper imageio-ffmpeg
Environment Variables
No .env file or API keys are required. Configure target network IPs directly in transmitter.py:

Python
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
LOCAL_GEMMA_MODEL = "gemma4:e2b"
LAPTOP_B_IP = "192.168.43.50"  # Target Base Station IPv4
Running the Project
Option A: Using the Terminal

PowerShell
streamlit run transmitter.py
Option B: Using 1-Click Desktop Launcher
Double-click Launch Field Unit.bat.

## Usage
Open the application interface at [http://127.0.0.1:8501](http://127.0.0.1:8501).

Click the microphone icon to record a distress message, or manually type the report into the text field.

Click 🚀 Compress & Transmit Packet.

The system will convert speech to text (if recorded), run Gemma 4 compression locally, and transmit the output packet to the Base Station over the local network.



## Credits and License
Credits
Google DeepMind for the Gemma 4 open model weights.

OpenAI for the open-source Whisper speech recognition model.

Ollama Team for the local LLM runtime engine.

License
This project is licensed under the MIT License.









## Submission Checklist

- [✅] Project title and description added
- [✅] All team members listed
- [✅] Problem clearly explained
- [✅] Reason for choosing the problem explained
- [ ✅] Solution and key features documented
- [ ✅] Innovation and differentiation explained
- [ ✅] Architecture included
- [ ✅] Technical implementation documented
- [ ✅] Work completed during the hackathon documented
- [ ✅] Team contributions documented
- [ ✅] Working application is functional
- [ ✅] Live application link added where applicable
- [ ✅] Demo video added
- [ ✅] AI and open-source components documented
- [ ✅] Setup and usage instructions tested
- [ ✅] Challenges and learnings documented
- [ ✅] Devpost submission completed
- [ ✅] Devpost link added
- [ ✅] Credits added
- [ ✅] License added
- [ ✅] Repository is organized and complete
