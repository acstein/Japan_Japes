# 🇯🇵 Japan Trip Planner

A simple web app for storing and visualizing locations for your trip to Japan.
Add destinations, view them in a table, and see them plotted on an interactive map.

## ✨ Features

🗺️ Interactive Map — View all saved locations across Japan.

📋 Data Table — Easily review and edit the location list using a clean Streamlit DataFrame interface.

➕ Add Locations — Save new spots (e.g., restaurants, temples, hotels) with coordinates and notes.

💾 Persistent Storage — Trip data stays saved in Supabase for easy access and updates.

## 🧰 Tech Stack

* Python (for backend logic and data handling)

* Pandas (for managing location data in a DataFrame)

* Plotly (for map visualization — depending on your setup)

* Streamlit (dashboarding and deployed with Streamlit Cloud)

* Supabase (for back-end database)

## 🚀 Getting Started

Visit the [app](https://japan-japes.streamlit.app/) - hosted on Streamlit Cloud!

## 📍 Example Data
| place_id | created_at | name | description | importance | lat | lon | link | place_type |
|----------|------------|------|-------------|------------|-----|-----|------|------------|
| abc123hash1 | 2025-10-28T20:55:30 | Tokyo Tower | Great city view | 5 | 35.6586 | 139.7454 | N/A | Location |
| def456hash2 | 2025-10-28T20:55:30 | Kyoto Station | Central travel hub | 6 | 34.9858 | 135.7588 | N/A | Location |
| hij789hash3 | 2025-10-28T20:55:30 | Fushimi Inari | Famous red torii gates | 10 | 34.9671 | 135.7727 | N/A | Location |

## 📄 License

This project is licensed under the MIT License.
