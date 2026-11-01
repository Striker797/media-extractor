import sys
from extract import extract_and_download

def main():
    print("=== Media Extractor CLI ===")
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Paste your streaming URL (e.g., Audiomack track link): ").strip()
        
    if not url:
        print("No URL provided. Exiting.")
        return
        
    success = extract_and_download(url)
    
    if success:
        print("\nDone! Check your 'downloads' folder. Point MusicBee's Monitored Folder to it!")
    else:
        print("\nExtraction failed. Please check the URL and try again.")

if __name__ == "__main__":
    main()