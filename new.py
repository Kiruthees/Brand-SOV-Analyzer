import os
import re
import json
import requests
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")


# ------------------ Utility: View Count Parser ------------------ #
def normalize_view_count(text) -> int:
    """Convert YouTube view count strings to integers."""
    if not isinstance(text, str):
        return 0
    txt = text.lower().replace(' views', '').strip()
    try:
        if 'k' in txt:
            return int(float(txt.replace('k', '')) * 1_000)
        elif 'm' in txt:
            return int(float(txt.replace('m', '')) * 1_000_000)
        elif 'b' in txt:
            return int(float(txt.replace('b', '')) * 1_000_000_000)
        return int(re.sub(r'\D', '', txt))
    except Exception:
        return 0


# ------------------ SERPAPI Fetchers ------------------ #
def google_search(keyword: str, limit: int = 10):
    print(f"[Google] Searching for: {keyword}")
    params = {
        "engine": "google",
        "q": keyword,
        "num": limit,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    try:
        r = requests.get("https://serpapi.com/search", params=params)
        r.raise_for_status()
        results = r.json().get("organic_results", [])
        return [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            }
            for item in results
        ]
    except Exception as err:
        print(f"Google fetch error: {err}")
        return []


def youtube_search(keyword: str, limit: int = 10):
    print(f"[YouTube] Searching for: {keyword}")
    params = {
        "engine": "youtube",
        "search_query": keyword,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    try:
        r = requests.get("https://serpapi.com/search", params=params)
        r.raise_for_status()
        videos = r.json().get("video_results", [])
        return [
            {
                "title": vid.get("title", ""),
                "views": normalize_view_count(vid.get("view_count_text", "0")),
                "snippet": vid.get("description", "")
            }
            for vid in videos[:limit]
        ]
    except Exception as err:
        print(f"YouTube fetch error: {err}")
        return []


# ------------------ LLM Keyword Generation ------------------ #
def brainstorm_keywords(base_term: str, brand: str, count: int = 5):
    """Generate related search terms for marketing analysis."""
    print(f"Brainstorming around seed: {base_term}")
    idea_prompt = f"""
    You are a marketing & SEO expert for "{brand}".
    Suggest {count} high-value related search terms for "{base_term}".
    Include a mix of:
    - Informational queries
    - Commercial/competitive comparisons
    - Long-tail descriptive phrases
    Return as JSON array of strings only.
    """
    try:
        resp = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": idea_prompt}],
            response_format={"type": "json_object"},
            temperature=0.5
        )
        parsed = json.loads(resp.choices[0].message.content)
        if isinstance(parsed, list):
            print(f"Generated: {parsed}")
            return parsed
        elif isinstance(parsed, dict):
            for v in parsed.values():
                if isinstance(v, list):
                    print(f"Generated: {v}")
                    return v
    except Exception as e:
        print(f"Keyword generation failed: {e}")
    return [base_term]


# ------------------ Keyword Analysis ------------------ #
def keyword_analysis(data: dict, brand: str, term: str):
    """Run SoV & sentiment analysis for a keyword using GPT."""
    print(f"Analyzing keyword: {term}")
    analysis_prompt = f"""
    Analyze this dataset for keyword "{term}" and brand "{brand}".

    GOOGLE:
    - SoV: (#results mentioning brand / total results) * 100
    - SoPV: (#positive sentiment results mentioning brand / total mentions) * 100

    YOUTUBE:
    - wSoV: (views of brand videos / total views) * 100
    - SoPV: (views of positive sentiment brand videos / total brand views) * 100

    Data:
    {json.dumps(data, indent=2)}

    Respond as JSON with:
    {{
      "keyword": "...",
      "google_analysis": {{"sov": %, "sopv": %}},
      "youtube_analysis": {{"wsov": %, "sopv": %}},
      "combined_insight": "..."
    }}
    """
    try:
        resp = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"},
            temperature=0.25
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        print(f"Keyword analysis failed: {e}")
        return {"keyword": term, "error": str(e)}


# ------------------ Final Report Generation ------------------ #
def compile_strategy_report(summaries: list, brand: str):
    """Merge keyword summaries into one marketing report."""
    print("Compiling strategic report...")
    final_prompt = f"""
    You are the CMO of "{brand}". 
    Using the following multi-platform keyword analyses:
    {json.dumps(summaries, indent=2)}

    Write a markdown report including:
    1. Executive Summary of brand's online presence
    2. Google vs YouTube performance comparison
    3. Top growth opportunities per platform
    4. 3 actionable recommendations
    """
    try:
        resp = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.35
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating report: {e}"


# ------------------ Orchestrator ------------------ #
class SOVAnalyzer:
    def __init__(self, brand, competitors=None):
        self.brand = brand
        self.competitors = competitors or []

    def process_keyword(self, term):
        g_results = google_search(term)
        y_results = youtube_search(term)
        if not g_results and not y_results:
            return {"keyword": term, "error": "No results"}
        return keyword_analysis(
            {"google_results": g_results, "youtube_results": y_results},
            self.brand,
            term
        )


# ------------------ Main Execution ------------------ #
if __name__ == "__main__":
    BRAND = "Atomberg"
    COMPETITORS = ["Usha", "Havells", "Bajaj", "Orient", "Crompton"]
    SEED = "smart fan"

    keyword_list = brainstorm_keywords(SEED, BRAND)
    analyzer = SOVAnalyzer(BRAND, COMPETITORS)

    results = []
    for kw in keyword_list:
        results.append(analyzer.process_keyword(kw))
        print("-" * 30)

    if results:
        report = compile_strategy_report(results, BRAND)
        print("\n" + "="*60)
        print(" FINAL STRATEGIC REPORT ")
        print("="*60)
        print(report)
