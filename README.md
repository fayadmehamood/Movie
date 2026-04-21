# 🎬 Movie Explorer & AI Recommendation System

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-black)
![License](https://img.shields.io/badge/License-Educational-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![AI](https://img.shields.io/badge/AI-Gemini-orange)

---

## 📌 Abstract
The rapid growth of digital streaming platforms has resulted in an overwhelming amount of content, making it difficult for users to discover movies that match their preferences. This project presents a **Movie Explorer and AI-powered Recommendation System** that combines traditional recommendation techniques with modern AI.

The system integrates **Content-Based Filtering, Collaborative Filtering (SVD), and a Hybrid Model**, along with **Google Gemini AI** for intelligent recommendations. It enhances user experience by offering personalized suggestions, movie details, and trailers, ultimately improving engagement and content discovery.

---

## 📸 Screenshots

### 🔍 Home Page
![Home Page](screenshots/home.png)

### 🎥 Movie Details & Trailer
![Movie Details](screenshots/movie.png)

### 🤖 AI Recommendations
![AI Recommendations](screenshots/recommendation.png)

> 📌 *Note:* Create a folder named `screenshots` in your project and add images with these names.

---

## 🚀 Features
- 🔍 Search movies by title  
- 🎭 Filter movies by genre and popularity  
- 🤖 AI-based personalized recommendations  
- 🎥 Watch official trailers (YouTube integration)  
- ⭐ View IMDb ratings, plot, and cast  
- ❤️ Add movies to watchlist  
- ⭐ Rate movies locally (stored in browser)  
- ⚡ Fast performance with caching  

---

## 🛠️ Tech Stack

### Backend
- Python (Flask)
- OMDb API (Movie Data)
- YouTube Data API (Trailers)
- Google Gemini API (AI Recommendations)

### Frontend
- HTML5  
- Tailwind CSS  
- JavaScript (Vanilla)

### Libraries
- flask  
- requests  
- google-api-python-client  
- google-generativeai  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/movie-explorer.git
cd movie-explorer

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
Activate the environment:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

If requirements.txt is not available:

pip install flask requests google-api-python-client google-generativeai

4️⃣ Configure API Keys

Open app2.py and replace:

OMDB_API_KEY = "your_omdb_api_key"
YOUTUBE_API_KEY = "your_youtube_api_key"
GEMINI_API_KEY = "your_gemini_api_key"

Get API keys from:

OMDb API: http://www.omdbapi.com/apikey.aspx
YouTube API: https://console.cloud.google.com/
Gemini API: https://ai.google.dev/

5️⃣ Run the Application
python app2.py

6️⃣ Open in Browser
http://127.0.0.1:5000
