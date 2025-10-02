# 🌟 PharmaVerse - The Ultimate Drug Discovery Hub

**Author:** Mohamed Dadapeer

An advanced medicine search system with a beautiful, modern interface built using FastAPI and PostgreSQL. PharmaVerse provides intelligent drug discovery across 280,227+ unique medicine records with multiple search algorithms and stunning visual design.

## ✨ Features

- **🎯 4 Advanced Search Types**: Prefix Quest, Deep Scan, AI Search, and Smart Match
- **🌊 Massive Database**: 280,227+ unique medicine records with complete pharmaceutical information
- **🚀 High Performance**: Lightning-fast search results with optimized PostgreSQL queries
- **💎 Beautiful UI**: Stunning PharmaVerse interface with glassmorphism design and smooth animations
- **🔥 REST API**: FastAPI-based endpoints with automatic documentation
- **⚡ Real-time Search**: Instant results with magical loading animations
- **📊 Smart Grid Layout**: 2-column responsive card layout that maximizes screen space
- **🎨 Single Color Theme**: Elegant purple gradient design throughout

## 🎨 Design Highlights

- **Glassmorphism**: Frosted glass containers with backdrop blur effects
- **Elegant Purple Theme**: Beautiful gradient from `#667eea` to `#764ba2`
- **Interactive Animations**: Floating particles, hover effects, and smooth transitions
- **Responsive Grid**: Cards automatically arrange in 2 columns on larger screens
- **Modern Typography**: Poppins font family for a professional look
- **Smart Cards**: Consistent heights and beautiful spacing

## 🛠️ Prerequisites

- Python 3.8+ (with pip)
- PostgreSQL (any version with standard SQL support)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for Google Fonts)
- Git (optional, for cloning repository)

## 🚀 Quick Setup & Run

> **💡 Windows Users**: All commands work in PowerShell or Command Prompt. Make sure Python is in your PATH.

### Step 1: Install Dependencies
```bash
# Install required Python packages
pip install fastapi uvicorn psycopg2-binary python-dotenv python-multipart

# Or install from requirements file
pip install -r requirements.txt
```

### Step 2: Setup PostgreSQL Database

**Option A: Automated Setup (Recommended)**
```bash
# Run the interactive setup script
python setup_database.py

# Import medicine data
python import_data.py
```

**Option B: Manual Setup**
```bash
# Create database manually
psql -U postgres -c "CREATE DATABASE medicine_search;"

# Run schema
psql -U postgres -d medicine_search -f schema.sql

# Import data
python import_data.py
```

### Step 3: Configure Database Connection
Update the `.env` file with your database credentials:
```properties
DB_NAME=medicine_search
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

### Step 4: Launch PharmaVerse
```bash
# Windows (PowerShell)
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# Linux/Mac
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### Step 5: Access PharmaVerse
Open your browser and navigate to:
- **🌟 PharmaVerse Interface**: `http://localhost:8000`
- **📚 API Documentation**: `http://localhost:8000/docs`
- **📋 Alternative Docs**: `http://localhost:8000/redoc`

## 🔍 Search Types Explained

### 🎯 **Prefix Quest**
- Finds medicines that **start with** your search term
- Perfect for: "asp" → finds "Aspirin", "Asparagus Extract"
- Best when: You know the beginning of a medicine name

### 🔍 **Deep Scan**  
- Finds medicines that **contain** your search term anywhere
- Perfect for: "pain" → finds "Aspirin", "Pain Relief", "Ibuprofen Pain"
- Best when: Searching by common medical terms

### 🧠 **AI Search**
- Intelligent search with **ranking and relevance scoring**
- Handles multiple words and prioritizes exact matches
- Perfect for: "heart medicine" → finds cardiovascular drugs ranked by relevance
- Best when: Complex queries with multiple terms

### 🌊 **Smart Match**
- **Handles typos** and similar spellings using fuzzy matching
- Uses similarity scoring to find close matches
- Perfect for: "aspirn" → finds "Aspirin", "paracetmol" → finds "Paracetamol"
- Best when: You're unsure of exact spelling

## 🌐 API Endpoints

### Search Endpoints
```http
GET /search/prefix?q=medicine_name    # Prefix Quest
GET /search/substring?q=medicine_name # Deep Scan  
GET /search/fulltext?q=medicine_name  # AI Search
GET /search/fuzzy?q=medicine_name     # Smart Match
```

### Health Check
```http
GET /health                           # System status
```

### Example API Calls
```bash
# Prefix search for medicines starting with "asp"
curl "http://localhost:8000/search/prefix?q=asp"

# Smart Match handles typos - "aspirn" finds "aspirin"
curl "http://localhost:8000/search/fuzzy?q=aspirn"

# AI Search for complex queries
curl "http://localhost:8000/search/fulltext?q=pain%20relief"
```

## 🎮 How to Use PharmaVerse

1. **🚀 Launch the application** following the setup steps above
2. **🌐 Open your browser** and go to `http://localhost:8000`
3. **🎯 Select search type** from the four magical options
4. **⌨️ Type medicine name** in the search box (try: "Avastin", "Paracetamol", "pain")
5. **🔍 Click Explore** or press Enter to search
6. **✨ View results** in the beautiful 2-column card layout
7. **📊 See statistics** showing search performance and result count

### Interface Features:
- 🎨 **Glassmorphism Design** - Modern frosted glass aesthetic
- 🌟 **Floating Particles** - Animated background elements
- 💫 **Interactive Cards** - Hover effects and smooth animations
- 📱 **Fully Responsive** - Works perfectly on all screen sizes
- 🚀 **Lightning Fast** - Instant search results with loading animations

