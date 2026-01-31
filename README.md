# VietDub - AI Video Dubbing Tool

🎬 Công cụ AI giúp lồng tiếng Việt cho video tự động.

## Tính năng

- 🎙️ **Transcription**: Chuyển đổi giọng nói thành văn bản (Whisper AI)
- 🌐 **Translation**: Dịch tự động sang tiếng Việt 
- 🔊 **Text-to-Speech**: Tạo giọng đọc tiếng Việt tự nhiên
- 🎬 **Video Export**: Xuất video với phụ đề và lồng tiếng

## Cài đặt

### Windows (Khuyến nghị)
Tải file `Visub_Setup.exe` từ [Releases](../../releases) và cài đặt.

### Chạy từ source code
```bash
# Clone repository
git clone https://github.com/yourusername/visub.git
cd visub

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

## Build Windows Installer

### Tự động (GitHub Actions)
1. Push code lên GitHub
2. Tạo tag version: `git tag v1.0.0 && git push --tags`
3. GitHub Actions sẽ tự động build và tạo Release

### Thủ công (trên Windows)
```powershell
# Cài đặt dependencies
pip install -r requirements.txt

# Build với PyInstaller
pyinstaller visub.spec --noconfirm

# Tạo installer (cần Inno Setup)
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss
```

## Cấu trúc dự án

```
visub-main/
├── app.py              # Main Streamlit app
├── config.py           # Configuration
├── run_app.pyw         # Windows launcher (no console)
├── visub.spec          # PyInstaller spec
├── requirements.txt    # Dependencies
├── core/               # Core modules
│   ├── transcriber.py  # Whisper transcription
│   ├── translator.py   # AI translation
│   ├── tts.py          # Text-to-speech
│   └── merger.py       # Video/audio merging
├── utils/              # Utility functions
├── installer/          # Installer scripts
│   └── setup.iss       # Inno Setup script
└── .github/workflows/  # CI/CD
    └── build-windows.yml
```

## API Keys cần thiết

- **OpenRouter API Key**: Để dịch thuật (lấy tại [openrouter.ai](https://openrouter.ai))
- **TTS API Key**: FPT.AI, ElevenLabs, hoặc OpenAI

## License

MIT License
