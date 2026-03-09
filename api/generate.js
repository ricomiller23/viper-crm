import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY || "",
});

export default async function handler(req, res) {
    if (req.method !== "POST") {
        return res.status(405).json({ error: "Method Not Allowed" });
    }

    try {
        if (!process.env.OPENAI_API_KEY) {
            return res.status(500).json({ error: "OPENAI_API_KEY not configured. Add it to Vercel environment." });
        }

        const { company, name, category, city_state, analysis } = req.body;

        const systemPrompt = `
You are the VP of Strategic Accounts for the CHIT Marketplace, an advanced cryptocurrency-based B2B treasury and settlement layer designed for high-margin, cash-heavy industries like ${category || 'Cannabis'} that struggle with traditional banking or compliance bottlenecks.

Your task is to write TWO distinct, highly personalized emails to this exact prospect:
Prospect Name: ${name || 'Executive'}
Company: ${company || 'your organization'}
Location: ${city_state || 'the local market'}
Industry Category: ${category || 'Adjunct'}
Internal Analysis Context: ${analysis || 'They need a compliant digital settlement solution.'}

---
Email 1: Cold Introduction
Write a punchy, 3-paragraph cold outreach email.
- Hook them by uniquely referencing their company and the specific banking/cash friction in the ${category || 'local'} industry. Use their Internal Analysis Context to customize this!
- Pitch the CHIT treasury system as a compliant, digital solution.
- Include a specific Call to Action (CTA) asking for a 10-minute discovery call next week. Do NOT use fake bracketed times.

Email 2: Warm Follow-up
Write a 2-paragraph follow-up. Assume they downloaded a CHIT whitepaper or you left a voicemail.
- Reiterate the core value prop tailored directly to their company.
- Propose a specific next step, like a small-scale pilot rollout or an introductory demo.

Format exactly like this, and include NO other conversational text:
***COLD INTRO***
Subject: [Your creative subject line]

[Body of cold intro]

***WARM FOLLOW-UP***
Subject: [Your creative subject line]

[Body of warm follow-up]
`;

        const response = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
                { role: "system", content: systemPrompt.trim() },
                { role: "user", content: `Generate the drafts for ${name} at ${company}.` }
            ],
            temperature: 0.7,
        });

        const body = response.choices[0].message?.content?.trim();

        return res.status(200).json({ success: true, body });
    } catch (error) {
        console.error("OpenAI error:", error.message);
        return res.status(500).json({ error: error.message });
    }
}
