from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "Intelligent Systems Services Engineer - Assignment Submission", border=False, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", size=11)

# Applicant Details
pdf.set_font("helvetica", "B", 12)
pdf.cell(0, 6, "Applicant Name: Anthony Opoku-Acheampong", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", size=11)
pdf.cell(0, 6, "Contact: +233598854433", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "Role: Intelligent Systems Services Engineer (Data Science)", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "Company: Npontu Technologies Ltd.", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)

# Overview
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 8, "Assignment Overview", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", size=11)
overview = (
    "Please find my complete submission for the 'Analyzing Customer Behavior for E-commerce Insights' assignment. "
    "To ensure the codebase is professional, reproducible, and easy to review, I have structured the entire project "
    "into an end-to-end data pipeline and uploaded it to GitHub, as requested for Data Science roles."
)
pdf.multi_cell(0, 6, overview)
pdf.ln(8)

# GitHub Link
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 8, "GitHub Repository Link", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", "U", 11)
pdf.set_text_color(0, 0, 255)
pdf.cell(0, 6, "https://github.com/Tony-Stone-Code/npontu-ecommerce-analysis", link="https://github.com/Tony-Stone-Code/npontu-ecommerce-analysis", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)
pdf.ln(8)

# Included items
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 8, "What is included in the Repository:", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", size=11)

items = [
    ("1. The Jupyter Notebook (notebooks/analysis.ipynb)", "Contains the Exploratory Data Analysis, data cleaning, and the XGBoost predictive model used to determine customer churn."),
    ("2. Business Insights (INSIGHTS.md)", "A summary of the model's feature importance, visualizations, and 4 actionable recommendations for the business (e.g. implementing the '60-Day Wall' trigger)."),
    ("3. Synthetic Data Pipeline (scripts/generate_data.py & pandas_processing.py)", "Scripts that programmatically generate 2.5 million realistic e-commerce events (tailored to African markets like Ghana and Nigeria) and aggregate them into RFM/engagement metrics."),
    ("4. Big Data Tooling (scripts/elasticsearch_ingest.py)", "An ingestion script that pushes the processed time-series event data into an Elasticsearch cloud cluster, paving the way for real-time Kibana dashboards."),
    ("5. Interview & Presentation Prep (docs/)", "Outlines and explanations of the technical architecture.")
]

for title, desc in items:
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 6, "   " + desc)
    pdf.ln(3)

pdf.ln(5)
pdf.cell(0, 6, "Thank you for your time and for the opportunity to work on this assignment.", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "I look forward to discussing my findings with the technical team.", new_x="LMARGIN", new_y="NEXT")

base_dir = os.path.dirname(os.path.dirname(__file__))
pdf.output(os.path.join(base_dir, "Npontu_Assignment_Submission.pdf"))
print("PDF Generated Successfully!")
