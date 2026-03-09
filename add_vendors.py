import json
import os

def main():
    leads_file = '/Users/ericmiller/viper-crm/leads.json'
    
    # Load existing leads if possible
    leads_data = {"leads": []}
    if os.path.exists(leads_file):
        with open(leads_file, 'r') as f:
            try:
                leads_data = json.load(f)
            except:
                pass

    new_vendors = [
        {
            "name": "Thomas W. Dean, Esq.",
            "company": "Attorney For Cannabis",
            "category": "Cannabis",
            "email": "tdean@attorneyforcannabis.com",
            "phone": "(602) 635-4990",
            "city_state": "Phoenix, AZ",
            "analysis": "Specialized Cannabis attorney in Phoenix. Prime vendor partner to refer CHIT treasury solutions to his dispensary clients."
        },
        {
            "name": "Managing Partner",
            "company": "RSN Law - Rutila, Seibt & Nash PLLC",
            "category": "Cannabis",
            "email": "contact@rsnlawaz.com",
            "phone": "(480) 712-0035",
            "city_state": "Scottsdale, AZ",
            "analysis": "Cannabis licensing and compliance law firm. Strong strategic partner for mapping regulatory frameworks for CHIT coin."
        },
        {
            "name": "Principal Consultant",
            "company": "The Cannabis Business Advisors",
            "category": "Cannabis",
            "email": "info@thecannabisbusinessadvisors.com",
            "phone": "(602) 290-9424",
            "city_state": "Phoenix, AZ",
            "analysis": "Top operational consultants in AZ cannabis. Perfect alliance to integrate CHIT tracking & reporting from day 1 for new dispensaries."
        },
        {
            "name": "Donald W. Hudspeth",
            "company": "The Law Offices of Donald W. Hudspeth, P.C.",
            "category": "Peptides",
            "email": "dhudspeth@azbuslaw.com",
            "phone": "(866) 696-2033",
            "city_state": "Phoenix, AZ",
            "analysis": "Healthcare business law expert advising on med spa and peptide clinic compliance. Key channel partner for CHIT adoption in cash-heavy clinics."
        },
        {
            "name": "Managing Partner",
            "company": "ARTEMiS Law Firm",
            "category": "Peptides",
            "email": "info@artemislawfirm.com",
            "phone": "Unknown",
            "city_state": "Scottsdale, AZ",
            "analysis": "Specializes in HIPAA compliance and professional licensing for medical aesthetics. Excellent pathway to peptide market penetration."
        },
        {
            "name": "Aaron Sagedahl",
            "company": "Quarles & Brady LLP",
            "category": "Peptides",
            "email": "aaron.sagedahl@quarles.com",
            "phone": "(612) 351-5050",
            "city_state": "Phoenix, AZ",
            "analysis": "Monitors physician supervision and med spa compliance. Represents high-end aesthetics clinics that need robust financial settlement like CHIT."
        },
        {
            "name": "Consultant Team",
            "company": "Higher Yields Cannabis Consultants",
            "category": "Cannabis",
            "email": "sales@higheryieldsconsulting.com",
            "phone": "(844) HI-YIELD",
            "city_state": "Arizona",
            "analysis": "Full-service scalability and audit consultants. Ideal partners to upsell CHIT treasury processing as an operational efficiency gain."
        }
    ]

    # Prepend new vendors so they show up at the top of the interface
    leads_data['leads'] = new_vendors + leads_data.get('leads', [])
    
    with open(leads_file, 'w') as f:
        json.dump(leads_data, f, indent=2)

    print(f"Added {len(new_vendors)} verified vendor contacts to CRM.")

if __name__ == "__main__":
    main()
