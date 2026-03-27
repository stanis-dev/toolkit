"""Analyze audio files with VibeNet and store features in PostgreSQL.

Run inside the vibenet Docker container with music mounted at /music.
Connects to PostgreSQL at host.docker.internal:5432.

Usage:
  # Analyze new/missing tracks only (incremental)
  python3 vibenet-analyze.py

  # Analyze specific files
  python3 vibenet-analyze.py "/music/Artist/Album/track.flac"

  # Force re-analyze everything
  python3 vibenet-analyze.py --full
"""
import vibenet, psycopg2, os, sys

MUSIC_DIR = "/music"
EXTENSIONS = (".flac", ".mp3", ".ogg", ".m4a", ".wav")
DB_DSN = "host=host.docker.internal port=5432 dbname=music user=postgres password=password"

def get_conn():
    return psycopg2.connect(DB_DSN)

def get_existing_paths(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT file_path FROM audio_features")
        return {row[0] for row in cur.fetchall()}

def analyze(model, path):
    r = model.predict(path)[0]
    return (
        round(float(r.energy), 4),
        round(float(r.valence), 4),
        round(float(r.instrumentalness), 4),
        round(float(r.speechiness), 4),
        round(float(r.danceability), 4),
        round(float(r.acousticness), 4),
        round(float(r.liveness), 4),
    )

def find_all_tracks():
    tracks = []
    for root, dirs, files in os.walk(MUSIC_DIR):
        dirs[:] = [d for d in dirs if d != "deleted"]
        for f in sorted(files):
            if f.lower().endswith(EXTENSIONS):
                tracks.append(os.path.join(root, f))
    return tracks

UPSERT = """
INSERT INTO audio_features (file_path, energy, valence, instrumentalness, speechiness, danceability, acousticness, liveness)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (file_path) DO UPDATE SET
    energy=EXCLUDED.energy, valence=EXCLUDED.valence,
    instrumentalness=EXCLUDED.instrumentalness, speechiness=EXCLUDED.speechiness,
    danceability=EXCLUDED.danceability, acousticness=EXCLUDED.acousticness,
    liveness=EXCLUDED.liveness, analyzed_at=NOW()
"""

def main():
    conn = get_conn()
    model = vibenet.load_model()
    full = "--full" in sys.argv
    specific = [a for a in sys.argv[1:] if not a.startswith("--")]

    if specific:
        to_process = specific
    else:
        all_tracks = find_all_tracks()
        if full:
            to_process = all_tracks
        else:
            existing = get_existing_paths(conn)
            to_process = [t for t in all_tracks
                          if os.path.relpath(t, MUSIC_DIR) not in existing]

    if not to_process:
        print("No new tracks to process.")
        conn.close()
        return

    print(f"Processing {len(to_process)} tracks...")
    count = 0
    errors = 0
    with conn.cursor() as cur:
        for path in to_process:
            rel = os.path.relpath(path, MUSIC_DIR) if path.startswith(MUSIC_DIR) else path
            try:
                features = analyze(model, path)
                cur.execute(UPSERT, (rel,) + features)
                count += 1
                if count % 10 == 0:
                    conn.commit()
                    print(f"  {count}/{len(to_process)}...", flush=True)
            except Exception as e:
                errors += 1
                print(f"  ERROR: {rel}: {e}", file=sys.stderr, flush=True)
        conn.commit()

    conn.close()
    print(f"Done. {count} tracks analyzed, {errors} errors.")

if __name__ == "__main__":
    main()
