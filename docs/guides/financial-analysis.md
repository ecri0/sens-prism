# Financial Analysis with Sens Prism

Financial analysts, investors, and CFOs process hundreds of earnings reports, SEC filings, and market analyses to identify trends and risks. Sens Prism enables fast semantic search across financial documents while protecting sensitive data from exposure to LLMs.

## The Challenge

A financial analyst tracking 15 tech companies must:
- Read quarterly earnings reports (60+ pages each, 4 per year per company)
- Track metrics across years (revenue, margin, R&D spend)
- Identify risk disclosures and management guidance
- Cross-company comparison (which company is gaining market share?)
- Keep financial figures confidential (proprietary analysis for clients)

Manual review: 200+ hours per year
With Sens Prism: 30 hours of focused analysis

## Solution: Sens Prism Workflow

### Step 1: Upload Financial Documents

Build your analysis knowledge base:

```bash
# Upload company earnings reports
for company in apple google microsoft amazon; do
  for quarter in Q1 Q2 Q3 Q4; do
    for year in 2023 2024; do
      file="documents/${company}_${quarter}_${year}.pdf"
      if [ -f "$file" ]; then
        curl -X POST https://api.sens.ai/v1/documents \
          -H "Authorization: Bearer sens_sk_..." \
          -F "file=@$file" \
          -F "title=$company $quarter $year Earnings" \
          -F "tags=earnings,$company,10-q,$year"
      fi
    done
  done
done
```

Or programmatically:

```python
from sens import SensClient

client = SensClient(api_key="sens_sk_...")

companies = ["Apple", "Google", "Microsoft", "Amazon"]
for company in companies:
    for quarter in ["Q1", "Q2", "Q3", "Q4"]:
        for year in [2023, 2024]:
            doc = client.upload_document(
                file_path=f"documents/{company}_{quarter}_{year}.pdf",
                tags=["earnings", company.lower(), "10-q", str(year)]
            )
            print(f"Uploaded: {doc.title}")
```

**Smart Sanitizer** automatically protects:
- Specific revenue figures (flagged for redaction)
- Profit margins and cost breakdowns
- Forward-looking financial guidance
- Executive compensation details

Sensitive numbers are removed before any LLM processing, but tracked for your internal use.

### Step 2: Track Financial Metrics Across Time

Query the same metric across companies and quarters:

```python
# Find revenue growth rates
result = client.query(
    query="What was the year-over-year revenue growth?",
    tags=["earnings", "2024"],
    limit=5
)

print("2024 Revenue Growth:")
context = client.get_context_rail(result.query_id)
for source in context.sources:
    print(f"  {source.document_title}: {source.excerpt}")
    print(f"    Confidence: {source.confidence_score:.0%}")
    print()
```

Response example:
```
Q1 2024 Earnings - Apple: "Year-over-year revenue increased 5% to $90.7 billion"
Q1 2024 Earnings - Google: "Year-over-year revenue growth of 13% to $84.3 billion"
Q1 2024 Earnings - Microsoft: "Year-over-year growth of 17% in cloud revenue"
```

The Context Rail shows:
- **Exact page** where figure appears
- **Confidence score** (0.98 for numeric figures vs. 0.75 for interpretive statements)
- **Semantic layer** (Chunk=raw number, Pragmatic=growth interpretation)

### Step 3: Cross-Company Comparison

Identify trends and competitive positioning:

```python
# Find what each company is investing in
companies = ["Apple", "Google", "Microsoft", "Amazon"]

for company in companies:
    result = client.query(
        query="What are the primary areas of capital expenditure and R&D investment?",
        tags=["earnings", company.lower()],
        limit=3
    )
    print(f"\n{company}:")
    print(f"  {result.answer}")
    print(f"  Confidence: {result.confidence_score:.0%}")
```

