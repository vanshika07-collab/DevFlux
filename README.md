# DevFlux
A web data intelligence platform that analyzes public GitHub projects to uncover emerging, growing, and underexplored technology trends.Open-Source AI/ML Ecosystem Intelligence Radar

A longitudinal adoption and velocity tracking engine for machine learning frameworks, libraries, and breakout architectures powered by Bright Data Scraper Studio.

🔗 **Live Public Dashboard:** [https://devflux-analysis.streamlit.app/]  

---

## Overview & Problem Statement

Most open-source tracking tools rely on static cumulative star counts, heavily skewing visibility toward legacy monolithic projects while burying emerging, high-velocity developer tools.

**DevFlux** treats web data extraction as an automated time-series engine. By capturing daily multi-snapshot deltas across public GitHub machine learning repositories, DevFlux isolates:
- **Sector Velocity:** Normalized daily growth ($\Delta$) across specialized AI disciplines.
- **Momentum Index:** A compound score balancing absolute star volume with percentage growth rate.
- **Cooling / Regression Radar:** Real-time detection of stalled, deprecated, or unstarred codebases.

---

## Methodology: Moving Beyond Vanity Metrics

Raw star totals represent lagging historical mindshare. DevFlux implements three analytical layers to uncover authentic developer momentum:

1. **First-Order Time-Series Deltas ($\Delta S_t = S_t - S_{t-1}$):** Measures real-world 24-hour developer attention shifts rather than legacy star inertia.
2. **Domain-Normalized Velocity ($\bar{V}_c = \frac{1}{N_c} \sum \Delta S_i$):** Benchmarks average repo velocity within a specific discipline to prevent general deep learning giants from drowning out high-acceleration niches like Vector Retrieval or AI Agents.
3. **Compound Momentum Index:** Combines absolute growth with rate-of-change to distinguish genuine breakout frameworks from high-percentage noise.

---

## Bright Data Scraper Studio Integration

DevFlux relies on a custom web collector built with **Bright Data Scraper Studio** to extract structured metadata directly from public GitHub search feeds.

* **Custom Collector ID:** `c_msyw70buwjvpywmh0`
* **Target Population:** Public GitHub repositories matching `topic:machine-learning stars:>50`, ordered by recently updated (`s=updated&o=desc`).
* **Production API Endpoint:** `POST https://api.brightdata.com/dca/trigger?collector=c_msyw70buwjvpywmh0`
* **Automated Data Fetching (`src/fetcher.py`):** Calls the Collector API directly, polls for completion, and automatically ingests timestamped snapshots into `data/raw/`.
* **Idempotent Ingestion:** The pipeline verifies local snapshot existence prior to triggering live API calls to optimize credit utilization.

---

## Architecture & Pipeline
GitHub Search Feed (Web Data)    ------------>    Bright Data Web Scraper (Data Ingestion)    ------------>    validator (Schema verification & data integrity checks)    ------------>    classifier (Domain Taxonomy Classification)    ------------>       change_detector (Delta calculation & Star-growth velocity tracking)    ------------>    Analytics & Presentation Layer


---

## Domain Taxonomy
Repositories are systematically classified across 5 core machine learning focus areas:
1. **AI Agents & Automation** (`swarm`, `autonomous`, `crewai`, `langgraph`, `tool-use`)
2. **Computer Vision** (`image`, `yolo`, `segmentation`, `detection`, `opencv`)
3. **RAG & Retrieval** (`vector`, `embedding`, `chroma`, `pinecone`, `search`)
4. **MLOps & Orchestration** (`airflow`, `pipeline`, `orchestration`, `workflow`)
5. **Core ML & Deep Learning** (`pytorch`, `tensorflow`, `neural-network`, `cuda`)

---

## Milestone Tracker

[x] Milestone 1: Production web collector deployed on Bright Data Scraper Studio.
[x] Milestone 2: Multi-format validation, dynamic alias mapping, and schema auditing pipeline built.
[x] Milestone 3: Domain taxonomy classifier mapping active repositories into specialized sectors.
[x] Milestone 4: Time-series delta engine and momentum scoring algorithm implemented.
[x] Milestone 5: Public interactive visual radar deployed with Dark/Light theme switching and sector analytics.

---

## Quickstart & Local Reproduction

Anyone can clone and run DevFlux locally with existing data or by dropping new snapshot CSVs into `data/raw/`.

### 
# 1. Clone the repository
git clone [https://github.com/vanshika07-collab/DevFlux.git](https://github.com/vanshika07-collab/DevFlux.git)
cd DevFlux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automated data pipeline
python src/run_pipeline.py

# 4. Launch the interactive radar
streamlit run src/dashboard.py