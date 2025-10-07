# Multi-Agent Cost-Aware Phishing Defense
This repository contains a multi-agent system designed to analyze and defend against phishing attacks. The system leverages HTML content crawling, feature extraction, and dataset analysis to identify and mitigate phishing threats.

### Features
HTML Content Crawling: Extracts and processes HTML content from URLs.
Feature Extraction: Analyzes HTML features to identify phishing indicators.
Batch Processing: Combines and processes multiple datasets for scalability.
Dataset Support: Includes the PhiUSIIL Phishing URL Dataset for analysis.

## 1. HTML Content Crawling
Run the dom_content_crawler_main.py script to crawl and extract HTML content:

## 2. Batch Combination
Combine multiple CSV files into a single dataset using batch_combiner.py:

## 3. Analyze HTML Features
Use the html_content_crawler.py script to analyze and extract features: