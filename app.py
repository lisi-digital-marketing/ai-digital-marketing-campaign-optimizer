
import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
st.set_page_config(
    page_title="AI Digital Marketing Campaign Optimizer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Digital Marketing Campaign Optimizer")
st.write("AI-powered campaign prediction, ROI estimation and recommendation system")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model
model = joblib.load(
    os.path.join(PROJECT_DIR, "model.pkl")
)

# Load model columns
model_columns = joblib.load(
    os.path.join(PROJECT_DIR, "model_columns.pkl")
)

# Load dataset
df = pd.read_csv(
    os.path.join(
        PROJECT_DIR,
        "AI_Digital_Marketing_Campaign_Dataset.csv"
    )
)

st.sidebar.header("Campaign Information")

platform = st.sidebar.selectbox(
    "Platform",
    ["Google Ads", "Instagram", "Facebook"]
)

budget = st.sidebar.number_input(
    "Budget (₹)",
    min_value=1000,
    value=25000,
    step=1000
)

audience = st.sidebar.selectbox(
    "Audience",
    ["18-24", "25-34", "35-44", "45-54", "55+"]
)

location = st.sidebar.text_input(
    "Location",
    "Chennai"
)

duration = st.sidebar.number_input(
    "Campaign Duration (Days)",
    min_value=1,
    value=15
)

objective = st.sidebar.selectbox(
    "Objective",
    ["Lead Generation", "Website Traffic"]
)

