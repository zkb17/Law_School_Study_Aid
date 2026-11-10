from pathlib import Path
ROOT=Path(__file__).resolve().parent
html=(ROOT/'index.html').read_text()
css=(ROOT/'styles.css').read_text()
html=html.replace('<link rel="stylesheet" href="styles.css" />',f'<style>\n{css}\n</style>')
html=html.replace('<link rel="icon" href="favicon.svg" type="image/svg+xml" />','')
for f in ['data.js','cards.js','expanded-flashcards.js','expanded-bank.js','app.js']:
    js=(ROOT/f).read_text()
    assert '</script' not in js.lower(),f
    script=f'<script src="{f}"></script>'
    assert html.count(script)==1,f
    html=html.replace(script,f'\n<!-- {f} -->\n<script>\n{js}\n</script>')
assert '<script src=' not in html
out=Path('/mnt/data/Nebraska_Law_Study_Hub_828_Flashcards.html')
out.write_text(html,encoding='utf-8')
print('Standalone generated:',out, out.stat().st_size)
