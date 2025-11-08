"""
AI Insights Engine
Provides intelligent analysis, insights, and recommendations using Gemini AI
"""

import json
import logging
from typing import Any, Dict, List, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)


class AIInsightsEngine:
    """AI-powered insights and recommendations engine"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.model = None
        self.model_name = "gemini-1.5-pro"

        if genai and api_key:
            self._initialize_model()

    def _initialize_model(self):
        """Initialize Gemini AI model"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Initialized Gemini model: {self.model_name}")

        except Exception as e:
            logger.error(f"Error initializing Gemini model: {str(e)}")
            self.model = None

    def set_api_key(self, api_key: str) -> bool:
        """Set Gemini API key"""
        try:
            self.api_key = api_key
            self._initialize_model()
            return self.model is not None

        except Exception as e:
            logger.error(f"Error setting API key: {str(e)}")
            return False

    def analyze_data(
        self, data: Any, data_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze data and provide insights"""
        try:
            if not self.model:
                return {
                    "error": "AI model not initialized. Please set API key.",
                    "insights": [],
                    "recommendations": [],
                }

            # Prepare data summary
            data_summary = self._prepare_data_summary(data, data_context)

            # Create analysis prompt
            prompt = self._create_analysis_prompt(data_summary, data_context)

            # Generate insights
            response = self.model.generate_content(prompt)

            # Parse response
            insights = self._parse_insights_response(response.text)

            logger.info(f"Generated {len(insights.get('insights', []))} insights")
            return insights

        except Exception as e:
            logger.error(f"Error analyzing data: {str(e)}")
            return {
                "error": str(e),
                "insights": [],
                "recommendations": [],
            }

    def _prepare_data_summary(
        self, data: Any, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Prepare a summary of the data for analysis"""
        try:
            summary_parts = []

            # Add context information
            if context:
                summary_parts.append("Data Context:")
                if "source" in context:
                    summary_parts.append(f"- Source: {context['source']}")
                if "query" in context:
                    summary_parts.append(f"- Query: {context['query']}")
                if "table" in context:
                    summary_parts.append(f"- Table: {context['table']}")
                if "database" in context:
                    summary_parts.append(f"- Database: {context['database']}")
                summary_parts.append("")

            # Analyze data structure
            if isinstance(data, list):
                summary_parts.append(f"Data Type: List with {len(data)} items")

                if len(data) > 0:
                    # Sample first few items
                    sample_size = min(5, len(data))
                    summary_parts.append(f"\nFirst {sample_size} items:")

                    for i, item in enumerate(data[:sample_size]):
                        if isinstance(item, dict):
                            summary_parts.append(f"\nItem {i + 1}:")
                            for key, value in list(item.items())[:10]:
                                summary_parts.append(f"  {key}: {value}")
                        else:
                            summary_parts.append(f"  {i + 1}. {item}")

                    # Add column information if dict
                    if isinstance(data[0], dict):
                        columns = list(data[0].keys())
                        summary_parts.append(
                            f"\nColumns ({len(columns)}): {', '.join(columns)}"
                        )

            elif isinstance(data, dict):
                summary_parts.append("Data Type: Dictionary")
                summary_parts.append(f"Keys ({len(data)}): {', '.join(data.keys())}")

                # Show sample values
                summary_parts.append("\nSample values:")
                for key, value in list(data.items())[:10]:
                    summary_parts.append(f"  {key}: {value}")

            else:
                summary_parts.append(f"Data Type: {type(data).__name__}")
                summary_parts.append(f"Value: {str(data)[:500]}")

            return "\n".join(summary_parts)

        except Exception as e:
            logger.error(f"Error preparing data summary: {str(e)}")
            return f"Data: {str(data)[:500]}"

    def _create_analysis_prompt(
        self, data_summary: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create prompt for data analysis"""
        prompt_parts = [
            "You are a data analyst AI. Analyze the following data and provide:",
            "1. Key insights and observations",
            "2. Patterns and trends",
            "3. Actionable recommendations",
            "4. Potential issues or anomalies",
            "",
            "Please structure your response as JSON with the following format:",
            "{",
            '  "summary": "Brief overview of the data",',
            '  "insights": [',
            '    {"type": "insight_type", "description": "insight description", "importance": "high/medium/low"}',
            "  ],",
            '  "trends": [',
            '    {"pattern": "pattern description", "confidence": "high/medium/low"}',
            "  ],",
            '  "recommendations": [',
            '    {"action": "recommended action", "rationale": "why this action", "priority": "high/medium/low"}',
            "  ],",
            '  "anomalies": [',
            '    {"description": "anomaly description", "severity": "high/medium/low"}',
            "  ]",
            "}",
            "",
            "Data to analyze:",
            data_summary,
        ]

        # Add user question if provided
        if context and "question" in context:
            prompt_parts.insert(5, f"\nUser Question: {context['question']}\n")

        return "\n".join(prompt_parts)

    def _parse_insights_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response into structured insights"""
        try:
            # Try to find JSON in response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_text = response_text[start_idx:end_idx]
                insights = json.loads(json_text)
                return insights

            # If no JSON found, create structured response from text
            return {
                "summary": "Analysis completed",
                "insights": [
                    {
                        "type": "general",
                        "description": response_text,
                        "importance": "medium",
                    }
                ],
                "trends": [],
                "recommendations": [],
                "anomalies": [],
            }

        except json.JSONDecodeError:
            logger.warning("Could not parse JSON response, using text format")
            return {
                "summary": response_text[:200],
                "insights": [
                    {
                        "type": "general",
                        "description": response_text,
                        "importance": "medium",
                    }
                ],
                "trends": [],
                "recommendations": [],
                "anomalies": [],
            }

        except Exception as e:
            logger.error(f"Error parsing insights response: {str(e)}")
            return {
                "error": str(e),
                "raw_response": response_text,
                "insights": [],
                "recommendations": [],
            }

    def answer_question(
        self, question: str, data: Any, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Answer a question about the data"""
        try:
            if not self.model:
                return "AI model not initialized. Please set API key."

            # Prepare data context
            data_summary = self._prepare_data_summary(data, context)

            # Create prompt
            prompt = [
                f"Question: {question}",
                "",
                "Data Context:",
                data_summary,
                "",
                "Please provide a clear, concise answer based on the data provided.",
            ]

            # Generate response
            response = self.model.generate_content("\n".join(prompt))

            logger.info(f"Answered question: {question[:50]}...")
            return response.text

        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return f"Error: {str(e)}"

    def generate_recommendations(
        self, data: Any, goal: str, context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on data and goal"""
        try:
            if not self.model:
                return [
                    {
                        "action": "Set API key",
                        "rationale": "AI model not initialized",
                        "priority": "high",
                    }
                ]

            # Prepare data
            data_summary = self._prepare_data_summary(data, context)

            # Create prompt
            prompt = [
                f"Goal: {goal}",
                "",
                "Based on the following data, provide actionable recommendations:",
                data_summary,
                "",
                "Please provide recommendations in JSON format:",
                "[",
                '  {"action": "recommended action", "rationale": "why", "priority": "high/medium/low", "expected_impact": "description"}',
                "]",
            ]

            # Generate recommendations
            response = self.model.generate_content("\n".join(prompt))

            # Parse response
            try:
                # Find JSON array in response
                start_idx = response.text.find("[")
                end_idx = response.text.rfind("]") + 1

                if start_idx != -1 and end_idx > start_idx:
                    json_text = response.text[start_idx:end_idx]
                    recommendations = json.loads(json_text)
                    logger.info(f"Generated {len(recommendations)} recommendations")
                    return recommendations

            except json.JSONDecodeError:
                pass

            # Fallback: parse text response
            return [
                {
                    "action": "Review analysis",
                    "rationale": response.text,
                    "priority": "medium",
                }
            ]

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return [{"action": "Error", "rationale": str(e), "priority": "high"}]

    def summarize_data(
        self, data: Any, max_length: int = 200, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a concise summary of the data"""
        try:
            if not self.model:
                return "AI model not initialized."

            # Prepare data
            data_summary = self._prepare_data_summary(data, context)

            # Create prompt
            prompt = [
                f"Summarize the following data in {max_length} words or less:",
                data_summary,
            ]

            # Generate summary
            response = self.model.generate_content("\n".join(prompt))

            logger.info("Generated data summary")
            return response.text

        except Exception as e:
            logger.error(f"Error summarizing data: {str(e)}")
            return f"Error: {str(e)}"