if st.button("🚀 Analyze Campaign", use_container_width=True):

    platform_data = df[df["Platform"] == platform].mean(numeric_only=True)

    new_data = pd.DataFrame([{
        "Platform": platform,
        "Budget": budget,
        "Impressions": int(platform_data["Impressions"]),
        "Clicks": int(platform_data["Clicks"]),
        "Engagement": int(platform_data["Engagement"]),
        "Leads": int(platform_data["Leads"]),
        "Audience": audience,
        "Location": location,
        "Campaign_Duration_Days": duration,
        "Objective": objective
    }])

    new_data = pd.get_dummies(new_data)
    new_data = new_data.reindex(
        columns=model_columns,
        fill_value=0
    )

    predicted_conversions = max(
        0,
        round(model.predict(new_data)[0], 2)
    )

    platform_df = df[df["Platform"] == platform]

    revenue_per_conversion = (
        platform_df["Revenue"].sum()
        / platform_df["Conversions"].sum()
    )

    estimated_revenue = (
        predicted_conversions * revenue_per_conversion
    )

    estimated_roi = (
        (estimated_revenue - budget) / budget
    ) * 100

    historical_roi = df.groupby("Platform")["ROI"].mean()

    platform_roi = historical_roi.get(platform, 0)

    if platform_roi >= 1800:
        risk = "LOW"
    elif platform_roi >= 1000:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    st.subheader("📊 Campaign Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Predicted Conversions",
        predicted_conversions
    )

    col2.metric(
        "Estimated Revenue",
        f"₹{estimated_revenue:,.2f}"
    )

    col3.metric(
        "Estimated ROI",
        f"{estimated_roi:,.2f}%"
    )

    st.info(f"Risk Level: **{risk}**")

    st.subheader("🤖 AI Recommendation")

    if risk == "LOW":
        st.success(
            f"{platform} shows strong historical performance. "
            "The campaign is recommended for investment."
        )
    elif risk == "MEDIUM":
        st.warning(
            f"{platform} shows moderate historical performance. "
            "Consider testing with a controlled budget."
        )
    else:
        st.error(
            f"{platform} shows weaker historical performance. "
            "A cautious budget is recommended."
        )


    # =========================================================
    # DOWNLOAD CAMPAIGN REPORT
    # =========================================================

    st.divider()
    st.subheader("📥 Download Campaign Report")

    if risk == "LOW":
        recommendation_text = (
            f"{platform} shows strong historical performance. "
            "The campaign is recommended for investment."
        )
    elif risk == "MEDIUM":
        recommendation_text = (
            f"{platform} shows moderate historical performance. "
            "Consider testing the campaign with controlled spending."
        )
    else:
        recommendation_text = (
            f"{platform} shows relatively lower historical performance. "
            "Use caution and monitor campaign performance closely."
        )

    report_text = f"""
AI DIGITAL MARKETING CAMPAIGN REPORT
====================================

CAMPAIGN DETAILS
----------------
Platform: {platform}
Budget: ₹{budget:,.2f}
Audience: {audience}
Location: {location}
Campaign Duration: {duration} Days
Objective: {objective}

AI PREDICTION
-------------
Predicted Conversions: {predicted_conversions:.2f}
Estimated Revenue: ₹{estimated_revenue:,.2f}
Estimated ROI: {estimated_roi:.2f}%
Risk Level: {risk}

AI RECOMMENDATION
-----------------
{recommendation_text}

====================================
Generated by AI Digital Marketing
Campaign Optimizer
"""

    st.download_button(
        label="📥 Download Campaign Report",
        data=report_text,
        file_name="AI_Digital_Marketing_Campaign_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.subheader("📋 Campaign Summary")

    st.write({
        "Platform": platform,
        "Budget": f"₹{budget:,.2f}",
        "Audience": audience,
        "Location": location,
        "Duration": f"{duration} days",
        "Objective": objective
    })


# =========================================================
# WHAT-IF SIMULATION & AI BUDGET OPTIMIZER
# =========================================================

st.divider()
st.header("💰 What-If Simulation & AI Budget Optimizer")

st.write(
    "Test different budget allocations and find the allocation "
    "with the highest predicted conversions."
)

total_budget = st.number_input(
    "Enter Total Marketing Budget (₹)",
    min_value=15000,
    value=50000,
    step=5000
)

if st.button("🤖 Find Best Budget Allocation", use_container_width=True):

    step = 5000
    optimization_results = []

    for google_budget in range(5000, int(total_budget), step):

        for instagram_budget in range(5000, int(total_budget), step):

            facebook_budget = (
                int(total_budget)
                - google_budget
                - instagram_budget
            )

            if facebook_budget < 5000:
                continue

            # Google Ads prediction
            google_data = df[df["Platform"] == "Google Ads"].mean(
                numeric_only=True
            )

            google_input = pd.DataFrame([{
                "Platform": "Google Ads",
                "Budget": google_budget,
                "Impressions": int(google_data["Impressions"]),
                "Clicks": int(google_data["Clicks"]),
                "Engagement": int(google_data["Engagement"]),
                "Leads": int(google_data["Leads"]),
                "Audience": "25-34",
                "Location": "Chennai",
                "Campaign_Duration_Days": 15,
                "Objective": "Lead Generation"
            }])

            google_input = pd.get_dummies(google_input)
            google_input = google_input.reindex(
                columns=model_columns,
                fill_value=0
            )

            google_prediction = max(
                0,
                model.predict(google_input)[0]
            )

            # Instagram prediction
            instagram_data = df[df["Platform"] == "Instagram"].mean(
                numeric_only=True
            )

            instagram_input = pd.DataFrame([{
                "Platform": "Instagram",
                "Budget": instagram_budget,
                "Impressions": int(instagram_data["Impressions"]),
                "Clicks": int(instagram_data["Clicks"]),
                "Engagement": int(instagram_data["Engagement"]),
                "Leads": int(instagram_data["Leads"]),
                "Audience": "25-34",
                "Location": "Chennai",
                "Campaign_Duration_Days": 15,
                "Objective": "Lead Generation"
            }])

            instagram_input = pd.get_dummies(instagram_input)
            instagram_input = instagram_input.reindex(
                columns=model_columns,
                fill_value=0
            )

            instagram_prediction = max(
                0,
                model.predict(instagram_input)[0]
            )

            # Facebook prediction
            facebook_data = df[df["Platform"] == "Facebook"].mean(
                numeric_only=True
            )

            facebook_input = pd.DataFrame([{
                "Platform": "Facebook",
                "Budget": facebook_budget,
                "Impressions": int(facebook_data["Impressions"]),
                "Clicks": int(facebook_data["Clicks"]),
                "Engagement": int(facebook_data["Engagement"]),
                "Leads": int(facebook_data["Leads"]),
                "Audience": "25-34",
                "Location": "Chennai",
                "Campaign_Duration_Days": 15,
                "Objective": "Lead Generation"
            }])

            facebook_input = pd.get_dummies(facebook_input)
            facebook_input = facebook_input.reindex(
                columns=model_columns,
                fill_value=0
            )

            facebook_prediction = max(
                0,
                model.predict(facebook_input)[0]
            )

            total_conversions = (
                google_prediction
                + instagram_prediction
                + facebook_prediction
            )

            optimization_results.append({
                "Google Ads": google_budget,
                "Instagram": instagram_budget,
                "Facebook": facebook_budget,
                "Predicted Conversions": round(
                    total_conversions, 2
                )
            })

    optimization_df = pd.DataFrame(optimization_results)

    best_result = optimization_df.loc[
        optimization_df["Predicted Conversions"].idxmax()
    ]

    st.success("🎯 AI found the best budget allocation!")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Google Ads",
        f"₹{best_result['Google Ads']:,.0f}"
    )

    col2.metric(
        "Instagram",
        f"₹{best_result['Instagram']:,.0f}"
    )

    col3.metric(
        "Facebook",
        f"₹{best_result['Facebook']:,.0f}"
    )

    col4.metric(
        "Predicted Conversions",
        f"{best_result['Predicted Conversions']:.2f}"
    )

    st.subheader("📊 Recommended Budget Allocation")

    chart_data = pd.DataFrame({
        "Platform": [
            "Google Ads",
            "Instagram",
            "Facebook"
        ],
        "Budget": [
            best_result["Google Ads"],
            best_result["Instagram"],
            best_result["Facebook"]
        ]
    })

    st.bar_chart(
        chart_data.set_index("Platform")
    )

    st.subheader("🏆 Top 5 Budget Strategies")

    top_5 = optimization_df.sort_values(
        "Predicted Conversions",
        ascending=False
    ).head(5)

    st.dataframe(
        top_5,
        use_container_width=True
    )


# =========================================================
