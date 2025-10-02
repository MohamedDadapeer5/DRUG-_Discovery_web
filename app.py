from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv
import time
import re

load_dotenv()

app = FastAPI(title="PharmaVerse API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "medicine_search"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "Dadapeer"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html>
<head>
    <title>🌟 PharmaVerse - The Ultimate Drug Discovery Hub</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        body { 
            font-family: 'Poppins', sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; 
            padding: 20px;
            overflow-x: hidden;
        }
        

        
        .floating-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            width: 6px;
            height: 6px;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0; }
            50% { transform: translateY(-100px) rotate(180deg); opacity: 1; }
        }
        
        .container { 
            max-width: 1300px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 40px; 
            border-radius: 30px; 
            box-shadow: 0 25px 45px rgba(0,0,0,0.1), 0 0 0 1px rgba(255,255,255,0.1);
            position: relative;
            z-index: 2;
            animation: containerGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes containerGlow {
            0% { box-shadow: 0 25px 45px rgba(0,0,0,0.1), 0 0 30px rgba(255,255,255,0.1); }
            100% { box-shadow: 0 25px 45px rgba(0,0,0,0.2), 0 0 50px rgba(255,255,255,0.2); }
        }
        
        h1 { 
            color: white; 
            text-align: center; 
            margin-bottom: 20px; 
            font-size: 3.5em; 
            font-weight: 800; 
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
            color: white;
            animation: titlePulse 2s ease-in-out infinite alternate;
        }
        
        @keyframes titlePulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.05); }
        }
        
        .subtitle {
            text-align: center; 
            color: rgba(255,255,255,0.9); 
            font-size: 1.2em; 
            margin-bottom: 30px; 
            font-weight: 300;
        }
        
        .search-section { 
            margin-bottom: 40px; 
        }
        
        .search-box { 
            display: flex; 
            margin: 30px 0; 
            gap: 15px; 
            position: relative;
        }
        
        input[type="text"] { 
            flex: 1; 
            padding: 20px 25px; 
            font-size: 18px; 
            border: none;
            border-radius: 25px; 
            outline: none; 
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            font-family: 'Poppins', sans-serif;
        }
        
        input[type="text"]:focus { 
            background: rgba(255, 255, 255, 1);
            box-shadow: 0 0 0 4px rgba(255,255,255,0.3), 0 15px 35px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .search-btn-main { 
            padding: 20px 35px; 
            font-size: 18px; 
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer; 
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600; 
            box-shadow: 0 8px 25px rgba(255,107,107,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .search-btn-main::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        
        .search-btn-main:hover::before {
            left: 100%;
        }
        
        .search-btn-main:hover { 
            background: linear-gradient(45deg, #5a67d8, #6b46c1);
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 35px rgba(255,107,107,0.4);
        }
        
        .search-types { 
            display: flex; 
            justify-content: center; 
            gap: 20px; 
            flex-wrap: wrap; 
            margin: 30px 0; 
        }
        
        .search-btn { 
            padding: 15px 30px; 
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            color: white; 
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 30px; 
            cursor: pointer; 
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600; 
            font-size: 16px; 
            position: relative;
            overflow: hidden;
        }
        
        .search-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
            transition: all 0.4s;
            transform: translate(-50%, -50%);
        }
        
        .search-btn:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .search-btn:hover { 
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 10px 25px rgba(255,255,255,0.2);
            border-color: rgba(255, 255, 255, 0.5);
        }
        
        .search-btn.active { 
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; 
            border-color: transparent;
            box-shadow: 0 8px 25px rgba(255,107,107,0.4);
            transform: scale(1.1);
        }
        
        .results { 
            margin-top: 40px; 
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
            margin-top: 25px;
        }
        
        .medicine { 
            border: none;
            padding: 30px; 
            border-radius: 20px; 
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; 
            border: 1px solid rgba(255, 255, 255, 0.2);
            overflow: hidden;
            min-height: 280px;
        }
        
        .medicine::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
            pointer-events: none;
        }
        
        .medicine:hover::before {
            opacity: 1;
        }
        
        .medicine:hover { 
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1), 0 0 0 1px rgba(255,255,255,0.3);
            transform: translateY(-5px) scale(1.02);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        .medicine h4 { 
            color: white; 
            margin-bottom: 20px; 
            font-size: 1.4em; 
            display: flex; 
            align-items: center; 
            gap: 15px; 
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            flex-wrap: wrap;
        }
        
        .medicine p { 
            margin: 12px 0; 
            font-size: 16px; 
            line-height: 1.6; 
            color: rgba(255, 255, 255, 0.9);
        }
        
        .medicine strong { 
            color: white; 
            font-weight: 600;
        }
        
        .loading { 
            text-align: center; 
            color: white; 
            font-size: 1.5em; 
            padding: 50px; 
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.7; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.05); }
        }
        
        .score { 
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; 
            padding: 6px 15px; 
            border-radius: 25px; 
            font-size: 0.85em; 
            font-weight: 700;
            animation: scoreGlow 2s ease-in-out infinite alternate;
            white-space: nowrap;
        }
        
        @keyframes scoreGlow {
            0% { box-shadow: 0 0 10px rgba(255,107,107,0.5); }
            100% { box-shadow: 0 0 20px rgba(255,107,107,0.8); }
        }
        
        .search-info { 
            text-align: center; 
            margin: 30px 0; 
            padding: 20px; 
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px; 
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-weight: 600;
        }
        
        .no-results { 
            text-align: center; 
            font-size: 1.3em; 
            color: white; 
            padding: 50px; 
            background: rgba(255, 107, 107, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 107, 107, 0.3);
        }
        
        @media (max-width: 1200px) {
            .results-grid { grid-template-columns: 1fr; }
        }
        
        @media (max-width: 768px) {
            .container { padding: 25px; }
            h1 { font-size: 2.5em; }
            .search-types { justify-content: center; }
            .search-btn { padding: 12px 20px; font-size: 14px; }
            .search-box { flex-direction: column; }
            .results-grid { grid-template-columns: 1fr; }
        }
        
        /* Magical sparkle effect */
        .sparkle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: white;
            border-radius: 50%;
            animation: sparkle 1.5s ease-in-out infinite;
        }
        
        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="floating-particles"></div>
    <div class="container">
        <h1>🌟 PharmaVerse 🚀</h1>
        <div class="subtitle">
            The Ultimate Drug Discovery Universe ✨ Explore 280K+ Medicines
        </div>
        <div class="search-section">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Discover medicines across the PharmaVerse..." autocomplete="off">
                <button class="search-btn-main" onclick="searchMedicines()">
                    <span>🚀 Explore</span>
                </button>
            </div>
            <div class="search-types">
                <button class="search-btn active" id="prefix-btn" onclick="setSearchType('prefix')">🎯 Prefix Quest</button>
                <button class="search-btn" id="substring-btn" onclick="setSearchType('substring')">🔍 Deep Scan</button>
                <button class="search-btn" id="fulltext-btn" onclick="setSearchType('fulltext')">🧠 AI Search</button>
                <button class="search-btn" id="fuzzy-btn" onclick="setSearchType('fuzzy')">🌊 Smart Match</button>
            </div>
        </div>
        <div id="results" class="results"></div>
    </div>
    <script>
        let currentSearchType = 'prefix';
        
        // Create magical floating particles
        function createParticles() {
            const particlesContainer = document.querySelector('.floating-particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
                particlesContainer.appendChild(particle);
            }
        }
        
        // Create sparkle effects
        function createSparkles(element) {
            for (let i = 0; i < 5; i++) {
                const sparkle = document.createElement('div');
                sparkle.className = 'sparkle';
                sparkle.style.left = Math.random() * 100 + '%';
                sparkle.style.top = Math.random() * 100 + '%';
                sparkle.style.animationDelay = Math.random() * 1.5 + 's';
                element.style.position = 'relative';
                element.appendChild(sparkle);
                
                setTimeout(() => sparkle.remove(), 1500);
            }
        }
        
        function setSearchType(type) {
            currentSearchType = type;
            document.querySelectorAll('.search-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById(type + '-btn');
            activeBtn.classList.add('active');
            createSparkles(activeBtn);
        }
        
        async function searchMedicines() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) {
                // Create magical alert
                const alertDiv = document.createElement('div');
                alertDiv.innerHTML = '🌟 Ready to explore the PharmaVerse? Enter a medicine name! 🚀';
                alertDiv.style.cssText = `
                    position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                    background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 20px 30px;
                    border-radius: 15px; font-size: 18px; font-weight: 600; z-index: 1000;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3); animation: bounce 0.5s ease-out;
                `;
                document.body.appendChild(alertDiv);
                setTimeout(() => alertDiv.remove(), 3000);
                return;
            }
            
            // Enhanced loading with magic
            document.getElementById('results').innerHTML = `
                <div class="loading">
                    🚀 Exploring the PharmaVerse... 🌟<br>
                    <div style="margin-top: 20px; font-size: 0.8em;">Scanning 280,227 medicines across the universe</div>
                </div>
            `;
            
            try {
                const response = await fetch(`/search/${currentSearchType}?q=${encodeURIComponent(query)}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                
                const resultsDiv = document.getElementById('results');
                if (data.results && data.results.length > 0) {
                    const searchTypeNames = {
                        'prefix': '🎯 Prefix Quest',
                        'substring': '🔍 Deep Scan', 
                        'fulltext': '🧠 AI Search',
                        'fuzzy': '🌊 Smart Match'
                    };
                    
                    resultsDiv.innerHTML = `
                        <div class="search-info">
                            <strong>🎉 Mission accomplished! Discovered ${data.count} medicines using ${searchTypeNames[data.type]} in ${data.execution_time_ms}ms ⚡</strong>
                        </div>
                        <div class="results-grid">
                            ${data.results.map((med, index) => `
                                <div class="medicine" style="animation-delay: ${index * 0.1}s">
                                    <h4>
                                        💊 ${med.name}
                                        ${med.rank ? `<span class="score">✨ Rank: ${med.rank.toFixed(2)}</span>` : ''}
                                        ${med.similarity_score ? `<span class="score">🌟 ${(med.similarity_score * 100).toFixed(0)}% Match</span>` : ''}
                                    </h4>
                                    <p><strong>🏭 Manufacturer:</strong> ${med.manufacturer_name || '🌟 Universal Labs'}</p>
                                    <p><strong>🧬 Drug Type:</strong> ${med.type || '🚀 Advanced Formula'}</p>
                                    <p><strong>💰 Price:</strong> ${med.price || '🌟 Premium Quality'}</p>
                                    <p><strong>📦 Package:</strong> ${med.pack_size_label || '🎯 Standard Pack'}</p>
                                    <p><strong>⚗️ Composition:</strong> ${med.short_composition || '🧪 Active Compounds'}</p>
                                </div>
                            `).join('')}
                        </div>
                    `;
                    
                    // Add entrance animation to results
                    document.querySelectorAll('.medicine').forEach((med, index) => {
                        med.style.opacity = '0';
                        med.style.transform = 'translateY(30px)';
                        setTimeout(() => {
                            med.style.transition = 'all 0.6s ease-out';
                            med.style.opacity = '1';
                            med.style.transform = 'translateY(0)';
                        }, index * 100);
                    });
                    
                } else {
                    resultsDiv.innerHTML = `
                        <div class="no-results">
                            🌙 The magic orb shows no medicines for "${query}"<br>
                            💫 Try different incantations or change your spell type ✨
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('results').innerHTML = `
                    <div class="no-results">
                        🌩️ A magical disturbance occurred in the realm<br>
                        🔮 Please try casting your spell again
                    </div>
                `;
                console.error('Search error:', error);
            }
        }
        
        // Enhanced event listeners
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchMedicines();
            }
        });
        
        // Magical input focus effects
        document.getElementById('searchInput').addEventListener('focus', function() {
            createSparkles(this.parentElement);
        });
        
        // Initialize particles when page loads
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
            document.getElementById('searchInput').focus();
        });
        
        // Add hover effects to medicine cards
        document.addEventListener('click', function(e) {
            if (e.target.closest('.medicine')) {
                createSparkles(e.target.closest('.medicine'));
            }
        });
        
        // CSS for bounce animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes bounce {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
                50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>"""

@app.get("/health")
async def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicines")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {"status": "healthy", "medicines_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/search/prefix")
async def search_prefix(q: str = Query(..., min_length=1, max_length=100)):
    start_time = time.time()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, manufacturer_name, type, price, pack_size_label, short_composition
            FROM medicines
            WHERE name ILIKE %s || '%%'
            ORDER BY name
            LIMIT 100
        """, (q,))
        results = []
        for row in cursor.fetchall():
            results.append({
                "name": row[0],
                "manufacturer_name": row[1],
                "type": row[2],
                "price": row[3],
                "pack_size_label": row[4],
                "short_composition": row[5]
            })
        cursor.close()
        conn.close()
        execution_time = time.time() - start_time
        return {
            "query": q,
            "type": "prefix",
            "results": results,
            "count": len(results),
            "execution_time_ms": round(execution_time * 1000, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search/substring")
async def search_substring(q: str = Query(..., min_length=1, max_length=100)):
    start_time = time.time()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, manufacturer_name, type, price, pack_size_label, short_composition
            FROM medicines
            WHERE name ILIKE '%%' || %s || '%%'
            ORDER BY name
            LIMIT 100
        """, (q,))
        results = []
        for row in cursor.fetchall():
            results.append({
                "name": row[0],
                "manufacturer_name": row[1],
                "type": row[2],
                "price": row[3],
                "pack_size_label": row[4],
                "short_composition": row[5]
            })
        cursor.close()
        conn.close()
        execution_time = time.time() - start_time
        return {
            "query": q,
            "type": "substring",
            "results": results,
            "count": len(results),
            "execution_time_ms": round(execution_time * 1000, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search/fulltext")
async def search_fulltext(q: str = Query(..., min_length=1, max_length=100)):
    start_time = time.time()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Smart search with ranking based on position and exact matches
        cursor.execute("""
            SELECT name, manufacturer_name, type, price, pack_size_label, short_composition,
                   CASE 
                       WHEN LOWER(name) = LOWER(%s) THEN 1.0
                       WHEN LOWER(name) LIKE LOWER(%s) || ' %%' THEN 0.9
                       WHEN LOWER(name) LIKE '%% ' || LOWER(%s) || ' %%' THEN 0.8
                       WHEN LOWER(name) LIKE '%% ' || LOWER(%s) THEN 0.7
                       WHEN LOWER(name) LIKE LOWER(%s) || '%%' THEN 0.6
                       ELSE 0.5 
                   END as rank
            FROM medicines
            WHERE LOWER(name) LIKE '%%' || LOWER(%s) || '%%'
            ORDER BY rank DESC, name
            LIMIT 100
        """, (q, q, q, q, q, q))
        results = []
        for row in cursor.fetchall():
            results.append({
                "name": row[0],
                "manufacturer_name": row[1],
                "type": row[2],
                "price": row[3],
                "pack_size_label": row[4],
                "short_composition": row[5],
                "rank": row[6]
            })
        cursor.close()
        conn.close()
        execution_time = time.time() - start_time
        return {
            "query": q,
            "type": "fulltext",
            "results": results,
            "count": len(results),
            "execution_time_ms": round(execution_time * 1000, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search/fuzzy")
async def search_fuzzy(q: str = Query(..., min_length=1, max_length=100)):
    start_time = time.time()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Fuzzy search using trigrams with similarity scoring
        cursor.execute("""
            SELECT name, manufacturer_name, type, price, pack_size_label, short_composition,
                   similarity(name, %s) as similarity_score
            FROM medicines
            WHERE similarity(name, %s) > 0.3
            ORDER BY similarity_score DESC, name
            LIMIT 100
        """, (q, q))
        results = []
        for row in cursor.fetchall():
            results.append({
                "name": row[0],
                "manufacturer_name": row[1],
                "type": row[2],
                "price": row[3],
                "pack_size_label": row[4],
                "short_composition": row[5],
                "similarity_score": row[6]
            })
        cursor.close()
        conn.close()
        execution_time = time.time() - start_time
        return {
            "query": q,
            "type": "fuzzy",
            "results": results,
            "count": len(results),
            "execution_time_ms": round(execution_time * 1000, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)