This helps identify:
- **Who's investing in AI** (which companies spending on GPUs/chips?)
- **Geographic expansion** (which regions getting new data centers?)
- **Market positioning** (who's betting on which technologies?)

### Step 4: Risk & Disclosure Analysis

Find risk factors and forward guidance:

```python
# Identify company-specific risks
risk_queries = [
    "What regulatory risks are disclosed?",
    "What supply chain vulnerabilities does the company face?",
    "What is the company's exposure to geopolitical risks?"
]

for query in risk_queries:
    result = client.query(query, tags=["earnings", "2024"])
    print(f"\n{query}")
    print(f"  Answer: {result.answer}")

    # Check semantic layer to see if it's a known risk vs. speculative
    context = client.get_context_rail(result.query_id)
    for source in context.sources:
        if source.semantic_layer == "pragmatic":
            print(f"  ⚠️  Actionable risk from {source.document_title}: {source.excerpt}")
```

### Step 5: Export Analysis for Reports

Generate data for client reports:

```python
import json
from datetime import datetime

# Analyze all companies on key metrics
analysis = {}

metrics = [
    "What was gross margin?",
    "How much cash did the company generate from operations?",
    "What percentage of revenue is spent on R&D?"
]

for company in ["Apple", "Google", "Microsoft", "Amazon"]:
    analysis[company] = {}

    for metric in metrics:
        result = client.query(
            query=metric,
            tags=["earnings", company.lower(), "2024"]
        )

        context = client.get_context_rail(result.query_id)
        analysis[company][metric] = {
            "answer": result.answer,
            "confidence": result.confidence_score,
            "sources": [
                {
                    "document": s.document_title,
                    "page": s.page,
                    "excerpt": s.excerpt,
                    "confidence": s.confidence_score
                }
                for s in context.sources[:2]
            ]
        }

# Export for reporting
with open(f"analysis_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
    json.dump(analysis, f, indent=2)

print(f"Analysis saved with {len(analysis)} companies × {len(metrics)} metrics")
```

---

## Use Case Examples

### Example 1: Quarterly Performance Tracking

**Scenario**: Monitor how a company's performance changed quarter-over-quarter.

```python
# Track Apple's gross margin over time
quarters = [
    ("Apple", "Q1", 2024),
    ("Apple", "Q2", 2024),
    ("Apple", "Q3", 2024),
    ("Apple", "Q4", 2024),
]

margins = []
for company, quarter, year in quarters:
    result = client.query(
        query="What is the gross margin percentage?",
        tags=["earnings", company.lower(), str(year)],
        limit=1
    )

    context = client.get_context_rail(result.query_id)
    if context.sources:
        margins.append({
            "period": f"{quarter} {year}",
            "margin": result.answer,
            "source": context.sources[0].document_title,
            "confidence": result.confidence_score
        })

# Print trend
print("Apple Gross Margin Trend:")
for m in margins:
    print(f"  {m['period']}: {m['margin']} (confidence: {m['confidence']:.0%})")
```

### Example 2: Guidance & Outlook Analysis

**Scenario**: Extract management's forward-looking statements to assess growth expectations.

```python
# Find guidance across different company segments
segments = {
    "Cloud": "What is the expected growth rate for cloud revenue?",
    "AI": "What investment is planned for artificial intelligence?",
    "Hardware": "What are the expected hardware demand trends?"
}

for segment, query in segments.items():
    result = client.query(
        query=query,
        tags=["earnings", "2024"],
        confidence_threshold=0.80
    )

    print(f"\n{segment} Outlook:")
    print(f"  {result.answer}")

    # Check if this is management guidance (high confidence) vs. analyst interpretation
    if result.confidence_score > 0.90:
        print(f"  ✓ Direct management guidance")
    else:
        print(f"  ? Implied or interpreted guidance")
```

### Example 3: Competitive Intelligence

**Scenario**: Identify how companies are positioning against each other.

```python
# What is each company saying about cloud competition?
competitors = {
    "AWS": ["Amazon"],
    "Azure": ["Microsoft"],
    "Google Cloud": ["Google"],
    "Apple Private Cloud": ["Apple"]
}

for platform, companies in competitors.items():
    # How does each competitor respond to this platform?
    for company in companies:
        result = client.query(
            query=f"How is {company} competing in the {platform} market space?",
            tags=["earnings", company.lower()],
            confidence_threshold=0.75
        )

        if result.sources:
            print(f"\n{company} on {platform}:")
            print(f"  {result.answer}")
```

### Example 4: Risk Heatmap

**Scenario**: Build a risk matrix across companies and categories.

```python
import pandas as pd

companies = ["Apple", "Google", "Microsoft", "Amazon"]
risk_categories = [
    "Regulatory",
    "Supply Chain",
    "Competitive",
    "Technology Obsolescence",
    "Talent Retention"
]

# Build risk matrix
risk_matrix = {}

for company in companies:
    risk_matrix[company] = {}

    for risk_type in risk_categories:
        result = client.query(
            query=f"What {risk_type.lower()} risks does the company face?",
            tags=["earnings", company.lower()],
            confidence_threshold=0.70
        )

        # Use confidence score as risk severity proxy
        # (high confidence = well-documented risk)
        risk_matrix[company][risk_type] = result.confidence_score

# Visualize as DataFrame
df = pd.DataFrame(risk_matrix).T
print(df.round(2))

# Identify high-risk areas
high_risks = (df > 0.85).sum()
print(f"\nHigh-risk categories: {high_risks[high_risks > 0].index.tolist()}")
```

---

## Advanced Features

### Trend Detection Across Quarters

```python
# Query the same metric across all quarters
trend = []

for quarter in ["Q1", "Q2", "Q3", "Q4"]:
    result = client.query(
        query="What percentage of revenue comes from services?",
        tags=["earnings", "apple", "2024", quarter.lower()]
    )

    if result.sources:
        trend.append({
            "quarter": quarter,
            "value": result.answer,
            "confidence": result.confidence_score
        })

# Identify trend direction
if len(trend) >= 2:
    print("Services Revenue % Trend Q1 → Q4:")
    for t in trend:
        print(f"  {t['quarter']}: {t['value']}")
```

### Materiality Assessment

Use confidence scores to identify material vs. immaterial items:

```python
# Query many financial items and rank by confidence
items = [
    "Revenue growth",
    "Geographic mix",
    "R&D spending",
    "Executive compensation",
    "Related-party transactions"
]

materiality = []

for item in items:
    result = client.query(
        query=f"What is the {item}?",
        tags=["earnings", company.lower()]
    )

    materiality.append({
        "item": item,
        "confidence": result.confidence_score,
        "likely_material": result.confidence_score > 0.85
    })

# Sort by confidence
for m in sorted(materiality, key=lambda x: x['confidence'], reverse=True):
    status = "Material" if m['likely_material'] else "Non-material"
    print(f"{m['item']:30} - {status} (confidence: {m['confidence']:.0%})")
```

---

## Privacy & Compliance

### Protecting Sensitive Data

- **Financial figures** are redacted before LLM processing
- **Guidance and projections** are marked as sensitive
- **Management insights** stay encrypted in your infrastructure
- Your analysis never exposes raw financials to vendors

### Audit Trail

Every query is logged:
- Which documents were searched
- What metrics were queried
- Who ran the analysis
- When results were reviewed

This satisfies compliance and audit requirements.

### Regulatory Alignment

Sens Prism helps with:
- **Regulation FD**: Ensure selective disclosure compliance
- **SOX Section 302**: Document review procedures
- **Dodd-Frank**: Risk and compensation analysis
- **GDPR** (if analyzing EU companies): Protect personal data of executives

---

## Best Practices

### 1. Use Consistent Naming & Tags

```python
# ✓ Good: Consistent naming with year and quarter
tags=["earnings", company.lower(), "10-q", str(year), quarter.lower()]

# ✗ Avoid: Inconsistent naming
tags=["financials", company, "report"]
```

### 2. Set Appropriate Confidence Thresholds

- **>0.90**: Core financial metrics (revenue, net income)
- **0.80-0.90**: Important metrics (margins, growth rates)
- **0.70-0.80**: Forward guidance and management commentary
- **<0.70**: Speculative analysis (use cautiously)

### 3. Always Check Context Rail

Don't rely on the answer alone:

```python
context = client.get_context_rail(result.query_id)

for source in context.sources:
    # Verify the metric is in the right section
    if "Management's Discussion" in source.document_title:
        print("✓ From MD&A section (reliable)")
    elif "Footnotes" in source.document_title:
        print("⚠️  From footnotes (may be non-recurring)")
```

### 4. Document Your Sources

Include Context Rail citations in your analysis:

```python
# Example for client report
analysis_summary = f"""
Revenue Growth Analysis:
{result.answer}

Sources:
{context.sources[0].document_title}, p. {context.sources[0].page}
{context.sources[1].document_title}, p. {context.sources[1].page}

Confidence: {result.confidence_score:.0%}
"""
```

### 5. Cross-Verify Key Metrics

For critical analysis, query from multiple angles:

```python
# Verify the same metric three ways
metric_queries = [
    "What was net revenue in Q1 2024?",  # Direct
    "Total sales revenue?",  # Alternative wording
    "How much did the company generate in revenue?"  # Natural language
]

results = []
for q in metric_queries:
    r = client.query(q, tags=["earnings", "apple", "q1", "2024"])
    results.append(r.answer)

# If all three agree, high confidence in the number
if all(r == results[0] for r in results):
    print("✓ Metric verified across multiple query formulations")
```

---

## Integration with Tools

### Excel / Google Sheets

Use the APIs to populate spreadsheets:

```python
# Query multiple metrics and populate a spreadsheet
import gspread

client = SensClient(api_key="sens_sk_...")

# Connect to Google Sheets
gc = gspread.oauth()
ws = gc.open("Financial Analysis").sheet1

row = 2
for company in ["Apple", "Google", "Microsoft"]:
    result = client.query(
        query="What was the net income?",
        tags=["earnings", company.lower(), "2024"]
    )

    ws.update_cell(row, 1, company)
    ws.update_cell(row, 2, result.answer)
    ws.update_cell(row, 3, result.confidence_score)
    row += 1
```

### Power BI / Tableau

Export query results for visualization:

```python
# Export as CSV for import into BI tools
import csv

results = []
for metric in ["Revenue", "Gross Margin %", "R&D Spend"]:
    r = client.query(query=f"What is {metric}?", tags=["earnings"])
    results.append({
        "Metric": metric,
        "Value": r.answer,
        "Confidence": r.confidence_score
    })

with open("financial_metrics.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["Metric", "Value", "Confidence"])
    writer.writeheader()
    writer.writerows(results)
```

---

## Getting Started

1. **Gather your financial documents** (earnings reports, 10-Ks, 10-Qs)
2. **Sign up** at [sens.ai](https://sens.ai)
3. **Upload 1-2 sample reports** and test queries
4. **Build your analysis queries** based on Context Rail feedback
5. **Integrate with your existing analysis tools**

For financial analysis questions, email [finance@sens.ai](mailto:finance@sens.ai).
