import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class DesignProcessor:
    def __init__(self, test_mode: bool = True):
        self.api_key = os.getenv('PRINTFUL_API_KEY')
        self.store_id = os.getenv('STORE_ID')
        
        if not self.api_key or not self.store_id:
            raise ValueError("Missing required environment variables. Please check your .env file.")
            
        self.test_mode = test_mode
        self.logger = logging.getLogger(__name__)
        
        # Set up logging
        self.setup_logging()
        
    def setup_logging(self):
        """Set up logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"design_processor_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def process_design(self, file_path: Path):
        """Process a single design file"""
        try:
            # Parse filename
            parts = file_path.stem.split('_')
            if len(parts) != 3:
                self.logger.error(f"Invalid filename format: {file_path.name}")
                return False
                
            category, design_type, description = parts
            
            self.logger.info(f"Processing design: {file_path.name}")
            self.logger.info(f"Category: {category}, Type: {design_type}, Description: {description}")
            
            if self.test_mode:
                self.logger.info("[TEST MODE] Would create product with:")
                self.logger.info(f"- Design file: {file_path}")
                self.logger.info(f"- Category: {category}")
                self.logger.info(f"- Design type: {design_type}")
                self.logger.info(f"- Description: {description}")
                return True
            else:
                # Here we would call the actual Printful API
                # Implementation would go here
                self.logger.info("[PROD MODE] Creating product...")
                return True
                
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return False


class DesignHandler(FileSystemEventHandler):
    def __init__(self, processor: DesignProcessor):
        self.processor = processor
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path.suffix.lower() == '.png':
            self.processor.process_design(file_path)


def main():
    parser = argparse.ArgumentParser(description='Watch for new design files and process them')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()
    
    try:
        # Initialize processor
        processor = DesignProcessor(test_mode=args.test)
        
        # Set up file system watcher
        finished_dir = Path("designs/finished")
        event_handler = DesignHandler(processor)
        observer = Observer()
        observer.schedule(event_handler, str(finished_dir), recursive=False)
        observer.start()
        
        print(f"Watching directory: {finished_dir}")
        print(f"Running in {'TEST' if args.test else 'PRODUCTION'} mode")
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        print(f"Error: {str(e)}")
        return
        
    observer.join()

if __name__ == "__main__":
    main()