import pandas as pd

# Technology Category Rules
TAXONOMY = {
    "AI Agents": ["agent", "agents", "autonomous", "crewai", "langgraph", "swarm", "tool-use"],
    "Computer Vision": ["computer-vision", "image", "yolo", "opencv", "segmentation", "detection", "eraser"],
    "RAG & Retrieval": ["rag", "retrieval", "vector", "embedding", "search", "chroma", "pinecone"],
    "MLOps & Orchestration": ["airflow", "pipeline", "orchestration", "workflow", "scheduler", "mlops"],
    "Core ML & Deep Learning": ["deep-learning", "neural-network", "machine-learning", "pytorch", "tensorflow", "training"]
}

def classify_record(text_corpus: str) -> str:
    text = str(text_corpus).lower()
    for category, keywords in TAXONOMY.items():
        if any(kw in text for kw in keywords):
            return category
    return "General ML"

def process_and_classify(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)
    
    # Fill missing values
    df["repo_name"] = df["repo_name"].fillna("").astype(str) if "repo_name" in df.columns else df.get("product_page_url", "").astype(str)
    df["description"] = df["description"].fillna("").astype(str) if "description" in df.columns else ""
    df["topics"] = df["topics"].fillna("").astype(str) if "topics" in df.columns else ""
    
    # Combine signals for rule matching
    combined = df["repo_name"] + " " + df["description"] + " " + df["topics"]
    df["category"] = combined.apply(classify_record)
    
    df.to_csv(output_csv, index=False)
    print(f"✅ Classified {len(df)} records and saved to {output_csv}")
    print(df[["repo_name", "category"]].head(10))

if __name__ == "__main__":
    process_and_classify("data/sample/demo_run.csv", "data/processed/sample_classified.csv")