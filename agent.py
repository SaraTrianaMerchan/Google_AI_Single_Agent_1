#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import os

# Forzar UTF-8 en todo el sistema
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from retry import retry_config

#---create agent---

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

async def main():
    print("[OK] Root Agent defined.")
    
    #---create runner---
    # CORREGIDO: usar el mismo app_name que espera el agente
    runner = InMemoryRunner(agent=root_agent, app_name="agents")
    
    print("[OK] Runner created.")
    
    #---async function to run agent---
    question = "What is the Agent Developer Kit from Google?"
    
    print(f"[DEBUG] Sending question: {question}")
    
    try:
        response = await runner.run_debug(question)
        print("\n### Agent response:\n")
    except Exception as e:
        print(f"[ERROR] Failed to get response: {e}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

#---Run the script---

if __name__ == "__main__":
    # Verificar encoding del sistema
    print(f"[DEBUG] System encoding: {sys.getdefaultencoding()}")
    print(f"[DEBUG] Filesystem encoding: {sys.getfilesystemencoding()}")
    
    asyncio.run(main())
