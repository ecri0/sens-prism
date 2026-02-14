# Academic Literature Review with Sens Prism

Conducting a literature review across 50+ papers is exhausting: reading, annotating, cross-referencing, and synthesizing ideas manually takes months. Sens Prism enables semantic searching and concept mapping across your entire research corpus.

## The Challenge

A doctoral candidate researching "AI interpretability in neural networks" needs to:
- Read 100+ papers across multiple subfields
- Track concepts across papers (mechanistic interpretability vs. feature attribution)
- Identify gaps and contradictions in the literature
- Build a coherent synthesis of different approaches
- Maintain proper citations for each claim

Manual review of 100 papers: 200+ hours
With Sens Prism: 20 hours of focused research

## Solution: Sens Prism Workflow

### Step 1: Upload Your Research Corpus

Build your knowledge base with all relevant papers:

```bash
# Create batch upload script
for pdf in papers/*.pdf; do
  curl -X POST https://api.sens.ai/v1/documents \
    -H "Authorization: Bearer sens_sk_..." \
    -F "file=@$pdf" \
    -F "title=$(basename $pdf .pdf)" \
    -F "tags=research,ai,interpretability"
done
```

Or programmatically:

```python
from sens import SensClient
import glob

client = SensClient(api_key="sens_sk_...")

for pdf_path in glob.glob("papers/*.pdf"):
    doc = client.upload_document(
        file_path=pdf_path,
        tags=["research", "ai", "interpretability"]
    )
    print(f"Uploaded: {doc.title}")
```

**Result**: 100 papers indexed and semantically processed in your Sens Prism account.

### Step 2: Map Core Concepts Across Papers

Instead of manually taking notes, query concepts across your corpus:

```python
# Find all papers discussing sparse autoencoders
concept_query = "What is a sparse autoencoder and how is it used for mechanistic interpretability?"
result = client.query(concept_query, tags=["research"])

print(f"Found in {len(result.sources)} papers:")
for source in result.sources:
    print(f"  - Page {source.page}: {source.document_title}")
```

Context Rail shows you:
- **Which papers** discuss this concept
- **How it's defined** in each paper (variations matter!)
- **Related concepts** (SAE features, basis decomposition, etc.)
- **Confidence scores** indicating how central this concept is

### Step 3: Track Methodology & Results

Find papers with similar or contrasting methodologies:

```python
# Find all papers using activation patching
methodology_query = """
What experimental methodology is used to test if neurons are causally responsible
for model behavior?
"""
result = client.query(methodology_query, tags=["research"])

context = client.get_context_rail(result.query_id)
for source in context.sources:
    print(f"\n{source.document_title}")
    print(f"  Method excerpt: {source.excerpt[:200]}...")
    print(f"  Semantic layer: {source.semantic_layer}")
```

The **5-layer semantic model** helps you find:
- **L1 Chunk**: Exact methodological descriptions
- **L2 Concept**: Related method categories
- **L3 Context**: How this method relates to your research
- **L4 Pragmatic**: What the method enables or proves
- **L5 Universal**: Method independent of paper's LLM

### Step 4: Cross-Reference Claims & Results

Identify agreement and disagreement across papers:

```python
# Query for contradictory findings
contradiction_query = """
Do neural networks in this domain generalize to distribution shifts,
or do they fail out-of-distribution?
"""
result = client.query(contradiction_query, tags=["research"])

context = client.get_context_rail(result.query_id)

# Group by confidence: high-confidence claims vs. nuanced ones
high_confidence = [s for s in context.sources if s.confidence_score > 0.90]
nuanced = [s for s in context.sources if 0.70 < s.confidence_score <= 0.90]

print(f"Strong consensus ({len(high_confidence)} papers): {result.answer}")
print(f"Nuanced views ({len(nuanced)} papers):")
for source in nuanced[:3]:
    print(f"  - {source.document_title}: {source.excerpt[:100]}...")
```

### Step 5: Build Your Literature Map

Export citation data for writing your review:

