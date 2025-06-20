# Photography Gallery File System

This folder contains the file-based photography gallery system. Simply upload your images and edit the metadata file to manage your gallery.

## 📁 Folder Structure

```
gallery/
├── README.md                 # This documentation file
├── metadata.json            # Image metadata and configuration
├── images/                  # Main images folder (create this folder)
│   ├── your-image-1.jpg
│   ├── your-image-2.png
│   └── ...
└── thumbnails/              # Optional: thumbnails folder (create this folder)
    ├── your-image-1_thumb.jpg
    └── ...
```

## 🖼️ Adding New Images

### Step 1: Upload Images
1. Create the `images/` folder if it doesn't exist
2. Upload your images to `gallery/images/`
3. Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`

### Step 2: Update Metadata
Edit `metadata.json` and add your image information:

```json
{
  "id": 17,
  "filename": "your-new-image.jpg",
  "title": "Your Image Title",
  "caption": "A detailed description of your image that will appear in the lightbox.",
  "metadata": {
    "camera": "Canon EOS R5",
    "lens": "RF 24-70mm f/2.8",
    "settings": "f/8 • 1/125s • ISO 100"
  },
  "tags": ["landscape", "sunset", "nature"],
  "category": "landscape",
  "featured": false,
  "sortOrder": 17,
  "aspectRatio": 1.5,
  "dimensions": {
    "width": 1920,
    "height": 1280
  },
  "location": "Location Name",
  "dateCreated": "2024-06-18"
}
```

## 📝 Metadata Fields Explained

### Required Fields
- **`id`**: Unique identifier (integer)
- **`filename`**: Exact filename in the images folder
- **`title`**: Display title for the image
- **`caption`**: Description shown in lightbox

### Optional Fields
- **`metadata`**: Camera/technical information
  - `camera`: Camera model
  - `lens`: Lens used
  - `settings`: Exposure settings (f-stop, shutter, ISO)
- **`tags`**: Array of keywords for categorization
- **`category`**: Main category (landscape, urban, abstract, etc.)
- **`featured`**: Boolean - highlight important images
- **`sortOrder`**: Number for custom ordering
- **`aspectRatio`**: Width/height ratio for layout calculation
- **`dimensions`**: Original image dimensions
- **`location`**: Where the photo was taken
- **`dateCreated`**: When the photo was created

## 🎯 Categories

The system supports flexible categorization:

- **`landscape`**: Nature, mountains, scenery
- **`urban`**: City, architecture, buildings  
- **`night`**: Low light, astrophotography
- **`abstract`**: Artistic, experimental
- **`street`**: Candid, people, urban life
- **`nature`**: Wildlife, plants, natural details
- **`portrait`**: People photography
- **`travel`**: Travel photography
- **`macro`**: Close-up photography

## 🔧 Advanced Configuration

### Gallery Settings
Modify the `gallery.settings` section in `metadata.json`:

```json
"settings": {
  "masonryBaseHeight": 320,      // Base height for grid calculation
  "masonryMinRows": 20,          // Minimum grid rows per image
  "masonryMaxRows": 50,          // Maximum grid rows per image
  "slideshowInterval": 4000,     // Slideshow timing in milliseconds
  "imageFormats": ["jpg", "jpeg", "png", "webp", "gif"],
  "enableLazyLoading": true,     // Performance optimization
  "enableKeyboardNavigation": true
}
```

### Image Ordering
Control display order with `sortOrder`:
- Lower numbers appear first
- Same numbers maintain file order
- Featured images can be promoted

### Aspect Ratios
The system automatically calculates grid layout based on `aspectRatio`:
- **1.0**: Square images
- **1.5**: Standard 3:2 ratio
- **1.78**: 16:9 widescreen
- **0.67**: Portrait 2:3 ratio

## 🚀 Quick Start

1. **Create folder structure:**
   ```
   mkdir gallery/images
   mkdir gallery/thumbnails  # optional
   ```

2. **Upload your first image:**
   ```
   Copy your-photo.jpg to gallery/images/
   ```

3. **Add to metadata.json:**
   ```json
   {
     "id": 1,
     "filename": "your-photo.jpg",
     "title": "My First Photo",
     "caption": "This is my first gallery image.",
     "aspectRatio": 1.5
   }
   ```

4. **Refresh your photography page** - the image will appear automatically!

## 📱 Performance Tips

### Image Optimization
- **Recommended size**: 1920px width maximum
- **File size**: Keep under 500KB for web performance
- **Format**: Use `.webp` for best compression
- **Quality**: 85-90% JPEG quality is optimal

### Thumbnails (Optional)
- Create smaller versions (400px width) in `thumbnails/` folder
- Name them: `original-name_thumb.jpg`
- Update metadata with `"thumbnail": "filename_thumb.jpg"`

## 🛠️ Troubleshooting

### Images Not Appearing
1. Check file path: `gallery/images/filename.jpg`
2. Verify filename matches metadata exactly
3. Ensure image format is supported
4. Check browser console for errors

### Layout Issues
1. Verify `aspectRatio` values are correct
2. Adjust `masonryBaseHeight` in settings
3. Check `dimensions` are accurate

### Metadata Validation
The system will fallback to filename-based titles if metadata is invalid. Always validate your JSON syntax.

## 🔄 Backup & Restore

### Backup Your Gallery
```bash
# Backup images and metadata
zip -r gallery-backup.zip gallery/
```

### Restore Gallery
```bash
# Restore from backup
unzip gallery-backup.zip
```

This file-based system gives you complete control over your photography gallery while maintaining professional presentation and performance.