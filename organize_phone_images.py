"""
Interactive script to organize images from phone into dataset folders
Shows each image and lets you categorize it as clean/medium/dirty
"""
import os
import shutil
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import argparse

class ImageOrganizer:
    def __init__(self, source_folder, target_base='raw_data'):
        self.source_folder = Path(source_folder)
        self.target_base = Path(target_base)
        self.categories = ['clean', 'medium', 'dirty']
        
        # Create target directories
        for cat in self.categories:
            (self.target_base / cat).mkdir(parents=True, exist_ok=True)
        
        # Get all images
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG']
        self.images = []
        for ext in self.image_extensions:
            self.images.extend(self.source_folder.glob(f'*{ext}'))
            # Also check subdirectories
            self.images.extend(self.source_folder.glob(f'**/*{ext}'))
        
        # Remove duplicates and sort
        self.images = sorted(list(set(self.images)))
        
        # Counters
        self.counts = {cat: len(list((self.target_base / cat).glob('*.jpg'))) + 
                              len(list((self.target_base / cat).glob('*.png'))) 
                       for cat in self.categories}
        
        self.current_index = 0
        
        if not self.images:
            print(f"No images found in {source_folder}")
            return
        
        print(f"\nFound {len(self.images)} images to organize")
        print(f"Current counts: clean={self.counts['clean']}, medium={self.counts['medium']}, dirty={self.counts['dirty']}")
        
    def organize_gui(self):
        """GUI version - shows image and buttons"""
        if not self.images:
            return
        
        root = tk.Tk()
        root.title("Organize Phone Images")
        root.geometry("800x700")
        
        # Image display
        img_label = tk.Label(root)
        img_label.pack(pady=10)
        
        # Info label
        info_label = tk.Label(root, text="", font=("Arial", 12))
        info_label.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        def load_image():
            if self.current_index >= len(self.images):
                messagebox.showinfo("Complete", f"All images organized!\n\nFinal counts:\nClean: {self.counts['clean']}\nMedium: {self.counts['medium']}\nDirty: {self.counts['dirty']}")
                root.quit()
                return
            
            img_path = self.images[self.current_index]
            
            # Load and display image
            try:
                img = Image.open(img_path)
                # Resize for display (max 600x600)
                img.thumbnail((600, 600), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label.config(image=photo)
                img_label.image = photo  # Keep a reference
                
                # Update info
                info_label.config(text=f"Image {self.current_index + 1}/{len(self.images)}\n{img_path.name}\nSize: {img.size}")
            except Exception as e:
                info_label.config(text=f"Error loading image: {e}")
        
        def categorize(category):
            if self.current_index >= len(self.images):
                return
            
            img_path = self.images[self.current_index]
            
            # Determine file extension
            ext = img_path.suffix.lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                ext = '.jpg'
            
            # Generate filename
            self.counts[category] += 1
            new_filename = f"{category}_{self.counts[category]:04d}{ext}"
            target_path = self.target_base / category / new_filename
            
            # Copy file
            try:
                shutil.copy(img_path, target_path)
                print(f"Saved: {img_path.name} → {target_path}")
                
                # Move to next image
                self.current_index += 1
                load_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
        
        # Create buttons
        btn_clean = tk.Button(button_frame, text="Clean", command=lambda: categorize('clean'), 
                              bg='#4CAF50', fg='white', font=("Arial", 14), width=15, height=2)
        btn_clean.pack(side=tk.LEFT, padx=10)
        
        btn_medium = tk.Button(button_frame, text="Medium", command=lambda: categorize('medium'), 
                               bg='#FF9800', fg='white', font=("Arial", 14), width=15, height=2)
        btn_medium.pack(side=tk.LEFT, padx=10)
        
        btn_dirty = tk.Button(button_frame, text="Dirty", command=lambda: categorize('dirty'), 
                             bg='#F44336', fg='white', font=("Arial", 14), width=15, height=2)
        btn_dirty.pack(side=tk.LEFT, padx=10)
        
        # Skip button
        btn_skip = tk.Button(root, text="Skip", command=lambda: [setattr(self, 'current_index', self.current_index + 1), load_image()],
                             font=("Arial", 12))
        btn_skip.pack(pady=10)
        
        # Stats label
        stats_label = tk.Label(root, text="", font=("Arial", 10))
        stats_label.pack(pady=5)
        
        def update_stats():
            stats_label.config(text=f"Clean: {self.counts['clean']} | Medium: {self.counts['medium']} | Dirty: {self.counts['dirty']}")
            root.after(100, update_stats)
        
        # Load first image
        load_image()
        update_stats()
        
        # Keyboard shortcuts
        root.bind('c', lambda e: categorize('clean'))
        root.bind('m', lambda e: categorize('medium'))
        root.bind('d', lambda e: categorize('dirty'))
        root.bind('<Right>', lambda e: [setattr(self, 'current_index', self.current_index + 1), load_image()])
        root.bind('<Left>', lambda e: [setattr(self, 'current_index', max(0, self.current_index - 1)), load_image()])
        
        root.mainloop()
    
    def organize_cli(self):
        """Command-line version - shows image path and asks for category"""
        if not self.images:
            return
        
        print("\n" + "="*60)
        print("Organizing Images - Command Line Mode")
        print("="*60)
        print("\nInstructions:")
        print("  Press 'c' for clean")
        print("  Press 'm' for medium")
        print("  Press 'd' for dirty")
        print("  Press 's' to skip")
        print("  Press 'q' to quit")
        print("="*60 + "\n")
        
        for i, img_path in enumerate(self.images, 1):
            print(f"\n[{i}/{len(self.images)}] {img_path.name}")
            
            # Try to show image info
            try:
                img = Image.open(img_path)
                print(f"  Size: {img.size}, Format: {img.format}")
            except Exception as e:
                print(f"  Error opening image: {e}")
            
            while True:
                choice = input("  Category (c/m/d/s/q): ").lower().strip()
                
                if choice == 'q':
                    print("\nStopped organizing")
                    return
                elif choice == 's':
                    print("  Skipped")
                    break
                elif choice in ['c', 'm', 'd']:
                    category = {'c': 'clean', 'm': 'medium', 'd': 'dirty'}[choice]
                    
                    # Determine file extension
                    ext = img_path.suffix.lower()
                    if ext not in ['.jpg', '.jpeg', '.png']:
                        ext = '.jpg'
                    
                    # Generate filename
                    self.counts[category] += 1
                    new_filename = f"{category}_{self.counts[category]:04d}{ext}"
                    target_path = self.target_base / category / new_filename
                    
                    # Copy file
                    try:
                        shutil.copy(img_path, target_path)
                        print(f"  → Saved to {target_path}")
                        break
                    except Exception as e:
                        print(f"  Error: {e}")
                        break
                else:
                    print("  Invalid choice. Use c/m/d/s/q")
        
        print(f"\n\nOrganization complete!")
        print(f"Summary:")
        for cat in self.categories:
            print(f"  {cat}: {self.counts[cat]} images")

def organize_from_phone_folder(source_folder, target_base='raw_data', gui=True):
    """
    Organize images from phone folder into dataset structure
    
    Args:
        source_folder: Folder containing phone images
        target_base: Base directory for organized images
        gui: Use GUI (True) or CLI (False)
    """
    organizer = ImageOrganizer(source_folder, target_base)
    
    if not organizer.images:
        print(f"No images found in {source_folder}")
        return
    
    if gui:
        try:
            organizer.organize_gui()
        except Exception as e:
            print(f"GUI failed: {e}")
            print("Falling back to command-line mode...")
            organizer.organize_cli()
    else:
        organizer.organize_cli()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize phone images into dataset folders')
    parser.add_argument('--source', type=str, default=None,
                       help='Source folder with phone images (if not provided, will ask)')
    parser.add_argument('--target', type=str, default='raw_data',
                       help='Target base directory (default: raw_data)')
    parser.add_argument('--cli', action='store_true',
                       help='Use command-line interface instead of GUI')
    
    args = parser.parse_args()
    
    # If source not provided, try common locations
    if args.source is None:
        # Try to find images in Downloads or Desktop
        common_locations = [
            Path.home() / 'Downloads',
            Path.home() / 'Desktop',
            Path('.').absolute(),
        ]
        
        print("Looking for images in common locations...")
        for loc in common_locations:
            if loc.exists():
                images = list(loc.glob('*.jpg')) + list(loc.glob('*.png'))
                if images:
                    print(f"Found {len(images)} images in {loc}")
                    use = input(f"Use this folder? (y/n): ").lower()
                    if use == 'y':
                        args.source = str(loc)
                        break
        
        if args.source is None:
            args.source = input("Enter path to folder with phone images: ").strip()
    
    if not args.source or not Path(args.source).exists():
        print(f"Error: Source folder '{args.source}' does not exist")
        exit(1)
    
    organize_from_phone_folder(args.source, args.target, gui=not args.cli)
