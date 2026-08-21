from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DevFlux | Open Source Tech Radar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Sidebar & Theme Configuration
# ---------------------------------------------------------
with st.sidebar:
  st.markdown("## ⚡ DevFlux Radar")
  st.caption("Tracking what developers are actually building & adopting.")

  theme_mode = st.radio(
      "🎨 Theme Mode", ["Dark Velvet", "Clean Light"], index=0, horizontal=True
  )
  is_dark = theme_mode == "Dark Velvet"

  st.markdown("---")
  st.markdown("### 🎛️ Domain Filters")

# ---------------------------------------------------------
# Dynamic CSS Variables (Light vs Dark)
# ---------------------------------------------------------
if is_dark:
  bg_app = "#0B0F19"
  text_primary = "#F8FAFC"
  text_secondary = "#94A3B8"
  card_bg = (
      "linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8))"
  )
  card_border = "rgba(255, 255, 255, 0.08)"
  plotly_template = "plotly_dark"
  hero_grad = (
      "linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42,"
      " 0.95) 100%)"
  )
  insight_box = "rgba(30, 41, 59, 0.5)"
  insight_border = "#38BDF8"
else:
  bg_app = "#F8FAFC"
  text_primary = "#0F172A"
  text_secondary = "#475569"
  card_bg = "linear-gradient(145deg, #FFFFFF, #F1F5F9)"
  card_border = "rgba(0, 0, 0, 0.08)"
  plotly_template = "plotly_white"
  hero_grad = "linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%)"
  insight_box = "#F0F9FF"
  insight_border = "#0284C7"

