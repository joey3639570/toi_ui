# Text-to-Image UI

This repository provides a simple web UI for interacting with a text-to-image model served with BentoML.

## Running the Service

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Bento service:
   ```bash
   bentoml serve service:svc
   ```

The service exposes a `POST /generate` endpoint that accepts a JSON payload with a `prompt` field and returns an image.

## Using the UI

Open `ui/index.html` in your browser. Enter a prompt and submit. The page will call the API endpoint and display the generated image.

This project contains only a placeholder image generator. Integrate your text-to-image model inside `service.py` where noted.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
