import pandas as pd
import json
import re

def process_block(block, leads):
    company_name = "Unknown Company"
    phone = ""
    city_state = ""
    
    # First pass: find company name and phone
    for row in block:
        val1 = str(row.get(1, ''))
        if val1 and val1 != 'nan':
            if 'Marijuana' in val1 or 'Operating' in val1:
                match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', val1)
                if match:
                    phone = match.group()
            elif len(val1) > 2 and ' ' not in val1[:4] and company_name == "Unknown Company" and val1 != "Name":
                company_name = val1
                
    # Second pass: find people
    for row in block:
        name = str(row.get(3, ''))
        if name and name != 'nan' and name != 'NAME':
            address = str(row.get(4, ''))
            loc = "AZ"
            if address and address != 'nan':
                parts = address.split(',')
                if len(parts) >= 3:
                    loc = f"{parts[-3].strip()}, {parts[-2].strip()}"
                else:
                    loc = address
            
            # Use company from row 1 if possible
            row_comp = str(row.get(1, ''))
            if row_comp and row_comp != 'nan' and row_comp != 'Name' and not 'Marijuana' in row_comp:
                company_name = row_comp

            lead = {
                "name": name.strip(),
                "company": company_name.strip(),
                "category": "Cannabis",
                "email": "",
                "phone": phone.strip(),
                "city_state": loc.strip(),
                "analysis": "Sourced from AZ state dispensary licensure Matrix. High-cash volume cannabis enterprise directly suited for CHIT B2B digital treasury."
            }
            leads.append(lead)

def main():
    df = pd.read_excel("/Users/ericmiller/Downloads/Matrix.xlsx", header=None)
    leads = []
    
    # Read existing leads if any (to append rather than overwrite completely, or we can just overwrite)
    # The requirement is to start populating, let's just create a rich list of 100 leads to demonstrate scale.
    
    current_block = []
    for index, row in df.iterrows():
        val1 = row.get(1)
        val3 = row.get(3)
        if pd.isna(val1) and pd.isna(val3):
            if current_block:
                process_block(current_block, leads)
                current_block = []
        else:
            current_block.append({1: val1, 2: row.get(2), 3: val3, 4: row.get(4)})

    if current_block:
        process_block(current_block, leads)
        
    output = {"leads": leads[:120]}  # limit to 120 so the UI doesn't crash on this simple HTML page
    with open('/Users/ericmiller/viper-crm/leads.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Successfully exported {len(output['leads'])} (out of {len(leads)} total parsed) Cannabis leads to VIPER CRM.")

if __name__ == "__main__":
    main()
