### What is Guinan?
This is a project I have made built around Mozillas [DeepSpeech](https://github.com/mozilla/DeepSpeech) 
speech recognition engine.

This should work on both Windows x86_64 and Linux x86_64 but will not work on RPi OS 64 bit.

It is called Guinan based off of the Star Trek character, [Guinan](https://memory-alpha.fandom.com/wiki/Guinan).

##### What is DeepSpeech?
Deepspeech is a speech recognition engine that is built on top of Google's [TensorFlow](https://www.tensorflow.org/) 
framework.

It allows for local (offline) speech recognition, so you don't have to connect to an online API to perform decent 
speech recognition.

I have made this so that I can integrate into other projects such as my upcoming T-800 project. My previous projects 
[Nvidianator](https://www.hackster.io/314reactor/the-nvidianator-341f7a) and 
[EDITH glasses](https://www.hackster.io/314reactor/e-d-i-t-h-glasses-5604fa) used 
[wit.ai](https://wit.ai/) to perform speech recognition; which is effective; but of course requires API keys and
internet access.

##### Running Guinan
Run guinan/utils/model_dowloader.py to get the pre-trained conformer model.

Then you can run integrate_stt.py and seeing if it can translate speech to text (ensure you have a microphone).

##### Integrating Guinan into a project
Once cloned out from github, you can run the following command:

`pip install -e guinan/`

And this should install all dependencies.

You can then go into the folder guinan/utils and run model_dowloader.py to get the pre-trained conformer model.

Then you can run a test by running integrate_stt.py and seeing if it can translate speech to text 
(ensure you have a microphone).

Then this can be integrated into another program by importing run_stt_inference from integrate_stt.py:
`from guinan.integrate_stt import run_stt_inference`
Which can then be called from the program to record audio and get the text output.