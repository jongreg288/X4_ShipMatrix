# Made with the help of Claude, through Github Copilot. A labor borne of my desire to know which ship can carry the most and go the fastest.
# You can reach me through GitHub @jongreg288
from src.data_parser import load_ship_data, load_engine_data, parse_shields, load_weapons_from_csv, load_turrets_from_csv
from src.gui import ShipStatsApp
from src.x4_data_extractor import setup_x4_data
from src.loading_dialog import show_loading_dialog, update_loading_status, close_loading_dialog
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
from pathlib import Path

def safe_print(message):
    """Print that works in both console and executable mode."""
    try:
        if sys.stdout is not None:
            print(message)
    except (AttributeError, OSError):
        # If print fails, silently continue (executable mode)
        pass

def main():
    # Initialize Qt Application first
    app = QApplication(sys.argv)
    
    # Show disclaimer dialog
    disclaimer = QMessageBox()
    disclaimer.setWindowTitle("X4 ShipMatrix - Disclaimer")
    disclaimer.setIcon(QMessageBox.Icon.Information)
    disclaimer.setText("X4 ShipMatrix v0.2.1 Alpha")
    disclaimer.setInformativeText(
        "This is an unofficial, community-created tool for X4: Foundations.\n\n"
        "• This software is not affiliated with, endorsed by, or connected to Egosoft GmbH.\n"
        "• X4: Foundations and all related trademarks are property of Egosoft GmbH.\n"
        "• This tool extracts and analyzes game data for informational purposes only.\n"
        "• Use at your own risk. The developers are not responsible for any issues.\n\n"
        "This project is open source and provided as-is under the MIT License.\n"
        "Created by @jongreg288 with assistance from Claude AI."
    )
    disclaimer.setStandardButtons(QMessageBox.StandardButton.Ok)
    disclaimer.exec()
    
    # Check if data directory exists, if not try to set it up
    data_dir = Path("data")
    if not data_dir.exists() or not list(data_dir.glob("**/*.xml")):
        # Show loading dialog for windowed mode
        loading_dialog = show_loading_dialog()
        update_loading_status("X4 data not found. Locating X4 installation...")
        
        safe_print("X4 data not found. Attempting to locate and extract X4 game files...")
        
        success = setup_x4_data()
        if not success:
            close_loading_dialog()
            safe_print("\nCould not automatically set up X4 data.")
            safe_print("Please manually extract X4 XML files to the 'data' directory.")
            safe_print("See README.md for detailed instructions.")
            
            # Show error dialog in windowed mode
            if not (sys.stdout and hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()):
                QMessageBox.warning(None, "X4 ShipMatrix - Setup Required", 
                                  "Could not automatically set up X4 data.\n\n"
                                  "Please ensure X4: Foundations is installed and try again.\n"
                                  "Manual setup instructions are available in the README.")
            
            # Still try to continue in case user has partial data
    
    # Check CSV cache status and regenerate if needed
    try:
        from src.data_parser import check_csv_freshness, generate_all_csv_files
        
        csvs_exist, csvs_fresh, status_msg = check_csv_freshness()
        
        if not csvs_exist or not csvs_fresh:
            update_loading_status("Generating optimized data cache (first run or after update)...")
            safe_print(f"\nCSV Cache Status: {status_msg}")
            safe_print("Generating CSV data cache for faster loading...")
            
            try:
                result = generate_all_csv_files()
                safe_print(f"Generated cache: {result.get('ships', 0)} ships, "
                          f"{result.get('engines', 0)} engines, {result.get('shields', 0)} shields, "
                          f"{result.get('weapons', 0)} weapons, {result.get('turrets', 0)} turrets")
            except Exception as e:
                safe_print(f"Warning: CSV cache generation failed: {e}")
                safe_print("Continuing with direct XML parsing (slower)...")
        else:
            safe_print("CSV cache is up to date, loading optimized data...")
    except Exception as e:
        safe_print(f"Warning: Could not check CSV cache status: {e}")
        safe_print("Continuing with available data loading method...")
    
    # Update loading status
    update_loading_status("Loading engine data...")
    engines_df = load_engine_data()  # load engines first from all data locations
    
    update_loading_status("Loading ship data...")
    ships_df = load_ship_data(engines_df=engines_df)  #pass it in

    if ships_df.empty:
        close_loading_dialog()
        safe_print("No ships found — cannot launch GUI.")
        safe_print("Make sure X4 XML files are properly extracted to the data directory.")
        
        # Show error dialog in windowed mode (check if stdout is None or not a tty)
        if sys.stdout is None or not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            QMessageBox.critical(None, "X4 ShipMatrix - No Data", 
                               "No ship data found!\n\n"
                               "Please ensure X4: Foundations is properly installed and try again.")
        return

    update_loading_status("Loading shield data...")
    shields_df = parse_shields()

    update_loading_status("Loading weapons data...")
    weapons_df = load_weapons_from_csv()

    update_loading_status("Loading turrets data...")
    turrets_df = load_turrets_from_csv()

    # Close loading dialog and show main window
    close_loading_dialog()
    window = ShipStatsApp(ships_df, engines_df, shields_df, weapons_df, turrets_df)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
