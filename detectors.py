import re
from dataclasses import dataclass
from typing import List


@dataclass
class Entity:
    text: str
    label: str
    start: int
    end: int


# ============================================================
# REGEX PATTERNS
# ============================================================

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

# Indian +91 numbers and common international formats
PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\+?\s*91[\s.-]?)?"
    r"(?:[6-9]\d{9}|\d{2,4}[\s.-]\d{6,8})"
    r"(?!\d)"
)

SSN_PATTERN = re.compile(
    r"\b\d{3}-\d{2}-\d{4}\b"
)

CREDIT_CARD_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\d[ -]?){13,19}"
    r"(?!\d)"
)

IP_PATTERN = re.compile(
    r"\b(?:"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\."
    r"){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)"
    r"\b"
)

# Dates only when explicitly associated with DOB
DOB_PATTERN = re.compile(
    r"\b(?:date\s+of\s+birth|dob|birth\s+date)"
    r"\s*[:\-]?\s*"
    r"(?:"
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|"
    r"\d{1,2}\s+(?:Jan|January|Feb|February|Mar|March|Apr|April|"
    r"May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|"
    r"Nov|November|Dec|December)\s+\d{4}"
    r")",
    re.IGNORECASE
)


# ============================================================
# ADDRESS PATTERNS
# ============================================================

ADDRESS_LABEL_PATTERN = re.compile(
    r"\b(?:"
    r"registered\s+office|"
    r"corporate\s+office|"
    r"registered\s+address|"
    r"corporate\s+address|"
    r"mailing\s+address|"
    r"residential\s+address|"
    r"physical\s+address"
    r")"
    r"\s*(?:at|is|:|-)?\s*"
    r".*?"
    r"(?:\b\d{6}\b|\b\d{5}(?:-\d{4})?\b)"
    r"(?:,\s*[^.;\n]+)?",
    re.IGNORECASE
)

ADDRESS_AT_PATTERN = re.compile(
    r"\b(?:registered\s+office|corporate\s+office)"
    r"\s+(?:at|is)\s+"
    r".*?"
    r"\b\d{6}\b"
    r"(?:,\s*India)?",
    re.IGNORECASE
)


# ============================================================
# COMPANY / ORGANIZATION PATTERNS
# ============================================================

COMPANY_PATTERN = re.compile(
    r"\b"
    r"(?:"
    r"[A-Z][A-Za-z&.-]*(?:\s+[A-Z][A-Za-z&.-]*){0,8}"
    r"\s+"
    r"(?:"
    r"Limited|Ltd\.?|Private Limited|Pvt\.?\s*Ltd\.?|"
    r"LLP|Corporation|Inc\.?|Industries|Technologies|"
    r"Bank|Trust|Foundation|Association"
    r")"
    r")\b"
)


# ============================================================
# NAME PATTERNS
# ============================================================

# Names following strong contextual indicators.
CONTEXT_NAME_PATTERN = re.compile(
    r"\b(?:"
    r"Contact\s+Person|"
    r"Contact\s+Name|"
    r"Name\s+of\s+(?:the\s+)?Contact\s+Person|"
    r"Chairman\s+and\s+Executive\s+Director|"
    r"Chief\s+Executive\s+Officer|"
    r"Chief\s+Financial\s+Officer|"
    r"Company\s+Secretary|"
    r"Managing\s+Director|"
    r"Joint\s+Managing\s+Director|"
    r"Whole[-\s]time\s+Director|"
    r"Executive\s+Director|"
    r"Non[-\s]Executive\s+Director"
    r")"
    r"\s*(?:is|:|-)?\s*"
    r"([A-Z][A-Za-z'-]+(?:\s+[A-Z][A-Za-z'-]+){1,4})"
)


# Generic title-case human name.
# A stop-word list is applied later to reduce false positives.
GENERIC_NAME_PATTERN = re.compile(
    r"\b"
    r"[A-Z][a-z]{2,}"
    r"(?:\s+[A-Z][a-z]{2,}){1,3}"
    r"\b"
)


