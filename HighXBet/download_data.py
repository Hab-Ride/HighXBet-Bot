import pandas as pd
import requests
from io import StringIO
import os

print("📥 STARTING DATA DOWNLOAD...")

# Create data folders if they don't exist
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

def download_football_data():
    """Simple function to download football data"""
    
    # Leagues to download: E0=Premier League, E1=Championship
    leagues = ['E0', 'E1']
    all_data = []
    
    for league in leagues:
        try:
            # Download current season data
            url = f"https://www.football-data.co.uk/mmz4281/2324/{league}.csv"
            print(f"Downloading: {url}")
            
            response = requests.get(url)
            if response.status_code == 200:
                df = pd.read_csv(StringIO(response.text))
                df['League'] = league
                all_data.append(df)
                print(f"✅ SUCCESS: {league} - {len(df)} matches")
            else:
                print(f"❌ FAILED: {league}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    if all_data:
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Save raw data
        combined_df.to_csv('data/raw/historical_data.csv', index=False)
        print(f"💾 RAW DATA SAVED: data/raw/historical_data.csv")
        
        # Clean the data
        clean_data = clean_football_data(combined_df)
        
        # Save cleaned data
        clean_data.to_csv('data/processed/cleaned_data.csv', index=False)
        print(f"💾 CLEANED DATA SAVED: data/processed/cleaned_data.csv")
        
        # Show basic stats
        show_basic_stats(clean_data)
        
        return clean_data
    else:
        print("❌ NO DATA DOWNLOADED")
        return None

def clean_football_data(df):
    """Clean and prepare the data"""
    print("🧹 CLEANING DATA...")
    
    # Create a copy
    clean_df = df.copy()
    
    # Convert date
    clean_df['Date'] = pd.to_datetime(clean_df['Date'], dayfirst=True, errors='coerce')
    
    # Keep only essential columns that exist
    essential_cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'League']
    available_cols = [col for col in essential_cols if col in clean_df.columns]
    clean_df = clean_df[available_cols].dropna()
    
    # Create new columns for analysis
    clean_df['TotalGoals'] = clean_df['FTHG'] + clean_df['FTAG']
    clean_df['Over1.5'] = (clean_df['TotalGoals'] > 1.5).astype(int)
    clean_df['Over2.5'] = (clean_df['TotalGoals'] > 2.5).astype(int)
    clean_df['BTTS'] = ((clean_df['FTHG'] > 0) & (clean_df['FTAG'] > 0)).astype(int)
    
    print(f"✅ DATA CLEANED: {len(clean_df)} matches")
    return clean_df

def show_basic_stats(df):
    """Show basic statistics"""
    print("\n📊 BASIC STATISTICS:")
    print("=" * 40)
    print(f"Total matches: {len(df)}")
    print(f"Average goals per game: {df['TotalGoals'].mean():.2f}")
    print(f"Over 1.5 goals rate: {df['Over1.5'].mean():.1%}")
    print(f"Over 2.5 goals rate: {df['Over2.5'].mean():.1%}")
    print(f"Both Teams Score rate: {df['BTTS'].mean():.1%}")
    print("=" * 40)

# Run the download
if __name__ == "__main__":
    data = download_football_data()
    if data is not None:
        print("\n🎯 NEXT STEP: Run the analysis script!")
    else:
        print("\n�️  PLEASE CHECK YOUR INTERNET CONNECTION")