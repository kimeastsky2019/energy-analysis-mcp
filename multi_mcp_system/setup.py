#!/usr/bin/env python3
"""
Setup script for the Multi-MCP Time Series Analysis System.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)


def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = [
        "models/forecasting",
        "models/anomaly_detection", 
        "forecasting_models",
        "anomaly_models",
        "logs",
        "data",
        "results"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   Created: {directory}")
    
    print("✅ Directories created successfully")


def validate_configs():
    """Validate configuration files."""
    print("🔧 Validating configuration files...")
    
    config_files = [
        "config/forecasting_config.json",
        "config/anomaly_config.json", 
        "config/coordinator_config.json"
    ]
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                json.load(f)
            print(f"   ✅ {config_file}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"   ❌ {config_file}: {e}")
            sys.exit(1)
    
    print("✅ Configuration files validated successfully")


def create_startup_scripts():
    """Create startup scripts for the MCP servers."""
    print("🚀 Creating startup scripts...")
    
    # Create start_all.sh
    start_all_content = """#!/bin/bash
# Start all MCP servers

echo "🌟 Starting Multi-MCP Time Series Analysis System..."

# Start Forecasting MCP Server
echo "Starting Forecasting MCP Server..."
python forecasting_mcp_server.py &
FORECASTING_PID=$!

# Start Anomaly Detection MCP Server  
echo "Starting Anomaly Detection MCP Server..."
python anomaly_mcp_server.py &
ANOMALY_PID=$!

# Start Coordinator MCP Server
echo "Starting Coordinator MCP Server..."
python coordinator_mcp_server.py &
COORDINATOR_PID=$!

echo "✅ All servers started!"
echo "Forecasting MCP Server PID: $FORECASTING_PID"
echo "Anomaly Detection MCP Server PID: $ANOMALY_PID" 
echo "Coordinator MCP Server PID: $COORDINATOR_PID"

# Wait for user input to stop servers
echo "Press Enter to stop all servers..."
read

echo "🛑 Stopping all servers..."
kill $FORECASTING_PID $ANOMALY_PID $COORDINATOR_PID
echo "✅ All servers stopped"
"""
    
    with open("start_all.sh", "w") as f:
        f.write(start_all_content)
    
    os.chmod("start_all.sh", 0o755)
    print("   Created: start_all.sh")
    
    # Create start_forecasting.sh
    start_forecasting_content = """#!/bin/bash
# Start Forecasting MCP Server only

echo "🚀 Starting Forecasting MCP Server..."
python forecasting_mcp_server.py
"""
    
    with open("start_forecasting.sh", "w") as f:
        f.write(start_forecasting_content)
    
    os.chmod("start_forecasting.sh", 0o755)
    print("   Created: start_forecasting.sh")
    
    # Create start_anomaly.sh
    start_anomaly_content = """#!/bin/bash
# Start Anomaly Detection MCP Server only

echo "🔍 Starting Anomaly Detection MCP Server..."
python anomaly_mcp_server.py
"""
    
    with open("start_anomaly.sh", "w") as f:
        f.write(start_anomaly_content)
    
    os.chmod("start_anomaly.sh", 0o755)
    print("   Created: start_anomaly.sh")
    
    # Create start_coordinator.sh
    start_coordinator_content = """#!/bin/bash
# Start Coordinator MCP Server only

echo "🤝 Starting Coordinator MCP Server..."
python coordinator_mcp_server.py
"""
    
    with open("start_coordinator.sh", "w") as f:
        f.write(start_coordinator_content)
    
    os.chmod("start_coordinator.sh", 0o755)
    print("   Created: start_coordinator.sh")
    
    print("✅ Startup scripts created successfully")


def run_tests():
    """Run basic tests to verify installation."""
    print("🧪 Running basic tests...")
    
    try:
        # Test basic imports
        import numpy as np
        import pandas as pd
        import tensorflow as tf
        print("   ✅ Core dependencies imported successfully")
        
        # Test model imports
        from models.forecasting.lstm_model import LSTMForecaster
        from models.forecasting.cnn_model import CNNForecaster
        from models.anomaly_detection.prophet_model import ProphetAnomalyDetector
        from models.anomaly_detection.hmm_model import HMMAnomalyDetector
        print("   ✅ Model classes imported successfully")
        
        # Test utility imports
        from utils.data_preprocessing import prepare_forecasting_data
        from utils.model_utils import ModelEvaluator, ModelManager
        print("   ✅ Utility classes imported successfully")
        
        # Run example tests
        print("   🧪 Running example tests...")
        subprocess.check_call([sys.executable, "examples/basic_usage.py"], 
                            capture_output=True, text=True)
        print("   ✅ Example tests passed")
        
        print("✅ All tests passed successfully")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("   Some features may not work correctly")
        return False
    
    return True


def main():
    """Main setup function."""
    print("🌟 Multi-MCP Time Series Analysis System Setup")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Create directories
    create_directories()
    
    # Validate configs
    validate_configs()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Run tests
    tests_passed = run_tests()
    
    print("\n" + "=" * 60)
    if tests_passed:
        print("✅ Setup completed successfully!")
        print("\n🚀 To start the system:")
        print("   ./start_all.sh")
        print("\n📚 To run examples:")
        print("   python examples/basic_usage.py")
        print("   python examples/advanced_analysis.py")
    else:
        print("⚠️  Setup completed with warnings.")
        print("   Some features may not work correctly.")
        print("   Please check the error messages above.")
    
    print("\n📖 For more information, see README.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
