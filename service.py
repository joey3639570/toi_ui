import bentoml
from PIL.Image import Image
from annotated_types import Le, Ge
from typing_extensions import Annotated
from starlette.middleware.cors import CORSMiddleware
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_ID = "stabilityai/sdxl-turbo"

sample_prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."

my_image = bentoml.images.PythonImage(python_version="3.11") \
            .requirements_file("requirements.txt")

@bentoml.service(
    image=my_image,
    traffic={"timeout": 300},
    workers=1,
    labels={'owner': 'bentoml-team', 'project': 'gallery'},
    resources={
        "gpu": 1,
        "gpu_type": "nvidia-l4",
    },
    cors={
        "allow_origins": ["*"],
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "allow_credentials": True,
    }
)
class SDXLTurbo:
    model_path = bentoml.models.HuggingFaceModel(MODEL_ID)

    def __init__(self) -> None:
        logger.info("Initializing SDXLTurbo service...")
        try:
            from diffusers import AutoPipelineForText2Image
            import torch

            logger.info("Loading model from %s", self.model_path)
            self.pipe = AutoPipelineForText2Image.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                variant="fp16",
            )
            logger.info("Moving model to CUDA device")
            self.pipe.to(device="cuda")
            logger.info("Service initialization completed successfully")
        except Exception as e:
            logger.error("Error during initialization: %s", str(e))
            raise

    @bentoml.api
    def txt2img(
            self,
            prompt: str = sample_prompt,
            num_inference_steps: Annotated[int, Ge(1), Le(10)] = 1,
            guidance_scale: float = 0.0,
    ) -> Image:
        logger.info("Received request with prompt: %s", prompt)
        try:
            image = self.pipe(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            ).images[0]
            logger.info("Successfully generated image")
            return image
        except Exception as e:
            logger.error("Error generating image: %s", str(e))
            raise
