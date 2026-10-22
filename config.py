"""
RECLAIM AI - Configuration Module
Intelligent Lost Document Recovery Agent
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "reclaim-ai-hackathon-2026-secret-key-civic-impact")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "reclaim_ai.db"))
    
    # Gemini AI configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Official Government & Educational Domain Suffix Allowlist
    OFFICIAL_DOMAIN_SUFFIXES = [
        ".gov.in",
        ".nic.in",
        ".edu.in",
        ".ac.in",
        "digilocker.gov.in",
        "parivahan.gov.in",
        "uidai.gov.in",
        "incometax.gov.in",
        "voters.eci.gov.in",
        "passportindia.gov.in",
        "cbse.gov.in"
    ]
    
    # Known Unofficial / Third-party Agent domains used for safety testing & blacklisting
    KNOWN_UNOFFICIAL_DOMAINS = [
        "quick-pan-agent.com",
        "express-licence-brokers.in",
        "easyidentityreissue.online",
        "fastdocumentagents.in",
        "tatkalpanportal.biz",
        "instantvoterfix.org"
    ]
    
    # Blocked IP ranges and hostnames for SSRF protection
    BLOCKED_HOSTNAMES = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "169.254.169.254", # AWS/GCP/Azure instance metadata
        "metadata.google.internal",
        "::1"
    ]
    
    # Supported document categories
    DOCUMENT_CATEGORIES = [
        {
            "id": "edu_cert",
            "name": "Educational Certificate / Marksheet",
            "description": "Secondary school (10th), Senior secondary (12th), University Degree, or Diploma certificates.",
            "common_issuers": ["CBSE", "ICSE", "State Board of Secondary Education", "State / Central University"],
            "requires_fir": False,
            "requires_affidavit": True
        },
        {
            "id": "driving_licence",
            "name": "Driving Licence (DL)",
            "description": "Lost, stolen, or mutilated Motor Vehicle Driving Licence or Learner Licence.",
            "common_issuers": ["Ministry of Road Transport and Highways (MoRTH)", "State Transport Department / RTO"],
            "requires_fir": True, # For stolen/lost
            "requires_affidavit": False
        },
        {
            "id": "pan_card",
            "name": "PAN Card (Permanent Account Number)",
            "description": "Lost or damaged physical PAN card issued by Income Tax Department.",
            "common_issuers": ["Income Tax Department of India", "NSDL / Protean", "UTIITSL"],
            "requires_fir": False,
            "requires_affidavit": False
        },
        {
            "id": "aadhaar",
            "name": "Aadhaar Card (e-Aadhaar / PVC Reorder)",
            "description": "Aadhaar lost or damaged. Recovery of Enrollment ID (EID) or reprint.",
            "common_issuers": ["Unique Identification Authority of India (UIDAI)"],
            "requires_fir": False,
            "requires_affidavit": False
        },
        {
            "id": "voter_id",
            "name": "Voter ID (EPIC Card)",
            "description": "Electors Photo Identity Card replacement (Form 8).",
            "common_issuers": ["Election Commission of India (ECI)", "Chief Electoral Officer (State)"],
            "requires_fir": True, # In case of theft
            "requires_affidavit": False
        },
        {
            "id": "passport",
            "name": "Passport Reissue",
            "description": "Lost, stolen, or damaged Indian Passport reissue under normal or tatkaal scheme.",
            "common_issuers": ["Consular, Passport & Visa (CPV) Division, Ministry of External Affairs"],
            "requires_fir": True, # Mandatory police loss report
            "requires_affidavit": True # Annexure F affidavit
        },
        {
            "id": "other_cert",
            "name": "Other Government Certificate",
            "description": "Birth, Caste, Domicile, or Income Certificate replacement.",
            "common_issuers": ["State Revenue Department", "Municipal Corporation", "Tehsil / Taluka Office"],
            "requires_fir": False,
            "requires_affidavit": True
        }
    ]
