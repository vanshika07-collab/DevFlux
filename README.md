# DevFlux
A web data intelligence platform that analyzes public GitHub projects to uncover emerging, growing, and underexplored technology trends.

---

# Project Status
Currently under development as a part of web-data hackathon.

---

## Overview

DevFlux aims to analyze publicly available GitHub project data to understand:

- What developers are building
- Which technology areas are gaining momentum
- Which areas are becoming more saturated
- Which areas may be emerging or underexplored

---

## Technology

DevFlux is being built using web data, data analysis, machine learning, and a public-facing interface.

---

## Status

Development is currently underway.

---

# DevFlux
> A web data intelligence platform analyzing public GitHub ecosystem activity to detect emerging, accelerating, and saturated technology domains.

---

## 📌 Project Overview
DevFlux continuously monitors and analyzes open-source developer activity across public GitHub repositories. By processing snapshot time-series data, DevFlux uncovers:
- **Velocity & Momentum:** Which technology clusters are gaining developer adoption fastest.
- **Ecosystem Saturation:** High-density domains vs. emerging, underexplored niches.
- **Breakout Projects:** Emerging repositories exhibiting high star velocity.

---

## 🛠️ Architecture & Pipeline
GitHub Search Feed (Web Data)
    │
    ▼
[Bright Data Web Scraper] ──► Data Ingestion
    │
    ▼
[validator] ─────────────► Schema verification & data integrity checks
    │
    ▼
[classifier] ────────────► Domain Taxonomy Classification 
    │
    ▼
[change_detector] ───────► Delta calculation & Star-growth velocity tracking
    │  
    ▼
[Analytics & Presentation Layer] 

---

## 🏷️ Domain Taxonomy
Repositories are systematically classified across 5 core machine learning focus areas:
1. **AI Agents & Automation** (`swarm`, `autonomous`, `crewai`, `langgraph`, `tool-use`)
2. **Computer Vision** (`image`, `yolo`, `segmentation`, `detection`, `opencv`)
3. **RAG & Retrieval** (`vector`, `embedding`, `chroma`, `pinecone`, `search`)
4. **MLOps & Orchestration** (`airflow`, `pipeline`, `orchestration`, `workflow`)
5. **Core ML & Deep Learning** (`pytorch`, `tensorflow`, `neural-network`, `cuda`)

---

## 📊 Milestone Tracker
- [x] **Milestone 1:** Robust flat extraction scraper built and tested on GitHub search feeds.
- [x] **Milestone 2:** Data validation and schema verification established.
- [x] **Milestone 3:** Domain taxonomy classifier mapping 150+ baseline projects.
- [x] **Milestone 4:** Snapshot delta and velocity tracker implemented.
- [ ] **Milestone 5:** Multi-day snapshot collection & final trend visualization dashboard.