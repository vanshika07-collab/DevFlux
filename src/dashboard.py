from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DevFlux | Developer Ecosystem Radar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Theme State
# ---------------------------------------------------------
if "dark_theme" not in st.session_state:
  st.session_state.dark_theme = True

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
      "Data pipeline not initialized. Please execute `python"
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
# Top Navigation & Cute Flower Slider
# ---------------------------------------------------------
nav_col, switch_col = st.columns([5, 1.3])

with nav_col:
  selected_page = st.segmented_control(
      "Navigation",
      options=[
          "Overview",
          "Domain Guide & Trivia",
          "Sector Velocity",
          "Scale vs Velocity",
          "Repository Explorer",
          "Cooling Trends",
      ],
      default="Overview",
      label_visibility="collapsed",
  )

with switch_col:
  theme_toggle = st.toggle("🌸 Neon Dark", value=st.session_state.dark_theme)
  st.session_state.dark_theme = theme_toggle

is_dark = st.session_state.dark_theme

# ---------------------------------------------------------
# Dynamic Style Tokens (Cyberpunk Black vs Clean Light)
# ---------------------------------------------------------
if is_dark:
  bg_app = "#08080C"
  bg_secondary = "#12111A"
  text_primary = "#FFF0F5"
  text_secondary = "#FFA3C4"
  card_bg = (
      "linear-gradient(145deg, rgba(25, 16, 28, 0.9), rgba(12, 10, 18, 0.98))"
  )
  card_border = "rgba(255, 0, 122, 0.3)"
  card_glow = "0 8px 32px rgba(255, 0, 122, 0.15)"
  plotly_template = "plotly_dark"
  chart_font_color = "#FFF0F5"
  hero_grad = (
      "linear-gradient(135deg, rgba(35, 12, 35, 0.95) 0%, rgba(10, 8, 16, 0.98)"
      " 100%)"
  )
  insight_box = "rgba(255, 0, 128, 0.08)"
  insight_border = "#FF007F"
  accent_primary = "#FF007F"
  accent_secondary = "#FF3366"
  trivia_badge_bg = "rgba(255, 0, 127, 0.15)"
  trivia_popup_bg = "#180D1B"
  chart_palette = [
      "#FF007F",
      "#FF2A6D",
      "#FF5E7E",
      "#D100D1",
      "#9B00E8",
      "#FF80BF",
  ]
else:
  bg_app = "#FFF7F9"
  bg_secondary = "#FFE4EC"
  text_primary = "#1E0511"
  text_secondary = "#881337"
  card_bg = "linear-gradient(145deg, #FFFFFF, #FFF0F5)"
  card_border = "rgba(225, 29, 72, 0.25)"
  card_glow = "0 6px 24px rgba(225, 29, 72, 0.08)"
  plotly_template = "plotly_white"
  chart_font_color = "#1E0511"
  hero_grad = "linear-gradient(135deg, #FFE4E6 0%, #FECDD3 100%)"
  insight_box = "#FFF1F2"
  insight_border = "#E11D48"
  accent_primary = "#E11D48"
  accent_secondary = "#BE185D"
  trivia_badge_bg = "rgba(225, 29, 72, 0.12)"
  trivia_popup_bg = "#FFFFFF"
  chart_palette = [
      "#E11D48",
      "#BE185D",
      "#9F1239",
      "#FB7185",
      "#FDA4AF",
      "#F43F5E",
  ]