## 📁 Project Structure

```
PharmaVerse/
├── app.py                  # 🔥 Main FastAPI application (CORE)
├── schema.sql              # 🗄️ Database schema with indexes (CORE)
├── import_data.py          # 📥 Medicine data import script (CORE)
├── setup_database.py       # 🛠️ Database setup helper (CORE)
├── requirements.txt        # 📦 Python dependencies (CORE)
├── .env                    # 🔧 Environment configuration (CORE)
├── README.md               # 📚 This documentation (CORE)
├── benchmark.md            # 📊 Performance analysis
├── benchmark_queries.json  # 🧪 Test queries for evaluation
├── submission.json         # 📤 Results submission file
├── benchmark.py            # ⚡ Performance benchmarking
├── benchmark_results.json  # 📈 Benchmark test results
├── run.py                  # 🏃 Alternative application runner
├── docker-compose.yml      # 🐳 Docker container setup
├── Dockerfile              # 🐳 Docker image configuration
└── DB_Dataset/             # 📊 Medicine dataset folder
    └── DB_Dataset/
        └── data/           # 📁 JSON files (a.json to z.json)
```

## 🗄️ Database Schema

### Required Table Structure
```sql
CREATE TABLE medicines (
    id SERIAL PRIMARY KEY,
    sku_id VARCHAR(255) UNIQUE,
    name VARCHAR(500) NOT NULL,
    manufacturer_name VARCHAR(500),
    marketer_name VARCHAR(500),
    type VARCHAR(100),
    price DECIMAL(10,2),
    pack_size_label VARCHAR(255),
    short_composition TEXT,
    is_discontinued BOOLEAN DEFAULT FALSE,
    available BOOLEAN DEFAULT TRUE
);

-- Performance indexes
CREATE INDEX idx_medicines_name ON medicines(name);
CREATE INDEX idx_medicines_name_lower ON medicines(LOWER(name));
```

## 📊 Performance & Statistics

### 🚀 Database Metrics
- **280,227 unique medicines** (deduplicated from 380,948+ raw records)
- **Complete pharmaceutical data** including SKU, manufacturer, marketer information
- **Optimized B-tree indexes** for lightning-fast searches
- **Zero duplicate entries** - clean, normalized dataset

### ⚡ Performance Benchmarks
- **Average Response Time**: < 50ms for most queries
- **Concurrent Support**: Handles multiple simultaneous searches
- **Large Result Sets**: Returns up to 100 medicines per query
- **Memory Efficient**: Optimized PostgreSQL queries with proper indexing

### 🎯 Search Accuracy
- **Prefix Quest**: 100% accuracy for exact prefix matches
- **Deep Scan**: Comprehensive substring detection
- **AI Search**: Intelligent ranking with relevance scoring
- **Smart Match**: 85%+ accuracy for typo correction

## 🔧 Troubleshooting

### Common Issues & Solutions

**❌ Database Connection Error**
```bash
# Windows - Check PostgreSQL service
sc query postgresql-x64-13

# Linux/Mac - Check PostgreSQL service  
sudo systemctl status postgresql

# Verify database exists
psql -U postgres -l | grep medicine_search

# Test connection
psql -U postgres -d medicine_search -c "SELECT COUNT(*) FROM medicines;"
```

**❌ Port Already in Use**
```bash
# Windows - Check what's using the port
netstat -ano | findstr :8000

# Linux/Mac - Check what's using the port
netstat -tulpn | grep :8000

# Use different port
python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```

**❌ No Search Results**
```bash
# Verify data exists
psql -U postgres -d medicine_search -c "SELECT COUNT(*) FROM medicines WHERE name ILIKE '%aspirin%';"

# Check table structure
psql -U postgres -d medicine_search -c "\d medicines"
```

**❌ UI Not Loading**
- Clear browser cache and refresh
- Check browser console for JavaScript errors
- Ensure Google Fonts can load (check internet connection)
- Try different browser (Chrome, Firefox, Safari)

## 🌟 Features in Detail

### 🎨 Visual Design
- **Single Color Theme**: Elegant purple gradient (#667eea to #764ba2)
- **Glassmorphism**: Frosted glass containers with backdrop blur
- **Smooth Animations**: CSS transitions and hover effects
- **Responsive Grid**: Auto-adjusting 2-column layout on larger screens

### 🔍 Search Intelligence
- **Smart Ranking**: Results ranked by relevance and exact match priority
- **Typo Tolerance**: Fuzzy search handles common spelling mistakes
- **Multi-word Support**: AI search processes complex queries intelligently
- **Performance Optimization**: Indexed database queries for speed

### 💻 Technical Excellence
- **Modern Framework**: Built with FastAPI for high performance
- **Type Safety**: Full type hints and validation
- **API Documentation**: Auto-generated interactive docs
- **Error Handling**: Graceful error messages and recovery

## 🏆 Author

**Mohamed Dadapeer**  
*PharmaVerse Creator & Lead Developer*

---

## 🚀 Quick Start Commands

```bash
# Clone and setup
git clone <repository>
cd Medicine_Search_System-master

# Install dependencies
pip install -r requirements.txt

# Setup database (follow prompts)
python setup_database.py

# Import medicine data
python import_data.py

# Launch PharmaVerse (Windows)
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# Launch PharmaVerse (Linux/Mac)  
uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# Open in browser
# Navigate to: http://localhost:8000
```

---

*🌟 Built with passion using FastAPI, PostgreSQL, and modern web technologies*  
*✨ Experience the future of medicine discovery with PharmaVerse*