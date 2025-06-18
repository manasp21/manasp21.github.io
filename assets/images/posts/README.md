# Blog Post Images Organization

This directory contains images used in blog posts, organized by topic/category for easy management.

## Directory Structure

```
assets/images/posts/
├── quantum-computing/     # Images for quantum computing posts
├── music/                 # Images for music-related posts
├── programming/           # Images for programming/technical posts
├── research/             # Images for research posts
├── personal/             # Images for personal posts
└── general/              # General blog images not fitting other categories
```

## Usage in Posts

To include images in blog posts, use the Jekyll include:

```markdown
{% include image.html src="quantum-computing/circuit-diagram.png" alt="Quantum circuit diagram" caption="A simple quantum circuit showing superposition" %}
```

## Naming Conventions

- Use descriptive, kebab-case filenames: `quantum-circuit-diagram.png`
- Include post date or topic reference when helpful: `2024-01-quantum-ml-results.png`
- Use web-optimized formats (PNG for diagrams, JPG for photos, WebP when supported)

## Image Optimization

- Keep images under 1MB when possible
- Use appropriate dimensions (max 1200px width for blog content)
- Compress images while maintaining quality
- Include alt text for accessibility

## Categories

- **quantum-computing/**: Quantum circuits, algorithms, research diagrams
- **music/**: Harmonium photos, musical notation, instrument images
- **programming/**: Code screenshots, development setup, technical diagrams
- **research/**: Lab equipment, experimental setups, data visualizations
- **personal/**: Personal photos, campus life, hobbies
- **general/**: Headers, decorative images, misc content