```python
from datetime import datetime

# Query all papers on a topic
result = client.query(
    "What are the main approaches to mechanistic interpretability?",
    limit=20  # Get many sources for comprehensive map
)

context = client.get_context_rail(result.query_id)

# Create citation data
citations = []
for source in context.sources:
    citations.append({
        "paper": source.document_title,
        "page": source.page,
        "excerpt": source.excerpt,
        "confidence": source.confidence_score,
        "concept": source.matched_concepts,
        "layer": source.semantic_layer
    })

# Export to CSV for your writing process
import csv
with open("citations.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=citations[0].keys())
    writer.writeheader()
    writer.writerows(citations)

print(f"Exported {len(citations)} citations")
```

---

## Use Case Examples

### Example 1: Finding the Research Gap

**Scenario**: You want to identify what's NOT well-studied to find your dissertation topic.

```python
# Query what IS well-studied
studied = client.query(
    "How do we interpret the internal representations of large language models?",
    tags=["research"]
)
print(f"Well-studied: {len(studied.sources)} papers on LLM interpretation")

# Query what's emerging but less explored
emerging = client.query(
    "How do we identify causally relevant features in vision transformers?",
    tags=["research"],
    confidence_threshold=0.60  # Lower threshold shows emerging/uncertain areas
)
print(f"Emerging: {len(emerging.sources)} papers on vision transformer causality")

if len(studied.sources) > len(emerging.sources) * 3:
    print("↑ Vision transformer causality is underexplored relative to LLM interpretation")
```

### Example 2: Comparative Methodology Review

**Scenario**: Compare how different labs approach the same problem.

```python
# Compare sparse autoencoder approaches
labs = {
    "DeepMind": ["paper1.pdf", "paper2.pdf"],
    "Anthropic": ["paper3.pdf", "paper4.pdf"],
    "Other": ["paper5.pdf", "paper6.pdf"]
}

for lab, doc_ids in labs.items():
    result = client.query(
        "What training objective is used for the sparse autoencoder?",
        document_ids=doc_ids
    )
    print(f"\n{lab}:")
    print(f"  Answer: {result.answer}")
    print(f"  Confidence: {result.confidence_score:.0%}")
    print(f"  Sources: {len(result.sources)}")
```

### Example 3: Timeline of Concept Evolution

**Scenario**: Understand how a concept evolved across papers published over time.

```python
# Group papers by year
import re

papers_by_year = {}
for pdf in glob.glob("papers/*.pdf"):
    # Extract year from filename (e.g., "Smith_2021_SAE.pdf")
    match = re.search(r'_(\d{4})_', pdf)
    if match:
        year = match.group(1)
        if year not in papers_by_year:
            papers_by_year[year] = []
        papers_by_year[year].append(pdf)

# Track concept evolution
for year in sorted(papers_by_year.keys()):
    result = client.query(
        "What is the definition and role of polysemanticity in neural networks?",
        document_ids=[os.path.basename(p).replace('.pdf', '')
                      for p in papers_by_year[year]]
    )
    print(f"\n{year}: {result.answer[:150]}...")
    print(f"  Confidence: {result.confidence_score:.0%}")
```

### Example 4: Building Your Literature Synthesis

**Scenario**: Create a comprehensive literature map for your introduction section.

```python
# Identify major themes
themes = [
    "What is mechanistic interpretability?",
    "What are the main approaches (circuit analysis, feature attribution, SAE)?",
    "What are key case studies / empirical results?",
    "What are limitations of current approaches?",
    "What are open problems?"
]

synthesis = {}
for theme in themes:
    result = client.query(theme, tags=["research"], limit=10)
    context = client.get_context_rail(result.query_id)

    synthesis[theme] = {
        "overview": result.answer,
        "key_papers": [s.document_title for s in context.sources[:5]],
        "citations": [
            {
                "paper": s.document_title,
                "page": s.page,
                "excerpt": s.excerpt
            }
            for s in context.sources
        ]
    }

# Use this structure to write your literature review
print("Your literature map is ready for writing!")
```

---

## Advanced Features

### Citation Network Mapping

Use the Context Rail's **concept connections** to build a citation graph:

```python
# Find papers on concept A
result_a = client.query("sparse autoencoders", limit=5)

# Find papers on concept B
result_b = client.query("monosemanticity", limit=5)

# Papers discussing both are likely important bridges
common_papers = set(s.document_id for s in result_a.sources) & \
                set(s.document_id for s in result_b.sources)

if common_papers:
    print(f"Bridge papers: {[p.document_title for p in common_papers]}")
```

