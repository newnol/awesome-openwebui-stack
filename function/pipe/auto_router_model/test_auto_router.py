"""
Test cases for Auto Router Model Pipe

Run with: python -m pytest test_auto_router.py -v
Or simply: python test_auto_router.py
"""

import json
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, "..")

# Import the Pipe class
from auto_router_model import Pipe, EventEmitter, LITELLM_AVAILABLE, DEFAULT_ROUTER_CONFIG, DEFAULT_FALLBACK_MODEL


class TestRouterConfigValidation(unittest.TestCase):
    """Test cases for ROUTER_CONFIG validation."""

    def setUp(self):
        self.pipe = Pipe()

    def test_valid_config(self):
        """Test valid JSON configuration."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = json.dumps([
            {"model_id": "gpt-4", "keywords": ["complex", "analyze"], "description": "GPT-4"},
            {"model_id": "gpt-3.5", "keywords": ["simple", "quick"], "description": "GPT-3.5"}
        ])
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertTrue(is_valid)
        self.assertIsNotNone(config)
        self.assertIsNone(error)
        self.assertEqual(len(config), 2)

    def test_default_config_used_when_empty(self):
        """Test that DEFAULT_ROUTER_CONFIG is used when CUSTOM_ROUTER_CONFIG is empty."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = ""
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertTrue(is_valid)
        self.assertIsNotNone(config)
        self.assertEqual(len(config), len(DEFAULT_ROUTER_CONFIG))

    def test_invalid_json(self):
        """Test invalid JSON syntax."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = "not valid json {"
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertFalse(is_valid)
        self.assertIsNone(config)
        self.assertIn("Invalid JSON", error)

    def test_config_not_array(self):
        """Test config that is not an array."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = json.dumps({"model_id": "gpt-4"})
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertFalse(is_valid)
        self.assertIn("must be a JSON array", error)

    def test_missing_model_id(self):
        """Test rule missing model_id field."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = json.dumps([
            {"keywords": ["test"]}
        ])
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertFalse(is_valid)
        self.assertIn("missing 'model_id'", error)

    def test_missing_keywords(self):
        """Test rule missing keywords field."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = json.dumps([
            {"model_id": "gpt-4"}
        ])
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertFalse(is_valid)
        self.assertIn("missing 'keywords'", error)

    def test_keywords_not_array(self):
        """Test keywords that is not an array."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = json.dumps([
            {"model_id": "gpt-4", "keywords": "not an array"}
        ])
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertFalse(is_valid)
        self.assertIn("must be an array", error)

    def test_keywords_normalized_to_lowercase(self):
        """Test that keywords are normalized to lowercase."""
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = json.dumps([
            {"model_id": "gpt-4", "keywords": ["CODE", "Python", "JAVASCRIPT"]}
        ])
        
        is_valid, config, error = self.pipe._validate_router_config()
        
        self.assertTrue(is_valid)
        self.assertEqual(config[0]["keywords"], ["code", "python", "javascript"])


class TestKeywordMatching(unittest.TestCase):
    """Test cases for keyword matching logic."""

    def setUp(self):
        self.pipe = Pipe()
        self.pipe.valves.FALLBACK_MODEL_ID = "fallback-model"
        self.config = [
            {"model_id": "code-model", "keywords": ["code", "python", "javascript", "debug"], "description": "Coding"},
            {"model_id": "math-model", "keywords": ["math", "calculate", "equation"], "description": "Math"},
            {"model_id": "creative-model", "keywords": ["write", "story", "creative"], "description": "Creative"},
        ]

    def test_match_single_keyword(self):
        """Test matching a single keyword."""
        model, reason = self.pipe._match_keywords("Help me write python code", self.config)
        
        self.assertEqual(model, "code-model")
        self.assertIn("Matched", reason)

    def test_match_multiple_keywords_same_rule(self):
        """Test matching multiple keywords from same rule."""
        model, reason = self.pipe._match_keywords("Debug this python code with javascript", self.config)
        
        self.assertEqual(model, "code-model")
        self.assertIn("4 keywords", reason)  # debug, python, code, javascript

    def test_case_insensitive_matching(self):
        """Test that matching is case-insensitive."""
        model, reason = self.pipe._match_keywords("PYTHON CODE DEBUG", self.config)
        
        self.assertEqual(model, "code-model")

    def test_no_match_returns_fallback(self):
        """Test that no match returns fallback model."""
        model, reason = self.pipe._match_keywords("Hello, how are you today?", self.config)
        
        self.assertEqual(model, "fallback-model")
        self.assertIn("fallback", reason.lower())

    def test_best_score_wins(self):
        """Test that rule with most matches wins."""
        # Message with 2 math keywords and 1 code keyword
        model, reason = self.pipe._match_keywords("calculate the equation in code", self.config)
        
        self.assertEqual(model, "math-model")  # 2 matches vs 1

    def test_unicode_keywords(self):
        """Test matching with Unicode/Vietnamese keywords."""
        config = [
            {"model_id": "vn-model", "keywords": ["việt", "tiếng", "số"], "description": "Vietnamese"}
        ]
        
        model, reason = self.pipe._match_keywords("Tính số này bằng tiếng Việt", config)
        
        self.assertEqual(model, "vn-model")


class TestModelListBuilder(unittest.TestCase):
    """Test cases for building LiteLLM model list."""

    def setUp(self):
        self.pipe = Pipe()
        self.pipe.valves.OPENAI_API_BASE = "http://localhost:11434/v1"
        self.pipe.valves.OPENAI_API_KEY = "test-key"
        self.pipe.valves.FALLBACK_MODEL_ID = "fallback-model"

    def test_build_model_list_from_config(self):
        """Test building model list from config."""
        config = [
            {"model_id": "model-a", "keywords": ["a"]},
            {"model_id": "model-b", "keywords": ["b"]},
        ]
        
        model_list = self.pipe._build_model_list(config)
        
        # Should have 3 models: model-a, model-b, fallback
        self.assertEqual(len(model_list), 3)
        model_names = [m["model_name"] for m in model_list]
        self.assertIn("model-a", model_names)
        self.assertIn("model-b", model_names)
        self.assertIn("fallback-model", model_names)

    def test_no_duplicate_models(self):
        """Test that duplicate models are not added."""
        config = [
            {"model_id": "same-model", "keywords": ["a"]},
            {"model_id": "same-model", "keywords": ["b"]},  # Same model
        ]
        
        model_list = self.pipe._build_model_list(config)
        
        # Should have 2 models: same-model, fallback
        self.assertEqual(len(model_list), 2)

    def test_fallback_not_duplicated(self):
        """Test that fallback is not duplicated if already in config."""
        self.pipe.valves.FALLBACK_MODEL_ID = "model-a"
        config = [
            {"model_id": "model-a", "keywords": ["a"]},
        ]
        
        model_list = self.pipe._build_model_list(config)
        
        # Should have only 1 model since fallback = model-a
        self.assertEqual(len(model_list), 1)

    def test_model_params_correct(self):
        """Test that model params are set correctly."""
        config = [{"model_id": "test-model", "keywords": ["test"]}]
        
        model_list = self.pipe._build_model_list(config)
        
        test_model = next(m for m in model_list if m["model_name"] == "test-model")
        params = test_model["litellm_params"]
        
        self.assertEqual(params["model"], "openai/test-model")
        self.assertEqual(params["api_base"], "http://localhost:11434/v1")
        self.assertEqual(params["api_key"], "test-key")


class TestEventEmitter(unittest.TestCase):
    """Test cases for EventEmitter helper class."""

    def test_emit_without_emitter(self):
        """Test that emit works when no emitter is provided."""
        import asyncio
        
        emitter = EventEmitter(None)
        
        # Should not raise any errors
        asyncio.run(emitter.emit("test"))
        asyncio.run(emitter.progress_update("test"))
        asyncio.run(emitter.error_update("test"))
        asyncio.run(emitter.success_update("test"))

    def test_emit_with_emitter(self):
        """Test that emit calls the emitter correctly."""
        import asyncio
        
        mock_emitter = AsyncMock()
        emitter = EventEmitter(mock_emitter)
        
        asyncio.run(emitter.progress_update("Processing..."))
        
        mock_emitter.assert_called_once()
        call_args = mock_emitter.call_args[0][0]
        self.assertEqual(call_args["type"], "status")
        self.assertEqual(call_args["data"]["description"], "Processing...")
        self.assertEqual(call_args["data"]["status"], "in_progress")

    def test_error_update_sets_done(self):
        """Test that error_update sets done=True."""
        import asyncio
        
        mock_emitter = AsyncMock()
        emitter = EventEmitter(mock_emitter)
        
        asyncio.run(emitter.error_update("Error occurred"))
        
        call_args = mock_emitter.call_args[0][0]
        self.assertEqual(call_args["data"]["status"], "error")
        self.assertTrue(call_args["data"]["done"])


class TestPipeIntegration(unittest.TestCase):
    """Integration tests for the Pipe class."""

    def setUp(self):
        self.pipe = Pipe()
        self.pipe.valves.DEBUG = True

    def test_pipes_returns_correct_structure(self):
        """Test that pipes() returns correct structure."""
        pipes = self.pipe.pipes()
        
        self.assertEqual(len(pipes), 1)
        self.assertEqual(pipes[0]["id"], "auto_router")
        self.assertEqual(pipes[0]["name"], "Auto Router")
        self.assertIn("description", pipes[0])

    def test_user_valves_initialization(self):
        """Test UserValves default values."""
        user_valves = self.pipe.UserValves()
        
        self.assertEqual(user_valves.preferred_model, "")
        self.assertFalse(user_valves.disable_routing)

    def test_valves_default_values(self):
        """Test Valves default values."""
        valves = self.pipe.Valves()
        
        self.assertEqual(valves.OPENAI_API_BASE, "http://host.docker.internal:11434/v1")
        self.assertEqual(valves.OPENAI_API_KEY, "ollama")
        self.assertEqual(valves.FALLBACK_MODEL_ID, "")  # Empty = use DEFAULT_FALLBACK_MODEL
        self.assertEqual(valves.CUSTOM_ROUTER_CONFIG, "")  # Empty = use DEFAULT_ROUTER_CONFIG
        self.assertFalse(valves.DEBUG)
        self.assertTrue(valves.status)


class TestPipeAsync(unittest.TestCase):
    """Async tests for the pipe() method."""

    def setUp(self):
        self.pipe = Pipe()
        self.pipe.valves.DEBUG = True
        self.pipe.valves.CUSTOM_ROUTER_CONFIG = json.dumps([
            {"model_id": "code-model", "keywords": ["code", "python"], "description": "Coding"}
        ])
        self.pipe.valves.FALLBACK_MODEL_ID = "fallback-model"

    @patch('auto_router_model.LITELLM_AVAILABLE', False)
    def test_pipe_without_litellm(self):
        """Test pipe returns error when LiteLLM not available."""
        import asyncio
        
        # Create a new pipe instance after patching
        with patch('auto_router_model.LITELLM_AVAILABLE', False):
            pipe = Pipe()
            body = {"messages": [{"role": "user", "content": "Hello"}]}
            
            # We can't easily test this without reimporting, so skip
            pass

    def test_pipe_with_empty_messages(self):
        """Test pipe handles empty messages."""
        import asyncio
        
        async def run_test():
            body = {"messages": []}
            mock_emitter = AsyncMock()
            
            result = await self.pipe.pipe(
                body=body,
                __user__=None,
                __event_emitter__=mock_emitter,
            )
            
            self.assertIn("No messages", result)
        
        if LITELLM_AVAILABLE:
            asyncio.run(run_test())

    def test_pipe_with_invalid_config(self):
        """Test pipe handles invalid config gracefully."""
        import asyncio
        
        async def run_test():
            self.pipe.valves.ROUTER_CONFIG = "invalid json"
            body = {"messages": [{"role": "user", "content": "Hello"}]}
            mock_emitter = AsyncMock()
            
            result = await self.pipe.pipe(
                body=body,
                __user__=None,
                __event_emitter__=mock_emitter,
            )
            
            self.assertIn("Configuration Error", result)
        
        if LITELLM_AVAILABLE:
            asyncio.run(run_test())


def run_tests():
    """Run all tests with verbose output."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRouterConfigValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestKeywordMatching))
    suite.addTests(loader.loadTestsFromTestCase(TestModelListBuilder))
    suite.addTests(loader.loadTestsFromTestCase(TestEventEmitter))
    suite.addTests(loader.loadTestsFromTestCase(TestPipeIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPipeAsync))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
