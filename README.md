# AI Conversations Website (Static Version)

This repository contains a minimalist, shareable website for displaying AI conversations as supplementary material for a research paper.

## How to Use

1. **Deploy to GitHub Pages**
   - Push all files in this folder to your GitHub repository (e.g., `yourusername/ai-conversations-website`).
   - Enable GitHub Pages in your repository settings (set the source to the `main` branch or `/docs` folder as needed).
   - The site will be available at `https://yourusername.github.io/ai-conversations-website/`.

2. **Add Conversations**
   - Place your conversation folders and markdown files inside the `AI_Conversations` directory.
   - The website will automatically display all conversations in the sidebar.

## Folder Structure

- `index.html` — Main website file
- `css/` — Stylesheets
- `js/` — JavaScript (including markdown parser)
- `AI_Conversations/` — All your AI conversation folders and markdown files

## Features
- Minimalist, responsive, and dark-mode friendly UI
- Automatic detection of new conversation files
- Markdown rendering with code block support

---

**Note:** This static version does not require Node.js or a backend. All content is loaded client-side. For dynamic or private content, use the Node.js version. 