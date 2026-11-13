from pathlib import Path
import hashlib
import json
import shutil
from datetime import datetime, timezone

source = Path(__file__).resolve().parent.parent / 'nexus-b2a'
destination = Path(__file__).resolve().parent / 'nexus-vercel-preview'
if destination.exists():
    raise SystemExit('Preview directory exists; refusing to overwrite it.')
destination.mkdir(parents=True)
manifest = {}
for folder in ('app', 'schemas', 'data', 'tests'):
    for item in (source / folder).rglob('*'):
        if not item.is_file() or '__pycache__' in item.parts or item.suffix in ('.pyc', '.db') or item.name.startswith('.env'):
            continue
        relative = item.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = item.read_bytes()
        target.write_bytes(payload)
        manifest[str(relative)] = hashlib.sha256(payload).hexdigest()
for name in ('run_demo.py', 'pytest.ini'):
    shutil.copy2(source / name, destination / name)
database = destination / 'app/core/database.py'
text = database.read_text(encoding='utf-8')
old = 'default_db_path = str(Path(__file__).parent.parent.parent / "nexus_dev.db")'
assert old in text, 'Database source changed; adapter needs review'
text = text.replace('import sqlite3', 'import sqlite3\nimport tempfile', 1)
text = text.replace(old, 'default_db_path = str(Path(tempfile.gettempdir()) / "nexus_preview.db")')
database.write_text(text, encoding='utf-8')
(destination / 'source-manifest.json').write_text(json.dumps({'created_at': datetime.now(timezone.utc).isoformat(), 'source': str(source), 'files': manifest}, indent=2), encoding='utf-8')
print(json.dumps({'preview_directory': str(destination), 'source_files': len(manifest), 'source_files_modified': False}))
