"""
Tests for the Gemini Agent.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.agent.gemini_agent import GeminiAgent


class TestGeminiAgent(unittest.TestCase):
    @patch("google.generativeai.GenerativeModel")
    def test_get_response_success(self, mock_generative_model):
        """
        Tests a successful response from the Gemini agent.
        """
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value.text = "Hello, I am a bot."
        mock_generative_model.return_value = mock_model_instance

        agent = GeminiAgent(api_key="test_key")
        response = agent.get_response("Hello")

        self.assertEqual(response, "Hello, I am a bot.")
        mock_model_instance.generate_content.assert_called_once_with("Hello")

    @patch("google.generativeai.GenerativeModel")
    def test_get_response_error(self, mock_generative_model):
        """
        Tests an error response from the Gemini agent.
        """
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        mock_generative_model.return_value = mock_model_instance

        agent = GeminiAgent(api_key="test_key")
        response = agent.get_response("Hello")

        self.assertIn("An error occurred: API Error", response)


if __name__ == "__main__":
    unittest.main()
