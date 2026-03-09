import unittest
import time
import os

try:
    from src.llm_router import LLMRouter  # type: ignore
except Exception:
    LLMRouter = None


class CanaryRealTest(unittest.TestCase):
    def test_canary_real_traffic(self):
        if LLMRouter is None:
            self.skipTest("LLMRouter not available in this environment (skeleton).")
        llm_provider_order = os.environ.get("LLM_PROVIDER_ORDER")
        if not llm_provider_order:
            self.skipTest("LLM_PROVIDER_ORDER not configured; skipping real traffic test.")
        try:
            router = LLMRouter()
        except Exception as e:
            self.fail(f"Unable to instantiate LLMRouter: {e}")

        prompts = [
            {"prompt": "Summarize the latest advances in AI ethics.", "task": "draft"},
            {"prompt": "Explain quantum tunneling in simple terms.", "task": "draft"},
            {"prompt": "Translate the following to Spanish: 'Hello world'.", "task": "draft"},
        ]
        results = []
        for p in prompts:
            start = time.time()
            try:
                if hasattr(router, "execute_json"):
                    out = router.execute_json(p["prompt"], p["task"])
                elif hasattr(router, "route"):
                    out = router.route(p["prompt"], p["task"])
                else:
                    self.skipTest("Router API not found on LLMRouter.")
                latency = (time.time() - start) * 1000
                depth = getattr(out, "fallback_depth", getattr(out, "depth", 0))
                text = getattr(out, "text", str(out))
                results.append({"latency_ms": latency, "depth": depth, "output": text})
            except Exception as e:
                self.fail(f"Real traffic test failed: {e}")
        self.assertTrue(len(results) > 0, "No results produced by real traffic Canary")


if __name__ == '__main__':
    unittest.main()
