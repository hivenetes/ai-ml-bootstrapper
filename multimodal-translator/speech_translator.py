import argparse
import queue
import threading
import time
import json
import os
import asyncio
from datetime import datetime
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

import riva.client
from riva.client.argparse_utils import add_asr_config_argparse_parameters, add_connection_argparse_parameters
import riva.client.audio_io

class LanguageTranslator:
    def __init__(self, nmt_server: str, target_lang: str, output_file: str, source_lang: str):
        self.nmt_auth = riva.client.Auth(None, False, nmt_server)
        self.nmt_client = riva.client.NeuralMachineTranslationClient(self.nmt_auth)
        self.target_lang = target_lang
        self.source_lang = source_lang
        self.output_file = output_file
        self.queue = queue.Queue()
        self.running = False

    def translate_text(self, text: str) -> None:
        """Translate text and write to file"""
        try:
            response = self.nmt_client.translate(
                [text], 
                "", 
                self.source_lang, 
                self.target_lang
            )
            
            translated_text = response.translations[0].text
            
            # Write to file
            data = {
                "timestamp": datetime.now().isoformat(),
                "original": text,
                "translated": translated_text,
                "source_lang": self.source_lang,
                "target_lang": self.target_lang
            }
            
            with open(self.output_file, 'w') as f:
                json.dump(data, f)
            
            print(f"\n[{self.target_lang}] Original: {text}")
            print(f"[{self.target_lang}] Translated: {translated_text}")
            
        except Exception as e:
            print(f"Translation error for {self.target_lang}: {str(e)}")

    def process_queue(self):
        """Process translations from the queue"""
        while self.running:
            try:
                text = self.queue.get(timeout=0.5)
                self.translate_text(text)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Queue processing error for {self.target_lang}: {str(e)}")

class MultiLanguageSpeechTranslator:
    def __init__(self, asr_server: str, nmt_server: str, input_device: int, 
                 target_langs: List[str], output_dir: str, sample_rate_hz: int = 16000, 
                 chunk_size: int = 1600, source_lang: str = 'en-US'):
        # ASR setup
        self.asr_auth = riva.client.Auth(None, False, asr_server)
        self.asr_service = riva.client.ASRService(self.asr_auth)
        
        # Configuration
        self.input_device = input_device
        self.sample_rate_hz = sample_rate_hz
        self.chunk_size = chunk_size
        self.source_lang = source_lang
        
        # Create translators for each target language
        self.translators: Dict[str, LanguageTranslator] = {}
        self.translator_threads = []
        
        for target_lang in target_langs:
            output_file = os.path.join(output_dir, f"{target_lang}.json")
            translator = LanguageTranslator(
                nmt_server=nmt_server,
                target_lang=target_lang,
                output_file=output_file,
                source_lang=source_lang
            )
            self.translators[target_lang] = translator

    def get_asr_config(self):
        return riva.client.StreamingRecognitionConfig(
            config=riva.client.RecognitionConfig(
                encoding=riva.client.AudioEncoding.LINEAR_PCM,
                language_code=self.source_lang,
                max_alternatives=1,
                enable_automatic_punctuation=True,
                sample_rate_hertz=self.sample_rate_hz,
                audio_channel_count=1,
            ),
            interim_results=False,
        )

    def handle_asr_response(self, responses):
        """Process ASR responses and distribute to all language queues simultaneously"""
        for response in responses:
            if not response.results:
                continue
                
            for result in response.results:
                if result.is_final:
                    transcript = result.alternatives[0].transcript
                    if transcript.strip():
                        # Send to all language queues simultaneously
                        for translator in self.translators.values():
                            translator.queue.put(transcript)

    def run(self):
        """Main method to start the speech translation pipeline"""
        # Start all translator threads
        for translator in self.translators.values():
            translator.running = True
            thread = threading.Thread(target=translator.process_queue)
            thread.start()
            self.translator_threads.append(thread)
        
        try:
            # Start microphone stream
            with riva.client.audio_io.MicrophoneStream(
                self.sample_rate_hz,
                self.chunk_size,
                device=self.input_device,
            ) as audio_stream:
                # Process audio stream
                responses = self.asr_service.streaming_response_generator(
                    audio_chunks=audio_stream,
                    streaming_config=self.get_asr_config(),
                )
                
                # Handle responses
                self.handle_asr_response(responses)
                
        except KeyboardInterrupt:
            print("\nStopping speech translation...")
        finally:
            # Stop all translators
            for translator in self.translators.values():
                translator.running = False
            
            # Wait for all threads to finish
            for thread in self.translator_threads:
                thread.join()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Concurrent multi-language real-time speech-to-text translation using Riva AI Services",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    default_device_info = riva.client.audio_io.get_default_input_device_info()
    default_device_index = None if default_device_info is None else default_device_info['index']
    
    parser.add_argument("--asr-server", type=str, required=True, help="ASR server address (host:port)")
    parser.add_argument("--nmt-server", type=str, required=True, help="NMT server address (host:port)")
    parser.add_argument("--input-device", type=int, default=default_device_index, help="Input audio device index")
    parser.add_argument("--source-lang", type=str, default="en-US", help="Source language code")
    parser.add_argument("--target-langs", type=str, required=True, help="Comma-separated list of target language codes")
    parser.add_argument("--output-dir", type=str, required=True, help="Output directory for translation files")
    parser.add_argument("--list-devices", action="store_true", help="List available input devices")
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.list_devices:
        riva.client.audio_io.list_input_devices()
        return
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Split target languages
    target_langs = [lang.strip() for lang in args.target_langs.split(',')]
    
    translator = MultiLanguageSpeechTranslator(
        asr_server=args.asr_server,
        nmt_server=args.nmt_server,
        input_device=args.input_device,
        target_langs=target_langs,
        output_dir=args.output_dir,
        source_lang=args.source_lang
    )
    
    print(f"Starting concurrent multi-language speech translation from {args.source_lang}")
    print(f"Target languages: {', '.join(target_langs)}")
    print(f"Writing translations to: {args.output_dir}")
    print("Speak into your microphone. Press Ctrl+C to stop.")
    print("-"*50)
    
    translator.run()

if __name__ == "__main__":
    main()