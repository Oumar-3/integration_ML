import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

def train_model(input_csv, models_dir="models"):
    # Créer le dossier pour les modèles s'il n'existe pas
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    # Charger les données
    df = pd.read_csv(input_csv)
    
    # S'assurer que les colonnes sont bien typées
    df['Commune'] = df['Commune'].astype(str)
    df['Année'] = df['Année'].astype(int)
    df['Recettes'] = df['Recettes'].astype(float)
    df['Dépenses'] = df['Dépenses'].astype(float)
    
    # Entraîner un modèle par commune
    communes = df['Commune'].unique()
    for commune in communes:
        # Filtrer les données pour la commune
        df_commune = df[df['Commune'] == commune]
        
        # Vérifier qu'il y a assez de données
        if len(df_commune) < 5:  # Minimum 5 années pour entraîner
            print(f"Données insuffisantes pour {commune}, modèle non créé.")
            continue
        
        # Features et targets
        X = df_commune[['Année']]
        y = df_commune[['Recettes', 'Dépenses']]
        
        # Séparation des données
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Entraînement du modèle
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Sauvegarder le modèle
        model_file = os.path.join(models_dir, f"model_{commune.replace(' ', '_')}.pkl")
        joblib.dump(model, model_file)
        print(f"Modèle pour {commune} enregistré dans {model_file}")
    
    # Sauvegarder la liste des communes
    with open(os.path.join(models_dir, 'communes.txt'), 'w') as f:
        f.write('\n'.join(communes))
    print("Liste des communes enregistrée dans models/communes.txt")

if __name__ == "__main__":
    train_model("donnees_communes.csv")