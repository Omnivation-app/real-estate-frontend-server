from flask import Flask

app = Flask(__name__)

# HTML du frontend
HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real Estate - Annonces Immobilières</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .search-container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }

        .search-box input {
            flex: 1;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            transition: border-color 0.3s;
        }

        .search-box input:focus {
            outline: none;
            border-color: #667eea;
        }

        .search-box button {
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s;
        }

        .search-box button:hover {
            background: #764ba2;
        }

        .listings-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .listing-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }

        .listing-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }

        .listing-image {
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: white;
            padding: 20px;
            text-align: center;
            word-wrap: break-word;
        }

        .listing-content {
            padding: 20px;
        }

        .listing-title {
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }

        .listing-location {
            color: #666;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .loading {
            text-align: center;
            padding: 40px;
            font-size: 1.2em;
            color: #666;
        }

        .no-results {
            text-align: center;
            padding: 40px;
            font-size: 1.1em;
            color: #999;
            grid-column: 1 / -1;
        }

        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .result-count {
            text-align: center;
            padding: 20px;
            background: #e8f4f8;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: bold;
            color: #667eea;
        }
    </style>
</head>
<body>
    <header>
        <h1>🏠 Real Estate</h1>
        <p>Trouvez votre maison de rêve</p>
    </header>

    <div class="search-container">
        <div class="search-box">
            <input 
                type="text" 
                id="searchInput" 
                placeholder="Rechercher par lieu (ex: Cannes, Paris, Lyon...)"
            >
            <button onclick="search()">🔍 Rechercher</button>
        </div>
        <div id="error" class="error" style="display: none;"></div>
        <div id="resultCount" class="result-count" style="display: none;"></div>
    </div>

    <div id="loading" class="loading" style="display: none;">
        ⏳ Chargement des annonces... Cela peut prendre quelques minutes...
    </div>

    <div id="listings" class="listings-grid"></div>

    <footer>
        <p>&copy; 2026 Real Estate - Tous droits réservés</p>
    </footer>

    <script>
        const API_URL = 'https://omnivation-api-81002a93597c.herokuapp.com';

        async function search() {
            const searchTerm = document.getElementById('searchInput').value;
            await loadListings(searchTerm);
        }

        async function loadListings(location = '') {
            const loading = document.getElementById('loading');
            const listings = document.getElementById('listings');
            const error = document.getElementById('error');
            const resultCount = document.getElementById('resultCount');

            loading.style.display = 'block';
            listings.innerHTML = '';
            error.style.display = 'none';
            resultCount.style.display = 'none';

            try {
                // Utiliser l'API de scraping en temps reel
                let url = `${API_URL}/api/search-realtime`;
                if (location) {
                    url += `?location=${encodeURIComponent(location)}`;
                }

                const response = await fetch(url);
                if (!response.ok) throw new Error('Erreur lors du chargement');

                const data = await response.json();
                const listingsData = data.listings || [];

                loading.style.display = 'none';

                if (listingsData.length === 0) {
                    listings.innerHTML = `<div class="no-results">Aucune annonce trouvée pour "${location}"</div>`;
                    return;
                }

                // Afficher le nombre de résultats
                resultCount.innerHTML = `✅ ${listingsData.length} annonces trouvées pour "${location}"`;
                resultCount.style.display = 'block';

                listingsData.forEach(listing => {
                    const card = document.createElement('div');
                    card.className = 'listing-card';
                    const agencyName = listing.agency_name || 'Agence';
                    const agencyPhone = listing.agency_phone || '';
                    const agencyRating = listing.agency_rating || 0;
                    const url = listing.url || '#';
                    
                    card.innerHTML = `
                        <div class="listing-image">
                            📷 ${listing.title.substring(0, 50)}
                        </div>
                        <div class="listing-content">
                            <div class="listing-title">${listing.title.substring(0, 100)}</div>
                            <div class="listing-location">🏢 ${agencyName}</div>
                            <div style="font-size: 0.9em; color: #666; margin-top: 10px;">
                                ${agencyPhone ? '📞 ' + agencyPhone : 'Téléphone non disponible'}
                            </div>
                            ${agencyRating ? `<div style="color: #f39c12; margin-top: 5px;">⭐ ${agencyRating}/5</div>` : ''}
                            <div style="margin-top: 10px;">
                                <a href="${url}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">Voir l'annonce →</a>
                            </div>
                        </div>
                    `;
                    listings.appendChild(card);
                });

            } catch (err) {
                loading.style.display = 'none';
                error.style.display = 'block';
                error.innerHTML = `❌ Erreur: ${err.message}`;
            }
        }

        // Afficher un message d'accueil au démarrage
        window.addEventListener('load', () => {
            const listings = document.getElementById('listings');
            listings.innerHTML = '<div class="no-results" style="grid-column: 1 / -1; padding: 60px 20px; text-align: center;"><h2 style="font-size: 2em; margin-bottom: 20px; color: #667eea;">Bienvenue sur Real Estate</h2><p style="font-size: 1.1em; color: #666; margin-bottom: 30px;">Recherchez des annonces immobilieres par lieu</p><p style="color: #999;">Exemples: Nice, Cannes, Antibes, Toulon, Frejus...</p></div>';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_CONTENT

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
