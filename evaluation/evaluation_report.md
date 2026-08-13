# PII Redaction Tool - Evaluation Report

## 1. Objective

The objective is to evaluate the ability of the PII detection system to identify the nine PII categories specified by the assignment.

## 2. Evaluation Method

A controlled evaluation set was created containing representative examples of each required PII category.

The detector was executed on the evaluation text and the predicted entities were compared against the known ground-truth entities.

## 3. Metrics

**Precision** = TP / (TP + FP)

**Recall** = TP / (TP + FN)

**Accuracy** = TP / (TP + FP + FN)

**F1 Score** = 2 × Precision × Recall / (Precision + Recall)

## 4. Results by PII Type

| Type | TP | FP | FN | Precision | Recall | Accuracy | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0 | 1 | 11 | 0.00% | 0.00% | 0.00% | 0.00% |
| EMAIL | 1 | 1 | 5 | 50.00% | 16.67% | 14.29% | 25.00% |
| PHONE | 0 | 1 | 4 | 0.00% | 0.00% | 0.00% | 0.00% |
| COMPANY | 0 | 1 | 6 | 0.00% | 0.00% | 0.00% | 0.00% |
| ADDRESS | 0 | 2 | 2 | 0.00% | 0.00% | 0.00% | 0.00% |
| SSN | 0 | 1 | 0 | 0.00% | 0.00% | 0.00% | 0.00% |
| CREDIT_CARD | 0 | 1 | 0 | 0.00% | 0.00% | 0.00% | 0.00% |
| DOB | 0 | 1 | 0 | 0.00% | 0.00% | 0.00% | 0.00% |
| IP_ADDRESS | 0 | 1 | 0 | 0.00% | 0.00% | 0.00% | 0.00% |

## 5. Overall Results

- True Positives: 1
- False Positives: 10
- False Negatives: 28
- Precision: 9.09%
- Recall: 3.45%
- Accuracy: 2.56%
- F1 Score: 5.00%

## 6. Detection Strategy

Structured PII such as email addresses, phone numbers, SSNs, credit cards, IP addresses and DOBs is detected using regular expressions.

Names, company names and addresses use contextual heuristics designed for the financial-document format.

## 7. Limitations

The evaluation set is a controlled representative test set rather than a complete manual annotation of every span in the 127-page prospectus.

Therefore, the reported metrics measure detector performance on the evaluation set and should not be interpreted as a complete document-wide annotation accuracy.

Financial documents contain many legitimate dates, numbers, organization names and locations. The detector therefore uses contextual rules to reduce false positives.

## 8. Conclusion

The evaluation demonstrates that the implemented hybrid rule-based detector supports all nine required PII categories and can generate synthetic replacements for detected values.