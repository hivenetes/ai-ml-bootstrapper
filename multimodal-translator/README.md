# Real-time Speech Translation Web Interface

This guide provides steps for setting up a real-time speech translation web interface that combines Automatic Speech Recognition (ASR) and Neural Machine Translation (NMT) services to provide instant translations in multiple languages.

![web interface](web.png)

## Prerequisites

Before setting up this project, you need to have:

1. **ASR Server**: Follow the setup instructions in [ai-ml-bootstrapper/automatic-speech-recognition](../automatic-speech-recognition/README.md)
2. **Language Translator Server**: Follow the setup instructions in [ai-ml-bootstrapper/language-translator](../language-translator/README.md)
3. **Client Dependencies**:
   - Python 3.8+
   - Node.js 16+
   - npm 8+

## Project Setup

1. **Install Python Dependencies**:

   ```bash
   pip3 install nvidia-riva-client PyAudio
   ```

2. **Install Web App Dependencies**:

   ```bash
   cd web
   npm install
   ```

## Project Structure

```
real-time-translator/
├── translations/          # Directory for translation JSON files
├── web/                  # React web application
│   ├── src/
│   │   ├── components/
│   │   └── ...
├── speech_translator.py  # Multi-language translation script
└── README.md
```

## Running the Application

1. **Start the Translation Script**:

   Run the speech translator with your desired target languages. Replace `<asr-ip>` and `<nmt-ip>` with your server IPs:

   ```bash
   python3 speech_translator.py \
     --asr-server <asr-ip>:50051 \
     --nmt-server <nmt-ip>:50051 \
     --input-device 2 \
     --source-lang en-US \
     --target-langs de,fr,es \
     --output-dir translations
   ```

   To list available audio input devices:
   ```bash
   python3 speech_translator.py --list-devices
   ```

2. **Start the Web Interface**:

   ```bash
   cd web
   npm run dev
   ```

   The web interface will be available at `http://localhost:5173`

## Supported Languages

The system supports translation between the following languages:

| Language    | Code | Language    | Code |
|-------------|------|-------------|------|
| Arabic      | ar   | Japanese    | ja   |
| Bulgarian   | bg   | Korean      | ko   |
| Czech       | cs   | Lithuanian  | lt   |
| Danish      | da   | Latvian     | lv   |
| German      | de   | Dutch       | nl   |
| Greek       | el   | Norwegian   | no   |
| English     | en   | Polish      | pl   |
| Spanish     | es   | Portuguese  | pt   |
| Estonian    | et   | Romanian    | ro   |
| Finnish     | fi   | Russian     | ru   |
| French      | fr   | Slovak      | sk   |
| Hindi       | hi   | Slovenian   | sl   |
| Croatian    | hr   | Swedish     | sv   |
| Hungarian   | hu   | Turkish     | tr   |
| Indonesian  | id   | Ukrainian   | uk   |
| Italian     | it   | Vietnamese  | vi   |
| Chinese     | zh   |             |      |

## Features

- Real-time speech recognition
- Concurrent translation to multiple languages
- Modern web interface with dark mode
- Language search functionality
- Responsive design for mobile and desktop
- Full-screen translation display
- Easy language switching

## Technical Details

The application consists of two main components:

1. **Speech Translator Script (`speech_translator.py`)**:
   - Captures audio input using PyAudio
   - Streams audio to ASR service
   - Concurrently translates text to multiple languages
   - Writes translations to JSON files

2. **Web Interface (`web/`)**:
   - React-based frontend
   - Real-time updates using file polling
   - Tailwind CSS for styling
   - Responsive design
   - Language selection interface

## Troubleshooting

1. **Audio Device Issues**:
   - List available devices using `--list-devices`
   - Ensure microphone permissions are granted
   - Try different input devices if audio capture fails

2. **Translation Delays**:
   - Check network connectivity to ASR and NMT servers
   - Ensure both servers are running and accessible
   - Verify the correct ports are open

## Additional Resources

- [NVIDIA NGC Parakeet Documentation](https://build.nvidia.com/nvidia/parakeet-ctc-1_1b-asr/docker)
- [NVIDIA NGC MEGATRON-1B-NMT Documentation](https://build.nvidia.com/nvidia/megatron-1b-nmt/docker)
- [Original ASR Setup Guide](../automatic-speech-recognition/README.md)
- [Original Language Translator Setup Guide](../language-translator/README.md)