#!/usr/bin/env python3
"""
Site Reliability Monitor

Comprehensive monitoring system for the Jekyll website that:
- Checks site health and functionality
- Verifies deployments after commits
- Sends email alerts for issues
- Runs periodic health checks
"""

import sys
import time
import smtplib
import requests
import argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, Tuple
import json
import logging
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('utils/etc/site_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SiteReliabilityMonitor:
    def __init__(self, config_file: str = "utils/etc/site_monitor_config.json", local_mode: bool = False, verbose: bool = False):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.local_mode = local_mode
        self.verbose = verbose

        if local_mode:
            self.site_url = 'http://localhost:4000'
        else:
            self.site_url = self.config.get('site_url', 'https://unixwzrd.ai')

        self.health_checks = []
        self.issues = []
        self.check_results = {
            'pages': {'checked': 0, 'passed': 0, 'failed': 0, 'failed_items': []},
            'images': {'checked': 0, 'passed': 0, 'failed': 0, 'failed_items': []},
            'external_links': {'checked': 0, 'passed': 0, 'failed': 0, 'failed_items': []}
        }
        
        # Log which site we're testing
        if self.verbose:
            logger.info(f"   🎯 Testing site: {self.site_url}")

    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Sort critical pages for consistency
                if 'health_checks' in config and 'critical_pages' in config['health_checks']:
                    config['health_checks']['critical_pages'].sort()
                
                # Ensure external_links config exists with all required fields
                if 'external_links' not in config:
                    config['external_links'] = {
                        'slow_threshold': 2.0,
                        'max_failures_before_investigation': 10,
                        'max_failure_count': 50,  # Stop counting after this many failures
                        'max_slow_count': 30,      # Stop counting after this many slow responses
                        'critical_failure_threshold': 25,  # When to raise critical investigation alert
                        'critical_slow_threshold': 15,     # When to raise critical slow alert
                        'link_metrics': {}
                    }
                else:
                    # Ensure all required fields exist in existing config
                    external_links = config['external_links']
                    if 'slow_threshold' not in external_links:
                        external_links['slow_threshold'] = 2.0
                    if 'max_failures_before_investigation' not in external_links:
                        external_links['max_failures_before_investigation'] = 10
                    if 'max_failure_count' not in external_links:
                        external_links['max_failure_count'] = 50
                    if 'max_slow_count' not in external_links:
                        external_links['max_slow_count'] = 30
                    if 'critical_failure_threshold' not in external_links:
                        external_links['critical_failure_threshold'] = 25
                    if 'critical_slow_threshold' not in external_links:
                        external_links['critical_slow_threshold'] = 15
                    if 'link_metrics' not in external_links:
                        external_links['link_metrics'] = {}
                
                return config
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'site_url': 'https://unixwzrd.ai',
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': 'your-email@gmail.com',
                'sender_password': '',  # Use app password
                'recipient_email': 'your-email@gmail.com'
            },
            'health_checks': {
                'critical_pages': [
                    '/',
                    '/blog/',
                    '/projects/',
                    '/about/',
                    '/contact/'
                ],
                'check_images': True,
                'check_links': True,
                'check_response_time': True,
                'max_response_time': 5.0
            },
            'external_links': {
                'slow_threshold': 2.0,
                'max_failures_before_investigation': 10,
                'max_failure_count': 50,  # Stop counting after this many failures
                'max_slow_count': 30,      # Stop counting after this many slow responses
                'critical_failure_threshold': 25,  # When to raise critical investigation alert
                'critical_slow_threshold': 15,     # When to raise critical slow alert
                'link_metrics': {}
            },
            'deployment': {
                'check_delay_minutes': 10,
                'max_deployment_time': 15
            }
        }

    def _save_config(self, config: Dict) -> bool:
        """Save configuration to file with sorted critical pages."""
        try:
            # Ensure critical pages are sorted before saving
            if 'health_checks' in config and 'critical_pages' in config['health_checks']:
                config['health_checks']['critical_pages'].sort()
            
            # Create backup of current config
            backup_file = self.config_file.with_suffix('.json.backup')
            if self.config_file.exists():
                import shutil
                shutil.copy2(self.config_file, backup_file)
            
            # Write new config
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            if self.verbose:
                logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def add_health_check(self, check_func, name: str, critical: bool = True):
        """Add a custom health check function."""
        self.health_checks.append({
            'func': check_func,
            'name': name,
            'critical': critical
        })

    def check_site_availability(self) -> bool:
        """Check if the main site is accessible."""
        try:
            response = requests.get(self.site_url, timeout=10)
            if response.status_code == 200:
                logger.info(f"   ✅ Site is accessible: {response.status_code}")
                return True
            elif response.status_code == 404:
                # Check if this is our custom 404 page (site is working) or server error
                content = response.text.lower()
                if 'page not found' in content and 'distributed thinking systems' in content:
                    logger.info(f"   ✅ Site is accessible (serving custom 404 page): {response.status_code}")
                    return True
                else:
                    logger.error("  ❌ Site returned 404 but not serving custom 404 page")
                    self.issues.append("Site returned 404 but not serving custom 404 page")
                    return False
            else:
                logger.error(f"  ❌ Site returned status code: {response.status_code}")
                self.issues.append(f"Site returned status code {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"  ❌ Site is not accessible: {e}")
            self.issues.append(f"Site is not accessible: {e}")
            return False

    def check_page_response_time(self, url: str) -> Tuple[bool, float]:
        """Check response time for a specific page."""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time

            if response.status_code == 200:
                max_time = self.config['health_checks']['max_response_time']
                if response_time <= max_time:
                    if self.verbose:
                        logger.info(f"   ✅ {url}: {response_time:.2f}s")
                    return True, response_time
                else:
                    if self.verbose:
                        logger.warning(f"🐌 {url}: {response_time:.2f}s (slow)")
                    else:
                        logger.warning(f"🐌 {url}: {response_time:.2f}s (slow)")
                    self.issues.append(f"Slow response time for {url}: {response_time:.2f}s")
                    return False, response_time
            else:
                if self.verbose:
                    logger.error(f"  ❌ {url}: HTTP {response.status_code} ({response_time:.2f}s)")
                else:
                    logger.error(f"  ❌ {url}: HTTP {response.status_code}")
                self.issues.append(f"HTTP {response.status_code} for {url}")
                return False, response_time
        except Exception as e:
            if self.verbose:
                logger.error(f"  ❌ {url}: {e} (0.00s)")
            else:
                logger.error(f"  ❌ {url}: {e}")
            self.issues.append(f"Error accessing {url}: {e}")
            return False, 0.0

    def check_critical_pages(self) -> bool:
        """Check all critical pages are accessible."""
        logger.info("   🔍 Checking critical pages...")
        all_good = True
        self.check_results['pages'] = {'checked': 0, 'passed': 0, 'failed': 0, 'failed_items': []}

        for page in self.config['health_checks']['critical_pages']:
            url = f"{self.site_url}{page}"
            self.check_results['pages']['checked'] += 1
            success, response_time = self.check_page_response_time(url)
            if success:
                self.check_results['pages']['passed'] += 1
            else:
                self.check_results['pages']['failed'] += 1
                self.check_results['pages']['failed_items'].append(f"{url} (HTTP error)")
                all_good = False

        # Print summary
        if self.check_results['pages']['failed'] == 0:
            logger.info(f"   ✅ {self.check_results['pages']['passed']} pages checked and passed.")
        else:
            failed_count = self.check_results['pages']['failed']
            total_count = self.check_results['pages']['checked']
            logger.error(f"  ❌ {failed_count} pages failed out of {total_count} checked:")
            for item in self.check_results['pages']['failed_items']:
                logger.error(f"    - {item}")

        return all_good

    def check_images_on_page(self, page_url: str) -> bool:
        """Check that images on a page are loading correctly."""
        try:
            response = requests.get(page_url, timeout=10)
            
            # Handle 404 responses that serve our custom 404 page
            if response.status_code == 404:
                content = response.text.lower()
                if 'page not found' in content and 'distributed thinking systems' in content:
                    # This is our custom 404 page - check its images
                    if self.verbose:
                        logger.info(f"   📄 {page_url}: checking images on custom 404 page")
                else:
                    # This is a server error - can't check images
                    return False
            elif response.status_code != 200:
                return False

            # Simple check for broken image references
            content = response.text
            broken_images = []

            # Look for common broken image patterns, but exclude legitimate cases
            # Don't flag alt="404" on 404 pages as broken
            if '/404.html' in page_url or ('page not found' in content.lower() and 'distributed thinking systems' in content.lower()):
                # For 404 pages, only flag if there are obvious broken image indicators
                if 'alt="Image not found"' in content or 'alt="broken"' in content.lower():
                    broken_images.append("404 or missing images detected")
            else:
                # For other pages, check for broken image patterns
                if 'alt="404"' in content or 'alt="Image not found"' in content:
                    broken_images.append("404 or missing images detected")

            if broken_images:
                self.issues.append(f"Broken images on {page_url}: {', '.join(broken_images)}")
                return False

            return True
        except Exception as e:
            logger.error(f"Error checking images on {page_url}: {e}")
            return False

    def check_all_images(self) -> bool:
        """Check images on critical pages."""
        if not self.config['health_checks']['check_images']:
            return True

        logger.info("   🖼️ Checking images on critical pages...")
        all_good = True
        self.check_results['images'] = {'checked': 0, 'passed': 0, 'failed': 0, 'failed_items': []}

        for page in self.config['health_checks']['critical_pages']:
            url = f"{self.site_url}{page}"
            self.check_results['images']['checked'] += 1
            if self.check_images_on_page(url):
                self.check_results['images']['passed'] += 1
                if self.verbose:
                    logger.info(f"   ✅ {url}: images OK")
            else:
                self.check_results['images']['failed'] += 1
                self.check_results['images']['failed_items'].append(f"{url} (broken images)")
                all_good = False

        # Print summary
        if self.check_results['images']['failed'] == 0:
            logger.info(f"   ✅ {self.check_results['images']['passed']} images checked and passed.")
        else:
            failed_count = self.check_results['images']['failed']
            total_count = self.check_results['images']['checked']
            logger.error(f"  ❌ {failed_count} images failed out of {total_count} checked:")
            for item in self.check_results['images']['failed_items']:
                logger.error(f"    - {item}")

        return all_good

    def _get_site_domain(self) -> str:
        """Get the site domain from Jekyll config."""
        try:
            config_path = Path('_config.yml')
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    return config.get('url', 'https://unixwzrd.ai')
            else:
                # Fallback to default if config not found
                return 'https://unixwzrd.ai'
        except Exception as e:
            logger.warning(f"Could not read site domain from _config.yml: {e}")
            return 'https://unixwzrd.ai'

    def _is_internal_url(self, url: str) -> bool:
        """Check if URL is internal (localhost or our domain)."""
        # Check for localhost URLs
        if url.startswith('http://localhost:') or url.startswith('https://localhost:'):
            return True
        
        # Check for our domain URLs
        site_domain = self._get_site_domain()
        if site_domain in url:
            return True
        
        return False

    def _is_placeholder_link(self, url: str) -> bool:
        """Check if URL is a placeholder/example link that should be ignored."""
        placeholder_patterns = [
            'yourusername',
            'username',
            'your-repo',
            'repo-name',
            'path-to-image',
            'project-preview',
            'example.com',
            'placeholder',
            'demo',
            'test'
        ]
        
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in placeholder_patterns)

    def _get_jekyll_server_info(self) -> Dict[str, str]:
        """Get Jekyll server information from config and environment."""
        server_info = {
            'development_url': 'http://localhost:4000',
            'production_url': None
        }
        
        try:
            # Read from _config.yml
            config_path = Path('_config.yml')
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    server_info['production_url'] = config.get('url', 'https://unixwzrd.ai')
        except Exception as e:
            logger.warning(f"Could not read Jekyll config: {e}")
            server_info['production_url'] = 'https://unixwzrd.ai'
        
        return server_info

    def check_external_links(self) -> bool:
        """Check external links are working with comprehensive metrics tracking."""
        if not self.config['health_checks']['check_links']:
            return True

        logger.info("    🔗 Checking external links...")
        
        # Find all markdown files
        markdown_files = []
        for pattern in ['**/*.md', 'html/**/*.md']:
            markdown_files.extend(Path('.').glob(pattern))
        
        if not markdown_files:
            logger.warning("⚠️ No markdown files found to check for external links")
            return True
        
        # Extract external links from markdown files with source tracking
        external_links = {}  # url -> list of source pages
        internal_links = set()
        placeholder_links = set()
        
        for md_file in markdown_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find all external links using regex
                    import re
                    # Match markdown links: [text](url) where url starts with http/https
                    link_pattern = r'\[([^\]]+)\]\((https?://[^\s\)]+)\)'
                    matches = re.findall(link_pattern, content)
                    for text, url in matches:
                        if self._is_placeholder_link(url):
                            placeholder_links.add(url)
                        elif self._is_internal_url(url):
                            internal_links.add(url)
                        else:
                            if url not in external_links:
                                external_links[url] = []
                            external_links[url].append(str(md_file))
            except Exception as e:
                logger.warning(f"⚠️ Could not read {md_file}: {e}")
        
        if self.verbose and placeholder_links:
            logger.info(f"   🔗 Found {len(placeholder_links)} placeholder links (filtered out)")
            for url in sorted(placeholder_links):
                logger.info(f"    🔗 Placeholder: {url}")
        
        if self.verbose and internal_links:
            logger.info(f"   🔗 Found {len(internal_links)} internal links (filtered out)")
            for url in sorted(internal_links):
                logger.info(f"    🔗 Internal: {url}")
        
        if not external_links:
            logger.info("   ℹ️ No external links found in markdown files")
            return True
        
        if self.verbose:
            logger.info(f"   📋 Found {len(external_links)} unique external links to check")
        
        # Initialize link metrics if not exists
        if 'link_metrics' not in self.config['external_links']:
            self.config['external_links']['link_metrics'] = {}
        
        # Check each external link with comprehensive tracking
        all_good = True
        checked_count = 0
        passed_count = 0
        failed_count = 0
        link_results = {}
        
        for url in sorted(external_links.keys()):
            source_pages = external_links[url]
            if self.verbose:
                logger.info(f"   🔗 Checking {url} (found in {len(source_pages)} pages)")
                for page in source_pages:
                    logger.info(f"      📄 Source: {page}")
            checked_count += 1
            
            # Initialize metrics for this URL if not exists
            if url not in self.config['external_links']['link_metrics']:
                self.config['external_links']['link_metrics'][url] = {
                    'total_checks': 0,
                    'successful_checks': 0,
                    'failed_checks': 0,
                    'slow_checks': 0,
                    'last_check': None,
                    'last_status': None,
                    'last_response_time': None,
                    'last_error': None,
                    'average_response_time': 0.0,
                    'total_response_time': 0.0,
                    'source_pages': source_pages
                }
            else:
                # Update source pages if new ones found
                existing_pages = self.config['external_links']['link_metrics'][url].get('source_pages', [])
                for page in source_pages:
                    if page not in existing_pages:
                        existing_pages.append(page)
                self.config['external_links']['link_metrics'][url]['source_pages'] = existing_pages
            
            metrics = self.config['external_links']['link_metrics'][url]
            metrics['total_checks'] += 1
            metrics['last_check'] = datetime.now().isoformat()
            
            try:
                start_time = time.time()
                response = requests.head(url, timeout=10, allow_redirects=True)
                response_time = time.time() - start_time
                
                # Update response time metrics
                metrics['last_response_time'] = response_time
                metrics['total_response_time'] += response_time
                metrics['average_response_time'] = metrics['total_response_time'] / metrics['total_checks']
                
                # Determine status and update metrics
                slow_threshold = self.config['external_links']['slow_threshold']
                
                if response.status_code < 400:
                    # Success
                    metrics['successful_checks'] += 1
                    metrics['last_status'] = 'up'
                    metrics['last_response_time'] = response_time
                    metrics['last_error'] = None
                    status = 'up'
                    
                    # Check if slow
                    if response_time > slow_threshold:
                        # Only increment if under max limit
                        max_slow_count = self.config['external_links']['max_slow_count']
                        critical_slow_threshold = self.config['external_links']['critical_slow_threshold']
                        
                        if metrics['slow_checks'] < max_slow_count:
                            metrics['slow_checks'] += 1
                            status = 'slow'
                            
                            # Determine the problem type and message
                            problem_type = f"Slow {metrics['slow_checks']} times"
                            
                            # Build the main message line
                            main_msg = f"🐌 {url}: HTTP {response.status_code} ({response_time:.2f}s)"
                            
                            # Build the detail line with criticality first
                            if metrics['slow_checks'] >= critical_slow_threshold:
                                detail_msg = f"🚨 CRITICAL: {problem_type}"
                            else:
                                detail_msg = problem_type
                            
                            # Always show source pages for slow links on separate line
                            source_pages = metrics.get('source_pages', [])
                            if source_pages:
                                # Fixed indentation to align with HTTPS part of URL
                                indent_spaces = " " * 41  # Increased indentation to align with HTTPS
                                
                                source_info = ""
                                for page in source_pages:
                                    source_info += f"\n{indent_spaces}📄 {page}"
                            else:
                                source_info = ""
                            
                            logger.warning(f"{main_msg}\n{indent_spaces}{detail_msg}{source_info}")
                        else:
                            # At max limit
                            max_msg = f"🐌 {url}: HTTP {response.status_code} ({response_time:.2f}s) - SLOW (MAX SLOW COUNT REACHED: {max_slow_count})"
                            logger.warning(max_msg)
                    else:
                        status = 'up'
                        if self.verbose:
                            logger.info(f"    ✅ {url}: HTTP {response.status_code} ({response_time:.2f}s)")
                    
                    passed_count += 1
                else:
                    failed_count += 1
                    # Only increment if under max limit
                    max_failure_count = self.config['external_links']['max_failure_count']
                    if metrics['failed_checks'] < max_failure_count:
                        metrics['failed_checks'] += 1
                        metrics['last_status'] = 'down'
                        metrics['last_error'] = f"HTTP {response.status_code}"
                        status = 'down'
                        
                        # Check if we should investigate this link
                        max_failures = self.config['external_links']['max_failures_before_investigation']
                        critical_threshold = self.config['external_links']['critical_failure_threshold']
                        
                        # Check robots.txt for failed sites
                        robots_info = ""
                        if response.status_code in [403, 404, 503]:
                            robots_check = self._check_robots_txt(url)
                            if robots_check['blocks_all']:
                                robots_info = " (BLOCKED by robots.txt)"
                            elif robots_check['blocks_us']:
                                robots_info = " (BLOCKED by robots.txt for our user-agent)"
                            elif robots_check['exists']:
                                robots_info = " (robots.txt exists but doesn't block us)"
                        
                        # Format the error message with proper descriptions
                        main_msg, problem_type = self._format_error_message(
                            url, "http", response.status_code, response_time, 
                            metrics['failed_checks'], robots_info
                        )
                        
                        # Build the detail line with criticality first
                        if metrics['failed_checks'] >= critical_threshold:
                            detail_msg = f"🚨 CRITICAL: {problem_type}"
                        elif metrics['failed_checks'] >= max_failures:
                            detail_msg = f"INVESTIGATE: {problem_type}"
                        else:
                            detail_msg = problem_type
                        
                        # Always show source pages for failed links on separate line
                        source_pages = metrics.get('source_pages', [])
                        if source_pages:
                            # Fixed indentation to align with HTTPS part of URL
                            indent_spaces = " " * 41  # Increased indentation to align with HTTPS
                            
                            source_info = ""
                            for page in source_pages:
                                source_info += f"\n{indent_spaces}📄 {page}"
                        else:
                            source_info = ""
                        
                        logger.error(f"{main_msg}\n{indent_spaces}{detail_msg}{source_info}")
                    else:
                        # At max limit
                        max_msg = f"  ❌ {url}: HTTP {response.status_code} ({response_time:.2f}s) - DOWN (MAX FAILURE COUNT REACHED: {max_failure_count})"
                        logger.error(max_msg)
                    
                    self.check_results['external_links']['failed_items'].append(
                        f"{url}: HTTP {response.status_code} ({response_time:.2f}s)")
                    all_good = False
                    
            except requests.exceptions.Timeout:
                failed_count += 1
                # Only increment if under max limit
                max_failure_count = self.config['external_links']['max_failure_count']
                if metrics['failed_checks'] < max_failure_count:
                    metrics['failed_checks'] += 1
                    metrics['last_status'] = 'timeout'
                    metrics['last_error'] = 'Timeout'
                    status = 'timeout'
                    
                    # Format the error message with proper descriptions
                    main_msg, problem_type = self._format_error_message(
                        url, "timeout", response_time=response_time, 
                        count=metrics['failed_checks']
                    )
                    
                    # Build the detail line with criticality first
                    if metrics['failed_checks'] >= critical_threshold:
                        detail_msg = f"🚨 CRITICAL: {problem_type}"
                    elif metrics['failed_checks'] >= max_failures:
                        detail_msg = f"INVESTIGATE: {problem_type}"
                    else:
                        detail_msg = problem_type
                    
                    # Always show source pages for failed links on separate line
                    source_pages = metrics.get('source_pages', [])
                    if source_pages:
                        # Fixed indentation to align with HTTPS part of URL
                        indent_spaces = " " * 41  # Increased indentation to align with HTTPS
                        
                        source_info = ""
                        for page in source_pages:
                            source_info += f"\n{indent_spaces}📄 {page}"
                    else:
                        source_info = ""
                    
                    logger.error(f"{main_msg}\n{indent_spaces}{detail_msg}{source_info}")
                else:
                    # At max limit
                    max_msg = f"  ❌ {url}: Timeout (MAX FAILURE COUNT REACHED: {max_failure_count})"
                    logger.error(max_msg)
                
                self.check_results['external_links']['failed_items'].append(f"{url}: Timeout")
                all_good = False
                
            except requests.exceptions.ConnectionError:
                failed_count += 1
                # Only increment if under max limit
                max_failure_count = self.config['external_links']['max_failure_count']
                if metrics['failed_checks'] < max_failure_count:
                    metrics['failed_checks'] += 1
                    metrics['last_status'] = 'connection_error'
                    metrics['last_error'] = 'Connection error'
                    status = 'connection_error'
                    
                    # Always show source pages for failed links
                    source_pages = metrics.get('source_pages', [])
                    if source_pages:
                        # Fixed indentation to align with HTTPS part of URL
                        indent_spaces = " " * 41  # Increased indentation to align with HTTPS
                        
                        source_info = ""
                        for page in source_pages:
                            source_info += f"\n{indent_spaces}📄 {page}"
                    else:
                        source_info = ""
                    
                    # Format the error message with proper descriptions
                    main_msg, problem_type = self._format_error_message(
                        url, "connection_error", response_time=response_time, 
                        count=metrics['failed_checks']
                    )
                    
                    # Build the detail line with criticality first
                    if metrics['failed_checks'] >= critical_threshold:
                        detail_msg = f"🚨 CRITICAL: {problem_type}"
                    elif metrics['failed_checks'] >= max_failures:
                        detail_msg = f"INVESTIGATE: {problem_type}"
                    else:
                        detail_msg = problem_type
                    
                    # Always show source pages for failed links on separate line
                    source_pages = metrics.get('source_pages', [])
                    if source_pages:
                        # Fixed indentation to align with HTTPS part of URL
                        indent_spaces = " " * 41  # Increased indentation to align with HTTPS
                        
                        source_info = ""
                        for page in source_pages:
                            source_info += f"\n{indent_spaces}📄 {page}"
                    else:
                        source_info = ""
                    
                    logger.error(f"{main_msg}\n{indent_spaces}{detail_msg}{source_info}")
                else:
                    # At max limit
                    max_msg = f"  ❌ {url}: Connection error (MAX FAILURE COUNT REACHED: {max_failure_count})"
                    logger.error(max_msg)
                
                self.check_results['external_links']['failed_items'].append(f"{url}: Connection error")
                all_good = False
                
            except Exception as e:
                failed_count += 1
                # Only increment if under max limit
                max_failure_count = self.config['external_links']['max_failure_count']
                if metrics['failed_checks'] < max_failure_count:
                    metrics['failed_checks'] += 1
                    metrics['last_status'] = 'error'
                    metrics['last_error'] = str(e)
                    status = 'error'
                    
                    # Always show source pages for failed links
                    source_pages = metrics.get('source_pages', [])
                    if source_pages:
                        # Fixed indentation to align with HTTPS part of URL
                        indent_spaces = " " * 41  # Increased indentation to align with HTTPS
                        
                        source_info = ""
                        for page in source_pages:
                            source_info += f"\n{indent_spaces}📄 {page}"
                    else:
                        source_info = ""
                    
                    error_msg = f"  ❌ {url}: {str(e)} (been down {metrics['failed_checks']} times){source_info}"
                    
                    # Check thresholds for investigation
                    max_failures = self.config['external_links']['max_failures_before_investigation']
                    critical_threshold = self.config['external_links']['critical_failure_threshold']
                    
                    if metrics['failed_checks'] >= critical_threshold:
                        critical_msg = f"{error_msg} - 🚨 CRITICAL: INVESTIGATE IMMEDIATELY!"
                        logger.error(critical_msg)
                    elif metrics['failed_checks'] >= max_failures:
                        investigate_msg = f"{error_msg} - INVESTIGATE!"
                        logger.error(investigate_msg)
                    else:
                        logger.error(error_msg)
                else:
                    # At max limit
                    max_msg = f"  ❌ {url}: {str(e)} (MAX FAILURE COUNT REACHED: {max_failure_count})"
                    logger.error(max_msg)
                
                self.check_results['external_links']['failed_items'].append(f"{url}: {str(e)}")
                all_good = False
            
            # Store current result
            link_results[url] = {
                'status': status,
                'response_time': metrics['last_response_time'],
                'http_status': getattr(response, 'status_code', None) if 'response' in locals() else None,
                'error': metrics['last_error'],
                'metrics': metrics
            }
        
        # Update check results
        self.check_results['external_links']['checked'] = checked_count
        self.check_results['external_links']['passed'] = passed_count
        self.check_results['external_links']['failed'] = failed_count
        
        # Save updated metrics to config
        self._save_config(self.config)
        
        # Only show summary if not in verbose mode (to avoid redundancy)
        if not self.verbose:
            if not all_good:
                logger.error(f"  ❌ {failed_count} external links failed out of {checked_count} checked")
            else:
                logger.info(f"   ✅ All {checked_count} external links are working")
        
        return all_good

    def run_health_checks(self) -> bool:
        """Run all health checks."""
        logger.info("   🏥 Starting comprehensive health checks...")
        self.issues = []

        # Basic availability check - if this fails, everything else will fail
        if not self.check_site_availability():
            logger.error("  ❌ Site is not accessible. Skipping all other checks to avoid timeouts.")
            logger.warning("⚠️ Health checks failed: Site is down")
            return False

        # Critical pages check
        critical_pages_ok = self.check_critical_pages()
        if not critical_pages_ok:
            # Check if the index page specifically failed
            site_domain = self._get_site_domain()
            index_failed = any(
                "http://localhost:4000/" in item or f"{site_domain}/" in item 
                for item in self.check_results['pages']['failed_items']
            )
            if index_failed:
                logger.error("  🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨")
                logger.error("  🚨🚨🚨              CRITICAL: INDEX PAGE IS DOWN!               🚨🚨🚨")
                logger.error("  🚨🚨🚨 CRITICAL FAILURE - VISITORS CANNOT ACCESS YOUR HOMEPAGE! 🚨🚨🚨")
                logger.error("  🚨🚨🚨               IMMEDIATE ACTION REQUIRED!                 🚨🚨🚨")
                logger.error("  🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨")
            logger.warning("⚠️ Some critical pages failed, but continuing with other checks...")

        # Images check
        images_ok = self.check_all_images()
        if not images_ok:
            logger.warning("⚠️ Some images failed, but continuing with other checks...")

        # External links check
        external_links_ok = self.check_external_links()
        if not external_links_ok:
            logger.warning("⚠️ Some external links failed, but continuing with other checks...")

        # Custom health checks
        for check in self.health_checks:
            try:
                result = check['func']()
                if not result and check['critical']:
                    self.issues.append(f"Critical check failed: {check['name']}")
                    return False
                elif not result:
                    self.issues.append(f"Non-critical check failed: {check['name']}")
            except Exception as e:
                logger.error(f"Error in health check {check['name']}: {e}")
                if check['critical']:
                    self.issues.append(f"Critical check error: {check['name']} - {e}")
                    return False

        # Print final summary
        total_issues = len(self.issues)
        if total_issues == 0:
            logger.info("   🎉 All health checks passed! Your site is healthy and ready for visitors.")
        else:
            logger.warning(f"⚠️ Health checks completed with {total_issues} issues")
            logger.info("Please review and fix the issues listed above.")
        
        return total_issues == 0

    def send_alert_email(self, subject: str, body: str) -> bool:
        """Send alert email."""
        try:
            email_config = self.config['email']

            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['recipient_email']
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            server.send_message(msg)
            server.quit()

            logger.info("   📧 Alert email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send alert email: {e}")
            return False

    def post_commit_verification(self, commit_hash: str = None) -> bool:
        """Verify site after a commit with delay for deployment."""
        logger.info("   🚀 Starting post-commit verification...")

        delay_minutes = self.config['deployment']['check_delay_minutes']
        logger.info(f"   ⏳ Waiting {delay_minutes} minutes for deployment...")
        time.sleep(delay_minutes * 60)

        # Run health checks
        success = self.run_health_checks()

        if success:
            subject = "   ✅ Site Deployment Successful"
            body = f"""
Site deployment verification completed successfully!

Commit: {commit_hash or 'Unknown'}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Site URL: {self.site_url}

All health checks passed. Your site is running smoothly.
"""
        else:
            subject = "  ❌ Site Deployment Issues Detected"
            body = f"""
Site deployment verification found issues!

Commit: {commit_hash or 'Unknown'}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Site URL: {self.site_url}

Issues found:
{chr(10).join(f"- {issue}" for issue in self.issues)}

Please investigate and fix these issues.
"""

        # Send alert email
        self.send_alert_email(subject, body)

        return success

    def periodic_health_check(self) -> bool:
        """Run periodic health check."""
        logger.info("   ⏰ Running periodic health check...")

        success = self.run_health_checks()

        if not success:
            subject = "⚠️ Site Health Issues Detected"
            body = f"""
Periodic health check found issues!

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Site URL: {self.site_url}

Issues found:
{chr(10).join(f"- {issue}" for issue in self.issues)}

Please investigate these issues.
"""
            self.send_alert_email(subject, body)

        return success

    def _check_robots_txt(self, url: str) -> Dict[str, any]:
        """Check robots.txt for a given URL to see if we're being blocked."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            
            response = requests.get(robots_url, timeout=5, headers={
                'User-Agent': 'SiteReliabilityMonitor/1.0'
            })
            
            if response.status_code == 200:
                robots_content = response.text.lower()
                user_agent_blocked = 'user-agent: *' in robots_content and 'disallow: /' in robots_content
                specific_blocked = 'user-agent: sitereliabilitymonitor' in robots_content and 'disallow: /' in robots_content
                
                return {
                    'exists': True,
                    'blocks_all': user_agent_blocked,
                    'blocks_us': specific_blocked,
                    'content': robots_content[:200] + '...' if len(robots_content) > 200 else robots_content
                }
            else:
                return {
                    'exists': False,
                    'blocks_all': False,
                    'blocks_us': False,
                    'content': f"robots.txt returned {response.status_code}"
                }
        except Exception as e:
            return {
                'exists': False,
                'blocks_all': False,
                'blocks_us': False,
                'content': f"Error checking robots.txt: {str(e)}"
            }

    def reset_external_link_stats(self, reset_type: str = "all") -> bool:
        """Reset external link statistics.
        
        Args:
            reset_type: "all", "failed", "slow", "timeout", "connection_error", or "error"
        """
        if 'link_metrics' not in self.config['external_links']:
            logger.info("   ℹ️ No external link statistics to reset")
            return True
        
        reset_count = 0
        link_metrics = self.config['external_links']['link_metrics']
        
        for url, metrics in link_metrics.items():
            if reset_type == "all":
                # Reset all counters
                metrics['total_checks'] = 0
                metrics['successful_checks'] = 0
                metrics['failed_checks'] = 0
                metrics['slow_checks'] = 0
                metrics['last_check'] = None
                metrics['last_status'] = None
                metrics['last_response_time'] = None
                metrics['last_error'] = None
                metrics['average_response_time'] = 0.0
                metrics['total_response_time'] = 0.0
                reset_count += 1
            elif reset_type == "failed":
                # Reset only failed checks
                if metrics['failed_checks'] > 0:
                    metrics['failed_checks'] = 0
                    reset_count += 1
            elif reset_type == "slow":
                # Reset only slow checks
                if metrics['slow_checks'] > 0:
                    metrics['slow_checks'] = 0
                    reset_count += 1
            elif reset_type in ["timeout", "connection_error", "error"]:
                # Reset specific error types
                if metrics.get('last_error', '').lower().find(reset_type) != -1:
                    metrics['failed_checks'] = 0
                    metrics['last_error'] = None
                    reset_count += 1
        
        if reset_count > 0:
            self._save_config(self.config)
            logger.info(f"   ✅ Reset {reset_count} external link statistics for type: {reset_type}")
        else:
            logger.info(f"   ℹ️ No statistics found to reset for type: {reset_type}")
        
        return True

    def _get_http_status_description(self, status_code):
        """Get human-readable description for HTTP status codes."""
        descriptions = {
            200: "OK",
            201: "Created",
            202: "Accepted",
            204: "No Content",
            301: "Moved Permanently",
            302: "Found",
            304: "Not Modified",
            307: "Temporary Redirect",
            308: "Permanent Redirect",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            408: "Request Timeout",
            429: "Too Many Requests",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            999: "Unknown Error (LinkedIn)"
        }
        return descriptions.get(status_code, f"Unknown Status ({status_code})")

    def _format_error_message(self, url, error_type, status_code=None, response_time=None, count=None, robots_info=None):
        """Format error messages with proper descriptions."""
        # Build the main message line with response time
        if status_code:
            status_desc = self._get_http_status_description(status_code)
            main_msg = f"  ❌ {url}: HTTP {status_code} - {status_desc} ({response_time:.2f}s)"
        else:
            if error_type == "timeout":
                main_msg = f"  ❌ {url}: Connection timed out (N/A) ({response_time:.2f}s)"
            else:
                time_str = f"({response_time:.2f}s)" if response_time else "(N/A)"
                main_msg = f"  ❌ {url}: {error_type.title()} error (N/A) {time_str}"
        
        # Determine the problem type and message (proper capitalization)
        if robots_info and "BLOCKED by robots.txt" in robots_info:
            problem_type = f"Blocked by robots.txt {count} times"
        else:
            problem_type = f"Down {count} times"
        
        return main_msg, problem_type


def main():
    parser = argparse.ArgumentParser(description='Site Reliability Monitor')
    parser.add_argument('--mode', choices=['health', 'post-commit', 'periodic', 'reset'],
                        default='health', help='Monitoring mode')
    parser.add_argument('--commit-hash', help='Commit hash for post-commit verification')
    parser.add_argument('--config', default='utils/etc/site_monitor_config.json',
                        help='Configuration file path')
    parser.add_argument('--local', action='store_true',
                        help='Test against localhost (default: production site)')
    parser.add_argument('-V', '--verbose', action='store_true',
                        help='Verbose output showing all checked items')
    parser.add_argument('-r', '--reset', choices=['all', 'failed', 'slow', 'timeout', 'connection_error', 'error'],
                        help='Reset external link statistics (use with --mode reset)')

    args = parser.parse_args()

    monitor = SiteReliabilityMonitor(args.config, local_mode=args.local, verbose=args.verbose)

    if args.mode == 'health':
        success = monitor.run_health_checks()
        sys.exit(0 if success else 1)
    elif args.mode == 'post-commit':
        success = monitor.post_commit_verification(args.commit_hash)
        sys.exit(0 if success else 1)
    elif args.mode == 'periodic':
        success = monitor.periodic_health_check()
        sys.exit(0 if success else 1)
    elif args.mode == 'reset':
        if not args.reset:
            print("Error: --reset flag is required when using --mode reset")
            print("Available reset types: all, failed, slow, timeout, connection_error, error")
            sys.exit(1)
        success = monitor.reset_external_link_stats(args.reset)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
