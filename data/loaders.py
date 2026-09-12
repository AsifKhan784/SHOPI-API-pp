import os
import random
from typing import List
from api.models import Site, Proxy, Address
from api.config import settings

def load_sites() -> List[Site]:
    """Load sites from data/sites.txt"""
    sites = []
    try:
        with open(settings.SITES_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 1:
                        store = parts[0].strip()
                        product = parts[1].strip() if len(parts) > 1 else "/products/test"
                        price = parts[2].strip() if len(parts) > 2 else "2.95 USD"
                        site = Site(
                            store=store,
                            product=product,
                            price=price,
                            gateway="Shopify Payments",
                            weight=1
                        )
                        site.id = len(sites) + 1
                        sites.append(site)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(settings.SITES_FILE), exist_ok=True)
        with open(settings.SITES_FILE, 'w') as f:
            f.write("# Format: store|product|price\n")
            f.write("https://example.myshopify.com|/products/test|2.95 USD\n")
    
    if not sites:
        sites.append(Site(
            store="https://example.myshopify.com",
            product="/products/test",
            price="1.99 USD",
            gateway="Shopify Payments",
            weight=1,
            id=1
        ))
    
    return sites

def load_proxies() -> List[Proxy]:
    """Load proxies from data/proxies.txt
    Supports both formats:
      host:port:user:pass
      user:pass@host:port
    """
    proxies = []
    try:
        with open(settings.PROXIES_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    if '@' in line:
                        # user:pass@host:port
                        auth, hostport = line.rsplit('@', 1)
                        user, password = auth.split(':', 1)
                        host, port = hostport.split(':', 1)
                    else:
                        # host:port:user:pass
                        parts = line.split(':')
                        if len(parts) != 4:
                            continue
                        host, port, user, password = parts
                    
                    proxy = Proxy(
                        host=host,
                        port=int(port),
                        username=user,
                        password=password
                    )
                    proxy.id = len(proxies) + 1
                    proxies.append(proxy)
                except Exception:
                    continue
    except FileNotFoundError:
        os.makedirs(os.path.dirname(settings.PROXIES_FILE), exist_ok=True)
        with open(settings.PROXIES_FILE, 'w') as f:
            f.write("# Format: host:port:username:password  OR  user:pass@host:port\n")
    
    return proxies

def generate_email() -> str:
    """Generate random email"""
    prefix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
    domain = random.choice(settings.EMAIL_DOMAINS)
    return f"{prefix}{random.randint(10,99)}@{domain}"

def generate_address() -> Address:
    """Generate random US address"""
    first_names = ["John", "James", "Robert", "Michael", "David", "William"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
    streets = ["Main St", "Oak Ave", "Pine Rd", "Maple Dr", "Cedar Ln", "Elm St"]
    cities = ["New York", "Los Angeles", "Miami", "Austin", "Seattle", "Chicago"]
    states = ["NY", "CA", "FL", "TX", "WA", "IL"]
    
    return Address(
        first_name=random.choice(first_names),
        last_name=random.choice(last_names),
        address1=f"{random.randint(100,9999)} {random.choice(streets)}",
        city=random.choice(cities),
        state=random.choice(states),
        zip=f"{random.randint(10000,99999)}"
    )
