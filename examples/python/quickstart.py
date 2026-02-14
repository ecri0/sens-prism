#!/usr/bin/env python3
"""
Sens Prism Python SDK Quickstart Example

This example demonstrates the basic workflow:
1. Initialize the client
2. Upload a document
3. Query the document
4. View results with Context Rail
"""

import os
import time
from sens import SensClient
from sens.exceptions import SensError


def main():
    """Run the Sens Prism quickstart example."""

    # Initialize client with API key from environment
    api_key = os.getenv("SENS_API_KEY")
    if not api_key:
        print("Error: SENS_API_KEY environment variable not set")
        print("Get your key from https://dashboard.sens.ai")
        return

    client = SensClient(api_key=api_key)
    print("✓ Initialized Sens Prism client")

    # Step 1: Upload a document
    # For this example, we'll create a simple test document
    test_file = "/tmp/test_document.txt"
    with open(test_file, "w") as f:
        f.write("""
        Sens Prism: Sovereign AI Gateway

        Sens Prism is a platform that sits between users and large language models,
        providing unprecedented transparency, control, and data ownership.

        Core Features:
        1. Distill: Extract meaning from documents using mechanistic interpretability
        2. Protect: Remove sensitive data before it reaches the LLM
        3. Inject: Add relevant context to prompts for better answers

        Pricing:
        - Free Plan: $0/month, 10 requests/min, 5 documents/day
        - Prism Plan: $29/month, 100 requests/min, 100 documents/day
        - Enterprise: Custom pricing and unlimited resources

        Data Sovereignty:
        Your documents are encrypted and never leave your control.
        We use a Smart Sanitizer to remove PII before any processing.
        """)

    print("\n--- Uploading Document ---")
    try:
        doc = client.upload_document(
            file_path=test_file,
            title="Sens Prism Overview",
            tags=["product", "documentation"]
        )
        print(f"✓ Document uploaded: {doc.id}")
        print(f"  Status: {doc.status}")
        print(f"  Created: {doc.created_at}")

    except SensError as e:
        print(f"✗ Upload failed: {e}")
        return

    # Step 2: Wait for document to be processed
    print("\n--- Waiting for Processing ---")
    max_wait = 60
    waited = 0
    while waited < max_wait:
        doc_status = client.get_document(doc.id)
        print(f"  Status: {doc_status.status}")

        if doc_status.status == "ready":
            print("✓ Document ready to query!")
            break
        elif doc_status.status == "failed":
            print("✗ Document processing failed")
            return
        else:
            time.sleep(2)
            waited += 2

    # Step 3: Query the document
    print("\n--- Querying Document ---")
    query_text = "What are the key features of Sens Prism?"

    try:
        result = client.query(
            query=query_text,
            document_ids=[doc.id],
            limit=3,
            confidence_threshold=0.70
        )

        print(f"Query: {query_text}")
        print(f"\nAnswer: {result.answer}")
        print(f"Confidence: {result.confidence_score:.0%}")
        print(f"Processing time: {result.processing_time_ms}ms")
        print(f"Sources found: {len(result.sources)}")

    except SensError as e:
        print(f"✗ Query failed: {e}")
        return

    # Step 4: Get Context Rail for detailed information
    print("\n--- Context Rail Details ---")
    try:
        context = client.get_context_rail(result.query_id)

        print(f"Retrieved sources: {len(context.sources)}")
        for i, source in enumerate(context.sources, 1):
            print(f"\nSource {i}:")
            print(f"  Document: {source.document_title}")
            if source.page:
                print(f"  Page: {source.page}")
            print(f"  Confidence: {source.confidence_score:.0%}")
            if source.semantic_layer:
                print(f"  Semantic Layer: {source.semantic_layer}")
            if source.matched_concepts:
                print(f"  Concepts: {', '.join(source.matched_concepts)}")
            if source.excerpt:
                print(f"  Excerpt: {source.excerpt[:100]}...")

    except SensError as e:
        print(f"✗ Context Rail retrieval failed: {e}")
        return

    # Step 5: Query with different questions
    print("\n--- Additional Queries ---")
    queries = [
        "How much does Prism cost?",
        "How does Sens Prism protect data?",
    ]

    for query_text in queries:
        try:
            result = client.query(query_text, document_ids=[doc.id])
            print(f"\nQ: {query_text}")
            print(f"A: {result.answer}")
            print(f"  Confidence: {result.confidence_score:.0%}")
        except SensError as e:
            print(f"✗ Query failed: {e}")

    # Cleanup
    print("\n--- Cleanup ---")
    try:
        client.delete_document(doc.id)
        print("✓ Document deleted")
    except SensError as e:
        print(f"✗ Delete failed: {e}")

    print("\n✓ Quickstart complete!")


if __name__ == "__main__":
    main()
