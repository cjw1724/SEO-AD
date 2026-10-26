# -*- coding: utf-8 -*-
"""
HarnessVault: Persistent Knowledge Ledger & Dynamic Scaffold Injector for Harness².
Stores verified learnings, enforces immutable boundaries, and dynamically injects
runtime rules into prompts and execution policies.
"""
import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("HarnessVault")

DEFAULT_VAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "harness_learnings.json",
)

IMMUTABLE_BOUNDARIES_DEFAULT = [
    "OPENROUTER_API_KEY",
    "BLOGGER_BLOG_ID",
    "AGENTS.md",
    "MAX_DAILY_BUDGET",
    "SEO.env",
    "credentials.json",
    "token.json",
]


class HarnessVault:
    """Manages the persistent knowledge ledger and runtime scaffold injection for Harness²."""

    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = vault_path or DEFAULT_VAULT_PATH
        self._data: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        """Loads the knowledge ledger from disk, initializing defaults if absent."""
        if not os.path.exists(self.vault_path):
            self._data = self._generate_default_vault()
            self.save()
            return self._data

        try:
            with open(self.vault_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read vault at {self.vault_path}: {e}. Initializing defaults.")
            self._data = self._generate_default_vault()
            self.save()

        # Ensure required sections exist
        if "immutable_boundaries" not in self._data:
            self._data["immutable_boundaries"] = list(IMMUTABLE_BOUNDARIES_DEFAULT)
        if "learnings" not in self._data:
            self._data["learnings"] = []
        if "prompt_injections" not in self._data:
            self._data["prompt_injections"] = {}
        if "runtime_policies" not in self._data:
            self._data["runtime_policies"] = {}

        return self._data

    def save(self) -> bool:
        """Persists the in-memory ledger to disk atomically."""
        try:
            self._data["updated_at"] = datetime.now(timezone.utc).isoformat()
            os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
            temp_path = f"{self.vault_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            if os.path.exists(self.vault_path):
                os.replace(temp_path, self.vault_path)
            else:
                os.rename(temp_path, self.vault_path)
            return True
        except Exception as e:
            logger.error(f"Failed to save vault: {e}")
            return False

    def is_immutable(self, target_key: str) -> bool:
        """Checks if a target key or path violates constitutional immutable boundaries."""
        boundaries = self._data.get("immutable_boundaries", IMMUTABLE_BOUNDARIES_DEFAULT)
        normalized = target_key.strip().upper()
        for b in boundaries:
            if b.upper() in normalized:
                return True
        return False

    def get_learnings(self, domain: Optional[str] = None, active_only: bool = True) -> List[Dict[str, Any]]:
        """Retrieves learned scaffold patches, optionally filtered by domain and active status."""
        learnings = self._data.get("learnings", [])
        results = []
        for item in learnings:
            if active_only and item.get("status") != "ACTIVE":
                continue
            if domain and item.get("domain") != domain:
                continue
            results.append(item)
        return results

    def record_learning(
        self,
        domain: str,
        symptom: str,
        root_cause: str,
        scaffold_patch: str,
        fitness_score: float,
        status: str = "ACTIVE",
    ) -> Dict[str, Any]:
        """
        Records a newly verified learning into the persistent ledger.
        Increments active generation if fitness exceeds threshold.
        """
        # Security validation against immutable boundaries
        for text in [domain, symptom, root_cause, scaffold_patch]:
            if self.is_immutable(text):
                raise PermissionError(f"Attempted mutation violates constitutional boundary: {text}")

        next_idx = len(self._data.get("learnings", [])) + 1
        learning_id = f"LRN-{next_idx:03d}"
        entry = {
            "id": learning_id,
            "domain": domain,
            "symptom": symptom,
            "root_cause": root_cause,
            "scaffold_patch": scaffold_patch,
            "fitness_score": round(fitness_score, 2),
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
        }

        self._data.setdefault("learnings", []).append(entry)
        if fitness_score >= self.get_policy("min_fitness_threshold", 80.0):
            current_gen = self._data.get("active_generation", 1)
            self._data["active_generation"] = current_gen + 1

        self.save()
        return entry

    def inject_prompt_rules(self, agent_role: str, base_prompt: str) -> str:
        """
        Dynamically enriches an agent's base system prompt with verified Harness² rules.
        """
        injections = self._data.get("prompt_injections", {})
        rules = injections.get(agent_role, [])
        if not rules:
            return base_prompt

        injected_block = "\n\n### 🧬 [Harness² Self-Evolved Operational Directives]\n"
        for idx, rule in enumerate(rules, 1):
            injected_block += f"{idx}. {rule}\n"

        return f"{base_prompt.rstrip()}{injected_block}"

    def register_prompt_rule(self, agent_role: str, rule_text: str) -> bool:
        """Registers a new prompt rule for an agent role, guarding immutable boundaries."""
        if self.is_immutable(rule_text):
            raise PermissionError(f"Prompt rule violates immutable boundary: {rule_text}")

        self._data.setdefault("prompt_injections", {})
        role_rules = self._data["prompt_injections"].setdefault(agent_role, [])
        if rule_text not in role_rules:
            role_rules.append(rule_text)
            self.save()
            return True
        return False

    def get_policy(self, policy_name: str, default: Any = None) -> Any:
        """Gets a runtime execution policy value."""
        return self._data.get("runtime_policies", {}).get(policy_name, default)

    def set_policy(self, policy_name: str, value: Any) -> bool:
        """Sets a runtime execution policy value, guarding immutable boundaries."""
        if self.is_immutable(policy_name):
            raise PermissionError(f"Policy name violates immutable boundary: {policy_name}")
        self._data.setdefault("runtime_policies", {})[policy_name] = value
        return self.save()

    def _generate_default_vault(self) -> Dict[str, Any]:
        """Generates the initial genesis vault structure."""
        return {
            "schema_version": "2.0.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "active_generation": 1,
            "immutable_boundaries": list(IMMUTABLE_BOUNDARIES_DEFAULT),
            "learnings": [],
            "prompt_injections": {},
            "runtime_policies": {
                "retry_limit": 3,
                "fallback_fx_rate": 1380.0,
                "sandbox_timeout_seconds": 15,
                "min_fitness_threshold": 80.0,
                "encoding": "utf-8-sig",
            },
        }


# Global singleton instance for runtime import
default_vault = HarnessVault()
