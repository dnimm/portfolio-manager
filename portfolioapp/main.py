#!/usr/bin/env python3
"""
Main entry point for the Portfolio Manager application
"""
import sys
from cli.console_interface import ConsoleInterface
from services.exceptions import PortfolioManagerError

def main():
    """Main application entry point"""
    try:
        app = ConsoleInterface()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
        sys.exit(0)
    except PortfolioManagerError as e:
        print(f"\nApplication error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()