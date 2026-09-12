def load_proxies() -> List[Proxy]:
    proxies = []
    try:
        with open(settings.PROXIES_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Support both formats
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
        pass
    return proxies
