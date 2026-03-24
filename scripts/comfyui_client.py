import requests
import time
import uuid

class ComfyUIClient:
    def __init__(self, base_url="http://127.0.0.1:8188"):
        self.base_url = base_url
        self.client_id = str(uuid.uuid4())
        self.checkpoint_name = "v1-5-pruned-emaonly.safetensors"  # ✅ FIXED

    def generate_image(self, workflow: dict, prompt_text: str) -> str:
        # Inject prompt dynamically
        for node in workflow.values():
            if "inputs" in node and "text" in node["inputs"]:
                if node["inputs"]["text"] == "{{prompt}}":
                    node["inputs"]["text"] = prompt_text

        # Send prompt
        response = requests.post(
            f"{self.base_url}/prompt",
            json={"prompt": workflow, "client_id": self.client_id}
        )

        if response.status_code != 200:
            raise RuntimeError(f"ComfyUI request failed: {response.text}")

        prompt_id = response.json()["prompt_id"]

        # Wait for result (increased reliability)
        for _ in range(60):  # ✅ FIXED
            history = requests.get(
                f"{self.base_url}/history/{prompt_id}"
            ).json()

            if prompt_id in history:
                outputs = history[prompt_id]["outputs"]

                for node_id in outputs:
                    node_output = outputs[node_id]
                    if "images" in node_output:
                        images = node_output["images"]
                        if images:
                            filename = images[0]["filename"]
                            return f"ComfyUI/output/{filename}"

            time.sleep(0.5)

        raise RuntimeError("Timeout: No image generated from ComfyUI")
