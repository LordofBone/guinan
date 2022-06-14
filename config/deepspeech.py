from pathlib import Path

model_path = Path(__file__).parent.parent / f"models/"
file_path = Path(__file__).parent.parent / f"audio/recording.wav"

model = model_path / "deepspeech-0.9.3-models.pbmm"
scorer = model_path / "deepspeech-0.9.3-models.scorer"

beam_width = None
lm_alpha = None
lm_beta = None
hot_words = None
extended_output = False
json_output = False
candidate_transcripts = 3
