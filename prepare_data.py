import pandas as pd

def prepare_data(input_file, output_file):
    # Charger le fichier Excel
    df = pd.read_excel(input_file)

    # Sélectionner et renommer les colonnes
    df = df[['Commune', 'Année', 'Recettes (M€)', 'Dépenses (M€)']].dropna()
    df.columns = ['Commune', 'Année', 'Recettes', 'Dépenses']
    
    # Conversion des types
    df['Commune'] = df['Commune'].astype(str)
    df['Année'] = df['Année'].astype(int)
    df['Recettes'] = df['Recettes'].astype(float)
    df['Dépenses'] = df['Dépenses'].astype(float)

    # Filtrer les années valides
    df = df[(df['Année'] >= 2010) & (df['Année'] <= 2023)]

    # Sauvegarder en CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Données enregistrées dans {output_file}")

if __name__ == "__main__":
    prepare_data("donnees_communes.xlsx", "donnees_communes.csv")
