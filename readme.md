
# Labels Influence Graph Analysis

This project investigates the structural patterns behind artist **collaborations** in the contemporary **music industry** using a **graph-based approach**. By modeling the Spotify artist network as a graph, we analyze how specific artist features influence the formation of these connections. In particular, we focus on two key attributes: **musical genre** and **record label affiliation**. Using standard graph analysis techniques we explore how these features relate to network structure and cluster formation. Our results highlight musical genre as the most significant driver of collaborations, with label affiliation  playing a marginal role. The study provides a data-driven perspective on how artist communities are shaped in the modern music ecosystem.

## Setup

1. Register on both platforms:
   - Spotify Developer: https://developer.spotify.com/dashboard/applications
   - Last.fm API: https://www.last.fm/api/account/create

2. Create a `.env` file in the project folder with this format:

```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
LAST_FM=your_lastfm_api_key
ACCESS_TOKEN='put_the_token_here_after_getting_it'
```

## ⚙️ Workflow

- Step 1: Get the Spotify access token  
  `python getTokenSpoty.py` -> semplicemente di da il token che scade ogni ora e lo salva nell .env

- Step 2: Get artists from Last.fm and normalize its genre
  `python lastfmApiGetArtistandNormalizeGenre.py`

Step 5: Normalize Labels

`python labelMapper.py`

Usa il CSV `label_hierarchy.csv` aggiornato.

Mappa ogni etichetta grezza sulla sua major label (Universal, Sony, Warner...).

Se non trova corrispondenze ➔ automaticamente "Independent".


- Step 4: Get album info from Spotify (last album, features, label)  
  `python SpotifyApiGetAlbumData.py` -> this work actually but there can be other logic to be implemeneted to have more data like fetching all the features data another time, like to have more connection.

- Step 5: Filter Albums by Genre and Period

  `python filterGenresAndTimePeriod.py`

      Filtra i dati in base a:
          Genere normalizzato (es: "Pop", "Rock", ecc.)
          Periodo di pubblicazione (es: dopo il 2020)

  Output ➔ file tipo pop_post_2020-01-01_albums.json

- Step 6: Build and Visualize the Graph

    A seconda del tipo di analisi:

        Per analisi generiche sui dati filtrati:

    `python genreGraph.py`
    Per analisi clusterizzate per label:

    `python labelsGraph.py`

    Output:

        File grafici .png

        Grafi .graphml, .gexf

        Statistiche .txt

- Step 7: Analysis
  `cd analysis`
  `python runner.py` This will make the analysis for both labels and genres
  You can run just for one of them by specifying an attribute:
  `python runner.py [attribute]`
  Accepted attributes: 'main_genre', 'major_label'

## Attention
If you notice different number of nodes in the analysis of genres wrt the analysis of labels, it's because in the labels' analysis we filter out albums published with multiple labels.

## Filter by genre (2 order analysis)
Workflow to analyze the second order effects (of labels) obtained by fixing a genre.

- Step 1: change `TARGET_GENRE` in `filterGenresAndTimePeriod.py`. Then run:

    `python filterGenresAndTimePeriod.py`

- Step 2: run labels Graph using the generated json file

    `python3 labelsGraph.py data/Pop_post_2023-01-01_albums.json`

- Step 3: analysis
    `cd analysis`
    `python runner.py major_label`