st.markdown(
    f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    #MainMenu, footer {{
        visibility: hidden;
    }}
    
    html, body, [class*="stApp"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: {bg_app} !important;
        color: {text_primary} !important;
        font-size: 16px;
    }}
    
    /* Hero Banner */
    .hero-container {{
        background: {hero_grad};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 28px 34px;
        margin: 12px 0px 24px 0px;
        box-shadow: {card_glow};
    }}
    .hero-title {{
        font-size: 2.35rem;
        font-weight: 800;
        background: linear-gradient(90deg, {accent_primary}, {text_secondary});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }}
    .hero-subtitle {{
        color: {text_secondary};
        font-size: 1.08rem;
        line-height: 1.5;
        margin-bottom: 0px;
    }}
    
    /* Takeaway Box */
    .insight-pill {{
        background: {insight_box};
        border-left: 5px solid {insight_border};
        padding: 16px 22px;
        border-radius: 10px;
        margin: 20px 0px 28px 0px;
        color: {text_primary};
        font-size: 1.05rem;
        line-height: 1.55;
    }}
    
    /* Large KPI Metric Cards */
    div[data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: {card_glow};
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-3px);
        border-color: {accent_primary};
    }}
    div[data-testid="stMetric"] label {{
        color: {text_secondary} !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: {text_primary} !important;
        font-size: 2.3rem !important;
        font-weight: 800 !important;
    }}
    
    /* Domain Stacked Cards */
    .info-card-stacked {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 26px 30px;
        margin-bottom: 24px;
        box-shadow: {card_glow};
    }}
    .info-card-stacked h3 {{
        color: {accent_primary} !important;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 0px;
        margin-bottom: 12px;
    }}
    .info-card-stacked p {{
        font-size: 1.05rem;
        line-height: 1.65;
        color: {text_primary};
        margin-bottom: 14px;
    }}
    
    /* Hover Tooltip Box for Trivia */
    .tooltip-wrapper {{
        position: relative;
        display: inline-block;
        margin-top: 8px;
    }}
    .tooltip-trigger {{
        background: {trivia_badge_bg};
        border: 1px dashed {accent_primary};
        color: {accent_primary};
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .tooltip-content {{
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 130%;
        left: 0;
        width: 480px;
        max-width: 90vw;
        background: {trivia_popup_bg};
        color: {text_primary};
        border: 1.5px solid {accent_primary};
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        font-size: 0.98rem;
        line-height: 1.5;
        z-index: 100;
        transition: opacity 0.25s ease, visibility 0.25s ease;
    }}
    .tooltip-wrapper:hover .tooltip-content {{
        visibility: visible;
        opacity: 1;
    }}
    
    /* General text size enhancements */
    h1, h2, h3, h4 {{
        font-weight: 800 !important;
    }}
    .stMarkdown p {{
        font-size: 1.05rem;
    }}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Helper: In-Page Filters
# ---------------------------------------------------------
def render_inpage_filters(container_key_prefix: str) -> pd.DataFrame:
  with st.expander("Filter & Segment Parameters", expanded=False):
    f_col1, f_col2, f_col3 = st.columns(3)
    all_categories = sorted(
        df_latest["primary_category"].dropna().unique().tolist()
    )
    with f_col1:
      selected_categories = st.multiselect(
          "Technical Domains",
          options=all_categories,
          default=all_categories,
          key=f"{container_key_prefix}_cats",
      )
    all_signals = sorted(df_latest["signal"].dropna().unique().tolist())
    with f_col2:
      selected_signals = st.multiselect(
          "Momentum Tier",
          options=all_signals,
          default=all_signals,
          key=f"{container_key_prefix}_signals",
      )
    with f_col3:
      min_stars = st.slider(
          "Minimum Base Stars",
          min_value=int(df_latest["stars"].min()),
          max_value=int(df_latest["stars"].max()),
          value=int(df_latest["stars"].min()),
          step=50,
          key=f"{container_key_prefix}_stars",
      )

  filtered = df_latest[
      (df_latest["primary_category"].isin(selected_categories))
      & (df_latest["signal"].isin(selected_signals))
      & (df_latest["stars"] >= min_stars)
  ].copy()

  filtered["bubble_size"] = filtered["star_growth"].abs() + 4
  filtered["trajectory"] = filtered["star_growth"].apply(
      lambda x: (
          "Cooling"
          if x < 0
          else (
              "High Acceleration"
              if x >= 20
              else ("Gaining Traction" if x > 0 else "Steady")
          )
      )
  )
  return filtered


# ---------------------------------------------------------
# PAGE 1: OVERVIEW (HOME)
# ---------------------------------------------------------
if selected_page == "Overview":
  st.markdown(
      """
    <div class="hero-container">
        <div class="hero-title">DevFlux Ecosystem Radar</div>
        <div class="hero-subtitle">Continuous tracking of open-source developer activity, technology adoption velocity, and framework transitions.</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  fastest_domain = df_cat.sort_values(
      by="avg_growth_per_repo", ascending=False
  ).iloc[0]["primary_category"]
  top_gainer = df_latest.sort_values(by="star_growth", ascending=False).iloc[0]

  k1, k2, k3, k4 = st.columns(4)
  k1.metric(
      "Monitored Codebases",
      f"{len(df_latest):,}",
      delta=f"{len(df_latest)} active",
  )
  k2.metric("Total Ecosystem Stars", f"{df_latest['stars'].sum():,}")
  k3.metric("Leading Growth Sector", fastest_domain, delta="Top Velocity")
  k4.metric(
      "Top Breakout Project",
      top_gainer["repo_name"].split("/")[-1],
      delta=f"+{top_gainer['star_growth']} stars",
  )

  st.markdown(
      f"""
    <div class="insight-pill">
        <b>Current Movement Summary:</b> <b>{fastest_domain}</b> is averaging the strongest net growth per repository across the monitored cluster, with standout daily acceleration in <b>{top_gainer['repo_name']}</b> (+{top_gainer['star_growth']} stars).
    </div>
    """,
      unsafe_allow_html=True,
  )

  c1, c2 = st.columns(2)
  with c1:
    st.markdown("### Sector Growth Velocity")
    fig_cat = px.bar(
        df_cat.sort_values(by="avg_growth_per_repo", ascending=True),
        x="avg_growth_per_repo",
        y="primary_category",
        orientation="h",
        color="primary_category",
        text="avg_growth_per_repo",
        template=plotly_template,
        color_discrete_sequence=chart_palette,
        labels={
            "avg_growth_per_repo": "Average Stars / Repo",
            "primary_category": "Domain",
        },
    )
    fig_cat.update_layout(
        showlegend=False,
        font=dict(color=chart_font_color, size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=10, b=10),
    )
    fig_cat.update_traces(
        texttemplate="%{text:.1f} stars",
        textposition="outside",
        textfont=dict(color=chart_font_color, size=12),
    )
    st.plotly_chart(fig_cat, width="stretch")

  with c2:
    st.markdown("### Top Velocity Breakouts")
    top_plot = df_top.sort_values(by="momentum_score", ascending=True).tail(6)
    fig_top = px.bar(
        top_plot,
        x="star_growth",
        y="repo_name",
        orientation="h",
        color="primary_category",
        text="star_growth",
        template=plotly_template,
        color_discrete_sequence=chart_palette,
        labels={"star_growth": "Stars Gained", "repo_name": "Repository"},
    )
    fig_top.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=chart_font_color, size=13),
        margin=dict(l=10, r=20, t=10, b=10),
        showlegend=False,
    )
    fig_top.update_traces(
        texttemplate="+%{text}",
        textposition="outside",
        textfont=dict(color=chart_font_color, size=12),
    )
    st.plotly_chart(fig_top, width="stretch")

# ---------------------------------------------------------
# PAGE 2: DOMAIN GUIDE & TRIVIA (STACKED + HOVER TOOLTIP)
# ---------------------------------------------------------
elif selected_page == "Domain Guide & Trivia":
  st.markdown("## Domain Reference Guide & Industry Context")
  st.markdown(
      "A structured technical reference guide to machine learning disciplines,"
      " production applications, and historical trivia. Hover over the badges"
      " below to reveal context."
  )
  st.write("")

  # Stacked Domain 1
  st.markdown(
      """
    <div class="info-card-stacked">
        <h3>1. AI Agents & Autonomous Execution</h3>
        <p><b>Architectural Foundation:</b> Software systems pairing language models with continuous planning loops, short/long-term memory vector stores, and structured tool interfaces (shell execution, code execution, web scrapers, and REST APIs) to complete multi-step tasks without human oversight.</p>
        <p><b>Primary Industry Workloads:</b> Autonomous developer tools, scheduled market intelligence crawlers, self-resolving bug triage bots, and automated synthetic benchmark generators.</p>
        <div class="tooltip-wrapper">
            <div class="tooltip-trigger">💡 Hover for Industry Trivia</div>
            <div class="tooltip-content">
                <b>Did You Know?</b> Autonomous agent repositories (like AutoGPT and BabyAGI in 2023) crossed 100,000 GitHub stars faster than React, Linux, or Kubernetes, marking the fastest initial mindshare spike in open-source software history.
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Stacked Domain 2
  st.markdown(
      """
    <div class="info-card-stacked">
        <h3>2. Core ML & Deep Learning Foundations</h3>
        <p><b>Architectural Foundation:</b> Low-level tensor computation engines, automatic differentiation backends, custom GPU/TPU kernel optimizers (such as OpenAI Triton and FlashAttention), and foundation model architectures.</p>
        <p><b>Primary Industry Workloads:</b> Pre-training massive language models, quantized edge inference engines (e.g. llama.cpp, vLLM), and memory-efficient fine-tuning (LoRA, QLoRA).</p>
        <div class="tooltip-wrapper">
            <div class="tooltip-trigger">💡 Hover for Industry Trivia</div>
            <div class="tooltip-content">
                <b>Did You Know?</b> PyTorch was originally rewritten from Torch (which ran on Lua). Today, over 80% of published academic AI research papers implement their models using PyTorch backbones.
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Stacked Domain 3
  st.markdown(
      """
    <div class="info-card-stacked">
        <h3>3. MLOps & Production Infrastructure</h3>
        <p><b>Architectural Foundation:</b> Continuous integration and deployment (CI/CD) pipelines tailored for non-deterministic model checkpoints, GPU cluster orchestration, automated data validation, and feature storage.</p>
        <p><b>Primary Industry Workloads:</b> Automated dataset ingestion pipelines, model drift alerting, multi-GPU training schedulers, and zero-downtime serving deployments.</p>
        <div class="tooltip-wrapper">
            <div class="tooltip-trigger">💡 Hover for Industry Trivia</div>
            <div class="tooltip-content">
                <b>Did You Know?</b> Industry studies show that up to 85% of machine learning models developed in enterprise proof-of-concept environments fail to reach live production due to data pipeline friction rather than model quality.
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Stacked Domain 4
  st.markdown(
      """
    <div class="info-card-stacked">
        <h3>4. RAG & Vector Retrieval Systems</h3>
        <p><b>Architectural Foundation:</b> Retrieval-Augmented Generation bridges generative models with private external knowledge bases by transforming unstructured text into dense vector embeddings indexed in specialized vector databases.</p>
        <p><b>Primary Industry Workloads:</b> Enterprise semantic search, internal document discovery, compliance checking, legal contract querying, and factual grounding.</p>
        <div class="tooltip-wrapper">
            <div class="tooltip-trigger">💡 Hover for Industry Trivia</div>
            <div class="tooltip-content">
                <b>Did You Know?</b> Before dense vector embeddings became standard, enterprise search relied primarily on BM25 keyword matching (developed in the 1990s). Modern production retrieval engines now combine BM25 + dense vectors as 'Hybrid Search' for maximum recall.
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Stacked Domain 5
  st.markdown(
      """
    <div class="info-card-stacked">
        <h3>5. Computer Vision & Spatial Multimodal AI</h3>
        <p><b>Architectural Foundation:</b> Zero-shot open-vocabulary object detectors, semantic segmentation backends, 3D Gaussian splatting, and multimodal visual-language processors (VLMs).</p>
        <p><b>Primary Industry Workloads:</b> Autonomous robotics navigation, automated defect inspection in precision manufacturing, document OCR understanding, and medical radiology triage.</p>
        <div class="tooltip-wrapper">
            <div class="tooltip-trigger">💡 Hover for Industry Trivia</div>
            <div class="tooltip-content">
                <b>Did You Know?</b> Modern edge-optimized object detectors (like YOLOv10/v11 architectures) can process high-resolution video streams at over 200 frames per second on standard consumer hardware.
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

# ---------------------------------------------------------
# PAGE 3: SECTOR VELOCITY
# ---------------------------------------------------------
elif selected_page == "Sector Velocity":
  st.markdown("## Sector Velocity & Comparative Momentum")
  st.markdown(
      "Normalized cross-domain comparison evaluating which technical"
      " disciplines are attracting developers."
  )

  df_filtered = render_inpage_filters("sector_page")

  col1, col2 = st.columns(2)
  with col1:
    st.markdown("### Average Star Gains Per Repository")
    fig_cat = px.bar(
        df_cat.sort_values(by="avg_growth_per_repo", ascending=True),
        x="avg_growth_per_repo",
        y="primary_category",
        orientation="h",
        color="primary_category",
        text="avg_growth_per_repo",
        template=plotly_template,
        color_discrete_sequence=chart_palette,
        labels={
            "avg_growth_per_repo": "Stars / Repo",
            "primary_category": "Domain",
        },
    )
    fig_cat.update_layout(
        showlegend=False,
        font=dict(color=chart_font_color, size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=10, b=10),
    )
    fig_cat.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        textfont=dict(color=chart_font_color, size=12),
    )
    st.plotly_chart(fig_cat, width="stretch")

  with col2:
    st.markdown("### Top Velocity Breakouts")
    top_plot = df_filtered.sort_values(by="momentum_score", ascending=True).tail(
        8
    )
    fig_top = px.bar(
        top_plot,
        x="star_growth",
        y="repo_name",
        orientation="h",
        color="primary_category",
        text="star_growth",
        template=plotly_template,
        color_discrete_sequence=chart_palette,
        labels={"star_growth": "Stars Gained", "repo_name": "Repository"},
    )
    fig_top.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=chart_font_color, size=13),
        margin=dict(l=10, r=20, t=10, b=10),
        showlegend=False,
    )
    fig_top.update_traces(
        texttemplate="+%{text}",
        textposition="outside",
        textfont=dict(color=chart_font_color, size=12),
    )
    st.plotly_chart(fig_top, width="stretch")

# ---------------------------------------------------------
# PAGE 4: SCALE VS VELOCITY
# ---------------------------------------------------------
elif selected_page == "Scale vs Velocity":
  st.markdown("## Ecosystem Landscape: Scale vs. Velocity")
  st.markdown(
      "Bubble area indicates absolute delta volume. Top-right projects"
      " represent high-velocity developer adoption."
  )

  df_filtered = render_inpage_filters("matrix_page")

  if len(df_filtered) > 0:
    color_map = {
        "High Acceleration": "#FF007F" if is_dark else "#E11D48",
        "Gaining Traction": "#FF5E7E" if is_dark else "#BE185D",
        "Steady": "#A855F7" if is_dark else "#9333EA",
        "Cooling": "#6B7280" if is_dark else "#475569",
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
        size_max=34,
        color_discrete_map=color_map,
        labels={
            "stars": "Total Base Stars (Log Scale)",
            "star_growth_rate": "Growth Rate (%)",
            "trajectory": "Status",
        },
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=chart_font_color, size=13),
        height=580,
    )
    st.plotly_chart(fig_scatter, width="stretch")
  else:
    st.info("No repositories match the specified filter criteria.")

# ---------------------------------------------------------
# PAGE 5: REPOSITORY EXPLORER
# ---------------------------------------------------------
elif selected_page == "Repository Explorer":
  st.markdown("## Interactive Repository Explorer")
  st.markdown(
      "Inspect tracked repositories, adoption momentum, and upstream source"
      " code."
  )

  df_filtered = render_inpage_filters("explorer_page")

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
                "Upstream URL", display_text="Open on GitHub ↗"
            ),
            "stars": st.column_config.NumberColumn(
                "Total Stars", format="%d"
            ),
            "star_growth": st.column_config.NumberColumn(
                "24h Delta", format="%+d"
            ),
            "star_growth_rate": st.column_config.NumberColumn(
                "Growth Rate", format="%.2f%%"
            ),
            "momentum_score": st.column_config.ProgressColumn(
                "Momentum Score",
                help="Normalized compound momentum index (0-100)",
                min_value=0,
                max_value=100,
                format="%.1f",
            ),
        },
        hide_index=True,
        width="stretch",
        height=520,
    )
  else:
    st.warning("No projects match the active filter criteria.")

# ---------------------------------------------------------
# PAGE 6: COOLING TRENDS
# ---------------------------------------------------------
elif selected_page == "Cooling Trends":
  st.markdown("## Cooling & Stagnating Projects")
  st.markdown(
      "Repositories experiencing zero or negative growth during the current"
      " recording cycle."
  )

  cooling_df = df_latest[df_latest["star_growth"] <= 0].sort_values(
      by="star_growth", ascending=True
  )
  if len(cooling_df) > 0:
    c1, c2 = st.columns([1, 2])
    with c1:
      st.metric("Identified Cooling Projects", len(cooling_df))
      st.info(
          "Surfaces unstarring activity, archived repositories, or migrations"
          " toward alternative architectures."
      )
    with c2:
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
                  "Upstream", display_text="Visit ↗"
              ),
              "star_growth": st.column_config.NumberColumn(
                  "Delta", format="%d"
              ),
              "star_growth_rate": st.column_config.NumberColumn(
                  "Growth Rate", format="%.2f%%"
              ),
          },
          hide_index=True,
          width="stretch",
          height=360,
      )
  else:
    st.info("No repositories experienced negative velocity in this period.")