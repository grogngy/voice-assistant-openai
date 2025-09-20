import os
from dotenv import load_dotenv
load_dotenv()
from google.cloud import speech, texttospeech
from openai import OpenAI

def speech_to_text(audio_file_path):
    from google.cloud import speech

    client = speech.SpeechClient()
    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()
    print(f"[STT] Audio file read, {len(content)} bytes")
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,  # Match browser recording
        sample_rate_hertz=48000,                                    # Match browser recording
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    print(f"[STT] Google API response: {response}")
    if response.results:
        transcript = response.results[0].alternatives[0].transcript
        print(f"[STT] Recognized transcript: '{transcript}'")
        return transcript
    print("[STT] No transcript recognized.")
    return ""

def text_to_speech(text, output_path="output.mp3", voice_option=""):
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Default to a high-quality Google voice if none selected
    voice_params = {
        "default": {"language_code": "en-US", "name": "en-US-Wavenet-D", "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL},
        "en-US-Wavenet-D": {"language_code": "en-US", "name": "en-US-Wavenet-D", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
        "en-US-Wavenet-F": {"language_code": "en-US", "name": "en-US-Wavenet-F", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
        "en-GB-Wavenet-B": {"language_code": "en-GB", "name": "en-GB-Wavenet-B", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
        "en-GB-Wavenet-A": {"language_code": "en-GB", "name": "en-GB-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
        "es-ES-Wavenet-B": {"language_code": "es-ES", "name": "es-ES-Wavenet-B", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
        "es-ES-Wavenet-A": {"language_code": "es-ES", "name": "es-ES-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
        "es-US-Wavenet-B": {"language_code": "es-US", "name": "es-US-Wavenet-B", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
        "es-US-Wavenet-A": {"language_code": "es-US", "name": "es-US-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
        "es-MX-Wavenet-B": {"language_code": "es-MX", "name": "es-MX-Wavenet-B", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
        "es-MX-Wavenet-A": {"language_code": "es-MX", "name": "es-MX-Wavenet-A", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    }

    # Use the selected voice if available, else default
    params = voice_params.get(voice_option, voice_params["default"])
    voice = texttospeech.VoiceSelectionParams(
        language_code=params["language_code"],
        name=params["name"],
        ssml_gender=params["ssml_gender"]
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    return output_path


def openai_process_message(user_message):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables.")
    openai_client = OpenAI(api_key=openai_api_key)

    company_info = '''IdentIA Lab: A Human-Centric AI & Digital Transformation Partner\n\nIntroduction:\nIdentIA Lab is a laboratory of ideas, creativity, and artificial intelligence that functions as a human-centric digital transformation partner. Based in Bogotá, Colombia, our core mission is to deliver intelligent and human-focused solutions that empower individuals and businesses to grow, automate, and scale effectively. We are not a traditional agency; we are strategic allies dedicated to achieving our clients' goals by merging human creativity with advanced technology.\n\nCore Philosophy: Human + AI Synergy\nAt the heart of IdentIA Lab is the principle of "Human + AI." We believe that artificial intelligence is a powerful creative partner that augments and enhances human potential, rather than replacing it. Our approach ensures that every solution—from web design to digital marketing—is built on a foundation of human-centric design, enhanced by the efficiency and power of AI. Our cultural manifesto is clear: technology serves to potentate human creativity and connection.\n\nClient Partnership & Value Delivery:\nWe view our clients as strategic allies, not just customers. Our process is built on deep collaboration, where we immerse ourselves in your projects and vision as if they were our own. This partnership begins with education and is sustained by trust, using clear metrics and KPIs to guide our decisions.\nA key differentiator is our value-driven model. We deliver constant, tangible value rather than billing by the hour. Through agile, sprint-based planning, we provide useful results every week—including designs, content, web improvements, and progress reports—ensuring your project evolves and scales with your business needs.\n\nKey Principles & Non-Negotiables:\nOur identity is built on a foundation of authenticity, innovation, and human connection. We do not follow fleeting trends; we reinterpret them to create unique value. Our commitment to quality is unwavering, guided by several non-negotiables:\n* Clarity and Purpose: All communication must be clear and purposeful.\n* Authenticity: We avoid empty, fashionable formulas in favor of genuine solutions.\n* Data-Driven Decisions: We operate on a foundation of metrics and continuous learning.\n* Creative Disruption: We explore new forms of narrative and avoid imitation.\n* Consistency: We maintain visual and strategic unity across all efforts.\n\nServices:\nOur integrated services are designed to build a powerful and cohesive digital presence:\n* Web Design: We create websites optimized for conversion and brand identity, featuring responsive UX, chatbots, and automation.\n* Digital Marketing: Our automated, omnichannel strategies are powered by predictive analysis, AI, and real-world data.\n* Virtual Agents: We integrate intelligent chatbots and virtual agents to enhance customer service and streamline processes.\n* Events: We develop compelling brand narratives for events, activations, and conferences, supported by cutting-edge digital production.\n* Consulting: We start by deeply understanding your goals, audience, and market context to build a successful strategy.\n\nVision:\nOur vision is to become a leading benchmark for digital transformation with a human face in Latin America, fostering a community where creative, educational, and strategic content inspires growth and innovation.'''

    # Prepend company info as context for RAG
    system_prompt = f"""You are a helpful assistant for IdentIA Lab. Use the following company information to answer questions about IdentIA Lab.\n\n{company_info}\n\nUser: {{user_message}}"""
    full_prompt = system_prompt.format(user_message=user_message)
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=256,
        temperature=0.7,
    )
    print("OpenAI response:", response)
    return response.choices[0].message.content.strip()