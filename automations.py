#!/usr/bin/env python3
"""
BrainOps Product Automations
=============================
Multi-level automation system for continuous product generation and optimization.

Automation Levels:
1. Discovery - Find opportunities
2. Generation - Create products
3. Optimization - Improve existing products
4. Scaling - Expand successful products
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import httpx

BRAINOPS_API = os.getenv("BRAINOPS_API", "https://brainops-ai-agents.onrender.com")
API_KEY = os.getenv("BRAINOPS_API_KEY", "brainops_prod_key_2025")


class AutomationLevel(Enum):
    DISCOVERY = 1  # Find opportunities
    GENERATION = 2  # Create products
    OPTIMIZATION = 3  # Improve products
    SCALING = 4  # Expand reach


class AutomationTrigger(Enum):
    SCHEDULED = "scheduled"  # Time-based
    EVENT = "event"  # Event-driven
    THRESHOLD = "threshold"  # Metric-based
    MANUAL = "manual"  # On-demand


@dataclass
class Automation:
    """Automation definition"""
    id: str
    name: str
    level: AutomationLevel
    trigger: AutomationTrigger
    trigger_config: Dict
    action: str
    ai_providers: List[str]
    enabled: bool = True
    last_run: Optional[datetime] = None
    run_count: int = 0


class AutomationEngine:
    """
    Multi-level automation engine for product operations
    """

    def __init__(self):
        self.automations: Dict[str, Automation] = {}
        self.http_client = httpx.AsyncClient(timeout=120.0)
        self.running = False
        self._register_default_automations()

    def _register_default_automations(self):
        """Register default automation workflows"""

        # Level 1: Discovery Automations
        self.register(Automation(
            id="discover_market_gaps",
            name="Market Gap Discovery",
            level=AutomationLevel.DISCOVERY,
            trigger=AutomationTrigger.SCHEDULED,
            trigger_config={"interval_hours": 24},
            action="discover_market_gaps",
            ai_providers=["perplexity", "gemini"]
        ))

        self.register(Automation(
            id="competitor_monitoring",
            name="Competitor Analysis",
            level=AutomationLevel.DISCOVERY,
            trigger=AutomationTrigger.SCHEDULED,
            trigger_config={"interval_hours": 12},
            action="analyze_competitors",
            ai_providers=["perplexity", "claude"]
        ))

        self.register(Automation(
            id="trend_detection",
            name="Industry Trend Detection",
            level=AutomationLevel.DISCOVERY,
            trigger=AutomationTrigger.SCHEDULED,
            trigger_config={"interval_hours": 6},
            action="detect_trends",
            ai_providers=["perplexity"]
        ))

        # Level 2: Generation Automations
        self.register(Automation(
            id="template_generation",
            name="Template Product Generator",
            level=AutomationLevel.GENERATION,
            trigger=AutomationTrigger.EVENT,
            trigger_config={"event": "opportunity_discovered"},
            action="generate_template_product",
            ai_providers=["claude", "codex"]
        ))

        self.register(Automation(
            id="saas_feature_builder",
            name="SaaS Feature Builder",
            level=AutomationLevel.GENERATION,
            trigger=AutomationTrigger.MANUAL,
            trigger_config={},
            action="build_saas_feature",
            ai_providers=["codex", "claude"]
        ))

        self.register(Automation(
            id="content_creator",
            name="Educational Content Creator",
            level=AutomationLevel.GENERATION,
            trigger=AutomationTrigger.SCHEDULED,
            trigger_config={"interval_hours": 48},
            action="create_content",
            ai_providers=["claude", "gemini"]
        ))

        # Level 3: Optimization Automations
        self.register(Automation(
            id="pricing_optimizer",
            name="Dynamic Pricing Optimizer",
            level=AutomationLevel.OPTIMIZATION,
            trigger=AutomationTrigger.THRESHOLD,
            trigger_config={"metric": "conversion_rate", "threshold": 0.02},
            action="optimize_pricing",
            ai_providers=["claude"]
        ))

        self.register(Automation(
            id="copy_optimizer",
            name="Marketing Copy Optimizer",
            level=AutomationLevel.OPTIMIZATION,
            trigger=AutomationTrigger.SCHEDULED,
            trigger_config={"interval_hours": 72},
            action="optimize_copy",
            ai_providers=["claude", "gemini"]
        ))

        self.register(Automation(
            id="feature_enhancer",
            name="Product Feature Enhancer",
            level=AutomationLevel.OPTIMIZATION,
            trigger=AutomationTrigger.EVENT,
            trigger_config={"event": "customer_feedback_received"},
            action="enhance_features",
            ai_providers=["claude", "codex"]
        ))

        # Level 4: Scaling Automations
        self.register(Automation(
            id="market_expander",
            name="New Market Expander",
            level=AutomationLevel.SCALING,
            trigger=AutomationTrigger.THRESHOLD,
            trigger_config={"metric": "product_revenue", "threshold": 1000},
            action="expand_to_new_markets",
            ai_providers=["perplexity", "claude", "gemini"]
        ))

        self.register(Automation(
            id="product_cloner",
            name="Successful Product Cloner",
            level=AutomationLevel.SCALING,
            trigger=AutomationTrigger.THRESHOLD,
            trigger_config={"metric": "product_sales", "threshold": 100},
            action="clone_successful_product",
            ai_providers=["claude", "codex"]
        ))

        self.register(Automation(
            id="affiliate_program_creator",
            name="Affiliate Program Creator",
            level=AutomationLevel.SCALING,
            trigger=AutomationTrigger.MANUAL,
            trigger_config={},
            action="create_affiliate_program",
            ai_providers=["claude"]
        ))

    def register(self, automation: Automation):
        """Register an automation"""
        self.automations[automation.id] = automation

    async def execute_automation(self, automation_id: str, context: Dict = None) -> Dict:
        """Execute a specific automation"""
        automation = self.automations.get(automation_id)
        if not automation:
            return {"error": f"Automation {automation_id} not found"}

        if not automation.enabled:
            return {"error": f"Automation {automation_id} is disabled"}

        print(f"🤖 Executing: {automation.name}")
        print(f"   Level: {automation.level.name}")
        print(f"   AI Providers: {automation.ai_providers}")

        # Execute the action
        result = await self._run_action(automation, context or {})

        # Update automation stats
        automation.last_run = datetime.now()
        automation.run_count += 1

        # Store result in brain
        await self._store_result(automation, result)

        return result

    async def _run_action(self, automation: Automation, context: Dict) -> Dict:
        """Run the automation action"""
        action_handlers = {
            "discover_market_gaps": self._action_discover_market_gaps,
            "analyze_competitors": self._action_analyze_competitors,
            "detect_trends": self._action_detect_trends,
            "generate_template_product": self._action_generate_template,
            "build_saas_feature": self._action_build_saas_feature,
            "create_content": self._action_create_content,
            "optimize_pricing": self._action_optimize_pricing,
            "optimize_copy": self._action_optimize_copy,
            "enhance_features": self._action_enhance_features,
            "expand_to_new_markets": self._action_expand_markets,
            "clone_successful_product": self._action_clone_product,
            "create_affiliate_program": self._action_create_affiliate,
        }

        handler = action_handlers.get(automation.action)
        if handler:
            return await handler(automation, context)
        else:
            return {"error": f"Unknown action: {automation.action}"}

    # Discovery Actions
    async def _action_discover_market_gaps(self, automation: Automation, context: Dict) -> Dict:
        """Discover market gaps using AI"""
        response = await self.http_client.post(
            f"{BRAINOPS_API}/agents/MarketIntelligence/execute",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"task": {"action": "discover_gaps", "industry": context.get("industry", "roofing")}}
        )
        return response.json()

    async def _action_analyze_competitors(self, automation: Automation, context: Dict) -> Dict:
        """Analyze competitors"""
        response = await self.http_client.post(
            f"{BRAINOPS_API}/agents/CompetitiveIntelligence/execute",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"task": {"action": "analyze_competitors"}}
        )
        return response.json()

    async def _action_detect_trends(self, automation: Automation, context: Dict) -> Dict:
        """Detect industry trends"""
        response = await self.http_client.post(
            f"{BRAINOPS_API}/agents/TrendAnalyzer/execute",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"task": {"action": "detect_trends"}}
        )
        return response.json()

    # Generation Actions
    async def _action_generate_template(self, automation: Automation, context: Dict) -> Dict:
        """Generate a template product"""
        response = await self.http_client.post(
            f"{BRAINOPS_API}/agents/ProductGenerator/execute",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"task": {
                "action": "generate_template",
                "type": context.get("type", "spreadsheet"),
                "industry": context.get("industry", "roofing")
            }}
        )
        return response.json()

    async def _action_build_saas_feature(self, automation: Automation, context: Dict) -> Dict:
        """Build a SaaS feature"""
        return {
            "status": "initiated",
            "feature": context.get("feature_name", "New Feature"),
            "message": "SaaS feature build initiated via Codex"
        }

    async def _action_create_content(self, automation: Automation, context: Dict) -> Dict:
        """Create educational content"""
        response = await self.http_client.post(
            f"{BRAINOPS_API}/agents/ContentCreator/execute",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"task": {
                "action": "create_content",
                "type": context.get("content_type", "blog_post"),
                "topic": context.get("topic", "AI in roofing")
            }}
        )
        return response.json()

    # Optimization Actions
    async def _action_optimize_pricing(self, automation: Automation, context: Dict) -> Dict:
        """Optimize product pricing"""
        response = await self.http_client.post(
            f"{BRAINOPS_API}/agents/RevenueOptimizer/execute",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"task": {"action": "optimize_pricing"}}
        )
        return response.json()

    async def _action_optimize_copy(self, automation: Automation, context: Dict) -> Dict:
        """Optimize marketing copy"""
        return {
            "status": "initiated",
            "message": "Copy optimization initiated"
        }

    async def _action_enhance_features(self, automation: Automation, context: Dict) -> Dict:
        """Enhance product features based on feedback"""
        return {
            "status": "initiated",
            "message": "Feature enhancement initiated"
        }

    # Scaling Actions
    async def _action_expand_markets(self, automation: Automation, context: Dict) -> Dict:
        """Expand to new markets"""
        return {
            "status": "initiated",
            "target_markets": ["commercial roofing", "solar installation", "siding contractors"],
            "message": "Market expansion analysis initiated"
        }

    async def _action_clone_product(self, automation: Automation, context: Dict) -> Dict:
        """Clone successful product for new market"""
        return {
            "status": "initiated",
            "source_product": context.get("product_id"),
            "message": "Product cloning initiated"
        }

    async def _action_create_affiliate(self, automation: Automation, context: Dict) -> Dict:
        """Create affiliate program"""
        return {
            "status": "initiated",
            "message": "Affiliate program creation initiated"
        }

    async def _store_result(self, automation: Automation, result: Dict):
        """Store automation result in brain"""
        try:
            await self.http_client.post(
                f"{BRAINOPS_API}/brain/store",
                headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
                json={
                    "key": f"automation_{automation.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "value": {
                        "automation_id": automation.id,
                        "automation_name": automation.name,
                        "level": automation.level.value,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    },
                    "category": "automation_results",
                    "priority": "normal"
                }
            )
        except Exception as e:
            print(f"⚠️ Failed to store result: {e}")

    async def run_scheduled_automations(self):
        """Run all scheduled automations that are due"""
        now = datetime.now()

        for automation in self.automations.values():
            if automation.trigger != AutomationTrigger.SCHEDULED:
                continue

            if not automation.enabled:
                continue

            interval_hours = automation.trigger_config.get("interval_hours", 24)
            if automation.last_run:
                next_run = automation.last_run + timedelta(hours=interval_hours)
                if now < next_run:
                    continue

            print(f"⏰ Running scheduled automation: {automation.name}")
            await self.execute_automation(automation.id)

    async def start_automation_loop(self):
        """Start the continuous automation loop"""
        self.running = True
        print("🚀 Starting automation engine...")

        while self.running:
            try:
                await self.run_scheduled_automations()
            except Exception as e:
                print(f"⚠️ Automation loop error: {e}")

            # Check every 5 minutes
            await asyncio.sleep(300)

    def stop(self):
        """Stop the automation loop"""
        self.running = False
        print("🛑 Stopping automation engine...")

    def list_automations(self) -> List[Dict]:
        """List all automations"""
        return [
            {
                "id": a.id,
                "name": a.name,
                "level": a.level.name,
                "trigger": a.trigger.value,
                "enabled": a.enabled,
                "last_run": a.last_run.isoformat() if a.last_run else None,
                "run_count": a.run_count
            }
            for a in self.automations.values()
        ]


class ProductAutomationAPI:
    """
    REST API interface for product automations
    Integrates with BrainOps backend
    """

    def __init__(self):
        self.engine = AutomationEngine()

    async def handle_webhook(self, event_type: str, payload: Dict) -> Dict:
        """Handle incoming webhooks to trigger automations"""
        event_automations = [
            a for a in self.engine.automations.values()
            if a.trigger == AutomationTrigger.EVENT
            and a.trigger_config.get("event") == event_type
        ]

        results = []
        for automation in event_automations:
            result = await self.engine.execute_automation(automation.id, payload)
            results.append({
                "automation_id": automation.id,
                "result": result
            })

        return {"triggered": len(results), "results": results}

    async def check_thresholds(self, metrics: Dict) -> Dict:
        """Check metrics against automation thresholds"""
        threshold_automations = [
            a for a in self.engine.automations.values()
            if a.trigger == AutomationTrigger.THRESHOLD
        ]

        triggered = []
        for automation in threshold_automations:
            metric_name = automation.trigger_config.get("metric")
            threshold = automation.trigger_config.get("threshold")

            if metric_name in metrics and metrics[metric_name] >= threshold:
                result = await self.engine.execute_automation(automation.id, metrics)
                triggered.append({
                    "automation_id": automation.id,
                    "metric": metric_name,
                    "value": metrics[metric_name],
                    "threshold": threshold,
                    "result": result
                })

        return {"triggered": len(triggered), "results": triggered}


# CLI Entry Point
async def main():
    """Main entry point for automation system"""
    import sys

    engine = AutomationEngine()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            automations = engine.list_automations()
            print("\n📋 REGISTERED AUTOMATIONS:")
            print("-" * 60)
            for a in automations:
                status = "✅" if a["enabled"] else "❌"
                print(f"{status} [{a['level']}] {a['name']}")
                print(f"   ID: {a['id']}")
                print(f"   Trigger: {a['trigger']}")
                print(f"   Runs: {a['run_count']}")
                print()

        elif command == "run":
            automation_id = sys.argv[2] if len(sys.argv) > 2 else None
            if automation_id:
                result = await engine.execute_automation(automation_id)
                print(json.dumps(result, indent=2, default=str))
            else:
                print("Usage: python automations.py run <automation_id>")

        elif command == "start":
            await engine.start_automation_loop()

    else:
        print("Usage: python automations.py [list|run|start]")


if __name__ == "__main__":
    asyncio.run(main())
