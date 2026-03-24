from __future__ import annotations

import json
import random
import tempfile
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict
from urllib import parse, request
import time
from urllib.error import URLError, HTTPError


def _replace_prompt_tokens(value, prompt: str):
    if isinstance(value, str):
        return value.replace("{{prompt}}", prompt)
    if isinstance(value, list):
        return [_replace_prompt_tokens(item, prompt) for item in value]
    if isinstance(value, dict):
        return {key: _replace_prompt_tokens(item, prompt) for key, item in value.items()}
    return value


def _default_workflow(prompt: str, checkpoint_name: str) -> dict:
    seed = random.randint(1, 2**31 - 1)
    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": 20,
                "cfg": 7,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            },
        },
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": checkpoint_name}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 384, "height": 384, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": "blurry, text, watermark, logo, frame", "clip": ["4", 1]},
        },
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "kdp_theme", "images": ["8", 0]}},
    }


def _looks_like_api_workflow(workflow: dict) -> bool:
    if not isinstance(workflow, dict) or not workflow:
        return False
    sample_value = next(iter(workflow.values()))
    return isinstance(sample_value, dict) and "class_type" in sample_value and "inputs" in sample_value


@dataclass
class ComfyUIClient:
    base_url: str
    workflow_path: str | None = None
    checkpoint_name: str = "v1-5-pruned-emaonly.ckpt"
    timeout: float = 120.0
    client_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _cache: Dict[str, str] = field(default_factory=dict)
    _workflow_template: dict | None = None

    def _request_json(self, path: str, body: dict | None = None) -> dict:
        url = f"{self.base_url.rstrip('/')}{path}"
        payload = None if body is None else json.dumps(body).encode("utf-8")
        http_request = request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST" if body is not None else "GET",
        )
        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                data = response.read().decode("utf-8")
        except HTTPError as exc:
            raise RuntimeError(f"ComfyUI HTTP error {exc.code} on {path}") from exc
        except URLError as exc:
            raise RuntimeError(
                f"Cannot reach ComfyUI at {self.base_url}. Is ComfyUI running with API enabled?"
            ) from exc
        return json.loads(data)

    def _download_image(self, filename: str, subfolder: str = "", filetype: str = "output") -> str:
        query = parse.urlencode({"filename": filename, "subfolder": subfolder, "type": filetype})
        url = f"{self.base_url.rstrip('/')}/view?{query}"
        destination = Path(tempfile.gettempdir()) / f"kdp_{uuid.uuid4().hex}.png"
        with request.urlopen(url, timeout=self.timeout) as response:
            destination.write_bytes(response.read())
        return str(destination)

    def _workflow_for_prompt(self, prompt: str) -> dict:
        if self.workflow_path:
            if self._workflow_template is None:
                if not Path(self.workflow_path).exists():
                    raise FileNotFoundError(f"ComfyUI workflow file not found: {self.workflow_path}")
                template_text = Path(self.workflow_path).read_text(encoding="utf-8")
                self._workflow_template = json.loads(template_text)
            workflow = _replace_prompt_tokens(self._workflow_template, prompt)
            if not _looks_like_api_workflow(workflow):
                if isinstance(workflow, dict) and "nodes" in workflow:
                    raise RuntimeError(
                        "Workflow JSON is not in ComfyUI API format. Export with 'Save (API format)' in ComfyUI."
                    )
                raise RuntimeError("Workflow JSON is invalid. Expected ComfyUI API format prompt dictionary.")
            return workflow
        return _default_workflow(prompt=prompt, checkpoint_name=self.checkpoint_name)

    def validate_connection(self) -> None:
        self._request_json("/object_info")

    def render_theme_clipart(self, theme: str) -> str | None:
        if theme in self._cache:
            return self._cache[theme]

        prompt_text = (
            f"children book style cute clipart stickers about {theme}, white transparent background, colorful, simple"
        )
        workflow = self._workflow_for_prompt(prompt_text)
        response = self._request_json("/prompt", {"prompt": workflow, "client_id": self.client_id})
        if response.get("error"):
            raise RuntimeError(f"ComfyUI prompt error: {response['error']}")
        prompt_id = response.get("prompt_id")
        if not prompt_id:
            raise RuntimeError("ComfyUI did not return a prompt_id.")

        prompt_history = {}
        for _ in range(120):
            history = self._request_json(f"/history/{prompt_id}")
            prompt_history = history.get(prompt_id, {})
            if prompt_history.get("outputs"):
                break
            status = prompt_history.get("status", {}).get("status_str")
            if status == "error":
                messages = prompt_history.get("status", {}).get("messages", [])
                raise RuntimeError(f"ComfyUI generation failed: {messages}")
            time.sleep(1.0)
        outputs = prompt_history.get("outputs", {})
        if not outputs:
            raise RuntimeError("ComfyUI finished without image outputs. Check workflow SaveImage node and model paths.")
        for node_output in outputs.values():
            images = node_output.get("images", [])
            if not images:
                continue
            image = images[0]
            filename = image.get("filename")
            if not filename:
                continue
            path = self._download_image(
                filename=filename,
                subfolder=image.get("subfolder", ""),
                filetype=image.get("type", "output"),
            )
            self._cache[theme] = path
            return path
        raise RuntimeError("ComfyUI output did not include any image entries.")