st.markdown(
    f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="stApp"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: {bg_app} !important;
        color: {text_primary} !important;
    }}
    
    .hero-container {{
        background: {hero_grad};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }}
    .hero-title {{
        font-size: 2rem;
        font-weight: 800;
        color: {text_primary};
        margin-bottom: 4px;
    }}
    .hero-subtitle {{
        color: {text_secondary};
        font-size: 1rem;
        margin-bottom: 0px;
    }}
    
    .insight-pill {{
        background: {insight_box};
        border-left: 4px solid {insight_border};
        padding: 12px 18px;
        border-radius: 8px;
        margin: 12px 0px 20px 0px;
        color: {text_primary};
        font-size: 0.93rem;
    }}
    
    div[data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }}
    div[data-testid="stMetric"] label {{
        color: {text_secondary} !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: {text_primary} !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Data Loader
# ---------------------------------------------------------
BASE_DIR = (
    Path(__file__).resolve().parent.parent if "__file__" in locals() else Path(".")
)
PROCESSED_DIR = BASE_DIR / "data" / "processed"

category_file = PROCESSED_DIR / "category_velocity.csv"
latest_deltas_file = PROCESSED_DIR / "latest_repo_deltas.csv"
top_breakouts_file = PROCESSED_DIR / "top_breakout_repositories.csv"

if not (category_file.exists() and latest_deltas_file.exists()):
  st.error(
      "⚠️ Data files are being initialized. Please run `python"
      " src/run_pipeline.py` first."
  )
  st.stop()

df_cat = pd.read_csv(category_file)
df_latest = pd.read_csv(latest_deltas_file)
df_top = (
    pd.read_csv(top_breakouts_file)
    if top_breakouts_file.exists()
    else df_latest.head(10)
)

growth_col = (
    "net_star_growth"
    if "net_star_growth" in df_cat.columns
    else (
        "total_star_growth"
        if "total_star_growth" in df_cat.columns
        else df_cat.columns[3]
    )
)

# ---------------------------------------------------------
# Sidebar Filter Controls
# ---------------------------------------------------------
with st.sidebar:
  all_categories = sorted(
      df_latest["primary_category"].dropna().unique().tolist()
  )
  selected_categories = st.multiselect(
      "Focus Areas",
      options=all_categories,
      default=all_categories,
      help="Filter projects by technical domain.",
  )

  all_signals = sorted(df_latest["signal"].dropna().unique().tolist())
  selected_signals = st.multiselect(
      "Adoption Velocity",
      options=all_signals,
      default=all_signals,
      help="Filter by momentum categorization.",
  )

  min_stars = st.slider(
      "Minimum Total Stars",
      min_value=int(df_latest["stars"].min()),
      max_value=int(df_latest["stars"].max()),
      value=int(df_latest["stars"].min()),
      step=50,
  )

# Baseline Filter
df_filtered = df_latest[
    (df_latest["primary_category"].isin(selected_categories))
    & (df_latest["signal"].isin(selected_signals))
    & (df_latest["stars"] >= min_stars)
].copy()

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown(
    """
<div class="hero-container">
    <div class="hero-title">⚡ DevFlux Technology Radar</div>
    <div class="hero-subtitle">Real-time developer movement, open-source adoption shifts, and breakout frameworks.</div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Metric Summary Cards
# ---------------------------------------------------------
fastest_domain = df_cat.sort_values(
    by="avg_growth_per_repo", ascending=False
).iloc[0]["primary_category"]
top_gainer = df_latest.sort_values(by="star_growth", ascending=False).iloc[0]

k1, k2, k3, k4 = st.columns(4)
k1.metric(
    "Tracked Projects",
    f"{len(df_latest):,}",
    delta=f"{len(df_filtered)} in active view",
)
k2.metric("Total Ecosystem Stars", f"{df_latest['stars'].sum():,}")
k3.metric("Fastest Moving Sector", fastest_domain, delta="Top Velocity")
k4.metric(
    "Leading Breakout Project",
    top_gainer["repo_name"].split("/")[-1],
    delta=f"+{top_gainer['star_growth']} stars",
)

# ---------------------------------------------------------
# Dynamic Takeaway Banner
# ---------------------------------------------------------
st.markdown(
    f"""
<div class="insight-pill">
    💡 <b>Ecosystem Note:</b> <b>{fastest_domain}</b> is recording the highest star velocity per repository, with standout activity in <b>{top_gainer['repo_name']}</b> (+{top_gainer['star_growth']} stars in the latest snapshot).
</div>
""",
    unsafe_allow_html=True,
)

# Safe sizing & trajectories for visualizations
df_filtered["bubble_size"] = df_filtered["star_growth"].abs() + 3
df_filtered["trajectory"] = df_filtered["star_growth"].apply(
    lambda x: (
        "🔻 Cooling Down"
        if x < 0
        else (
            "🚀 High Acceleration"
            if x >= 20
            else ("⚡ Gaining Traction" if x > 0 else "🌱 Steady")
        )
    )
)

# ---------------------------------------------------------
# Interactive Analytics Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Sector Velocity",
    "🪐 Velocity vs Scale",
    "🔍 Project Explorer",
    "🔻 Cooling Trends",
])

with tab1:
  c1, c2 = st.columns(2)
  with c1:
    st.markdown("#### Average Stars Gained Per Repository")
    fig_cat = px.bar(
        df_cat.sort_values(by="avg_growth_per_repo", ascending=True),
        x="avg_growth_per_repo",
        y="primary_category",
        orientation="h",
        color="primary_category",
        text="avg_growth_per_repo",
        template=plotly_template,
        color_discrete_sequence=px.colors.qualitative.Prism,
        labels={
            "avg_growth_per_repo": "Stars / Repo",
            "primary_category": "Domain",
        },
    )
    fig_cat.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=10, b=10),
    )
    fig_cat.update_traces(texttemplate="%{text:.1f} ★", textposition="outside")
    st.plotly_chart(fig_cat, width="stretch")

  with c2:
    st.markdown("#### Top Velocity Breakouts (24-Hour Spike)")
    top_plot = df_top.sort_values(by="momentum_score", ascending=True).tail(7)
    fig_top = px.bar(
        top_plot,
        x="star_growth",
        y="repo_name",
        orientation="h",
        color="primary_category",
        text="star_growth",
        template=plotly_template,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={"star_growth": "Stars Gained", "repo_name": "Project"},
    )
    fig_top.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=10, b=10),
        showlegend=False,
    )
    fig_top.update_traces(texttemplate="+%{text} ★", textposition="outside")
    st.plotly_chart(fig_top, width="stretch")

with tab2:
  st.markdown("#### Growth Velocity vs Total Community Size")
  st.caption(
      "Hover over bubbles to inspect repos. Top-right quadrant highlights"
      " rapid adoption."
  )

  if len(df_filtered) > 0:
    color_map = {
        "🚀 High Acceleration": "#38BDF8",
        "⚡ Gaining Traction": "#818CF8",
        "🌱 Steady": "#A78BFA",
        "🔻 Cooling Down": "#F87171",
    }

    fig_scatter = px.scatter(
        df_filtered,
        x="stars",
        y="star_growth_rate",
        size="bubble_size",
        color="trajectory",
        hover_name="repo_name",
        hover_data={
            "stars": True,
            "star_growth": True,
            "star_growth_rate": ":.2f%",
            "primary_category": True,
            "bubble_size": False,
        },
        log_x=True,
        template=plotly_template,
        size_max=32,
        color_discrete_map=color_map,
        labels={
            "stars": "Total Stars (Log Scale)",
            "star_growth_rate": "Growth Rate (%)",
            "trajectory": "Adoption Trend",
        },
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=520
    )
    st.plotly_chart(fig_scatter, width="stretch")
  else:
    st.info("No projects match the selected sidebar filters.")

with tab3:
  st.markdown(f"#### Viewing {len(df_filtered)} Projects")

  if len(df_filtered) > 0:
    display_df = df_filtered[[
        "repo_name",
        "primary_category",
        "stars",
        "star_growth",
        "star_growth_rate",
        "momentum_score",
        "signal",
        "repo_url",
    ]].sort_values(by="momentum_score", ascending=False)

    st.dataframe(
        display_df,
        column_config={
            "repo_url": st.column_config.LinkColumn(
                "Repository", display_text="Open on GitHub ↗"
            ),
            "stars": st.column_config.NumberColumn(
                "Total Stars", format="%d ⭐"
            ),
            "star_growth": st.column_config.NumberColumn(
                "24h Change", format="%+d"
            ),
            "star_growth_rate": st.column_config.NumberColumn(
                "Growth Rate", format="%.2f%%"
            ),
            "momentum_score": st.column_config.ProgressColumn(
                "Momentum",
                help="Balanced adoption index (0-100)",
                min_value=0,
                max_value=100,
                format="%.1f",
            ),
        },
        hide_index=True,
        width="stretch",
        height=480,
    )
  else:
    st.warning("No projects match the active filters.")

with tab4:
  st.markdown("#### Cooling & Stagnating Projects")
  st.caption(
      "Repositories with zero or negative star change over the recording"
      " window."
  )

  cooling_df = df_latest[df_latest["star_growth"] <= 0].sort_values(
      by="star_growth", ascending=True
  )
  if len(cooling_df) > 0:
    st.dataframe(
        cooling_df[[
            "repo_name",
            "primary_category",
            "stars",
            "star_growth",
            "star_growth_rate",
            "repo_url",
        ]],
        column_config={
            "repo_url": st.column_config.LinkColumn(
                "GitHub", display_text="Visit ↗"
            ),
            "star_growth": st.column_config.NumberColumn(
                "Change", format="%d"
            ),
            "star_growth_rate": st.column_config.NumberColumn(
                "Growth Rate", format="%.2f%%"
            ),
        },
        hide_index=True,
        width="stretch",
        height=320,
    )
  else:
    st.info("No repositories experienced negative velocity in this period.")