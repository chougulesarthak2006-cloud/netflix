#!/usr/bin/env python3
"""
visualization/api/index.py
--------------------------
Vercel Serverless Function entrypoint for internal 'visualization' service.
Provides chart metadata and visualization endpoints for internal service calls.
"""

import json
from http.server import BaseHTTPRequestHandler

CHARTS = [
    {"filename": "01_movies_vs_tv_shows.png", "url": "/results/charts/01_movies_vs_tv_shows.png", "title": "01 Movies Vs Tv Shows"},
    {"filename": "02_releases_by_year.png", "url": "/results/charts/02_releases_by_year.png", "title": "02 Releases By Year"},
    {"filename": "03_top_10_countries.png", "url": "/results/charts/03_top_10_countries.png", "title": "03 Top 10 Countries"},
    {"filename": "04_ratings_distribution.png", "url": "/results/charts/04_ratings_distribution.png", "title": "04 Ratings Distribution"},
    {"filename": "05_top_10_genres.png", "url": "/results/charts/05_top_10_genres.png", "title": "05 Top 10 Genres"},
    {"filename": "06_titles_added_by_year.png", "url": "/results/charts/06_titles_added_by_year.png", "title": "06 Titles Added By Year"},
    {"filename": "netflix_analysis_dashboard.png", "url": "/results/charts/netflix_analysis_dashboard.png", "title": "Netflix Analysis Dashboard"}
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        clean_path = self.path.split("?")[0]

        if clean_path in ["/api/charts", "/charts", "/"]:
            self.send_json(CHARTS)
        elif clean_path == "/api/health":
            self.send_json({"status": "healthy", "service": "visualization", "chart_count": len(CHARTS)})
        else:
            self.send_json({"error": "Endpoint not found on visualization service"}, status=404)

    def send_json(self, data, status=200):
        content = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content)
