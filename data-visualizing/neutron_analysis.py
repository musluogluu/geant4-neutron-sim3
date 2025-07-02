import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 18

def plot_energy_distribution_log_histogram(csv_path: str):
    df = pd.read_csv(csv_path)
    
    MIN_PLOT_ENERGY_THRESHOLD = 1e-6 

    energies_to_plot = df['Energy(MeV)'][df['Energy(MeV)'] >= MIN_PLOT_ENERGY_THRESHOLD]

    if energies_to_plot.empty:
        print(f"Uyarı: Enerji dağılımı grafiği çizilemiyor. Enerjisi >= {MIN_PLOT_ENERGY_THRESHOLD:.1e} MeV olan nötron bulunamadı.")
        return
    
    plt.figure(figsize=(10, 7))
    
    min_data_energy = energies_to_plot.min()
    max_data_energy = energies_to_plot.max()

    log_min_plot = np.log10(max(MIN_PLOT_ENERGY_THRESHOLD, min_data_energy))
    log_max_plot = np.log10(max_data_energy)

    if log_min_plot >= log_max_plot: 
        print(f"Uyarı: Logaritmik enerji aralığı ({min_data_energy:.2e} - {max_data_energy:.2e} MeV) çok dar veya sabit. Doğrusal ölçekli histogram kullanılıyor.")
        bins = np.linspace(min_data_energy, max_data_energy + (max_data_energy * 0.1), 20)
        
        n, bins_hist, patches = plt.hist(energies_to_plot, bins=bins, density=False, 
                                          edgecolor='black', linewidth=0.8, alpha=0.7, 
                                          log=True if np.max(energies_to_plot.value_counts().values) > 100 else False)
        
        cmap = plt.cm.Greens
        for i, patch in enumerate(patches):
            color = cmap(i / len(patches))
            patch.set_facecolor(color)

        sns.kdeplot(energies_to_plot, ax=plt.gca(), color='black', linewidth=1, linestyle='-')
        
        plt.xscale('linear')
        plt.ylabel('Count')
        plt.title('Neutron Energy Spectrum (Linear Scale - Narrow Range)', pad=20, fontsize=18, fontweight='bold')
    else:
        bins = np.logspace(log_min_plot, log_max_plot, 80) 

        n, bins_hist, patches = plt.hist(energies_to_plot, bins=bins, density=False, 
                                          edgecolor='black', linewidth=0.8, alpha=0.7, log=True)
        
        cmap = plt.cm.Greens
        for i, patch in enumerate(patches):
            color = cmap(i / len(patches))
            patch.set_facecolor(color)
        
        try:
            sns.kdeplot(energies_to_plot, ax=plt.gca(), color='black', linewidth=1, linestyle='-')
        except Exception as e:
            print(f"Uyarı: KDE çizimi sırasında hata oluştu, KDE çizilemiyor: {e}")
            print("KDE, çok geniş logaritmik aralıklarda sorun çıkarabilir. Histogram yeterli olabilir.")

        plt.title(f'Neutron Energy Spectrum (Excluding Neutrons < {MIN_PLOT_ENERGY_THRESHOLD:.1e} MeV)', pad=20, fontsize=18, fontweight='bold')
        plt.xlabel('Kinetic Energy (MeV)', fontsize=16)
        plt.ylabel('Count (Log Scale)', fontsize=16)
        plt.xscale('log')
        plt.tick_params(axis='x', which='minor')

    plt.grid(True, which="both", ls="--", alpha=0.6) 
    plt.tight_layout()
    plt.show()

