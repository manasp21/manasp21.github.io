# Blog Images Structure

## Directory Organization

### `/posts/YYYY/`
Original high-quality images used in blog post content.
- **Naming**: `post-slug-hero.jpg` (or .png, .webp)
- **Usage**: Place at the start of blog posts for hero images
- **Processing**: Source for automatic cover generation

### `/covers/YYYY/`
Auto-generated blurred cover versions for thumbnails and hero banners.
- **Naming**: `post-slug-cover-blur.jpg`
- **Usage**: Automatically used in blog index and post headers
- **Generation**: Created by blog manager script from posts/ images

## Image Specifications

### Original Images (posts/)
- **Recommended size**: 1200x800px or larger
- **Format**: JPEG, PNG, or WebP
- **Quality**: High resolution for crisp display in post content

### Generated Covers (covers/)
- **Hero size**: 1200x400px (for post headers)
- **Thumbnail size**: 300x200px (for blog index cards)
- **Effect**: Gaussian blur + 20% dark overlay
- **Format**: Optimized JPEG (85% quality)

## Usage Workflow

1. **Add image to post**: Place image at start of blog post markdown
2. **Auto-generation**: Blog manager automatically creates blurred cover
3. **YAML update**: Frontmatter updated with image paths
4. **Display**: Covers used in blog index and post hero sections

## File Examples

```
posts/2025/ai-future-hero.jpg          → Original image in post
covers/2025/ai-future-cover-blur.jpg   → Auto-generated blurred cover
```

## Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)