### Confidence as Relevance

The semantic layers' confidence scores tell you:
- **>0.95**: Core concept, clearly defined, widely cited
- **0.85-0.95**: Well-established but may have nuances
- **0.70-0.85**: Relevant but emerging or disputed
- **<0.70**: Tangential or speculative

Use this to organize your review by consensus level.

### Exporting for Writing

```python
# Create a markdown file with citations and excerpts
with open("literature_review.md", "w") as f:
    f.write("# Literature Review on Mechanistic Interpretability\n\n")

    for theme, data in synthesis.items():
        f.write(f"## {theme}\n\n")
        f.write(f"{data['overview']}\n\n")
        f.write("### Key Sources\n\n")

        for citation in data['citations'][:5]:
            f.write(f"- **{citation['paper']}** (p. {citation['page']})\n")
            f.write(f"  > {citation['excerpt']}\n\n")
```

---

## Best Practices

### 1. Use High-Quality Papers

Sens Prism works best with:
- Peer-reviewed papers (arXiv, conferences, journals)
- High-quality technical books
- Position papers from recognized researchers

Avoid:
- Preprints that may have errors
- Marketing materials masquerading as research
- Conflicting versions of the same paper (keep only latest)

### 2. Organize with Tags

Add meaningful tags during upload:

```python
client.upload_document(
    "Anthropic_Circuits_Nature_2024.pdf",
    tags=["circuit-analysis", "mechanistic-interpretability", "anthropic", "2024"]
)
```

Then query by tag to narrow scope:
```python
result = client.query(
    "What is mechanistic interpretability?",
    tags=["mechanistic-interpretability"]
)
```

### 3. Check Context Rail Always

The confidence score and semantic layer tell you:
- **How reliable** is this claim (confidence)?
- **What type of information** is this (layer)?
- **Where exactly** does it say this (page)?

Don't just copy the answer—verify it in Context Rail.

### 4. Track Your Queries

Save queries and results for reproducibility:

```python
import json
from datetime import datetime

query_log = []

for query_text in my_queries:
    result = client.query(query_text)
    query_log.append({
        "timestamp": datetime.now().isoformat(),
        "query": query_text,
        "answer": result.answer,
        "confidence": result.confidence_score,
        "papers_cited": len(result.sources)
    })

with open("query_log.json", "w") as f:
    json.dump(query_log, f, indent=2)
```

Your advisor can review how you found your sources.

### 5. Iterate & Refine

Your first query might not be perfect:

```python
# Broad query
result1 = client.query("What is mechanistic interpretability?")
# Answer: General overview, might be too broad

# Refined query
result2 = client.query(
    "What mechanistic interpretability techniques are used to study transformer attention heads?"
)
# Answer: More specific, better targeted results
```

Use the answers to refine your follow-up questions.

---

## Integration with Writing Tools

### Zotero / Mendeley

Export your Context Rail citations as bibtex:

```python
# Generate bibtex from query results
context = client.get_context_rail(query_id)
for source in context.sources:
    # Parse the paper title and year
    bibtex = f"""@article{{{source.document_id},
  title={{{source.document_title}}},
  year={{YEAR}},
  url={{https://notes.your-domain.com/{source.document_id}}}
}}"""
    print(bibtex)
```

### Obsidian / Notion

Create a literature note for each paper with Context Rail excerpts:

```markdown
# {Paper Title}

**Key Concepts**: {matched_concepts from Context Rail}

**Relevance to My Research**: {from pragmatic layer}

**Key Excerpts**:
> {excerpt from Context Rail}
> (p. {page})

**Related Papers**: {from concept connections}
```

---

## Getting Started

1. **Gather your papers** in a folder
2. **Sign up** at [sens.ai](https://sens.ai)
3. **Upload your corpus** (100 papers takes ~10 minutes)
4. **Start with broad queries** to understand your corpus
5. **Refine queries** based on Context Rail results
6. **Export citations** for your literature review

For research-specific questions, email [research@sens.ai](mailto:research@sens.ai).
