from pathlib import Path
import shutil

root = Path(__file__).resolve().parent

# Copy existing images to simpler static names
source_images = {
    'Images/Villa-Carafa-Apulia.jpg': 'static/images/hero.jpg',
    'Images/Villa-Carafa-Apulia.jpg': 'static/images/villa-carafa.jpg',
    'Images/Die Kathedralevon_Trani.jpg': 'static/images/cathedral-trani.jpg',
    'Images/Antrag.png': 'static/images/proposal.png',
}
for src, dst in source_images.items():
    shutil.copyfile(root / src, root / dst)

# Create placeholder SVG assets
svg_assets = {
    'static/images/story-1.svg': '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800">
  <rect width="1200" height="800" fill="#f4efe6"/>
  <circle cx="600" cy="420" r="240" fill="#c5a55a" fill-opacity="0.18"/>
  <rect x="240" y="220" width="720" height="360" rx="24" fill="#fffdf8" stroke="#c5a55a" stroke-width="8"/>
  <text x="600" y="390" text-anchor="middle" font-family="Georgia, serif" font-size="48" fill="#333">Unsere Geschichte</text>
  <text x="600" y="455" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#555">Ein Moment, den wir teilen werden</text>
</svg>
''',
    'static/images/story-2.svg': '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800">
  <rect width="1200" height="800" fill="#faf8f5"/>
  <rect x="180" y="180" width="840" height="440" rx="28" fill="#fff" stroke="#d4b96e" stroke-width="8"/>
  <circle cx="420" cy="420" r="140" fill="#c5a55a" fill-opacity="0.16"/>
  <text x="600" y="390" text-anchor="middle" font-family="Georgia, serif" font-size="44" fill="#333">Das erste Date</text>
  <text x="600" y="455" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#555">Ein schöner Anfang, der uns verbindet</text>
</svg>
''',
    'static/images/story-3.svg': '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800">
  <rect width="1200" height="800" fill="#f8f2e8"/>
  <rect x="200" y="180" width="800" height="440" rx="30" fill="#fffdf9" stroke="#c5a55a" stroke-width="8"/>
  <path d="M600 260c80 0 140 60 140 140 0 90-90 180-140 220-50-40-140-130-140-220 0-80 60-140 140-140z" fill="#c5a55a" fill-opacity="0.22"/>
  <text x="600" y="390" text-anchor="middle" font-family="Georgia, serif" font-size="44" fill="#333">Der Antrag</text>
  <text x="600" y="455" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#555">Der Moment, der alles verändert</text>
</svg>
''',
    'static/images/trauzeuge-severin.svg': '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
  <rect width="600" height="600" rx="32" fill="#f7efe1"/>
  <circle cx="300" cy="300" r="180" fill="#c5a55a" fill-opacity="0.24"/>
  <text x="300" y="285" text-anchor="middle" font-family="Georgia, serif" font-size="42" fill="#333">Severin</text>
  <text x="300" y="338" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#555">Trauzeuge</text>
</svg>
''',
    'static/images/trauzeuge-daniel.svg': '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
  <rect width="600" height="600" rx="32" fill="#f7efe1"/>
  <circle cx="300" cy="300" r="180" fill="#d4b96e" fill-opacity="0.24"/>
  <text x="300" y="285" text-anchor="middle" font-family="Georgia, serif" font-size="42" fill="#333">Daniel</text>
  <text x="300" y="338" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#555">Trauzeuge</text>
</svg>
''',
    'static/images/trauzeugin-cinzia.svg': '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
  <rect width="600" height="600" rx="32" fill="#f7efe1"/>
  <circle cx="300" cy="300" r="180" fill="#c5a55a" fill-opacity="0.20"/>
  <text x="300" y="285" text-anchor="middle" font-family="Georgia, serif" font-size="42" fill="#333">Cinzia</text>
  <text x="300" y="338" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#555">Trauzeugin</text>
</svg>
''',
    'static/images/trauzeugin-anouk.svg': '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
  <rect width="600" height="600" rx="32" fill="#f7efe1"/>
  <circle cx="300" cy="300" r="180" fill="#d4b96e" fill-opacity="0.18"/>
  <text x="300" y="285" text-anchor="middle" font-family="Georgia, serif" font-size="42" fill="#333">Anouk</text>
  <text x="300" y="338" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#555">Trauzeugin</text>
</svg>
''',
}
for rel_path, content in svg_assets.items():
    (root / rel_path).write_text(content, encoding='utf-8')

# Update the template to use Django static tags
index_path = root / 'templates/wedding/index.html'
text = index_path.read_text(encoding='utf-8')
text = text.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n{% load static %}\n', 1)
text = text.replace('href="style.css"', 'href="{% static \'css/style.css\' %}"')
text = text.replace('src="images/Die Kathedralevon_Trani.jpg"', 'src="{% static \'images/cathedral-trani.jpg\' %}"')
text = text.replace('src="images/Villa-Carafa-Apulia.jpg"', 'src="{% static \'images/villa-carafa.jpg\' %}"')
text = text.replace('src="images/story-1.jpg"', 'src="{% static \'images/story-1.svg\' %}"')
text = text.replace('src="images/story-2.jpg"', 'src="{% static \'images/story-2.svg\' %}"')
text = text.replace('src="images/Antrag.png"', 'src="{% static \'images/proposal.png\' %}"')
text = text.replace('src="images/trauzeuge-severin.jpg"', 'src="{% static \'images/trauzeuge-severin.svg\' %}"')
text = text.replace('src="images/trauzeuge-daniel.jpg"', 'src="{% static \'images/trauzeuge-daniel.svg\' %}"')
text = text.replace('src="images/trauzeugin-cinzia.jpg"', 'src="{% static \'images/trauzeugin-cinzia.svg\' %}"')
text = text.replace('src="images/trauzeugin-anouk.jpg"', 'src="{% static \'images/trauzeugin-anouk.svg\' %}"')
old_video = '''  <video class="hero-video" autoplay muted loop playsinline preload="auto">
      <source src="MARRIAGE PROPOSAL 2.mp4" type="video/mp4">
    </video>'''
new_video = '''  <img class="hero-video" src="{% static 'images/hero.jpg' %}" alt="Villa Carafa in Apulien" loading="eager">'''
if old_video in text:
    text = text.replace(old_video, new_video)
index_path.write_text(text, encoding='utf-8')

# Update CSS to reference the hero image via relative path
css_path = root / 'static/css/style.css'
css_text = css_path.read_text(encoding='utf-8')
css_text = css_text.replace("background: url('images/hero.jpg') center center / cover no-repeat;", "background: url('../images/hero.jpg') center center / cover no-repeat;")
css_path.write_text(css_text, encoding='utf-8')
