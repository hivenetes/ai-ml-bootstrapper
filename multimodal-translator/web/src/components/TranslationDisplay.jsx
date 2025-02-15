import { useState, useEffect } from 'react';
import { Globe2, ChevronUp, ChevronDown } from 'lucide-react';

const LANGUAGES = [
  { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
  { code: 'bg', name: 'Bulgarian', flag: '🇧🇬' },
  { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
  { code: 'hr', name: 'Croatian', flag: '🇭🇷' },
  { code: 'cs', name: 'Czech', flag: '🇨🇿' },
  { code: 'da', name: 'Danish', flag: '🇩🇰' },
  { code: 'nl', name: 'Dutch', flag: '🇳🇱' },
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'et', name: 'Estonian', flag: '🇪🇪' },
  { code: 'fi', name: 'Finnish', flag: '🇫🇮' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'el', name: 'Greek', flag: '🇬🇷' },
  { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'hu', name: 'Hungarian', flag: '🇭🇺' },
  { code: 'id', name: 'Indonesian', flag: '🇮🇩' },
  { code: 'it', name: 'Italian', flag: '🇮🇹' },
  { code: 'ja', name: 'Japanese', flag: '🇯🇵' },
  { code: 'ko', name: 'Korean', flag: '🇰🇷' },
  { code: 'lv', name: 'Latvian', flag: '🇱🇻' },
  { code: 'lt', name: 'Lithuanian', flag: '🇱🇹' },
  { code: 'no', name: 'Norwegian', flag: '🇳🇴' },
  { code: 'pl', name: 'Polish', flag: '🇵🇱' },
  { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
  { code: 'ro', name: 'Romanian', flag: '🇷🇴' },
  { code: 'ru', name: 'Russian', flag: '🇷🇺' },
  { code: 'sk', name: 'Slovak', flag: '🇸🇰' },
  { code: 'sl', name: 'Slovenian', flag: '🇸🇮' },
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'sv', name: 'Swedish', flag: '🇸🇪' },
  { code: 'tr', name: 'Turkish', flag: '🇹🇷' },
  { code: 'uk', name: 'Ukrainian', flag: '🇺🇦' },
  { code: 'vi', name: 'Vietnamese', flag: '🇻🇳' }
];

const TranslationDisplay = () => {
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [translation, setTranslation] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showLanguages, setShowLanguages] = useState(true);
  
  const selectLanguage = (langCode) => {
    setSelectedLanguage(langCode === selectedLanguage ? null : langCode);
    setShowLanguages(false);
  };

  const filteredLanguages = LANGUAGES.filter(lang =>
    lang.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    if (!selectedLanguage) {
      setTranslation(null);
      setShowLanguages(true);
      return;
    }

    const interval = setInterval(async () => {
      try {
        const response = await fetch(`/translations/${selectedLanguage}.json`);
        const data = await response.json();
        setTranslation(data);
      } catch (error) {
        console.error(`Error fetching ${selectedLanguage} translation:`, error);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [selectedLanguage]);

  return (
    <div className="min-h-screen h-screen flex flex-col bg-gray-900">
      {/* Header */}
      <header className="p-4 sm:p-6 bg-gray-800">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-center text-xl sm:text-3xl font-bold text-white">
            <Globe2 className="mr-2 h-6 w-6 sm:h-8 sm:w-8" />
            DigitalOcean Deploy - Real time Jack Pearce Translator
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col p-4 sm:p-6">
        <div className="max-w-7xl mx-auto w-full flex-1 flex flex-col">
          {!selectedLanguage && (
            <div className="text-xl text-gray-400 italic text-center mb-4">
              Please select a language to start translation
            </div>
          )}

          {/* Language Selection Section */}
          {selectedLanguage && (
            <button
              onClick={() => setShowLanguages(!showLanguages)}
              className="flex items-center justify-between w-full bg-gray-800 rounded-lg shadow-lg p-4 mb-4 text-white hover:bg-gray-700 transition-colors"
            >
              <div className="flex items-center">
                <span className="text-2xl mr-2">
                  {LANGUAGES.find(l => l.code === selectedLanguage)?.flag}
                </span>
                <span className="font-medium">
                  {LANGUAGES.find(l => l.code === selectedLanguage)?.name}
                </span>
              </div>
              {showLanguages ? <ChevronUp className="h-6 w-6" /> : <ChevronDown className="h-6 w-6" />}
            </button>
          )}

          {/* Expandable Language Selection */}
          {showLanguages && (
            <div className="bg-gray-800 rounded-lg shadow-lg p-4 sm:p-6 mb-4">
              <h2 className="text-lg font-semibold mb-4 text-white">Select Target Language</h2>
              
              <input
                type="text"
                placeholder="Search languages..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full p-2 mb-4 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              
              <div className="flex flex-wrap gap-2 sm:gap-4">
                {filteredLanguages.map(lang => (
                  <button
                    key={lang.code}
                    onClick={() => selectLanguage(lang.code)}
                    className={`flex items-center px-3 sm:px-4 py-2 rounded-full transition-colors text-sm sm:text-base ${
                      selectedLanguage === lang.code
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    <span className="mr-2">{lang.flag}</span>
                    {lang.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Translation Display */}
          {selectedLanguage && (
            <div className="flex-1 flex flex-col">
              <div className="bg-gray-800 rounded-lg shadow-lg p-4 sm:p-8 flex-1 flex flex-col">
                {translation ? (
                  <div className="space-y-4 sm:space-y-8 flex-1 flex flex-col">
                    <div className="flex-1 bg-gray-700 p-4 sm:p-6 rounded-lg flex flex-col justify-center min-h-[40vh]">
                      <div className="text-sm text-gray-400 mb-2">Original</div>
                      <div className="text-2xl sm:text-4xl md:text-5xl font-medium text-white break-words">
                        {translation.original}
                      </div>
                    </div>
                    <div className="flex-1 bg-blue-900 p-4 sm:p-6 rounded-lg flex flex-col justify-center min-h-[40vh]">
                      <div className="text-sm text-blue-300 mb-2">Translation</div>
                      <div className="text-2xl sm:text-4xl md:text-5xl font-medium text-white break-words">
                        {translation.translated}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="flex-1 flex items-center justify-center">
                    <div className="text-xl text-gray-400 italic text-center">
                      Waiting for translations...
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default TranslationDisplay;