# Chengdu80_prototype - Corporate Risk Assessment Platform

## Overview
This project is a **Corporate Risk Assessment Platform** that integrates real-time news articles and company stock data to classify risks, generate summaries, and provide risk scores. It helps decision-makers assess potential vulnerabilities and their impact on stock performance through interactive visualizations.

## Features
- **Automated Real-Time Risk Categorization**: Fetches and classifies real-time news into four risk types: Operational, Legal, Loan, and Other Risks.
- **AI-Driven Summarization**: Generates structured summaries and risk scores using GPT-based models (GPT 3.5 Turbo and 4).
- **Risk-Stock Correlation**: Provides visual insights into how corporate risks affect stock prices.
- **Interactive Dashboard**: Displays risk scores and stock trend graphs for early risk warnings.

## Project Workflow
1. **Data Ingestion**: Fetches real-time news articles using News API and company stock data via Yahoo Finance API.
2. **Risk Classification**: Classifies the news articles into four distinct risk categories.
3. **Summarization and Risk Scoring**: Uses GPT-based models to generate summaries and calculate a risk score for each category.
4. **Visualizations**:
   - Risk scores 
   - Stock performance trends 
5. **User Dashboard**: Interactive user interface for stakeholders to track risks and stock movements in real-time.

## Tech Stack
- **Backend**: Python, Flask
- **Data Sources**: News API, yFinance
- **AI Models**: GPT-3.5 Turbo and 4
- **Frontend**: HTML, CSS, JavaScript (Highcharts for stock visualizations)



