# Presentation Structure & Talking Points

If you are asked to present your assignment, follow this structure. It is designed to show that you are not just a coder, but a strategic engineer who understands business value.

## 1. Introduction & Approach (2 mins)
* "Thank you for the opportunity to present my solution."
* "My goal for this assignment wasn't just to train a model, but to build an end-to-end pipeline that mirrors a real-world e-commerce architecture."
* "I broke the problem down into four phases: Synthetic Data Generation, Data Engineering/Aggregation, Predictive Modeling, and Big Data Dashboarding."

## 2. The Data & Context (2 mins)
* "I generated roughly 2.5 million records representing 50,000 customers."
* "I specifically tailored the dataset to the **African context**. I included cities across Ghana, Nigeria, and South Africa, and modeled realistic payment preferences like Mobile Money."
* "I also intentionally dirtied the data with duplicates and missing values to simulate real-world extraction pipelines."

## 3. Feature Engineering (2 mins)
* "To predict churn, raw logs aren't enough. I used optimized Pandas to aggregate the transactional and session data into customer profiles."
* "I focused heavily on **RFM metrics** (Recency, Frequency, Monetary) and **behavioral engagement** (like bounce rates and session durations)."

## 4. The Predictive Model (3 mins)
* "For the modeling phase, I defined a churned customer as one who hasn't purchased in 60 days."
* "I started with a Logistic Regression baseline, but e-commerce behavior is highly non-linear. I moved to **XGBoost**, which dramatically improved performance and handled the natural class imbalance of churn datasets."
* "The model achieved strong precision and recall, but more importantly, it allowed us to extract feature importance."

## 5. Actionable Business Insights (3 mins)
*(This is where you win the interview. Focus on the 'So What?')*
* "Based on the model's feature importance and my EDA, I have 3 key recommendations for the business:"
  1. **The 60-Day Wall**: "Activity drops off sharply before churn. We shouldn't wait 60 days to react. We should implement automated re-engagement triggers at 21 and 45 days of inactivity."
  2. **Engagement Over Revenue**: "The model showed that frequent browsing, even without purchasing, is a massive deterrent to churn. We should gamify or reward daily logins."
  3. **Payment Friction**: "Mobile money is dominating the West African segments. We should run a campaign offering a 5% discount for Mobile Money users to increase conversion rates in those regions."

## 6. The Big Data Component (2 mins)
* "Finally, for the Big Data requirement, I built an integration with **Elasticsearch**."
* "Elasticsearch is the ideal choice here because it is fundamentally designed for time-series event data. Instead of running heavy SQL queries for basic metrics, Elasticsearch allows business teams to use Kibana to visualize live metrics (like revenue by category or live session counts) in milliseconds."

## 7. Conclusion
* "In summary, this pipeline takes raw, messy data, structures it into actionable ML features, and serves it to both predictive models and real-time dashboards."
* "I'm happy to walk through the codebase or answer any questions."
