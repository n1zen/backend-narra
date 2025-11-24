# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta

# def generate_narra_soil_dataset(n_samples=1000, seed=42):
#     """
#     Generate synthetic soil data for narra tree suitability classification.
    
#     Ranges based on frontend specifications:
#     - Soil Moisture: 20-60% (VWC - Volumetric Water Content)
#     - Temperature: 18-35°C (tropical to subtropical)
#     - EC (Electrical Conductivity): 500-2000 μs/cm (microsiemens per centimeter)
#     - pH: 5.5-7.5 (slightly acidic to neutral)
#     - Nitrogen: 40-100 mg/kg
#     - Phosphorus: 15-25 mg/kg
#     - Potassium: 120-200 mg/kg
#     """
#     np.random.seed(seed)
    
#     data = []
    
#     for i in range(n_samples):
#         # Determine if this sample will be suitable (1) or not (0)
#         is_suitable = np.random.choice([0, 1], p=[0.4, 0.6])
        
#         if is_suitable:
#             # Generate values within optimal ranges (centered in the range)
#             moisture = np.random.normal(40, 7)      # Mean 40%, std 7% (range: 20-60)
#             temp = np.random.normal(26.5, 3.5)      # Mean 26.5°C, std 3.5°C (range: 18-35)
#             ec = np.random.normal(1250, 300)        # Mean 1250 μs/cm, std 300 (range: 500-2000)
#             ph = np.random.normal(6.5, 0.4)         # Mean 6.5, std 0.4 (range: 5.5-7.5)
#             nitrogen = np.random.normal(70, 12)     # Mean 70 mg/kg (range: 40-100)
#             phosphorus = np.random.normal(20, 2.5)  # Mean 20 mg/kg (range: 15-25)
#             potassium = np.random.normal(160, 15)   # Mean 160 mg/kg (range: 120-200)
#         else:
#             # Generate values outside optimal ranges
#             # Randomly choose which parameters are problematic
#             moisture = np.random.choice([
#                 np.random.normal(10, 5),    # Too dry
#                 np.random.normal(75, 10)    # Too wet
#             ])
#             temp = np.random.choice([
#                 np.random.normal(12, 3),    # Too cold
#                 np.random.normal(40, 4)     # Too hot
#             ])
#             ec = np.random.choice([
#                 np.random.normal(200, 100),  # Too low (nutrient-poor)
#                 np.random.normal(3500, 800)  # Too high (saline)
#             ])
#             ph = np.random.choice([
#                 np.random.normal(4.5, 0.5), # Too acidic
#                 np.random.normal(8.5, 0.5)  # Too alkaline
#             ])
#             nitrogen = np.random.choice([
#                 np.random.normal(20, 10),   # Too low
#                 np.random.normal(130, 20)   # Too high
#             ])
#             phosphorus = np.random.choice([
#                 np.random.normal(8, 3),     # Too low
#                 np.random.normal(35, 8)     # Too high
#             ])
#             potassium = np.random.choice([
#                 np.random.normal(60, 25),   # Too low
#                 np.random.normal(280, 40)   # Too high
#             ])
        
#         # Clip values to realistic ranges
#         moisture = np.clip(moisture, 0, 100)
#         temp = np.clip(temp, 5, 50)
#         ec = np.clip(ec, 0, 10000)  # Max 10000 μs/cm
#         ph = np.clip(ph, 3, 10)
#         nitrogen = np.clip(nitrogen, 0, 250)
#         phosphorus = np.clip(phosphorus, 0, 100)
#         potassium = np.clip(potassium, 0, 500)
        
#         data.append({
#             'moisture': round(moisture, 2),
#             'temperature': round(temp, 2),
#             'ec': round(ec, 2),
#             'ph': round(ph, 2),
#             'nitrogen': round(nitrogen, 2),
#             'phosphorus': round(phosphorus, 2),
#             'potassium': round(potassium, 2),
#             'suitable': is_suitable
#         })
    
#     return pd.DataFrame(data)

# if __name__ == "__main__":
#     # Generate training dataset
#     df = generate_narra_soil_dataset(n_samples=2000)
#     df.to_csv('narra_soil_training_data.csv', index=False)
#     print(f"Generated {len(df)} samples")
#     print(f"Suitable: {df['suitable'].sum()} ({df['suitable'].mean()*100:.1f}%)")
#     print(f"Not Suitable: {(1-df['suitable']).sum()} ({(1-df['suitable']).mean()*100:.1f}%)")
    
#     print("\n" + "="*60)
#     print("DATASET STATISTICS")
#     print("="*60)
#     print("\nSuitable samples statistics:")
#     print(df[df['suitable']==1].describe())
    
#     print("\nNot suitable samples statistics:")
#     print(df[df['suitable']==0].describe())
    
#     print("\n" + "="*60)
#     print("DATASET PREVIEW")
#     print("="*60)
#     print(df.head(10))

import pandas as pd
import numpy as np

# Generate synthetic dataset
np.random.seed(42)
n_samples = 1000

# Create features with realistic ranges
data = {
    'moisture': np.random.uniform(20, 80, n_samples),  # percentage
    'temperature': np.random.uniform(20, 35, n_samples),  # Celsius
    'ec': np.random.uniform(0.5, 3.0, n_samples),  # dS/m
    'ph': np.random.uniform(4.5, 8.5, n_samples),
    'nitrogen': np.random.uniform(10, 100, n_samples),  # ppm
    'phosphorus': np.random.uniform(5, 80, n_samples),  # ppm
    'potassium': np.random.uniform(20, 150, n_samples)  # ppm
}

df = pd.DataFrame(data)

# Create target based on narra requirements
df['suitable'] = (
    (df['ph'] >= 5.5) & (df['ph'] <= 7.5) &
    (df['moisture'] >= 40) & (df['moisture'] <= 70) &
    (df['temperature'] >= 22) & (df['temperature'] <= 32) &
    (df['nitrogen'] >= 30) &
    (df['phosphorus'] >= 15) &
    (df['potassium'] >= 40)
).astype(int)

# Add some noise (make it realistic - not perfect boundaries)
noise_mask = np.random.random(n_samples) < 0.1
df.loc[noise_mask, 'suitable'] = 1 - df.loc[noise_mask, 'suitable']

df.to_csv('narra_soil_data.csv', index=False)