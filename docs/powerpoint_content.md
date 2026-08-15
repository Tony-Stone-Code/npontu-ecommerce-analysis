# PowerPoint Presentation Guide

This document contains the slide-by-slide content for your final presentation, as well as an AI prompt you can use to auto-generate the slides in tools like Gamma.app, Canva, or PowerPoint Copilot.

---

## 🤖 AI Prompt for Auto-Generating Slides
*Copy and paste the prompt below into an AI presentation tool (like ChatGPT Plus with the Canva plugin, Gamma.app, or Microsoft Copilot) to generate your slides instantly:*

> **Prompt:** "Act as a Senior Data Scientist presenting to an executive team. I need a 7-slide professional presentation based on an analysis of e-commerce customer behavior. The goal is to present findings on customer churn and give actionable recommendations. 
> 
> Use a clean, modern corporate theme with data visualization placeholders. Here is the outline:
> Slide 1: Title (Intelligent Systems E-Commerce Analysis)
> Slide 2: The Challenge & Architecture (Predicting churn using a Big Data pipeline)
> Slide 3: Customer Landscape (African context, mobile dominance)
> Slide 4: Feature Engineering (RFM and Engagement)
> Slide 5: Predictive Modeling (XGBoost performance)
> Slide 6: Key Findings & Business Insights
> Slide 7: Actionable Recommendations
> 
> Keep the text concise and punchy. Emphasize business value over deep technical jargon."

---

## 📊 Slide-by-Slide Content (If building manually)

### Slide 1: Title Slide
* **Title:** Analyzing Customer Behavior for E-Commerce Insights
* **Subtitle:** An End-to-End Pipeline for Predicting Churn & Driving Engagement
* **Presenter:** Tony Stone | Intelligent Systems Services Engineer Candidate
* **Visual:** Minimalist e-commerce/data network background.

### Slide 2: The Objective & Architecture
* **Header:** Moving From Raw Data to Actionable Insights
* **Content:**
  * **Objective:** Identify churn indicators and personalize the shopping experience to drive retention.
  * **The Pipeline:**
    * *Simulated Data*: ~2.5M event logs (50k customers) focusing on African markets.
    * *Processing Engine*: Pandas aggregated raw events into flattened customer profiles.
    * *Machine Learning*: XGBoost algorithm for high-accuracy churn prediction.
    * *Big Data / Dashboarding*: Elasticsearch + Kibana for real-time visualization.
* **Visual:** A simple 4-step flowchart showing (Data -> Processing -> ML -> Kibana).

### Slide 3: The Customer Landscape
* **Header:** Understanding Our Audience
* **Content:**
  * **Mobile First:** 70% of browsing sessions originate from Mobile devices, with significantly shorter session durations than Desktop.
  * **Regional Payment Preferences:** Mobile Money dominates the West/East African segments (Ghana, Kenya), while Credit Cards remain strong in South Africa.
  * **The Benchmark:** The platform sees an average churn rate of ~25%.
* **Visual:** A pie chart showing Device Type splits, or a map highlighting African markets.

### Slide 4: Feature Engineering (Finding the Signal)
* **Header:** What Predicts Behavior?
* **Content:**
  * We aggregated two main categories of features to feed our model:
  * **RFM Metrics:** Recency (days since last purchase), Frequency (total purchases), and Monetary value (total spent).
  * **Engagement Metrics:** Average session duration, bounce rates, and total sessions.
  * *Finding:* Engagement (Total Sessions) often predicts retention better than past revenue alone.
* **Visual:** A bulleted list with simple icons (Calendar for Recency, Shopping Cart for Frequency, Clock for Engagement).

### Slide 5: Predictive Modeling
* **Header:** Predicting Churn Before It Happens
* **Content:**
  * **The Challenge:** Churn prediction datasets are highly imbalanced (most people don't churn).
  * **The Solution:** XGBoost (Extreme Gradient Boosting).
  * **Why XGBoost?** Handles non-linear relationships natively, gracefully manages missing data, and excels on imbalanced data.
  * **Outcome:** The model successfully isolates high-risk customers based on declining engagement trends before the 60-day churn window hits.
* **Visual:** A generic "Feature Importance" horizontal bar chart (Recency at the top, followed by Total Sessions).

### Slide 6: Key Findings
* **Header:** What The Data Tells Us
* **Content:**
  * **The 60-Day Wall:** Customer activity doesn't drop to zero overnight; it decays sharply around 45 days of inactivity.
  * **The Loyalty Shield:** Customers in Gold/Platinum tiers churn at roughly half the rate of Bronze customers, regardless of age.
  * **Friction Points:** High bounce rates on Mobile devices suggest the mobile checkout flow may be causing cart abandonment.

### Slide 7: Actionable Recommendations
* **Header:** Strategic Next Steps
* **Content:**
  * **1. Pre-emptive Re-engagement:** Launch automated email/SMS triggers at 21 days of inactivity—don't wait for the 60-day churn mark.
  * **2. Reward Browsing, Not Just Buying:** Gamify the app experience by rewarding daily logins to increase `total_sessions` (our strongest retention predictor).
  * **3. Lean into Mobile Money:** Offer a 5% discount for using Mobile Money in Ghana/Nigeria to reduce payment friction and boost conversion.
* **Visual:** 3 bold icons next to each recommendation.

### Slide 8 (Optional): Technical Q&A
* **Header:** Questions?
* **Content:** Links to GitHub Repo, Kaggle Notebook, and Architecture Diagrams.
