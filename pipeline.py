#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time
from datetime import datetime

# BrainOps Product Pipeline Orchestrator
# Coordinates: Perplexity -> Claude -> Codex -> Gemini

PIPELINE_ROOT = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(PIPELINE_ROOT, "artifacts")

def ensure_artifacts_dir(run_id):
    path = os.path.join(ARTIFACTS_DIR, run_id)
    os.makedirs(path, exist_ok=True)
    return path

def run_step(step_name, command, cwd=None):
    print(f"\n🚀 [Pipeline] Starting Step: {step_name}")
    try:
        # We use the 'brain' wrapper to inject context
        full_command = f"source ~/.bashrc && {command}"
        result = subprocess.run(
            full_command, 
            shell=True, 
            executable="/bin/bash",
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        if result.returncode != 0:
            print(f"❌ Step Failed: {result.stderr}")
            return None
        print(f"✅ Step Complete.")
        return result.stdout.strip()
    except Exception as e:
        print(f"🔥 Execution Error: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline.py <product_concept>")
        sys.exit(1)

    concept = sys.argv[1]
    run_id = f"run_{int(time.time())}"
    work_dir = ensure_artifacts_dir(run_id)
    
    print(f"🏭 BrainOps Product Factory initialized for: '{concept}'")
    print(f"📂 Workspace: {work_dir}")

    # --- STEP 1: MARKET RESEARCH (Perplexity / Gemini) ---
    # We use Gemini here as a proxy for deep research if Perplexity CLI isn't installed
    print("🔍 Phase 1: Market Intelligence")
    research_prompt = f"Analyze the market for '{concept}'. Identify 3 gaps, ideal pricing, and technical requirements. Output JSON."
    market_data = run_step("Market Analysis", f"brain gemini -p \"{research_prompt}\"")
    
    if not market_data:
        print("Aborting pipeline.")
        sys.exit(1)
        
    with open(f"{work_dir}/1_market_data.json", "w") as f:
        f.write(market_data)

    # --- STEP 2: SPECIFICATION (Claude) ---
    print("📝 Phase 2: Product Spec & Architecture")
    spec_prompt = f"Based on this market data: {market_data}. Write a detailed PRD (Product Requirements Doc) and Technical Architecture for a MVP. Include stack details."
    spec_doc = run_step("Spec Generation", f"brain claude \"{spec_prompt}\"")
    
    with open(f"{work_dir}/2_product_spec.md", "w") as f:
        f.write(spec_doc or "Error generating spec")

    # --- STEP 3: CODE GENERATION (Codex) ---
    print("💻 Phase 3: Construction")
    # Realistically, Codex CLI needs file inputs. We'd generate a prompt file.
    # Here we simulate the scaffold command.
    scaffold_prompt = f"Scaffold a Next.js project for: {concept}. Use Tailwind, Supabase."
    
    if "--live" in sys.argv:
        print("⚡ LIVE MODE: Executing Codex...")
        run_step("Code Gen", f"brain codex exec \"{scaffold_prompt}\"", cwd=work_dir)
    else:
        print("⚠️  (Dry Run: Pass --live to execute Codex scaffolding)")

    # --- STEP 4: ASSETS & COPY (Gemini/Claude) ---
    print("🎨 Phase 4: Assets & Marketing")
    copy_prompt = f"Write a high-conversion landing page copy for {concept}."
    copy_text = run_step("Copywriting", f"brain claude \"{copy_prompt}\"")
    
    with open(f"{work_dir}/4_landing_page.md", "w") as f:
        f.write(copy_text or "")

    print(f"\n✨ Pipeline Complete! Artifacts saved in {work_dir}")

if __name__ == "__main__":
    main()