# LUMO Studios

Creative production landing page with Three.js particle animation.

**Live site:** https://milesbrooksdev.github.io/lumostudios/

## Converting Your SolidWorks Speaker to Point Cloud

### 1. Export from SolidWorks

1. Open your speaker assembly in SolidWorks
2. **File → Save As**
3. Choose format: **STL** (preferred) or **OBJ**
4. Set options:
   - Binary STL (smaller file size)
   - Resolution: Fine (for smooth surfaces)
   - Export as single file (merge components if you want the whole speaker)

### 2. Install Converter Dependencies

```bash
pip install trimesh numpy
# Optional: for visualization preview
pip install matplotlib
```

### 3. Convert to Point Cloud

```bash
python convert_to_pcd.py your-speaker.stl speaker.pcd --points 15000
```

Options:
- `--points 15000` — Number of points to sample (default: 10000)
- `--vis` — Preview the point cloud before saving

For a speaker, 10,000–20,000 points usually looks good. More points = denser cloud but larger file.

### 4. Deploy

Copy the generated `speaker.pcd` to your repo and push:

```bash
cp speaker.pcd /path/to/lumostudios/
cd /path/to/lumostudios/
git add speaker.pcd
git commit -m "Add speaker point cloud"
git push
```

GitHub Pages will auto-deploy. The site will load your speaker instead of the demo point cloud.

### Tips

- **File too big?** Reduce `--points` to 5000–8000
- **Not enough detail?** Increase `--points` to 25000+
- **Preview looks wrong?** The converter centers and normalizes scale automatically
- **Missing parts?** Export individual speaker components (cone, cabinet, etc.) and convert separately

## Credits

Built with Three.js and the PCDLoader addon.
