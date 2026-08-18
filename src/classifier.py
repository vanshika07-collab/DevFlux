import os
import pandas as pd

# Domain Taxonomy (Evaluated top-to-bottom: Specific domains before General/Core ML)
TAXONOMY = {
    "AI Agents": ["agent", "agents", "autonomous", "crewai", "langgraph", "swarm", "trading-bot", "tool-use"],
    "Computer Vision": ["computer-vision", "image", "yolo", "opencv", "segmentation", "detection", "eraser", "ocr"],
    "RAG & Retrieval": ["rag", "retrieval", "vector", "embedding", "search", "chroma", "pinecone", "milvus"],
    "MLOps & Orchestration": ["airflow", "pipeline", "orchestration", "workflow", "scheduler", "mlops", "docker", "kubernetes"],
    "Core ML & Deep Learning": ["deep-learning", "neural-network", "machine-learning", "pytorch", "tensorflow", "training", "cuda"]
}

def classify_record(text_corpus: str) -> str:
    text = str(text_corpus).lower()
    for category, keywords in TAXONOMY.items():
        if any(kw in text for kw in keywords):
            return category
    return "General ML"

def process_and_classify(input_csv: str, output_csv: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv)
    
    # Fill missing text values
    df["repo_name"] = df["repo_name"].fillna("").astype(str) if "repo_name" in df.columns else ""
    df["description"] = df["description"].fillna("").astype(str) if "description" in df.columns else ""
    df["topics"] = df["topics"].fillna("").astype(str) if "topics" in df.columns else ""
    
    # Combine signals for rule matching
    combined = df["repo_name"] + " " + df["description"] + " " + df["topics"]
    df["category"] = combined.apply(classify_record)
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print(f"✅ Classified {len(df)} records and saved to {output_csv}")
    print("\n--- Category Distribution ---")
    print(df["category"].value_counts().to_string())
    return df

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if "__file__" in locals() else "."
    raw_path = os.path.join(base_dir, "data", "raw", "raw_2026_08_19.csv")
    classified_path = os.path.join(base_dir, "data", "processed", "classified_2026_08_19.csv")
    process_and_classify(raw_path, classified_path)