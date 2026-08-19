from pathlib import Path
import pandas as pd

TAXONOMY = {
    "AI Agents": ["agent", "agents", "autonomous", "crewai", "langgraph", "swarm", "trading-bot", "tool-use"],
    "Computer Vision": ["computer-vision", "image", "yolo", "opencv", "segmentation", "detection", "eraser", "ocr"],
    "RAG & Retrieval": ["rag", "retrieval", "vector", "embedding", "search", "chroma", "pinecone", "milvus"],
    "MLOps & Orchestration": ["airflow", "pipeline", "orchestration", "workflow", "scheduler", "mlops", "docker", "kubernetes"],
    "Core ML & Deep Learning": ["deep-learning", "neural-network", "machine-learning", "pytorch", "tensorflow", "training", "cuda"]
}

def classify_record(repo_name: str, topics: str, language: str) -> list:
    text = f"{repo_name} {topics} {language}".lower()
    matched = [cat for cat, kws in TAXONOMY.items() if any(kw in text for kw in kws)]
    return matched if matched else ["General ML"]

def classify_all_snapshots():
    base = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path(".")
    processed_dir = base / "data" / "processed"
    clean_files = sorted(processed_dir.glob("clean_*.csv"))

    if not clean_files:
        print("⚠️ No cleaned snapshots found to classify.")
        return []

    print("=" * 60)
    print("STEP 3: DOMAIN TAXONOMY CLASSIFICATION")
    print("=" * 60)

    classified_files = []
    for filepath in clean_files:
        df = pd.read_csv(filepath)

        classifications = df.apply(
            lambda r: classify_record(r["repo_name"], r["topics"], r["language"]), 
            axis=1
        )

        df["categories"] = classifications.apply(lambda cats: "|".join(cats))
        df["primary_category"] = classifications.apply(lambda cats: cats[0])

        out_name = filepath.name.replace("clean_", "classified_")
        out_path = processed_dir / out_name
        df.to_csv(out_path, index=False)
        
        print(f"   🏷️ {filepath.name} -> {out_name} ({len(df)} repos)")
        classified_files.append(out_path)

    return classified_files

if __name__ == "__main__":
    classify_all_snapshots()