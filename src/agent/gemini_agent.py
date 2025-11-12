"""
Core Gemini Agent for V-Mart Personal AI Agent
Enhanced with reasoning capabilities, context management, and multi-modal support

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import json
import time
from collections import deque
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

        # Rate limiting (15 requests per minute for free tier)
        self.request_times = deque(maxlen=15)  # Track last 15 requests
        self.min_delay_between_requests = (
            4.5  # 4.5 seconds = ~13 requests/minute (safer than 15/min)
        )

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
        self.system_prompt = """You are the Gemini AI Insights Analyzer for V-Mart Retail.
        Your role is to provide tightly integrated, comprehensive analysis of business data.
        
        CORE CAPABILITIES:
        ✓ Cross-file correlation analysis (merge data across multiple files using common keys)
        ✓ Duplicate detection and elimination (identify and merge duplicate entries)
        ✓ Data curation and validation (ensure accuracy, completeness, consistency)
        ✓ Pattern recognition across datasets (find insights that emerge from correlating data)
        ✓ Actionable recommendations with clear rationale
        
        ANALYSIS METHODOLOGY:
        1. COMPREHENSIVE DATA READING:
           - Process ALL provided data completely (never skip sections)
           - Extract every relevant metric, value, and data point
           - Parse all columns, rows, and data structures thoroughly
        
        2. CROSS-FILE CORRELATION:
           - Identify common keys (Store_ID, Date, Product_ID, Location, etc.)
           - Merge and correlate data across multiple files
           - Build unified insights from combined datasets
           - Example: Match Store_101 sales from CSV with inventory from Excel
        
        3. DUPLICATE DETECTION & ELIMINATION:
           - Identify duplicate entries across all data sources
           - Merge duplicates intelligently (use most recent/complete/accurate)
           - Flag discrepancies in duplicate data
           - NEVER double-count metrics (sales, revenue, inventory)
        
        4. DATA CURATION:
           - Validate data integrity (check for missing values, outliers, inconsistencies)
           - Remove noise and focus on relevant metrics
           - Standardize formats (dates, currency, units)
           - Flag data quality issues explicitly
        
        5. INSIGHTS GENERATION:
           - Provide CRISP insights (clear, direct findings)
           - Deliver CURATED recommendations (relevant, prioritized, actionable)
           - Create CONCISE strategic actionables (3-5 key steps)
           - Include DETAILED summarization (comprehensive overview)
        
        6. CITATION & TRANSPARENCY:
           - Cite specific data points with file names and locations
           - Quote exact values (no approximations)
           - Clearly state when data is unavailable
           - Reference sources for every claim
        
        When analyzing weather + store data:
        - Correlate weather patterns with sales/footfall trends
        - Consider competitive pressure from nearby stores
        - Identify location-specific opportunities
        - Provide data-driven recommendations with clear rationale
        
        ALWAYS use a reasoning approach:
        - Break down complex questions into logical steps
        - Show your analytical process
        - Cite specific data points to support conclusions
        - Provide actionable recommendations with expected outcomes"""

    def _check_rate_limit(self) -> float:
        """
        Check if we're hitting rate limits and return delay needed.

        Returns:
            float: Number of seconds to wait (0 if no wait needed)
        """
        current_time = time.time()

        # Remove requests older than 60 seconds
        while self.request_times and (current_time - self.request_times[0]) > 60:
            self.request_times.popleft()

        # If we have 15 requests in the last 60 seconds, wait
        if len(self.request_times) >= 15:
            oldest_request = self.request_times[0]
            wait_time = 60 - (current_time - oldest_request)
            return max(wait_time, 0)

        # Check minimum delay between consecutive requests
        if self.request_times:
            last_request = self.request_times[-1]
            time_since_last = current_time - last_request
            if time_since_last < self.min_delay_between_requests:
                return self.min_delay_between_requests - time_since_last

        return 0

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
        max_retries = 3  # Reduced to 3 for faster failure feedback
        base_delay = 2  # 2 seconds base delay

        def send_progress(message: str):
            """Send progress update if callback is provided"""
            if progress_callback:
                progress_callback(message)

        for attempt in range(max_retries):
            try:
                # Check rate limit before making request
                wait_time = self._check_rate_limit()
                if wait_time > 0:
                    send_progress(
                        f"⏳ Rate limit protection: waiting {wait_time:.1f} seconds..."
                    )
                    time.sleep(wait_time)

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

                # Record request time for rate limiting
                self.request_times.append(time.time())

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
                    or "rate limit" in error_message.lower()
                    or "busy" in error_message.lower()
                ):
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2s, 4s, 8s
                        delay = base_delay * (2**attempt)
                        send_progress(
                            f"⏳ API busy, retrying in {delay}s... (attempt {attempt + 1}/{max_retries})"
                        )
                        print(
                            f"⚠️  Rate limit detected. Auto-retry in {delay}s (Attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(delay)
                        send_progress("🔄 Retrying...")
                        continue
                    else:
                        # After all retries exhausted - simpler message
                        return """⚠️ **Gemini API is Busy**

The API is experiencing high traffic right now. 

**Please wait 30-60 seconds and try again.**

💡 Tips:
- Simplify your question
- Break complex queries into smaller parts
- If analyzing files, try smaller samples

*Technical: Free tier allows 15 requests/minute, 1500/day*"""
                else:
                    # For non-rate-limit errors, return immediately
                    print(f"❌ Non-rate-limit error: {error_message}")
                    return f"**An error occurred:**\n\n{error_message}\n\nPlease try rephrasing your question or contact support if the issue persists."

        return """⚠️ **API Request Limit Reached**

Please wait 30-60 seconds before trying again.

The API is currently busy with high traffic."""

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
