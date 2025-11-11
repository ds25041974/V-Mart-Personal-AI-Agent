"""
Core Gemini Agent for V-Mart Personal AI Agent
Enhanced with reasoning capabilities, context management, and multi-modal support

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import json
import time
from typing import Callable, Dict, List, Optional

import google.generativeai as genai

from .context_manager import AIContextManager


class GeminiAgent:
    def __init__(self, api_key: str):
        """
        Initializes the Gemini Agent.

        Args:
            api_key (str): The API key for the Gemini LLM.
        """
        genai.configure(api_key=api_key)

        # Initialize models - using latest free tier Gemini 2.0 Flash (free for all users)
        self.chat_model = genai.GenerativeModel("gemini-2.0-flash")
        self.vision_model = genai.GenerativeModel("gemini-2.0-flash")

        # Context management
        self.conversation_history: List[Dict] = []
        self.max_history = 10

        # AI Context Manager for store, weather, and competitor data
        try:
            self.context_manager = AIContextManager()
        except Exception as e:
            print(f"Warning: AI Context Manager initialization failed: {e}")
            self.context_manager = None

        # System prompt for V-Mart context
        self.system_prompt = """You are a highly intelligent AI assistant for V-Mart Retail. 
        Your role is to help with business decisions, data analysis, and daily operations.
        You should be professional, analytical, and provide actionable recommendations.
        Always consider V-Mart's retail context when providing responses.
        
        When provided with store location, weather, and competitor data, ALWAYS analyze:
        1. How weather conditions may affect customer footfall and sales
        2. Competitive pressure from nearby stores
        3. Location-specific opportunities and challenges
        4. Data-driven recommendations for optimizing performance
        
        Use a reasoning approach:
        - Break down complex questions into steps
        - Cite specific data points from the context
        - Explain your thought process
        - Provide actionable recommendations with clear rationale"""

    def get_response(
        self,
        prompt: str,
        use_context: bool = True,
        analytics_context: Optional[str] = None,
        store_id: Optional[str] = None,
        city: Optional[str] = None,
        include_weather: bool = True,
        include_competitors: bool = True,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Gets a response from the Gemini LLM with context awareness and retry logic.

        Args:
            prompt (str): The prompt to send to the LLM.
            use_context (bool): Whether to use conversation history.
            analytics_context (str): Optional analytics data context to include.
            store_id (str): Optional store ID to include location/weather/competitor context.
            city (str): Optional city name for city-level context.
            include_weather (bool): Include weather data in context.
            include_competitors (bool): Include competitor data in context.
            progress_callback (Callable): Optional callback function for progress updates.

        Returns:
            str: The response from the LLM.
        """
        max_retries = 5
        base_delay = 2  # Start with 2 seconds

        def send_progress(message: str):
            """Send progress update if callback is provided"""
            if progress_callback:
                progress_callback(message)

        for attempt in range(max_retries):
            try:
                send_progress("🔄 Gathering context data...")

                # Build full prompt with all contexts
                prompt_parts = [self.system_prompt]

                # Add store/weather/competitor context if requested
                if self.context_manager and (store_id or city):
                    send_progress("📍 Loading store location data...")

                    if store_id:
                        context_str = self.context_manager.format_context_for_ai(
                            store_id=store_id
                        )
                        if context_str:
                            prompt_parts.append(context_str)
                            send_progress("✅ Store context loaded")
                    elif city:
                        context_str = self.context_manager.format_context_for_ai(
                            city=city
                        )
                        if context_str:
                            prompt_parts.append(context_str)
                            send_progress("✅ City context loaded")

                # Add analytics context if provided
                if analytics_context:
                    send_progress("📊 Loading analytics data...")
                    prompt_parts.append(
                        "\n=== CURRENT ANALYTICS DATA ===\n"
                        + analytics_context
                        + "\n=== END ANALYTICS DATA ===\n"
                    )
                    prompt_parts.append(
                        "Use the analytics data above to provide data-driven insights and recommendations. "
                        "Cite specific numbers and trends from the data when making recommendations."
                    )
                    send_progress("✅ Analytics data loaded")

                # Add conversation history if requested
                if use_context and self.conversation_history:
                    send_progress("💭 Loading conversation history...")
                    context = self._build_context()
                    prompt_parts.append(f"\nPrevious conversation:\n{context}")

                # Add user prompt
                prompt_parts.append(f"\nUser: {prompt}")
                prompt_parts.append(
                    "\nProvide your response with clear reasoning, citing specific data points from the context. "
                    "Break down complex analysis into steps."
                )

                full_prompt = "\n".join(prompt_parts)

                send_progress("🤖 AI is analyzing your question...")
                send_progress("🧠 Applying reasoning to data...")

                response = self.chat_model.generate_content(full_prompt)
                response_text = response.text

                send_progress("✅ Analysis complete!")

                # Update conversation history
                self._update_history(prompt, response_text)

                return response_text

            except Exception as e:
                error_message = str(e)

                # Check if it's a rate limit error (429)
                if (
                    "429" in error_message
                    or "Resource exhausted" in error_message
                    or "quota" in error_message.lower()
                ):
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2s, 4s, 8s, 16s, 32s
                        delay = base_delay * (2**attempt)
                        print(
                            f"Rate limit hit. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(delay)
                        continue
                    else:
                        return "⚠️ Rate limit exceeded. The API is currently busy. Please try again in a few minutes.\n\nTip: Try reducing the frequency of requests or wait 60 seconds before trying again."
                else:
                    # For non-rate-limit errors, return immediately
                    return f"An error occurred: {error_message}"

        return "Maximum retry attempts reached. Please try again later."

    def analyze_data(self, data: str, analysis_type: str = "general") -> str:
        """
        Analyzes complex data and provides recommendations.

        Args:
            data (str): The data to analyze.
            analysis_type (str): Type of analysis (general, financial, sales, inventory)

        Returns:
            str: The analysis and recommendations.
        """
        analysis_prompts = {
            "general": "Analyze the following data and provide comprehensive insights and recommendations for V-Mart Retail:",
            "financial": "Perform a detailed financial analysis of the following data for V-Mart Retail, including profitability, trends, and recommendations:",
            "sales": "Analyze the sales data below for V-Mart Retail, identify patterns, trends, and provide actionable recommendations:",
            "inventory": "Analyze the inventory data for V-Mart Retail, identify overstocking/understocking issues, and provide recommendations:",
        }

        prompt = f"{analysis_prompts.get(analysis_type, analysis_prompts['general'])}\n\n{data}"
        return self.get_response(prompt, use_context=False)

    def reasoning_task(self, task_description: str, data: Optional[str] = None) -> Dict:
        """
        Performs complex reasoning tasks with step-by-step analysis.

        Args:
            task_description (str): Description of the task.
            data (str): Optional data to use in reasoning.

        Returns:
            Dict: Structured reasoning response with steps and conclusion.
        """
        prompt = f"""Perform the following task with detailed step-by-step reasoning:
        
Task: {task_description}
{f"Data: {data}" if data else ""}

Provide your response in the following JSON format:
{{
    "steps": ["step 1 description", "step 2 description", ...],
    "analysis": "detailed analysis",
    "recommendation": "actionable recommendation",
    "risks": ["potential risk 1", "potential risk 2", ...],
    "conclusion": "final conclusion"
}}"""

        try:
            response = self.get_response(prompt, use_context=False)
            # Try to parse JSON response
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # If not valid JSON, return structured text
                return {"raw_response": response, "status": "unstructured"}
        except Exception as e:
            return {"error": str(e)}

    def summarize_document(
        self, document_text: str, summary_type: str = "brief"
    ) -> str:
        """
        Summarizes a document.

        Args:
            document_text (str): The document text to summarize.
            summary_type (str): Type of summary (brief, detailed, executive)

        Returns:
            str: The summary.
        """
        summary_instructions = {
            "brief": "Provide a brief 2-3 sentence summary of the following document:",
            "detailed": "Provide a detailed summary of the following document, covering all key points:",
            "executive": "Provide an executive summary suitable for V-Mart leadership, highlighting key insights and recommendations:",
        }

        prompt = f"{summary_instructions.get(summary_type, summary_instructions['brief'])}\n\n{document_text}"
        return self.get_response(prompt, use_context=False)

    def extract_insights(
        self, data: str, focus_area: Optional[str] = None
    ) -> List[str]:
        """
        Extracts key insights from data.

        Args:
            data (str): The data to analyze.
            focus_area (str): Optional focus area (e.g., "sales", "customer behavior")

        Returns:
            List[str]: List of key insights.
        """
        prompt = f"""Extract key insights from the following data{f" focusing on {focus_area}" if focus_area else ""}:

{data}

Provide insights as a numbered list, with each insight being clear and actionable."""

        response = self.get_response(prompt, use_context=False)
        # Parse numbered list
        insights = [
            line.strip()
            for line in response.split("\n")
            if line.strip() and line[0].isdigit()
        ]
        return insights

    def decision_support(self, decision: str, context: str, options: List[str]) -> Dict:
        """
        Provides decision support with pros/cons analysis.

        Args:
            decision (str): The decision to be made.
            context (str): Context and background information.
            options (List[str]): List of options to consider.

        Returns:
            Dict: Structured decision analysis.
        """
        options_text = "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(options)])

        prompt = f"""Help make the following business decision for V-Mart Retail:

Decision: {decision}

Context: {context}

Options:
{options_text}

Analyze each option with:
- Pros and Cons
- Impact assessment
- Risk level
- Recommended option with justification"""

        response = self.get_response(prompt, use_context=False)
        return {"analysis": response}

    def clear_history(self):
        """Clears conversation history."""
        self.conversation_history = []

    def _build_context(self) -> str:
        """Builds context string from conversation history."""
        context_parts = []
        for entry in self.conversation_history[-self.max_history :]:
            context_parts.append(f"User: {entry['user']}")
            context_parts.append(f"Assistant: {entry['assistant']}")
        return "\n".join(context_parts)

    def _update_history(self, user_message: str, assistant_message: str):
        """Updates conversation history."""
        self.conversation_history.append(
            {"user": user_message, "assistant": assistant_message}
        )

        # Trim history if too long
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history :]
