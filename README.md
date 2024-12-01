# Printful Design Automation

This tool automates the process of creating Printful products from design files. It includes a GUI for renaming design files and a watcher script that automatically processes new designs.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/joshcork/printful-automation.git
cd printful-automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.template .env
```
Then edit `.env` with your actual Printful API key and Store ID.

## Usage

### Design Renamer
Place your PNG design files in the `designs/incoming` folder and run:
```bash
python design_renamer.py
```

### Design Watcher
To watch for new designs in test mode:
```bash
python design_watcher.py --test
```

To run in production mode:
```bash
python design_watcher.py
```

## Directory Structure
```
printful-automation/
├── designs/
│   ├── incoming/    # Drop new files here
│   └── finished/    # Renamed files go here
├── logs/           # Processing logs
└── .env           # Configuration (not in git)