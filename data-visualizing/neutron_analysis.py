# File: neutron_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plot_energy_distribution(csv_path: str):
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Energy(MeV)'], bins=50, kde=True, color='skyblue')
    plt.title('Nötron Enerji Dağılımı')
    plt.xlabel('Enerji (MeV)')
    plt.ylabel('Nötron Sayısı')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_energy_vs_angle_3d(csv_path: str):
    df = pd.read_csv(csv_path)
    energy = df['Energy(MeV)']
    theta = np.deg2rad(df['Theta(deg)'])
    phi = np.deg2rad(df['Phi(deg)'])

    r = energy / energy.max() * 100  # normalize radius
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=energy, cmap='viridis', alpha=0.7, s=15, linewidth=0)

    ax.set_title('Nötron Nokta Bulutu (Enerji ve Yön)')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    fig.colorbar(scatter, ax=ax, label='Enerji (MeV)')
    plt.tight_layout()
    plt.show()


def plot_angle_distribution(csv_path: str):
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Theta(deg)'], bins=36, kde=False, color='coral')
    plt.title('Açıya Göre Nötron Dağılımı')
    plt.xlabel('Theta (deg)')
    plt.ylabel('Nötron Sayısı')
    plt.grid(True)
    plt.tight_layout()
    plt.show()