# DevFlux
A web data intelligence platform that analyzes public GitHub projects to uncover emerging, growing, and underexplored technology trends.

---

# Project Status
DevFlux continuously monitors and analyzes open-source developer activity across public GitHub repositories. By processing snapshot time-series data, DevFlux uncovers:
- **Velocity & Momentum:** Which technology clusters are gaining developer adoption fastest.
- **Ecosystem Saturation:** High-density domains vs. emerging, underexplored niches.
- **Breakout Projects:** Emerging repositories exhibiting high star velocity and organic momentum.

---

## 📌 Project Overview
DevFlux continuously monitors and analyzes open-source developer activity across public GitHub repositories. By processing snapshot time-series data, DevFlux uncovers:
- **Velocity & Momentum:** Which technology clusters are gaining developer adoption fastest.
- **Ecosystem Saturation:** High-density domains vs. emerging, underexplored niches.
- **Breakout Projects:** Emerging repositories exhibiting high star velocity.

---

## 🛠️ Architecture & Pipeline
GitHub Search Feed (Web Data)    ------------>    Bright Data Web Scraper (Data Ingestion)    ------------>    validator (Schema verification & data integrity checks)    ------------>    classifier (Domain Taxonomy Classification)    ------------>       change_detector (Delta calculation & Star-growth velocity tracking)    ------------>    Analytics & Presentation Layer


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
- [x] **Milestone 5:** Interactive web dashboard deployed with real-time KPI metrics and visual analytics (dashboard.py).
---

## 🚀 Quickstart & Local Reproduction

Anyone can clone and run DevFlux locally with existing data or by dropping new snapshot CSVs into `data/raw/`.

### 
1. Clone & Install Dependencies

Bash
git clone [https://github.com/vanshika07-collab/DevFlux.git](https://github.com/vanshika07-collab/DevFlux.git)
cd DevFlux
pip install -r requirements.txt

2. Execute Pipeline
Process, clean, audit, classify, and calculate longitudinal momentum across all raw snapshots:

Bash
python src/run_pipeline.py

3. Launch Interactive Dashboard

Bash
streamlit run src/dashboard.py
View the dashboard locally