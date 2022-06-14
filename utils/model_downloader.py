import wget
from config.deepspeech import *
from utils.load_bar_non_iterable import progress_bar


@progress_bar(description="Downloading DeepSpeech models", leave=True, increments=10, ascii_bar=False,
              expected_time=180)
def download_models():
    model_url = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"
    response_model = wget.download(model_url, f"{model_path}/deepspeech-0.9.3-models.pbmm")

    scorer_url = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"
    response_scorer = wget.download(scorer_url, f"{model_path}/deepspeech-0.9.3-models.scorer")

    print(response_model)
    print(response_scorer)


if __name__ == "__main__":
    download_models()
