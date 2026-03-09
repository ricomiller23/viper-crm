import json
import os
import re
import time
from typing import List, Optional
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from openai import OpenAI

class Lead(BaseModel):
    name: str = Field(description="Name of the key contact, owner, doctor, or founder. If unknown, leave blank.")
    company: str = Field(description="Name of the clinic, dispensary, or business.")
    category: str = Field(description="Strictly one of: 'Psychedelics', 'Peptides', 'Cannabis', or 'Other'")
    email: Optional[str] = Field(description="Email address of the business or contact if found.")
    phone: Optional[str] = Field(description="Phone number of the business if found.")
    city_state: str = Field(description="Location of the business (e.g., 'Phoenix, AZ').")
    analysis: str = Field(description="A 2-3 sentence analysis of why this business is a good match for the CHIT coin settlement layer. Focus on high-margin cash models.")

# Prompt to extract the precise Lead structure
EXTRACT_PROMPT = """
You are an expert sales intelligence agent for VIPER CRM.
Your objective is to review the following scraped website text from an "adjunct" health/alternative medicine clinic and extract the key contact information.

Target Profile:
We are looking for alternative medicine or lifestyle clinics (Ketamine, Psilocybin, TRT, Peptides, HRT, MMJ). These are cash-heavy, high-margin businesses that could benefit from adopting the CHIT Marketplace token (a B2B stablecoin settlement layer).

Text Content:
{text}

Instructions:
1. Extract the name of the owner, primary doctor, or director.
2. Extract the business name.
3. Categorize it strictly as 'Psychedelics', 'Peptides', 'Cannabis', or 'Other'.
4. Extract the best contact email and phone number.
5. Extract the city and state.
6. Write a short analysis (2-3 sentences) on why this specific business matches our CHIT target profile based on what they do.
"""

def extract_text_from_url(url: str) -> str:
    """Basic fallback text scraper."""
    try:
        # Avoid simple bot blockers
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Kill scripts and styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.extract()
            text = soup.get_text(separator=' ', strip=True)
            # Take the first ~5000 chars to avoid blowing up context window
            return text[:5000]
    except Exception as e:
        print(f"Scrape error for {url}: {e}")
    return ""

def process_lead(client: OpenAI, text: str) -> Optional[dict]:
    """Uses OpenAI Structured Outputs to parse the text into our exact Lead schema."""
    if not text or len(text) < 100:
        return None
        
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a highly accurate data extraction CRM agent."},
                {"role": "user", "content": EXTRACT_PROMPT.format(text=text)}
            ],
            response_format=Lead,
        )
        lead = completion.choices[0].message.parsed
        return lead.model_dump()
    except Exception as e:
        print(f"Extraction error: {e}")
        return None

def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found. Attempting a mock fallback for demonstration.")
        # If no key, we will just pipe in a mock file to prove the system works.
        mock_data = {
            "leads": [
                {
                    "name": "Dr. Sarah Jenkins",
                    "company": "Optimum HRT & Peptides",
                    "category": "Peptides",
                    "email": "hello@optimum-hrt.fake",
                    "phone": "(480) 555-1234",
                    "city_state": "Scottsdale, AZ",
                    "analysis": "High volume TRT clinic operating mostly out-of-pocket cash. Prime target for CHIT adoption."
                }
            ]
        }
        with open('leads.json', 'w') as f:
            json.dump(mock_data, f, indent=2)
        print("Wrote mock leads.json")
        return

    client = OpenAI(api_key=api_key)
    
    # We will search for 2 of each category to seed the CRM
    queries = [
        "ketamine clinic arizona contact team",
        "peptide therapy trt clinic scottsdale contact"
    ]
    
    all_leads = []
    
    with DDGS() as ddgs:
        for query in queries:
            print(f"Searching: {query}")
            results = ddgs.text(query, max_results=3)
            
            for res in results:
                url = res.get("href")
                title = res.get("title")
                print(f"  -> Scraping: {title} ({url})")
                
                # Introduce a small delay to respect rate limits
                time.sleep(2)
                
                text_content = extract_text_from_url(url)
                if text_content:
                    lead_data = process_lead(client, text_content)
                    if lead_data:
                        print(f"     Found Lead: {lead_data['company']} - {lead_data['name']}")
                        all_leads.append(lead_data)

    print(f"\nFinished scraping. Extracted {len(all_leads)} leads.")
    
    output = {"leads": all_leads}
    with open('leads.json', 'w') as f:
        json.dump(output, f, indent=2)
        
    print("Saved to leads.json")

if __name__ == "__main__":
    main()
