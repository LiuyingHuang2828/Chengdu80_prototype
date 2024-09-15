# Chengdu80_prototype - Corporate Risk Assessment Platform

## Overview
This project is a **Corporate Risk Assessment Platform** that integrates real-time news articles, company stock data and company 10K annual report to identify corporate vulnerabilities, classify risks, generate summaries, and provide risk scores. It helps decision-makers assess potential vulnerabilities and their impact on stock performance through interactive visualizations.

## Features
- **Automated Real-Time Risk Categorization**: Fetches and classifies real-time news into four risk types: Operational, Legal, Loan, and Other Risks.
- **AI-Driven Summarization**: Generates structured summaries and risk scores using GPT-based models (GPT 3.5 Turbo and 4).
- **Risk-Stock Correlation**: Provides visual insights into how corporate risks affect stock prices.
- **Interactive Dashboard**: Displays risk scores and stock trend graphs for early risk warnings.

## Project Workflow
1. **Data Ingestion**: Fetches real-time news articles using News API, company stock data via Yahoo Finance API, and company 10K Annual Report though SEC fillings database.
2. **Risk Classification**: Classifies the news articles into four distinct risk categories.
3. **Summarization and Risk Scoring**: Uses GPT-based models to generate summaries and calculate a risk score for each category.
4. **Visualizations**:
   - Risk scores 
   - Stock performance trends 
5. **User Dashboard**: Interactive user interface for stakeholders to track risks and stock movements in real-time.

## Tech Stack
- **Backend**: Python, Flask
- **Data Sources**: News API, yFinance, SEC Edgar
- **AI Models**: GPT-3.5 Turbo and 4, DeepSeek-Chat
- **Frontend**: HTML, CSS, JavaScript (Highcharts for stock visualizations)

## Future Work
- Optimize the process for generating corporate vulnerability reports from 10K Annual Reports, ensuring seamless integration into the main summarization and risk assessment pipeline.