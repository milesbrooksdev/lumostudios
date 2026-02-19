#!/usr/bin/env python3
"""
STL/OBJ to PCD Converter
Convert SolidWorks mesh exports to point cloud format for Three.js

Usage:
    python convert_to_pcd.py input.stl output.pcd --points 10000
    python convert_to_pcd.py speaker.obj speaker.pcd --points 5000 --vis

Requirements:
    pip install trimesh numpy
"""

import argparse
import struct
import numpy as np
import trimesh


def sample_points_from_mesh(mesh_path, num_points=10000):
    """
    Load mesh and sample points from its surface.
    Uses trimesh's sample method which distributes points by surface area.
    """
    print(f"Loading mesh: {mesh_path}")
    mesh = trimesh.load(mesh_path, force='mesh')
    
    print(f"Mesh has {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    print(f"Sampling {num_points} points from surface...")
    
    # Sample points evenly distributed by surface area
    points = mesh.sample(num_points)
    
    # Center the point cloud at origin
    centroid = np.mean(points, axis=0)
    points = points - centroid
    
    # Normalize scale to fit in view (roughly -0.5 to 0.5 range)
    max_dist = np.max(np.linalg.norm(points, axis=1))
    if max_dist > 0:
        points = points / (max_dist * 2)
    
    print(f"Point cloud bounds: {np.min(points, axis=0)} to {np.max(points, axis=0)}")
    
    return points


def write_pcd_binary(points, output_path):
    """
    Write points to binary PCD file format.
    Matches the format expected by Three.js PCDLoader.
    """
    num_points = len(points)
    
    # PCD header
    header = f"""# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH {num_points}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {num_points}
DATA binary
"""
    
    with open(output_path, 'wb') as f:
        f.write(header.encode('ascii'))
        # Write points as 32-bit floats (little-endian)
        for point in points:
            f.write(struct.pack('<fff', point[0], point[1], point[2]))
    
    print(f"Saved {num_points} points to: {output_path}")


def preview_point_cloud(points):
    """Open a quick matplotlib visualization."""
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Sample for display if too many points
        display_points = points[::max(1, len(points)//5000)]
        
        ax.scatter(display_points[:, 0], display_points[:, 1], display_points[:, 2],
                   c='#e67e22', s=1, alpha=0.6)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Point Cloud Preview ({len(points)} points)')
        
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("Install matplotlib to use --vis: pip install matplotlib")


def main():
    parser = argparse.ArgumentParser(
        description='Convert STL/OBJ mesh to PCD point cloud for Three.js'
    )
    parser.add_argument('input', help='Input mesh file (.stl or .obj)')
    parser.add_argument('output', help='Output PCD file (.pcd)')
    parser.add_argument('--points', '-p', type=int, default=10000,
                        help='Number of points to sample (default: 10000)')
    parser.add_argument('--vis', '-v', action='store_true',
                        help='Show preview visualization')
    
    args = parser.parse_args()
    
    # Sample points from mesh
    points = sample_points_from_mesh(args.input, args.points)
    
    # Preview if requested
    if args.vis:
        preview_point_cloud(points)
    
    # Write PCD file
    write_pcd_binary(points, args.output)
    
    print("Done! Copy the .pcd file to your repo and update the loader path.")


if __name__ == '__main__':
    main()
