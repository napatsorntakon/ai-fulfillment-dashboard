# 📦 AI Fulfillment Dashboard

An interactive analytics dashboard that leverages AI to identify fulfillment inefficiencies and recommend operational improvements.

## Dashboard Preview

### Main Dashboard
<img width="2760" height="1332" alt="image" src="https://github.com/user-attachments/assets/11f5200d-73dc-4190-971a-14d90c7c5414" />


### Operational Insights
<img width="2782" height="754" alt="image" src="https://github.com/user-attachments/assets/6fb50354-3fad-4df6-ac13-e1cdbef405cc" />


## Features

* KPI tracking (delay, on-time rate, total orders)
* Interactive filtering by warehouse and delay reason
* Visual insights (delay distribution & order trends)
* AI-powered analysis and Q&A
* What-if simulation to estimate operational improvements

## Architecture Diagram

<img width="1536" height="1024" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/b8b828e1-a888-42ba-8421-9902e642bd41" />

## AI Capabilities

* Uses LLMs to analyze fulfillment patterns and operational performance
* Combines aggregated metrics with sampled transactional data (hybrid context approach)
* Generates actionable operational insights and recommendations
<img width="2742" height="1534" alt="image" src="https://github.com/user-attachments/assets/c610924d-d312-4d02-87b9-88a8a0abe342" />

## Business Impact

This project demonstrates how AI-assisted analytics can support fulfillment and warehouse operations by transforming raw operational data into actionable insights.

Key business values include:

* Faster identification of fulfillment bottlenecks and delay patterns
* Improved operational visibility through KPI monitoring and visual analytics
* AI-generated root cause analysis to support operational decision-making
* What-if simulation to evaluate potential process improvements
* Reduced manual analysis effort for operations and business teams

The dashboard is designed to simulate real-world operational analytics workflows commonly used in e-commerce and supply chain environments.

## Tech Stack

* **Python** – data processing and application logic
* **Pandas** – data cleaning, aggregation, and KPI calculation
* **Streamlit** – interactive dashboard development
* **Plotly** – interactive data visualization
* **Google Gemini API** – AI-powered analysis and Q&A
* **Streamlit Community Cloud** – dashboard deployment
* **GitHub** – version control and project hosting

## Dataset

Synthetic fulfillment dataset (500 rows) containing:

* Order lifecycle data
* Warehouse operation metrics
* Delivery delays and operational issue categories

## Live Demo

Please use this sample dataset for the demo:

[fulfillment_dummy_500_rows.csv](https://github.com/napatsorntakon/ai-fulfillment-dashboard/blob/main/fulfillment_dummy_500_rows.csv)

👉 https://ai-fulfillment-dashboardgit-5bgj3h7jo6wa5eshnkga5v.streamlit.app/

## Example Insights

* Identified top delay warehouses contributing to late deliveries
* Highlighted operational root causes such as stockouts and courier issues
* Simulated potential service-level improvements from delay reduction initiatives

## Author

Napatsorn Takon
