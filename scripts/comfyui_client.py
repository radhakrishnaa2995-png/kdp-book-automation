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
        with request.urlopen(http_request, timeout=self.timeout) as response:
            data = response.read().decode("utf-8")
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
                template_text = Path(self.workflow_path).read_text(encoding="utf-8")
                self._workflow_template = json.loads(template_text)
            return _replace_prompt_tokens(self._workflow_template, prompt)
        return _default_workflow(prompt=prompt, checkpoint_name=self.checkpoint_name)

    def render_theme_clipart(self, theme: str) -> str | None:
        if theme in self._cache:
            return self._cache[theme]

        prompt_text = (
            f"children book style cute clipart stickers about {theme}, white transparent background, colorful, simple"
        )
        workflow = self._workflow_for_prompt(prompt_text)
        response = self._request_json("/prompt", {"prompt": workflow, "client_id": self.client_id})
        prompt_id = response.get("prompt_id")
        if not prompt_id:
            return None

        prompt_history = {}
        for _ in range(24):
            history = self._request_json(f"/history/{prompt_id}")
            prompt_history = history.get(prompt_id, {})
            if prompt_history.get("outputs"):
                break
            time.sleep(0.5)
        outputs = prompt_history.get("outputs", {})
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
        return None