NAME_STOPWORDS = {
    "Red Herring Prospectus",
    "Book Built Offer",
    "Book Running Lead",
    "Lead Managers",
    "Running Lead Managers",
    "Offer Document",
    "Offer Price",
    "Fresh Issue",
    "Offer Sale",
    "Equity Shares",
    "Face Value",
    "Financial Statements",
    "General Information",
    "Risk Factors",
    "Corporate Governance",
    "Key Managerial Personnel",
    "Board Directors",
    "Companies Act",
    "Securities Exchange",
    "Stock Exchanges",
    "National Stock",
    "Registered Office",
    "Corporate Office",
    "India Limited",
}


# ============================================================
# DETECTION HELPERS
# ============================================================

def add_entity(
    entities: List[Entity],
    text: str,
    label: str,
    start: int,
    end: int
):
    if not text.strip():
        return

    entities.append(
        Entity(
            text=text,
            label=label,
            start=start,
            end=end
        )
    )


def detect_regex_entities(text: str) -> List[Entity]:
    entities = []

    patterns = [
        ("EMAIL", EMAIL_PATTERN),
        ("PHONE", PHONE_PATTERN),
        ("SSN", SSN_PATTERN),
        ("CREDIT_CARD", CREDIT_CARD_PATTERN),
        ("IP_ADDRESS", IP_PATTERN),
        ("DOB", DOB_PATTERN),
    ]

    for label, pattern in patterns:
        for match in pattern.finditer(text):
            value = match.group()

            # Avoid treating ordinary short numeric values as phones.
            if label == "PHONE":
                digits = re.sub(r"\D", "", value)

                if len(digits) < 10:
                    continue

                # Avoid obvious financial values with too many digits.
                if len(digits) > 15:
                    continue

            add_entity(
                entities,
                value,
                label,
                match.start(),
                match.end()
            )

    return entities


def detect_addresses(text: str) -> List[Entity]:
    """
    Detect physical/mailing addresses.

    The prospectus frequently labels addresses as:
    - Registered Office
    - Corporate Office
    - Registered Address
    - Corporate Address
    - Mailing Address

    We use the label as strong contextual evidence and then
    capture the address until a reasonable terminating boundary.
    """

    entities = []

    # --------------------------------------------------------
    # 1. Registered / Corporate Office
    # --------------------------------------------------------

    office_pattern = re.compile(
        r"\b(?:"
        r"Registered\s+Office|"
        r"Corporate\s+Office|"
        r"Registered\s+Address|"
        r"Corporate\s+Address|"
        r"Mailing\s+Address|"
        r"Physical\s+Address"
        r")"
        r"\s*"
        r"[:\-]?"
        r"\s*"
        r"(.{10,500}?"
        r"(?:"
        r"\b\d{6}\b"
        r"|"
        r"\b\d{5}(?:-\d{4})?\b"
        r"))",
        re.IGNORECASE
    )

    for match in office_pattern.finditer(text):

        full_text = match.group(0).strip()

        # Avoid extremely long accidental captures.
        if len(full_text) > 600:
            continue

        add_entity(
            entities,
            full_text,
            "ADDRESS",
            match.start(),
            match.end()
        )

    # --------------------------------------------------------
    # 2. Indian PIN-code based addresses
    # --------------------------------------------------------

    pin_pattern = re.compile(
        r"(?<!\d)"
        r"("
        r"(?:"
        r"(?:Flat|Plot|Shop|Office|Unit|No\.?|"
        r"Floor|Building|Tower|House|Survey\s+No\.?)"
        r"\s*)?"
        r"\d+[A-Za-z]?"
        r"(?:[\/-]\d+[A-Za-z]?)?"
        r"(?:,\s*|\s+)"
        r"(?:"
        r"[^,\n;]{2,80}"
        r"(?:,\s*|\s+)"
        r"){1,5}"
        r"(?:"
        r"Pune|Mumbai|Delhi|Bangalore|Bengaluru|"
        r"Hyderabad|Kolkata|Chennai|Ahmedabad|"
        r"Thane|Nashik|Maharashtra|Karnataka|"
        r"West Bengal|Gujarat|Tamil Nadu|"
        r"India"
        r")"
        r"[^;\n]{0,120}"
        r"\b\d{6}\b"
        r")",
        re.IGNORECASE
    )

    for match in pin_pattern.finditer(text):

        value = match.group(1).strip()

        if len(value) < 20:
            continue

        add_entity(
            entities,
            value,
            "ADDRESS",
            match.start(1),
            match.end(1)
        )

    return entities


