# -*- coding: utf-8 -*-
"""
engine/matcher/topic_clusters/__init__.py
-----------------------------------------
Blogin 365 AI Holdings 5대 골든 니치 30-Day 토픽 클러스터 레지스트리 (v8.0 Apex).
"""

from typing import Dict, Any

from .hair import HAIR_TRANSPLANT_CLUSTER
from .subsidy import GOVERNMENT_SUBSIDY_CLUSTER
from .savings import CASHFLOW_HACKS_CLUSTER
from .medical import MEDICAL_WELLNESS_CLUSTER
from .career import CAREER_CERT_CLUSTER

ALL_CLUSTERS: Dict[str, Dict[str, Any]] = {
    "hair_transplant": HAIR_TRANSPLANT_CLUSTER,
    "government_subsidy": GOVERNMENT_SUBSIDY_CLUSTER,
    "cashflow_hacks": CASHFLOW_HACKS_CLUSTER,
    "medical_wellness": MEDICAL_WELLNESS_CLUSTER,
    "career_cert": CAREER_CERT_CLUSTER
}

CATEGORY_TO_CLUSTER_MAP: Dict[str, str] = {
    "HAIR": "hair_transplant",
    "SUBSIDY": "government_subsidy",
    "SAVINGS": "cashflow_hacks",
    "MEDICAL": "medical_wellness",
    "CAREER": "career_cert"
}

__all__ = [
    "ALL_CLUSTERS",
    "CATEGORY_TO_CLUSTER_MAP",
    "HAIR_TRANSPLANT_CLUSTER",
    "GOVERNMENT_SUBSIDY_CLUSTER",
    "CASHFLOW_HACKS_CLUSTER",
    "MEDICAL_WELLNESS_CLUSTER",
    "CAREER_CERT_CLUSTER"
]
