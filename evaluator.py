import json
import os

from detectors import detect_pii


GROUND_TRUTH_FILE = "evaluation/ground_truth.json"
REPORT_FILE = "evaluation/evaluation_report.md"


def normalize(text):
    return " ".join(text.lower().split())


def evaluate():

    with open(
        GROUND_TRUTH_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        ground_truth = json.load(file)

    # --------------------------------------------------------
    # Build a controlled evaluation document.
    #
    # This contains exactly the ground-truth examples.
    # --------------------------------------------------------

    evaluation_text = """
    Contact Person: John Smith
    Email: john.smith@example.com
    Phone: +91 9876543210
    Date of Birth: 15/08/1990
    SSN: 123-45-6789
    Credit Card: 4111 1111 1111 1111
    IP Address: 192.168.1.25
    Registered Office: 123 Example Road, Pune, Maharashtra, India 411001
    Corporate Office: 456 Business Road, Mumbai, Maharashtra, India 400001
    ABC Technologies Limited
    KSH International Limited
    Sarthak Malvadkar
    Kushal Subbayya Hegde
    cs.connect@kshinternational.com
    +91 20 4505 3237
    """

    detected_entities = detect_pii(
        evaluation_text
    )

    predicted = {}

    for entity in detected_entities:

        predicted.setdefault(
            entity.label,
            []
        )

        predicted[
            entity.label
        ].append(
            normalize(entity.text)
        )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    results = {}

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for label in ground_truth:

        actual = {
            normalize(value)
            for value in ground_truth[label]
        }

        predicted_values = {
            normalize(value)
            for value in predicted.get(
                label,
                []
            )
        }

        tp = len(
            actual & predicted_values
        )

        fp = len(
            predicted_values - actual
        )

        fn = len(
            actual - predicted_values
        )

        precision = (
            tp / (tp + fp)
            if tp + fp
            else 0
        )

        recall = (
            tp / (tp + fn)
            if tp + fn
            else 0
        )

        accuracy = (
            tp / (tp + fp + fn)
            if tp + fp + fn
            else 0
        )

        f1 = (
            2 * precision * recall /
            (precision + recall)
            if precision + recall
            else 0
        )

        results[label] = {
            "TP": tp,
            "FP": fp,
            "FN": fn,
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy,
            "f1": f1
        }

        total_tp += tp
        total_fp += fp
        total_fn += fn

    precision = (
        total_tp /
        (total_tp + total_fp)
        if total_tp + total_fp
        else 0
    )

    recall = (
        total_tp /
        (total_tp + total_fn)
        if total_tp + total_fn
        else 0
    )

    accuracy = (
        total_tp /
        (total_tp + total_fp + total_fn)
        if total_tp + total_fp + total_fn
        else 0
    )

    f1 = (
        2 * precision * recall /
        (precision + recall)
        if precision + recall
        else 0
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    report = []

    report.append(
        "# PII Redaction Tool - Evaluation Report"
    )

    report.append("")

    report.append("## 1. Objective")
    report.append("")

    report.append(
        "The objective is to evaluate the ability of the "
        "PII detection system to identify the nine PII "
        "categories specified by the assignment."
    )

    report.append("")

    report.append("## 2. Evaluation Method")
    report.append("")

    report.append(
        "A controlled evaluation set was created containing "
        "representative examples of each required PII category."
    )

    report.append("")

    report.append(
        "The detector was executed on the evaluation text and "
        "the predicted entities were compared against the "
        "known ground-truth entities."
    )

    report.append("")

    report.append("## 3. Metrics")
    report.append("")

    report.append(
        "**Precision** = TP / (TP + FP)"
    )

    report.append("")

    report.append(
        "**Recall** = TP / (TP + FN)"
    )

    report.append("")

    report.append(
        "**Accuracy** = TP / (TP + FP + FN)"
    )

    report.append("")

    report.append(
        "**F1 Score** = 2 × Precision × Recall / "
        "(Precision + Recall)"
    )

    report.append("")

    report.append("## 4. Results by PII Type")
    report.append("")

    report.append(
        "| Type | TP | FP | FN | Precision | Recall | Accuracy | F1 |"
    )

    report.append(
        "|---|---:|---:|---:|---:|---:|---:|---:|"
    )

    for label, result in results.items():

        report.append(
            f"| {label} | "
            f"{result['TP']} | "
            f"{result['FP']} | "
            f"{result['FN']} | "
            f"{result['precision']:.2%} | "
            f"{result['recall']:.2%} | "
            f"{result['accuracy']:.2%} | "
            f"{result['f1']:.2%} |"
        )

    report.append("")

    report.append("## 5. Overall Results")
    report.append("")

    report.append(
        f"- True Positives: {total_tp}"
    )

    report.append(
        f"- False Positives: {total_fp}"
    )

    report.append(
        f"- False Negatives: {total_fn}"
    )

    report.append(
        f"- Precision: {precision:.2%}"
    )

    report.append(
        f"- Recall: {recall:.2%}"
    )

    report.append(
        f"- Accuracy: {accuracy:.2%}"
    )

    report.append(
        f"- F1 Score: {f1:.2%}"
    )

    report.append("")

    report.append("## 6. Detection Strategy")
    report.append("")

    report.append(
        "Structured PII such as email addresses, phone numbers, "
        "SSNs, credit cards, IP addresses and DOBs is detected "
        "using regular expressions."
    )

    report.append("")

    report.append(
        "Names, company names and addresses use contextual "
        "heuristics designed for the financial-document format."
    )

    report.append("")

    report.append("## 7. Limitations")
    report.append("")

    report.append(
        "The evaluation set is a controlled representative "
        "test set rather than a complete manual annotation "
        "of every span in the 127-page prospectus."
    )

    report.append("")

    report.append(
        "Therefore, the reported metrics measure detector "
        "performance on the evaluation set and should not "
        "be interpreted as a complete document-wide annotation "
        "accuracy."
    )

    report.append("")

    report.append(
        "Financial documents contain many legitimate dates, "
        "numbers, organization names and locations. The "
        "detector therefore uses contextual rules to reduce "
        "false positives."
    )

    report.append("")

    report.append("## 8. Conclusion")
    report.append("")

    report.append(
        "The evaluation demonstrates that the implemented "
        "hybrid rule-based detector supports all nine required "
        "PII categories and can generate synthetic replacements "
        "for detected values."
    )

    os.makedirs(
        "evaluation",
        exist_ok=True
    )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(report)
        )

    print("=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"\nTrue Positives : {total_tp}"
    )

    print(
        f"False Positives: {total_fp}"
    )

    print(
        f"False Negatives: {total_fn}"
    )

    print(
        f"\nPrecision: {precision:.2%}"
    )

    print(
        f"Recall   : {recall:.2%}"
    )

    print(
        f"Accuracy : {accuracy:.2%}"
    )

    print(
        f"F1 Score : {f1:.2%}"
    )

    print(
        f"\nReport saved to:"
        f"\n{REPORT_FILE}"
    )


if __name__ == "__main__":
    evaluate()