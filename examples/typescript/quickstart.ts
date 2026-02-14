/**
 * Sens Prism TypeScript SDK Quickstart Example
 *
 * This example demonstrates the basic workflow:
 * 1. Initialize the client
 * 2. Upload a document
 * 3. Query the document
 * 4. View results with Context Rail
 */

import * as fs from "fs";
import * as path from "path";
import { SensClient } from "../../sdk/typescript/src/index";
import { SensError } from "../../sdk/typescript/src/exceptions";

async function main() {
  // Initialize client with API key from environment
  const apiKey = process.env.SENS_API_KEY;
  if (!apiKey) {
    console.error("Error: SENS_API_KEY environment variable not set");
    console.error("Get your key from https://dashboard.sens.ai");
    return;
  }

  const client = new SensClient({ apiKey });
  console.log("✓ Initialized Sens Prism client");

  // Step 1: Create and upload a document
  const testFile = "/tmp/test_document.txt";
  const testContent = `
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
`;

  fs.writeFileSync(testFile, testContent);

  console.log("\n--- Uploading Document ---");
  try {
    const doc = await client.uploadDocument(testFile, {
      title: "Sens Prism Overview",
      tags: ["product", "documentation"],
    });

    console.log(`✓ Document uploaded: ${doc.id}`);
    console.log(`  Status: ${doc.status}`);
    console.log(`  Created: ${doc.createdAt}`);

    // Step 2: Wait for document to be processed
    console.log("\n--- Waiting for Processing ---");
    let maxWait = 60;
    let waited = 0;

    while (waited < maxWait) {
      const docStatus = await client.getDocument(doc.id);
      console.log(`  Status: ${docStatus.status}`);

      if (docStatus.status === "ready") {
        console.log("✓ Document ready to query!");
        break;
      } else if (docStatus.status === "failed") {
        console.log("✗ Document processing failed");
        return;
      } else {
        await new Promise((resolve) => setTimeout(resolve, 2000));
        waited += 2;
      }
    }

    // Step 3: Query the document
    console.log("\n--- Querying Document ---");
    const queryText = "What are the key features of Sens Prism?";

    const result = await client.query(queryText, {
      documentIds: [doc.id],
      limit: 3,
      confidenceThreshold: 0.7,
    });

    console.log(`Query: ${queryText}`);
    console.log(`\nAnswer: ${result.answer}`);
    console.log(
      `Confidence: ${(result.confidenceScore * 100).toFixed(0)}%`
    );
    console.log(`Processing time: ${result.processingTimeMs}ms`);
    console.log(`Sources found: ${result.sources.length}`);

    // Step 4: Get Context Rail for detailed information
    console.log("\n--- Context Rail Details ---");
    const context = await client.getContextRail(result.queryId);

    console.log(`Retrieved sources: ${context.sources.length}`);
    context.sources.forEach((source, i) => {
      console.log(`\nSource ${i + 1}:`);
      console.log(`  Document: ${source.documentTitle}`);
      if (source.page) {
        console.log(`  Page: ${source.page}`);
      }
      console.log(
        `  Confidence: ${(source.confidenceScore ?? 0) * 100).toFixed(0)}%`
      );
      if (source.semanticLayer) {
        console.log(`  Semantic Layer: ${source.semanticLayer}`);
      }
      if (source.matchedConcepts) {
        console.log(`  Concepts: ${source.matchedConcepts.join(", ")}`);
      }
      if (source.excerpt) {
        console.log(`  Excerpt: ${source.excerpt.substring(0, 100)}...`);
      }
    });

    // Step 5: Query with different questions
    console.log("\n--- Additional Queries ---");
    const queries = [
      "How much does Prism cost?",
      "How does Sens Prism protect data?",
    ];

    for (const query of queries) {
      const result = await client.query(query, { documentIds: [doc.id] });
      console.log(`\nQ: ${query}`);
      console.log(`A: ${result.answer}`);
      console.log(
        `  Confidence: ${(result.confidenceScore * 100).toFixed(0)}%`
      );
    }

    // Cleanup
    console.log("\n--- Cleanup ---");
    await client.deleteDocument(doc.id);
    console.log("✓ Document deleted");

    // Clean up test file
    fs.unlinkSync(testFile);

    console.log("\n✓ Quickstart complete!");
  } catch (error) {
    if (error instanceof SensError) {
      console.error(`✗ Error: ${error}`);
    } else {
      console.error(`✗ Unexpected error:`, error);
    }
  }
}

main();