def plot_energy_vs_angle_3d(csv_path: str):
    df = pd.read_csv(csv_path)
    df_filtered = df[df['Energy(MeV)'] > 0].copy() 
    if df_filtered.empty:
        print("Uyarı: 3D enerji-açı grafiği çizilemiyor. Pozitif enerjili nötron bulunamadı.")
        return
    energy = df_filtered['Energy(MeV)']
    theta = np.deg2rad(df_filtered['Theta(deg)'])
    phi = np.deg2rad(df_filtered['Phi(deg)'])
    x = energy * np.sin(theta) * np.cos(phi)
    y = energy * np.sin(theta) * np.sin(phi)
    z = energy * np.cos(theta)
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=energy, cmap='viridis', alpha=0.7, s=15, linewidth=0)
    ax.set_title('Neutron Scatter Cloud: Energy and Angular Distribution', 
                 fontsize=18, fontweight='bold', pad=20, y=1.0) 
    ax.set_xlabel('X-Component (Energy-weighted)', fontsize=14, labelpad=10)
    ax.set_ylabel('Y-Component (Energy-weighted)', fontsize=14, labelpad=10)
    ax.set_zlabel('Z-Component (Energy-weighted)', fontsize=14, labelpad=10)
    fig.colorbar(scatter, ax=ax, label='Energy (MeV)', pad=0.1)
    plt.tight_layout()
    plt.show()

def plot_angle_distribution(csv_path: str):
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Theta(deg)'], bins=36, kde=False, color='coral')
    plt.title('Neutron Count vs. Theta Angle', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('Theta Angle (degrees)', fontsize=14)
    plt.ylabel('Neutron Count', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def analyze_neutrons(csv_path: str):
    try:
        df = pd.read_csv(csv_path)
        print(f"\n--- Nötron Analiz Raporu ---")
        print(f"Veri Kaynağı: {csv_path}")
        total_neutrons = len(df)
        print(f"Toplam Nötron Sayısı: {total_neutrons}")
        print("\n--- Enerji İstatistikleri (MeV) ---")
        print(df['Energy(MeV)'].describe())
        print("\n*Not: İstatistikler, sıfır kinetik enerjili nötronlar da dahil olmak üzere tüm kaydedilen nötronları içerir. Logaritmik gösterim amaçlı grafikler, sıfır enerjili nötronları hariç tutabilir.*")
        print("\n--- Teta Açısı İstatistikleri (derece) ---")
        print(df['Theta(deg)'].describe())
        print(f"\n--- Grafik Oluşturuluyor ---")
        
        print("\n--- Grafik 1: Nötron Enerji Spektrumu ---")
        print("Bu grafik, nötronların kinetik enerji dağılımını gösterir. Geniş bir enerji aralığını (çok düşükten çok yükseğe) etkili bir şekilde görselleştirmek için hem enerji (X ekseni) hem de sayım (Y ekseni) logaritmik ölçekte gösterilir. Kernel Yoğunluk Tahmini (KDE), altında yatan enerji dağılımının pürüzsüz bir temsilini sağlar. Sıfır kinetik enerjiye sahip nötronlar veya tanımlanan çizim eşiğinin altındaki enerjiler, logaritmik ölçekte temsil edilemedikleri için bu grafikten çıkarılmıştır.")
        plot_energy_distribution_log_histogram(csv_path) 
        
        print("\n--- Grafik 2: Nötron Sayısı vs. Teta Açısı ---")
        print("Bu histogram, nötronların 'Teta' açısına (derece cinsinden polar açı) göre açısal dağılımını gösterir. Nötron emisyonunun veya saçılmasının tercih edilen yönlerini anlamaya yardımcı olur.")
        plot_angle_distribution(csv_path)
        
        print("\n--- Grafik 3: Nötron Saçılım Bulutu (Enerji ve Açısal Dağılım) ---")
        print("Bu 3D saçılım grafiği, nötronların birleşik enerji ve açısal dağılımını görselleştirir. Her nokta bir nötronu temsil eder; X, Y ve Z eksenlerindeki konumu enerjisi ve yönü ile orantılıdır. Her noktanın rengi de kinetik enerjisini gösterir ve nötronun tespit veya etkileşim anındaki durumuna dair kapsamlı bir genel bakış sunar.")
        plot_energy_vs_angle_3d(csv_path)

    except FileNotFoundError:
        print(f"Hata: '{csv_path}' dosyası bulunamadı. Lütfen yolu kontrol edin.")
    except KeyError as e:
        print(f"Hata: CSV'de beklenen sütun eksik: {e}. Lütfen CSV başlıklarınızı kontrol edin.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")