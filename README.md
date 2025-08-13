# SOVAnalyzer: AI-Powered Brand & Competitor Analysis

Welcome to **SOVAnalyzer**, an intelligent tool designed to analyze and compare online visibility (Share of Voice - SoV) across Google and YouTube, providing powerful insights for brand strategy. Built with the power of GPT-4, this tool helps marketers and SEO professionals to understand their brand's online presence, spot opportunities, and stay ahead of competitors.

---

## 🚀 **Features**

- **Google & YouTube Search:** Fetch the latest search results and video data from Google and YouTube.
- **View Count Normalization:** Automatically converts YouTube view count data into a comparable numerical format.
- **Keyword Generation:** Leverages OpenAI to brainstorm high-value, SEO-friendly search terms for marketing campaigns.
- **SoV & Sentiment Analysis:** Conducts detailed analysis of search results and video views to calculate Share of Voice (SoV) and sentiment performance.
- **Comprehensive Marketing Reports:** Combines data into a markdown report highlighting actionable insights and strategies for brand growth.

---

## 🛠 **Tech Stack**

- **Python** - The backbone of the project, handling all data fetching, processing, and analysis.
- **OpenAI (GPT-4)** - Used to generate relevant keywords and analyze data with advanced AI models.
- **SerpAPI** - Fetches live Google and YouTube search data for real-time analysis.
- **dotenv** - Loads environment variables to keep your API keys secure.

---

## 📦 **Installation**

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/SOVAnalyzer.git
   cd SOVAnalyzer
   
2. Set up .env file with the following content:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   SERPAPI_API_KEY=your_serpapi_api_key

---

## ⚙ *Usage*
- **Keyword Brainstorming** - Generate a list of high-value SEO-related keywords for a given seed term and brand.
    ```bash
    keyword_list = brainstorm_keywords("seed_term", "brand_name")
    
- **Analyzing Brand's SoV & Sentiment** - Perform analysis on Google search results and YouTube video data for a specific keyword.
    ```
    analyzer = SOVAnalyzer("our_brand", competitors=["brand1", "brand2"])
    results = analyzer.process_keyword("seed_term")
    
- **Compiling Strategic Report** - Generate a comprehensive marketing strategy report based on multiple keyword analyses.
    ```
    report = compile_strategy_report(results, "brand_name")
    print(report)
    
---

## 📊 **How It Works**
### Google & YouTube Data Fetching:
Using SerpAPI, the tool queries Google and YouTube for the most relevant search results and videos related to a given keyword.

### Keyword Generation:
Leveraging OpenAI's GPT-4 model, the tool generates related search terms, including informational, competitive, and long-tail keywords.

### SoV Analysis:
The tool calculates the Share of Voice (SoV) by analyzing the number of results mentioning the brand divided by the total results. It also measures sentiment (positive vs. negative) to evaluate the brand's online presence.

### Strategy Report:
A final markdown report is generated that provides a comprehensive analysis of the brand's performance on Google vs. YouTube, growth opportunities, and actionable recommendations for brand improvement.
