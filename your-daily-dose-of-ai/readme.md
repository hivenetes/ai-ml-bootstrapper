# Your Daily Dose of AI

This project is part of the [AI/ML Bootstrapper](https://github.com/hivenetes/ai-ml-bootstrapper) repository. 

A Streamlit application that creates AI-powered audio podcasts from web content and custom URLs. The application scrapes content, generates summaries, and converts them into audio format for easy consumption.

## Features

### 1. Listen to AI Doses
- Browse and play audio podcasts organized by date
- Audio player with standard playback controls
- Clear organization of content with dates and timestamps

### 2. Create a New AI Dose
- **Create Today's Podcast**: Automatically generates a podcast from today's AI news and updates
- **Custom URL Management**:
  - Add URLs of your choice to include in podcasts
  - View list of saved URLs with addition dates
  - Delete URLs that are no longer needed
- **Create from Saved URLs**: Generate podcasts specifically from your saved URLs

### 3. Manage AI Doses
- View all generated podcasts with creation dates and times
- Delete unwanted podcasts and their associated report files
- Organized display with easy-to-use controls

## Installation

1. Clone the repository:

git clone https://github.com/hivenetes/ai-ml-bootstrapper.git

2. Navigate to the project directory:

cd your-daily-dose-of-ai

3. Install required packages:

pip install -r requirements.txt

4. Set up environment variables:  
Copy `.env.example` file and create a `.env` file in the root directory and update API keys.  
[Here](https://docs.digitalocean.com/products/genai-platform/how-to/manage-ai-agent/create-agent) you can find details about creating Agent in GenAI Platform.

## Usage

1. Start the Streamlit application:

streamlit run main.py

2. Access the application in your web browser at `http://localhost:8501` (Or click the URL in the terminal)

## Project Structure

```
├── main.py                          # Main Streamlit application
├── database.py                      # SQLite database operations
├── src                              # Source files
   ├── get_daily_updates.py          # Run the flow
   ├── daily_updates_urls_finder.py  # URL finding and listing
   ├── daily_updates_scraper.py      # URL scraper and highlights generator
   ├── daily_updates_podcaster.py    # Audio file creator
   ├── database.py                   # Handle database operations
├── audio_files/                     # Directory for generated audio files
└── custom_urls.db                   # SQLite database for custom URLs
```

## Dependencies

- Python 3.10+
- Streamlit
- SQLite3
- gTTS (Google Text-to-Speech)
- Other dependencies listed in requirements.txt

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- GenAI Platform for LLama Models
- OpenAI for GPT models
- Streamlit for the web framework
- Google Text-to-Speech for audio generation
