from detectors import detect_pii


test_text = """
Contact Person: John Smith
Email: john.smith@example.com
Phone: +91 9876543210
Date of Birth: 15/08/1990
SSN: 123-45-6789
Credit Card: 4111 1111 1111 1111
IP Address: 192.168.1.25
Registered Office: 123 Example Road, Pune, Maharashtra, India 411001
ABC Technologies Limited
"""


entities = detect_pii(test_text)


print("=" * 60)
print("DETECTOR TEST")
print("=" * 60)

for entity in entities:

    print(
        f"{entity.label:<15} | "
        f"{entity.text}"
    )

print("=" * 60)
print(
    f"Total entities detected: {len(entities)}"
)