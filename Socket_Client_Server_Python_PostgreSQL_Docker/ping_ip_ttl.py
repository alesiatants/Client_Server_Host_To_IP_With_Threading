import subprocess
import re
import socket

def get_ip_ttl(domain):
    '''Получение IPv4-адреса и TTL по домену'''
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        print('Ошибка при получении IPv4-адреса')
        return 0
		# Очистка кэша
    result = subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = subprocess.run(["ping", domain, "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode > 0:
        print('Ошибка соединения с DNS сервером')
        return 0

    # Поиск TTL в выводе
    ttl_match = re.search(r'TTL=(\d+)', result.stdout)

    if ttl_match:
        ttl = int(ttl_match.group(1))
        return ttl, ip
    else:
        print('Не удалось извлечь TTL')
        return 0