import json
import sys
from pathlib import Path

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai_module.nlp_pipeline import ReqLintEngine

def run_evaluation():
    engine = ReqLintEngine()
    dataset_path = Path(__file__).parent / "sample_dataset.json"
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print("=== ReqLint AI Engine Benchmark Evaluation ===")
    total = len(dataset)
    passed = 0

    for item in dataset:
        report = engine.audit_requirement(item["text"])
        detected_rule_ids = {s.rule_id for s in report.smells}
        expected_rule_ids = set(item["expected_smells"])

        is_match = expected_rule_ids.issubset(detected_rule_ids) if expected_rule_ids else len(detected_rule_ids) == 0
        status = "PASSED" if is_match else "FAILED"
        if is_match:
            passed += 1

        print(f"[{status}] ID #{item['id']} ({report.detected_language.value.upper()})")
        print(f"   Input: '{item['text']}'")
        print(f"   Detected Smells: {list(detected_rule_ids)}")
        print(f"   Quality Score: {report.scores.overall_quality_score}/100\n")

    print(f"Evaluation Complete: {passed}/{total} test cases passed ({passed/total*100:.1f}% Accuracy)")

if __name__ == "__main__":
    run_evaluation()
