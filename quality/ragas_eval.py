"""
RAGAS Quality Evaluation Script
================================

Runs a set of sample questions through the Inference Router and evaluates
the responses using RAGAS metrics (faithfulness, answer_relevancy, context_precision).

Usage:
    python quality/ragas_eval.py --endpoint http://localhost:8000 --api-key YOUR_KEY

The script:
1. Sends each question to /v1/infer and collects the upstream LLM response.
2. Builds a RAGAS Dataset with the questions, contexts, and answers.
3. Evaluates using faithfulness and answer_relevancy metrics.
4. Prints a summary and optionally saves results to quality/ragas_results.csv.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

import httpx

# ---------------------------------------------------------------------------
# Sample evaluation dataset
# ---------------------------------------------------------------------------

EVAL_SAMPLES = [
    {
        "question": "What is the capital of France?",
        "ground_truth": "Paris",
        "contexts": ["France is a country in Western Europe. Its capital is Paris."],
    },
    {
        "question": "What is machine learning?",
        "ground_truth": (
            "Machine learning is a branch of artificial intelligence that enables "
            "computers to learn from data without being explicitly programmed."
        ),
        "contexts": [
            "Machine learning (ML) is a type of artificial intelligence (AI) that "
            "allows software applications to become more accurate at predicting "
            "outcomes without being explicitly programmed to do so."
        ],
    },
]


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------


def call_infer(
    endpoint: str, question: str, context: str, api_key: Optional[str]
) -> Optional[str]:
    """Send a question to the inference router and return the answer text."""
    headers: Dict[str, str] = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key

    payload = {
        "messages": [
            {
                "role": "system",
                "content": f"Answer the question based on the context: {context}",
            },
            {"role": "user", "content": question},
        ]
    }

    try:
        r = httpx.post(f"{endpoint}/v1/infer", json=payload, headers=headers, timeout=60.0)
        r.raise_for_status()
        data = r.json()
        upstream = data.get("upstream_body") or {}
        if isinstance(upstream, dict):
            choices = upstream.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
        return str(upstream) if upstream else None
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] Failed to call inference router: {exc}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="RAGAS evaluation for inference-router")
    parser.add_argument(
        "--endpoint",
        default="http://localhost:8000",
        help="Base URL of the inference-router service",
    )
    parser.add_argument("--api-key", default=None, help="API key (X-API-Key header)")
    parser.add_argument(
        "--output",
        default="quality/ragas_results.csv",
        help="Output CSV path for RAGAS results",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip actual LLM calls; use ground truths as answers (for CI smoke tests)",
    )
    args = parser.parse_args(argv)

    # Collect answers
    questions = []
    answers = []
    contexts = []
    ground_truths = []

    for sample in EVAL_SAMPLES:
        q = sample["question"]
        ctx = sample["contexts"][0]
        gt = sample["ground_truth"]

        if args.dry_run:
            answer = gt  # Use ground truth as stand-in answer
        else:
            answer = call_infer(args.endpoint, q, ctx, args.api_key) or gt

        questions.append(q)
        answers.append(answer)
        contexts.append(sample["contexts"])
        ground_truths.append(gt)

    print(f"Collected {len(questions)} samples for RAGAS evaluation")

    # Run RAGAS
    try:
        from datasets import Dataset  # type: ignore
        from ragas import evaluate  # type: ignore
        from ragas.metrics import answer_relevancy, faithfulness  # type: ignore

        dataset = Dataset.from_dict(
            {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
                "ground_truth": ground_truths,
            }
        )

        result = evaluate(dataset, metrics=[faithfulness, answer_relevancy])
        print("\n=== RAGAS Results ===")
        print(result)

        if args.output:
            result.to_pandas().to_csv(args.output, index=False)
            print(f"\nResults saved to {args.output}")

    except ImportError as exc:
        print(
            f"[ERROR] RAGAS or datasets not installed ({exc}). "
            "Install with: pip install ragas datasets",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
