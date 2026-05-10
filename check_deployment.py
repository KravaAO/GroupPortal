#!/usr/bin/env python
"""
Deployment Checklist Script
Checks if the project is ready for deployment
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists"""
    env_path = Path('.env')
    if env_path.exists():
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found. Copy .env.example to .env")
        return False

def check_secret_key():
    """Check if SECRET_KEY is set and not the default insecure one"""
    try:
        from decouple import config
        secret_key = config('SECRET_KEY')
        if 'django-insecure' in secret_key:
            print("✗ SECRET_KEY is still using the insecure default. Generate a new one!")
            print("  Run: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\"")
            return False
        else:
            print("✓ SECRET_KEY is configured")
            return True
    except Exception as e:
        print(f"✗ Error checking SECRET_KEY: {e}")
        return False

def check_debug_setting():
    """Check DEBUG setting"""
    try:
        from decouple import config
        debug = config('DEBUG', default=True, cast=bool)
        if debug:
            print("⚠ DEBUG is True. Set to False for production!")
            return False
        else:
            print("✓ DEBUG is False (production-ready)")
            return True
    except Exception as e:
        print(f"✗ Error checking DEBUG: {e}")
        return False

def check_allowed_hosts():
    """Check ALLOWED_HOSTS"""
    try:
        from decouple import config, Csv
        allowed_hosts = config('ALLOWED_HOSTS', default='', cast=Csv())
        if not allowed_hosts or allowed_hosts == ['localhost', '127.0.0.1']:
            print("⚠ ALLOWED_HOSTS not configured for production. Add your domain!")
            return False
        else:
            print(f"✓ ALLOWED_HOSTS configured: {allowed_hosts}")
            return True
    except Exception as e:
        print(f"✗ Error checking ALLOWED_HOSTS: {e}")
        return False

def check_requirements():
    """Check if requirements.txt exists"""
    req_path = Path('requirements.txt')
    if req_path.exists():
        print("✓ requirements.txt exists")
        return True
    else:
        print("✗ requirements.txt not found")
        return False

def check_staticfiles():
    """Check static files configuration"""
    static_root = Path('staticfiles')
    if static_root.exists():
        print("✓ staticfiles directory exists (run collectstatic if needed)")
    else:
        print("⚠ staticfiles directory not found. Run: python manage.py collectstatic")
        return False
    return True

def check_database():
    """Check database configuration"""
    try:
        from decouple import config
        db_engine = config('DATABASE_ENGINE', default='django.db.backends.sqlite3')
        
        if 'sqlite3' in db_engine:
            print("⚠ Using SQLite. Consider PostgreSQL for production")
            return False
        else:
            print(f"✓ Database configured: {db_engine}")
            return True
    except Exception as e:
        print(f"✗ Error checking database: {e}")
        return False

def main():
    print("=" * 60)
    print("GroupPortal Deployment Readiness Check")
    print("=" * 60)
    print()
    
    checks = [
        ("Environment File", check_env_file),
        ("Secret Key", check_secret_key),
        ("Debug Mode", check_debug_setting),
        ("Allowed Hosts", check_allowed_hosts),
        ("Requirements", check_requirements),
        ("Static Files", check_staticfiles),
        ("Database", check_database),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        results.append(check_func())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓ Project is ready for deployment!")
    else:
        print("⚠ Some checks failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == '__main__':
    main()
