from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DevFlux Intelligence",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ DevFlux: GitHub ML Ecosystem Intelligence")
st.caption("Longitudinal developer activity & technology velocity tracking powered by Bright Data Scraper Studio.")

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path(".")
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Load generated tables
longitudinal_file = PROCESSED_DIR / "longitudinal_all_snapshots.csv"
latest_deltas_file = PROCESSED_DIR / "latest_repo_deltas.csv"
category_velocity_file = PROCESSED_DIR / "category_velocity.csv"
top_breakouts_file = PROCESSED_DIR / "top_breakout_repositories.csv"

if category_velocity_file.exists() and latest_deltas_file.exists():
    df_cat = pd.read_csv(category_velocity_file)
    df_latest = pd.read_csv(latest_deltas_file)
    df_top = pd.read_csv(top_breakouts_file) if top_breakouts_file.exists() else df_latest.head(10)

    # Dynamic column resolver
    growth_col = (
        "net_star_growth" if "net_star_growth" in df_cat.columns 
        else "total_star_growth" if "total_star_growth" in df_cat.columns 
        else "net_growth" if "net_growth" in df_cat.columns 
        else df_cat.columns[3]
    )

    # Top KPI Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monitored Repositories", len(df_latest))
    c2.metric("Total Ecosystem Stars", f"{df_latest['stars'].sum():,}")
    c3.metric("Net 24h Star Growth", f"+{int(df_cat[growth_col].sum()):,} stars")
    top_cat = df_cat.sort_values(by=growth_col, ascending=False).iloc[0]["primary_category"]
    c4.metric("Fastest Growing Domain", top_cat)

    st.markdown("---")

    # Visual Analytics Row
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Category Velocity (Net Star Growth)")
        fig_velocity = px.bar(
            df_cat,
            x=growth_col,
            y="primary_category",
            orientation="h",
            color="primary_category",
            labels={growth_col: "Net Star Growth (Δ)", "primary_category": "Domain"},
            text=growth_col
        )
        fig_velocity.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_velocity, width="stretch")

    with col_right:
        st.subheader("🔥 Top Breakout Repositories (Momentum)")
        top_plot = df_top.head(5)
        fig_breakouts = px.bar(
            top_plot,
            x="star_growth",
            y="repo_name",
            orientation="h",
            color="primary_category",
            labels={"star_growth": "Stars Gained", "repo_name": "Repository"},
            text="star_growth"
        )
        fig_breakouts.update_layout(yaxis={'autorange': 'reversed'})
        st.plotly_chart(fig_breakouts, width="stretch")

    # Full Interactive Explorer
    st.subheader("🔍 Real-Time Momentum Explorer")
    display_cols = ["repo_name", "primary_category", "stars", "stars_prev", "star_growth", "star_growth_rate", "momentum_score", "signal", "language", "repo_url"]
    existing = [c for c in display_cols if c in df_latest.columns]
    st.dataframe(df_latest[existing], width="stretch")

else:
    st.warning("Processed snapshot data not found. Please run 'python src/run_pipeline.py' first.")