def detect_companies(text: str) -> List[Entity]:
    entities = []

    for match in COMPANY_PATTERN.finditer(text):
        value = match.group().strip()

        if len(value) < 4:
            continue

        add_entity(
            entities,
            value,
            "COMPANY",
            match.start(),
            match.end()
        )

    return entities


def detect_contextual_names(text: str) -> List[Entity]:
    entities = []

    for match in CONTEXT_NAME_PATTERN.finditer(text):
        # Group 1 is the actual name.
        name = match.group(1)

        start = match.start(1)
        end = match.end(1)

        # Trim punctuation-like trailing fragments.
        name = name.strip(" ,.;:")

        if len(name.split()) < 2:
            continue

        add_entity(
            entities,
            name,
            "PERSON",
            start,
            end
        )

    return entities


def detect_generic_names(text: str) -> List[Entity]:
    entities = []

    for match in GENERIC_NAME_PATTERN.finditer(text):
        value = match.group().strip()

        if value in NAME_STOPWORDS:
            continue

        words = value.split()

        # Names normally have 2-4 words.
        if not 2 <= len(words) <= 4:
            continue

        # Skip if it looks like a heading.
        if value.isupper():
            continue

        # Skip phrases containing obvious non-person words.
        bad_words = {
            "Company",
            "Limited",
            "Private",
            "Office",
            "Director",
            "Manager",
            "Management",
            "Statement",
            "Committee",
            "Shares",
            "Investor",
            "Offer",
            "Price",
            "Report",
            "India",
            "Maharashtra",
            "Pune",
            "Mumbai",
            "December",
            "January",
            "February",
            "March",
            "April",
            "August",
            "September",
            "October",
            "November",
        }

        if any(word in bad_words for word in words):
            continue

        add_entity(
            entities,
            value,
            "PERSON",
            match.start(),
            match.end()
        )

    return entities


# ============================================================
# OVERLAP HANDLING
# ============================================================

PRIORITY = {
    "EMAIL": 100,
    "PHONE": 95,
    "SSN": 95,
    "CREDIT_CARD": 95,
    "IP_ADDRESS": 90,
    "DOB": 90,
    "ADDRESS": 85,
    "COMPANY": 80,
    "PERSON": 70,
}


def resolve_overlaps(entities: List[Entity]) -> List[Entity]:
    """
    Keep the strongest non-overlapping entities.
    """

    if not entities:
        return []

    # Higher priority first; for equal priority, longer entity first.
    sorted_entities = sorted(
        entities,
        key=lambda e: (
            -PRIORITY.get(e.label, 0),
            -(e.end - e.start),
            e.start
        )
    )

    selected = []

    for entity in sorted_entities:
        overlaps = False

        for existing in selected:
            if not (
                entity.end <= existing.start
                or entity.start >= existing.end
            ):
                overlaps = True
                break

        if not overlaps:
            selected.append(entity)

    return sorted(selected, key=lambda e: e.start)


def detect_pii(text: str) -> List[Entity]:
    """
    Detect supported PII types.

    Person detection intentionally uses contextual patterns only.
    Generic capitalized-phrase detection is disabled because
    financial prospectuses contain many capitalized headings,
    organization names, legal terms and geographical names that
    are not people.
    """

    entities = []

    # Structured PII
    entities.extend(
        detect_regex_entities(text)
    )

    # Physical addresses
    entities.extend(
        detect_addresses(text)
    )

    # Organizations / companies
    entities.extend(
        detect_companies(text)
    )

    # People only when strong contextual evidence exists
    entities.extend(
        detect_contextual_names(text)
    )

    # IMPORTANT:
    # Do NOT call detect_generic_names().
    #
    # A financial prospectus contains thousands of normal
    # capitalized phrases which would otherwise be incorrectly
    # classified as person names.

    return resolve_overlaps(entities)