import bentoml
from bentoml.io import JSON, Image
from PIL import Image as PILImage

svc = bentoml.Service("text_to_image_service")

@svc.api(input=JSON(), output=Image())
def generate(data: dict) -> PILImage.Image:
    """Generate an image from a text prompt.

    This implementation returns a placeholder image. Replace the body with your
    text-to-image model inference code.
    """
    prompt = data.get("prompt", "")
    # TODO: integrate real text-to-image model using `prompt`
    img = PILImage.new("RGB", (512, 512), color="white")
    return img
