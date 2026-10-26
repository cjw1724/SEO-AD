# -*- coding: utf-8 -*-
"""
engine/matcher/topic_clusters/__init__.py
-----------------------------------------
Blogin 365 AI Holdings - Universal Topic Clusters Registry (v9.0 Apex)

특정 키워드 하드코딩 파이썬 파일(hair.py, medical.py 등)을 폐기하고,
data/universal_clusters.json 및 UniversalTopicEngine 기반으로 동적 로드.
"""

import os
import json
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
JSON_PATH = os.path.join(BASE_DIR, "data", "universal_clusters.json")

def _load_all_clusters() -> Dict[str, Dict[str, Any]]:
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [topic_clusters] universal_clusters.json 로드 경고: {e}")
    return {}

ALL_CLUSTERS: Dict[str, Dict[str, Any]] = _load_all_clusters()

CATEGORY_TO_CLUSTER_MAP: Dict[str, str] = {
    "HAIR": "hair_transplant",
    "SUBSIDY": "government_subsidy",
    "SAVINGS": "cashflow_hacks",
    "MEDICAL": "medical_wellness",
    "CAREER": "career_cert"
}

HAIR_TRANSPLANT_CLUSTER = ALL_CLUSTERS.get("hair_transplant", {})
GOVERNMENT_SUBSIDY_CLUSTER = ALL_CLUSTERS.get("government_subsidy", {})
CASHFLOW_HACKS_CLUSTER = ALL_CLUSTERS.get("cashflow_hacks", {})
MEDICAL_WELLNESS_CLUSTER = ALL_CLUSTERS.get("medical_wellness", {})
CAREER_CERT_CLUSTER = ALL_CLUSTERS.get("career_cert", {})

__all__ = [
    "ALL_CLUSTERS",
    "CATEGORY_TO_CLUSTER_MAP",
    "HAIR_TRANSPLANT_CLUSTER",
    "GOVERNMENT_SUBSIDY_CLUSTER",
    "CASHFLOW_HACKS_CLUSTER",
    "MEDICAL_WELLNESS_CLUSTER",
    "CAREER_CERT_CLUSTER"
]
