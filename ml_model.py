import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import json
import shap
import matplotlib
matplotlib.use('Agg')  # For headless environments
import matplotlib.pyplot as plt

class NarraSoilClassifier:
    def __init__(self):
        self.model = None
        self.feature_names = ['moisture', 'temperature', 'ec', 'ph', 
                             'nitrogen', 'phosphorus', 'potassium']
        self.optimal_ranges = {
            'moisture': (20, 60),      # 20% - 60% VWC
            'temperature': (18, 35),   # 18°C - 35°C
            'ec': (500, 2000),         # 500 - 2000 μs/cm
            'ph': (5.5, 7.5),          # 5.5 - 7.5
            'nitrogen': (40, 100),     # 40 - 100 mg/kg
            'phosphorus': (15, 25),    # 15 - 25 mg/kg
            'potassium': (120, 200)    # 120 - 200 mg/kg
        }
        self.explainer = None
        
    def train(self, data_path='narra_soil_training_data.csv'):
        """Train the Random Forest classifier"""
        print("Loading training data...")
        df = pd.read_csv(data_path)
        
        X = df[self.feature_names]
        y = df['suitable']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        # Train Random Forest (inherently interpretable)
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nModel Accuracy: {accuracy*100:.2f}%")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Not Suitable', 'Suitable']))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        # Initialize SHAP explainer for detailed explanations
        print("\nInitializing SHAP explainer...")
        self.explainer = shap.TreeExplainer(self.model)
        
        # Save the model
        self.save_model()
        
        return accuracy
    
    def predict(self, soil_data):
        """
        Predict suitability and provide explanations
        
        Args:
            soil_data: dict with keys matching feature_names
        
        Returns:
            dict with prediction, probability, and explanations
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Convert to DataFrame
        X = pd.DataFrame([soil_data])[self.feature_names]
        
        # Get prediction
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]
        
        # Get SHAP values for explanation
        shap_values = self.explainer.shap_values(X)
        
        # Extract SHAP values for class 1 (suitable)
        if isinstance(shap_values, list):
            # Binary classification: shap_values is [class_0_values, class_1_values]
            shap_array = shap_values[1]
        else:
            # Single array output
            shap_array = shap_values
        
        # Ensure we have a 1D array of SHAP values
        if len(shap_array.shape) > 1:
            shap_values_suitable = shap_array[0]
        else:
            shap_values_suitable = shap_array
        
        # Convert to plain Python list
        shap_values_list = [float(val) for val in shap_values_suitable.flatten()]
        
        # Create feature contributions (FIXED: removed duplication)
        feature_contributions = []
        for i, feature in enumerate(self.feature_names):
            min_val, max_val = self.optimal_ranges[feature]
            feature_value = float(soil_data[feature])
            
            # Determine if value is in optimal range
            if min_val <= feature_value <= max_val:
                status = 'optimal'
            elif feature_value < min_val:
                status = 'too_low'
            else:
                status = 'too_high'
            
            contribution = {
                'feature': feature,
                'value': feature_value,
                'optimal_range': self.optimal_ranges[feature],
                'shap_value': shap_values_list[i],
                'importance': float(self.model.feature_importances_[i]),
                'status': status
            }
            
            feature_contributions.append(contribution)
        
        # Sort by absolute SHAP value (impact on decision)
        feature_contributions.sort(key=lambda x: abs(x['shap_value']), reverse=True)
        
        # Generate human-readable explanation
        explanation = self._generate_explanation(prediction, feature_contributions)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(feature_contributions)
        
        return {
            'suitable': bool(prediction),
            'probability': {
                'not_suitable': float(probability[0]),
                'suitable': float(probability[1])
            },
            'confidence': float(max(probability)),
            'feature_contributions': feature_contributions,
            'explanation': explanation,
            'recommendations': recommendations
        }
    
    def _generate_explanation(self, prediction, contributions):
        """Generate human-readable explanation"""
        if prediction == 1:
            text = "✓ This soil is SUITABLE for planting narra trees.\n\n"
        else:
            text = "✗ This soil is NOT SUITABLE for planting narra trees.\n\n"
        
        text += "Key factors:\n"
        
        # Top 3 most impactful features
        for i, contrib in enumerate(contributions[:3], 1):
            feature = contrib['feature'].replace('_', ' ').title()
            value = contrib['value']
            status = contrib['status']
            min_val, max_val = contrib['optimal_range']
            
            if status == 'optimal':
                status_text = f"✓ OPTIMAL (within {min_val}-{max_val})"
            elif status == 'too_low':
                status_text = f"✗ TOO LOW (optimal: {min_val}-{max_val})"
            else:
                status_text = f"✗ TOO HIGH (optimal: {min_val}-{max_val})"
            
            text += f"{i}. {feature}: {value:.2f} - {status_text}\n"
        
        return text
    
    def _generate_recommendations(self, contributions):
        """Generate actionable recommendations based on soil parameters"""
        recommendations = []
        
        for contrib in contributions:
            feature = contrib['feature']
            status = contrib['status']
            value = contrib['value']
            min_val, max_val = contrib['optimal_range']
            
            if status == 'too_low':
                if feature == 'moisture':
                    recommendations.append(f"Increase irrigation - current moisture is {value:.1f}%, target: {min_val}-{max_val}%")
                elif feature == 'temperature':
                    recommendations.append(f"Consider greenhouse or wait for warmer season - current temp: {value:.1f}°C")
                elif feature == 'ph':
                    recommendations.append(f"Add lime to raise pH from {value:.1f} to {min_val}-{max_val}")
                elif feature == 'nitrogen':
                    recommendations.append(f"Apply nitrogen fertilizer (urea or ammonium sulfate)")
                elif feature == 'phosphorus':
                    recommendations.append(f"Apply phosphorus fertilizer (superphosphate)")
                elif feature == 'potassium':
                    recommendations.append(f"Apply potassium fertilizer (muriate of potash)")
                    
            elif status == 'too_high':
                if feature == 'moisture':
                    recommendations.append(f"Improve drainage - current moisture is {value:.1f}%, target: {min_val}-{max_val}%")
                elif feature == 'temperature':
                    recommendations.append(f"Provide shade or wait for cooler season - current temp: {value:.1f}°C")
                elif feature == 'ec':
                    recommendations.append(f"High salinity detected ({value:.0f} μs/cm) - leach soil with fresh water")
                elif feature == 'ph':
                    recommendations.append(f"Add sulfur or organic matter to lower pH from {value:.1f} to {min_val}-{max_val}")
                elif feature in ['nitrogen', 'phosphorus', 'potassium']:
                    recommendations.append(f"Reduce {feature} fertilization - current level is too high")
        
        if not recommendations:
            recommendations.append("All soil parameters are within optimal range for narra planting")
        
        return recommendations
    
    def save_model(self, model_path='narra_model.joblib'):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save")
        
        joblib.dump({
            'model': self.model,
            'feature_names': self.feature_names,
            'optimal_ranges': self.optimal_ranges,
            'explainer': self.explainer
        }, model_path)
        print(f"\nModel saved to {model_path}")
    
    def load_model(self, model_path='narra_model.joblib'):
        """Load trained model"""
        data = joblib.load(model_path)
        self.model = data['model']
        self.feature_names = data['feature_names']
        self.optimal_ranges = data['optimal_ranges']
        self.explainer = data['explainer']
        print(f"Model loaded from {model_path}")

# Training script
if __name__ == "__main__":
    classifier = NarraSoilClassifier()
    
    # Train the model
    classifier.train('narra_soil_data.csv')
    
    # Test with example data
    print("\n" + "="*60)
    print("TESTING WITH EXAMPLE DATA")
    print("="*60)
    
    # Example 1: Good soil (within optimal ranges)
    test_soil_good = {
        'moisture': 40.0,       # Within 20-60%
        'temperature': 26.5,    # Within 18-35°C
        'ec': 1250,             # Within 500-2000 μs/cm
        'ph': 6.5,              # Within 5.5-7.5
        'nitrogen': 70.0,       # Within 40-100 mg/kg
        'phosphorus': 20.0,     # Within 15-25 mg/kg
        'potassium': 160.0      # Within 120-200 mg/kg
    }
    
    print("\n--- Example 1: Optimal Soil ---")
    result = classifier.predict(test_soil_good)
    print(result['explanation'])
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    
    # Example 2: Poor soil (outside optimal ranges)
    test_soil_poor = {
        'moisture': 10.0,       # Too dry (< 20%)
        'temperature': 40.0,    # Too hot (> 35°C)
        'ec': 3500,             # Too high/saline (> 2000 μs/cm)
        'ph': 8.5,              # Too alkaline (> 7.5)
        'nitrogen': 20.0,       # Too low (< 40 mg/kg)
        'phosphorus': 8.0,      # Too low (< 15 mg/kg)
        'potassium': 60.0       # Too low (< 120 mg/kg)
    }
    
    print("\n--- Example 2: Poor Soil ---")
    result = classifier.predict(test_soil_poor)
    print(result['explanation'])
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")

    # Example 3: STI SOIL
    test_soil_sti = {
        'moisture': 32.0,
        'temperature': 19.9,
        'ec': 554,
        'ph': 6.3,
        'nitrogen': 77.0,
        'phosphorus': 224,
        'potassium': 218.0
    }

    print("\n--- Example 3: STI Soil ---")
    result = classifier.predict(test_soil_sti)
    print(result['explanation'])
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")