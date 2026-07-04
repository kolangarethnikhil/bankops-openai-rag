"""Synthetic Indian banking operations KB derived from public regulatory facts."""

from copy import deepcopy


RBI_UNAUTHORIZED_URL = "https://www.rbi.org.in/commonman/English/Scripts/Notification.aspx?Id=2336"
RBI_KYC_URL = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566"


KB_ITEMS = [
    {
        "id": "RBI-UT-001",
        "title": "Unauthorized Electronic Transaction Reporting",
        "risk": "High",
        "tags": ["unauthorized", "fraud", "upi", "card", "sms", "reporting", "complaint"],
        "source_url": RBI_UNAUTHORIZED_URL,
        "source_note": "RBI customer protection circular, reporting of unauthorized electronic banking transactions.",
        "text": (
            "When a customer reports an unauthorized electronic banking transaction, the bank must provide 24x7 "
            "reporting channels, acknowledge the complaint, record the date and time of the customer response, and "
            "take immediate steps to prevent further unauthorized transactions."
        ),
    },
    {
        "id": "RBI-UT-002",
        "title": "Customer Liability Timeline",
        "risk": "High",
        "tags": ["liability", "working days", "three", "seven", "limited liability", "zero liability"],
        "source_url": RBI_UNAUTHORIZED_URL,
        "source_note": "RBI customer liability timelines for third-party breach reporting.",
        "text": (
            "For third-party breaches where neither the bank nor the customer is responsible, reporting within "
            "3 working days gives zero liability. Reporting within 4 to 7 working days gives limited liability. "
            "Reporting beyond 7 working days follows the bank board-approved customer liability policy."
        ),
    },
    {
        "id": "RBI-UT-003",
        "title": "Shadow Reversal and 90-Day Resolution",
        "risk": "High",
        "tags": ["shadow reversal", "10 working days", "90 days", "complaint", "compensation"],
        "source_url": RBI_UNAUTHORIZED_URL,
        "source_note": "RBI timeline for crediting customer accounts and resolving liability.",
        "text": (
            "After notification, the bank should credit the unauthorized transaction amount as a shadow reversal "
            "within 10 working days. Customer liability must be resolved within 90 days, and if not resolved within "
            "90 days, compensation should follow the RBI customer protection timelines."
        ),
    },
    {
        "id": "RBI-UT-004",
        "title": "Burden of Proof for Customer Liability",
        "risk": "High",
        "tags": ["burden of proof", "customer liability", "evidence", "negligence"],
        "source_url": RBI_UNAUTHORIZED_URL,
        "source_note": "RBI states burden of proving customer liability lies on the bank.",
        "text": (
            "The burden of proving customer liability in unauthorized electronic banking transactions lies on the bank. "
            "The agent should not blame the customer without evidence or promise final reimbursement before investigation."
        ),
    },
    {
        "id": "RBI-KYC-001",
        "title": "Customer Due Diligence for Individuals",
        "risk": "Medium",
        "tags": ["kyc", "cdd", "customer due diligence", "identity", "aadhaar", "pan", "individual"],
        "source_url": RBI_KYC_URL,
        "source_note": "RBI Master Direction KYC, customer due diligence procedure for individuals.",
        "text": (
            "For individual customer due diligence, regulated entities collect identity and address evidence, validate "
            "official identifiers as applicable, and maintain customer identification records before establishing an "
            "account-based relationship."
        ),
    },
    {
        "id": "RBI-KYC-002",
        "title": "Ongoing Due Diligence and Customer Profile",
        "risk": "Medium",
        "tags": ["ongoing due diligence", "monitoring", "risk profile", "customer profile", "transactions"],
        "source_url": RBI_KYC_URL,
        "source_note": "RBI Master Direction KYC includes ongoing due diligence and risk management sections.",
        "text": (
            "Banks should keep customer profiles current, monitor transactions against the customer's risk profile, "
            "and refresh records based on risk. Unusual activity should be reviewed instead of being automatically approved."
        ),
    },
    {
        "id": "RBI-KYC-003",
        "title": "Beneficial Owner Identification",
        "risk": "High",
        "tags": ["beneficial owner", "company account", "legal entity", "ownership", "authorized signatory"],
        "source_url": RBI_KYC_URL,
        "source_note": "RBI Master Direction KYC, identification of beneficial owner for legal entities.",
        "text": (
            "For legal entity onboarding, banks must identify and verify beneficial owners and authorized signatories. "
            "A company account should not be activated when beneficial ownership is unclear or evidence is incomplete."
        ),
    },
    {
        "id": "RBI-KYC-004",
        "title": "Enhanced Due Diligence for Higher Risk Customers",
        "risk": "High",
        "tags": ["enhanced due diligence", "edd", "pep", "high risk", "source of funds", "senior management"],
        "source_url": RBI_KYC_URL,
        "source_note": "RBI Master Direction KYC, enhanced due diligence requirements for higher-risk scenarios.",
        "text": (
            "Higher-risk customers such as politically exposed persons require enhanced due diligence, appropriate risk "
            "management checks, source of funds or wealth assessment, and senior management approval where applicable."
        ),
    },
]


def get_kb():
    """Return a defensive copy of the synthetic KB."""
    return deepcopy(KB_ITEMS)
