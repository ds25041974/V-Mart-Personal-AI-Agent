"""
Core Gemini Agent for V-Mart Personal AI Agent
Enhanced with reasoning capabilities, context management, and multi-modal support

Developed by: DSR
Inspired by: LA
Powered by: Gemini AI
"""

import json
from typing import Dict, List, Optional

import google.generativeai as genai


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

        # System prompt for V-Mart context
        self.system_prompt = """You are a highly intelligent AI assistant for V-Mart Retail. 
        Your role is to help with business decisions, data analysis, and daily operations.
        You should be professional, analytical, and provide actionable recommendations.
        Always consider V-Mart's retail context when providing responses."""

    def get_response(self, prompt: str, use_context: bool = True) -> str:
        """
        Gets a response from the Gemini LLM with context awareness.

        Args:
            prompt (str): The prompt to send to the LLM.
            use_context (bool): Whether to use conversation history.

        Returns:
            str: The response from the LLM.
        """
        try:
            if use_context and self.conversation_history:
                # Build context-aware prompt
                context = self._build_context()
                full_prompt = f"{self.system_prompt}\n\nPrevious conversation:\n{context}\n\nUser: {prompt}"
            else:
                full_prompt = f"{self.system_prompt}\n\nUser: {prompt}"

            response = self.chat_model.generate_content(full_prompt)
            response_text = response.text

            # Update conversation history
            self._update_history(prompt, response_text)

            return response_text
        except Exception as e:
            return f"An error occurred: {e}"

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
            except:
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
