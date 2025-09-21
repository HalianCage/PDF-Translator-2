# Chinese PDF Translator

A desktop application that translates Chinese text in PDF documents to English using machine learning models. The application features a modern React frontend with Tauri for desktop integration and a FastAPI backend for PDF processing and translation.

## 🌟 Features

- **PDF Processing**: Extract Chinese text from PDF documents while preserving layout and positioning
- **AI Translation**: Uses Helsinki-NLP's opus-mt-zh-en model for accurate Chinese-to-English translation
- **Real-time Progress**: Live status updates during the translation process
- **Desktop App**: Cross-platform desktop application built with Tauri
- **Offline Capable**: Works without internet connection using local ML models
- **Background Processing**: Non-blocking translation with job status tracking

## 🏗️ Architecture

### Frontend (React + Tauri)
- **React 19** with modern hooks and functional components
- **Tauri 2.8** for desktop application framework
- **Vite** for fast development and building
- Real-time status polling and file upload interface

### Backend (FastAPI + Python)
- **FastAPI** for high-performance API server
- **PyMuPDF (fitz)** for PDF text extraction and manipulation
- **Transformers** for machine learning model integration
- **Background task processing** with job status tracking

### Machine Learning
- **Helsinki-NLP/opus-mt-zh-en** model for Chinese-to-English translation
- **Offline model** stored locally for privacy and performance
- **SentencePiece tokenization** for accurate text processing

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** (recommended: Python 3.11+)
- **Node.js 18+** and npm
- **Rust** (for Tauri development)
- **Git**

### Platform Support
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd project_PDF_translator
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv
```

#### Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Python Dependencies
```bash
pip install fastapi uvicorn transformers torch torchvision torchaudio
pip install pymupdf python-multipart
pip install pyinstaller  # For building executable
```

#### Verify Model Setup
Ensure the `offline_model` directory contains the following files:
- `config.json`
- `generation_config.json`
- `model.safetensors`
- `source.spm`
- `target.spm`
- `special_tokens_map.json`
- `tokenizer_config.json`
- `vocab.json`

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Install Tauri CLI (if not already installed)
```bash
npm install -g @tauri-apps/cli
```

## 🏃‍♂️ Running in Development Mode

### Option 1: Full Desktop Application (Recommended)

1. **Start the Backend Server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The backend will start on `http://localhost:8000`

2. **Start the Frontend (in a new terminal):**
   ```bash
   cd frontend
   npm run tauri dev
   ```
   This will open the desktop application window.

### Option 2: Web Development Mode

1. **Start the Backend Server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start the Frontend Development Server:**
   ```bash
   cd frontend
   npm run dev
   ```
   Access the application at `http://localhost:5173`

## 📦 Building for Production

### Backend Executable
```bash
cd backend
pyinstaller --onefile --add-data "offline_model;offline_model" main.py
```
The executable will be created in `backend/dist/`

### Frontend Desktop App
```bash
cd frontend
npm run tauri build
```
The desktop application will be built in `frontend/src-tauri/target/release/`

## 🔧 Configuration

### Backend Configuration
- **Port**: Default `8000` (configurable in `main.py`)
- **CORS**: Configured for all origins in development
- **Model Path**: Automatically detects model location in both dev and production modes

### Frontend Configuration
- **Backend URL**: Configured in `App.jsx` (default: `http://localhost:8000`)
- **Window Settings**: Configurable in `tauri.conf.json`
- **Security**: CSP configured for localhost communication

## 📖 Usage

1. **Launch the Application**: Start the desktop app or open in browser
2. **Select PDF**: Click "Choose File" and select a PDF with Chinese text
3. **Translate**: Click "Translate" to start the process
4. **Monitor Progress**: Watch real-time status updates:
   - "Starting process..."
   - "Step 1/3: Extracting text..."
   - "Step 2/3: Translating text..."
   - "Step 3/3: Creating final PDF..."
5. **Download**: The translated PDF will automatically download when complete

## 🛠️ API Endpoints

### Health Check
```
GET /health
```
Returns server status and readiness.

### Start Translation
```
POST /start-translation/
```
Upload a PDF file to start translation process.
- **Body**: `multipart/form-data` with PDF file
- **Response**: `{"job_id": "uuid"}`

### Check Job Status
```
GET /job-status/{job_id}
```
Check the status of a translation job.
- **Response**: `{"job_id": "uuid", "status": "status", "error": "error_message"}`

### Download Result
```
GET /download/{job_id}
```
Download the translated PDF file.

## 📁 Project Structure

```
project_PDF_translator/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main server file
│   ├── venv/               # Python virtual environment
│   ├── dist/               # Built executables
│   └── build/              # PyInstaller build files
├── frontend/               # React + Tauri frontend
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── components/     # React components
│   │   └── assets/         # Static assets
│   ├── src-tauri/          # Tauri configuration
│   └── package.json        # Node.js dependencies
├── offline_model/          # ML model files
│   ├── config.json
│   ├── model.safetensors
│   └── ...                 # Other model files
├── output_pdfs/            # Generated translated PDFs
└── README.md              # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend fails to start**
   - Ensure Python virtual environment is activated
   - Check that all dependencies are installed
   - Verify the `offline_model` directory exists and contains all required files

2. **Frontend can't connect to backend**
   - Ensure backend is running on `http://localhost:8000`
   - Check firewall settings
   - Verify CORS configuration

3. **Translation fails**
   - Check that the PDF contains Chinese text
   - Ensure the model files are complete and uncorrupted
   - Check backend logs for detailed error messages

4. **Build issues**
   - Ensure all dependencies are installed
   - Check that Rust toolchain is properly installed for Tauri
   - Verify PyInstaller is installed for backend builds

### Logs
- **Backend logs**: Check `backend/backend.log`
- **Frontend logs**: Check browser developer console
- **Tauri logs**: Check terminal output during development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for the translation model
- [Tauri](https://tauri.app/) for the desktop application framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Note**: This application requires significant computational resources for the machine learning model. Ensure your system meets the minimum requirements for optimal performance.
