import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import matplotlib.patheffects as path_effects
from scipy.interpolate import splprep, splev
import random

# Create figure with black background
plt.figure(figsize=(12, 10), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

# Function to create heart shape with sketch effect
def sketch_heart(x0, y0, size, noise_level=0.02):
    # Parametric equations for a heart shape
    t = np.linspace(0, 2*np.pi, 100)
    x = x0 + size * 16 * np.sin(t)**3
    y = y0 + size * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
    
    # Add some noise to create sketch effect
    noise_x = np.array([random.gauss(0, noise_level) for _ in range(len(x))])
    noise_y = np.array([random.gauss(0, noise_level) for _ in range(len(y))])
    
    x_noisy = x + noise_x * size
    y_noisy = y + noise_y * size
    
    return x_noisy, y_noisy

# Function to create pencil stroke effect
def pencil_effect(x, y, ax, color='#CCCCCC', alpha=0.6, linewidth=1.5):
    # Create multiple slightly offset lines to simulate pencil strokes
    for i in range(5):
        noise = 0.01 * np.random.randn(len(x))
        ax.plot(x + noise, y + noise, color=color, alpha=alpha/2, linewidth=linewidth, zorder=1)
    
    # Main outline
    ax.plot(x, y, color='white', alpha=alpha, linewidth=linewidth+0.5, zorder=2)
    
    # Add some random short strokes for texture
    for _ in range(20):
        idx = np.random.randint(0, len(x)-5)
        length = np.random.randint(3, 10)
        ax.plot(x[idx:idx+length], y[idx:idx+length], color='white', 
                alpha=alpha*0.8, linewidth=linewidth*0.7, zorder=1)

# Draw multiple hearts with sketch effect
heart_positions = [
    (0, 0, 1),      # Center heart
    (-5, 5, 0.7),   # Top left heart
    (5, 5, 0.7),    # Top right heart
    (-5, -5, 0.7),  # Bottom left heart
    (5, -5, 0.7)    # Bottom right heart
]

# Add some random smaller hearts for decoration
for _ in range(8):
    x_pos = random.uniform(-8, 8)
    y_pos = random.uniform(-8, 8)
    # Avoid placing small hearts too close to the main hearts
    if any(np.sqrt((x_pos-x)**2 + (y_pos-y)**2) < 2 for x, y, _ in heart_positions):
        continue
    heart_positions.append((x_pos, y_pos, random.uniform(0.2, 0.4)))

# Draw all hearts with pencil effect
for x0, y0, size in heart_positions:
    x, y = sketch_heart(x0, y0, size)
    
    # Create shading effect inside the heart
    plt.fill(x, y, color='#333333', alpha=0.3, zorder=1)
    
    # Add pencil stroke effect
    pencil_effect(x, y, ax, color='#DDDDDD', alpha=0.8, linewidth=1.5*size)
    
    # Add some cross-hatching for shading
    if size > 0.5:  # Only for larger hearts
        for i in range(20):
            start_idx = np.random.randint(0, len(x)//2)
            end_idx = np.random.randint(len(x)//2, len(x))
            plt.plot([x[start_idx], x[end_idx]], [y[start_idx], y[end_idx]], 
                     color='white', alpha=0.1, linewidth=0.5, zorder=1)

# Add the name "شهد" in an elegant font in the center
name = "شهد"
text = plt.text(0, 0, name, 
         fontsize=60, 
         color='white',
         family='DejaVu Sans',  # Arabic-compatible font
         ha='center', 
         va='center',
         weight='bold',
         zorder=10)

# Add glow effect to the text
text.set_path_effects([
    path_effects.Stroke(linewidth=3, foreground='#888888'),
    path_effects.Normal(),
    path_effects.Stroke(linewidth=2, foreground='#FFFFFF', alpha=0.6),
    path_effects.Normal()
])

# Add some random dots like stars in the background
for _ in range(100):
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    size = random.uniform(0.01, 0.05)
    alpha = random.uniform(0.3, 1.0)
    plt.scatter(x, y, s=size*100, color='white', alpha=alpha, zorder=0)

# Set equal aspect ratio and remove axes
plt.axis('equal')
plt.axis('off')

# Set limits to ensure all hearts are visible
plt.xlim(-10, 10)
plt.ylim(-10, 10)

# Show the plot
plt.tight_layout()
plt.show()

print("تم رسم القلوب بأسلوب الرصاص مع اسم 'شهد' بخط جميل على خلفية سوداء!")
