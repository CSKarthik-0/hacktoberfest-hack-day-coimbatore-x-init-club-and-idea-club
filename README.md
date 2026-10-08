# ResilientMesh

> Offline-first emergency field terminal that converts speech and unstructured distress reports into ultra-dense telemetry packets using local Whisper STT and local Gemma 4 inference, transmitted over zero-internet Wi-Fi mesh networks

## Team

**Team Name:** [Team Name]


| Member | Contribution   |
| ------ | -------------- |
| [Name] | [Contribution] |
| [Name] | [Contribution] |
| [Name] | [Contribution] |
| [Name] | [Contribution] |


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


### Technology Stack


| Category        | Technologies                |
| --------------- | --------------------------- |
| Frontend        | [Technologies / N/A]        |
| Backend         | [Technologies / N/A]        |
| Database        | [Technologies / N/A]        |
| AI / ML         | [Models / frameworks / N/A] |
| Infrastructure  | [Technologies / N/A]        |
| APIs / Services | [Services / N/A]            |


If a category or technology is not implemented in the project, specify `N/A` instead of leaving the field blank.

### How It Works

[Explain the major components of the system and how they interact.]

### Technical Decisions

[Explain important architectural, algorithmic, or engineering decisions made during development.]

## Implementation During the Hackathon

[Describe what the team built during the Hack Day and the major functionality or components completed during the event.]

### Team Contributions

- **[Member Name]:** [Contribution]
- **[Member Name]:** [Contribution]
- **[Member Name]:** [Contribution]
- **[Member Name]:** [Contribution]

## Working Application

**Live Application:** [Live URL]

[Briefly explain how the deployed application can be accessed and what functionality can be tested.]

The submitted application should be functional and accessible through the provided link where applicable.

## Demo Video

**Demo Video:** [Video URL]

[Provide a short demonstration of the working project, covering the main user flow and important functionality.]

## Open Source and AI Usage

### AI / Models

- **[Model]:** [How it is used]

### Open Source Components

- **[Library / Framework]:** [Purpose]
- **[Dataset]:** [Purpose]
- **[API / Service]:** [Purpose]

[Include relevant licenses, attribution, and acknowledgements for external components.]

## Setup and Usage

### Prerequisites

- [Requirement]
- [Requirement]

### Installation

```bash
git clone [repository-url]
cd [project-directory]
[installation-command]
```

### Environment Variables

```env
[VARIABLE_NAME]=[value]
```



### Running the Project

```bash
[run-command]
```

### Usage

[Explain the basic steps required to use the project.]

## Devpost Submission

**Devpost Project:** [Devpost Project URL]

[Add the link to the team's Devpost submission. Ensure the Devpost project page is complete and contains the required project information, links, media, and team details.]

## Credits and License

### Credits

[Credit libraries, frameworks, datasets, models, APIs, contributors, and other external resources used.]

### License

[License name and/or link.]

## Submission Checklist

- [ ] Project title and description added
- [ ] All team members listed
- [ ] Problem clearly explained
- [ ] Reason for choosing the problem explained
- [ ] Solution and key features documented
- [ ] Innovation and differentiation explained
- [ ] Architecture included
- [ ] Technical implementation documented
- [ ] Work completed during the hackathon documented
- [ ] Team contributions documented
- [ ] Working application is functional
- [ ] Live application link added where applicable
- [ ] Demo video added
- [ ] AI and open-source components documented
- [ ] Setup and usage instructions tested
- [ ] Challenges and learnings documented
- [ ] Devpost submission completed
- [ ] Devpost link added
- [ ] Credits added
- [ ] License added
- [ ] Repository is organized and complete
