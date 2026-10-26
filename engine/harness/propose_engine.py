# -*- coding: utf-8 -*-
"""
ProposeEngine: Harness² Candidate Mutation Generator.
Analyzes failure traces, error signatures, and performance bottlenecks
to synthesize concrete scaffolding mutations (prompt directives, policy adjustments,
fallback routes) without modifying model weights.
"""
import sys
import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("ProposeEngine")


class FailureCategory:
    VALIDATION_ERROR = "VALIDATION_ERROR"
    ENCODING_ERROR = "ENCODING_ERROR"
    NETWORK_LATENCY = "NETWORK_LATENCY"
    DOM_OVERFLOW = "DOM_OVERFLOW"
    CALCULATION_ERROR = "CALCULATION_ERROR"
    GENERAL_RUNTIME = "GENERAL_RUNTIME"


class ProposeEngine:
    """Generates hypothesis mutations to the agent scaffold based on execution feedback."""

    def __init__(self, vault=None):
        self.vault = vault

    def classify_failure(self, error_message: str, stack_trace: str = "") -> str:
        """Classifies the failure signature into a recognized operational domain."""
        combined = f"{error_message} {stack_trace}".lower()

        if any(term in combined for term in ["cp949", "utf-8", "decode", "encode", "charmap", "한글 깨짐"]):
            return FailureCategory.ENCODING_ERROR
        if any(term in combined for term in ["400 bad request", "validation", "b:section", "missing tag", "schema"]):
            return FailureCategory.VALIDATION_ERROR
        if any(term in combined for term in ["timeout", "timed out", "connection", "rate limit", "429", "503", "socket"]):
            return FailureCategory.NETWORK_LATENCY
        if any(term in combined for term in ["overflow", "bbox", "pixel", "gap", "html14", "width", "375px"]):
            return FailureCategory.DOM_OVERFLOW
        if any(term in combined for term in ["zerodivision", "nan", "infinity", "math domain", "valueerror"]):
            return FailureCategory.CALCULATION_ERROR

        return FailureCategory.GENERAL_RUNTIME

    def propose_mutation(
        self,
        module_name: str,
        error_message: str,
        stack_trace: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Synthesizes a concrete scaffold mutation proposal from a failure trace.
        """
        category = self.classify_failure(error_message, stack_trace)
        proposal_id = f"PROP-{uuid.uuid4().hex[:8].upper()}"
        now_str = datetime.now(timezone.utc).isoformat()
        ctx = context or {}

        # 1. Validation Failures (e.g. Blogger XML / API)
        if category == FailureCategory.VALIDATION_ERROR:
            return {
                "proposal_id": proposal_id,
                "timestamp": now_str,
                "category": category,
                "module_name": module_name,
                "target_type": "PROMPT_RULE",
                "suggested_patch": "Enforce mandatory section tags (<b:section id='header'> and <b:section id='sidebar'>) in all generated templates.",
                "mutation_payload": {
                    "agent_role": "blogger_gateway",
                    "rule": "Always include valid b:section header and sidebar tags in theme XML.",
                    "policy_updates": {"retry_limit": 3},
                },
                "rationale": "Blogger backend validator strictly requires header/sidebar sections.",
            }

        # 2. Encoding Failures (e.g. PowerShell CP949)
        elif category == FailureCategory.ENCODING_ERROR:
            return {
                "proposal_id": proposal_id,
                "timestamp": now_str,
                "category": category,
                "module_name": module_name,
                "target_type": "RUNTIME_POLICY",
                "suggested_patch": "Force UTF-8 BOM encoding ('utf-8-sig') and 'chcp 65001' console active code page.",
                "mutation_payload": {
                    "policy_updates": {
                        "encoding": "utf-8-sig",
                        "chcp": 65001,
                    }
                },
                "rationale": "Windows PowerShell 5.1 requires UTF-8 BOM to prevent Korean character corruption.",
            }

        # 3. Network Latency & Rate Limits (e.g. FX / Market APIs)
        elif category == FailureCategory.NETWORK_LATENCY:
            return {
                "proposal_id": proposal_id,
                "timestamp": now_str,
                "category": category,
                "module_name": module_name,
                "target_type": "FALLBACK_ROUTE",
                "suggested_patch": "Activate client-side LocalStorage cache and engage SSOT Fallback (1,380.0 KRW).",
                "mutation_payload": {
                    "policy_updates": {
                        "fallback_fx_rate": 1380.0,
                        "cache_ttl_seconds": 3600,
                        "sandbox_timeout_seconds": 25,
                    }
                },
                "rationale": "External financial APIs are volatile; local caching + fallback prevents pipeline stalls.",
            }

        # 4. DOM Overflow & Ad Intrusion (e.g. Calculator grid blowout)
        elif category == FailureCategory.DOM_OVERFLOW:
            return {
                "proposal_id": proposal_id,
                "timestamp": now_str,
                "category": category,
                "module_name": module_name,
                "target_type": "PROMPT_RULE",
                "suggested_patch": "Apply 2x2 CSS Grid Dual-Shield with MutationObserver DOM sanitizer.",
                "mutation_payload": {
                    "agent_role": "cro_monetizer",
                    "rule": "Enforce 2x2 CSS grid with 100% width containment and MutationObserver ad shield.",
                    "policy_updates": {"max_content_width_px": 880},
                },
                "rationale": "Zero gap and zero horizontal scroll are required for high-converting Micro-SaaS UX.",
            }

        # 5. Calculation Bounds (e.g. Zero division, NaN)
        elif category == FailureCategory.CALCULATION_ERROR:
            return {
                "proposal_id": proposal_id,
                "timestamp": now_str,
                "category": category,
                "module_name": module_name,
                "target_type": "PROMPT_RULE",
                "suggested_patch": "Wrap all division and log calculations with boundary checks (Math.max(x, 0)).",
                "mutation_payload": {
                    "agent_role": "dataset_resolver",
                    "rule": "Clamp all numerical calculations to safe positive ranges to prevent NaN.",
                },
                "rationale": "Micro-SaaS calculators must never display NaN or Infinity to users.",
            }

        # 6. General Runtime Exception
        return {
            "proposal_id": proposal_id,
            "timestamp": now_str,
            "category": category,
            "module_name": module_name,
            "target_type": "RUNTIME_POLICY",
            "suggested_patch": "Increase auto-retry limit and invoke diagnostic telemetry logging.",
            "mutation_payload": {
                "policy_updates": {
                    "retry_limit": 4,
                    "diagnostic_logging": True,
                }
            },
            "rationale": f"Unclassified runtime exception '{error_message}'; engaging defensive retry policy.",
        }
