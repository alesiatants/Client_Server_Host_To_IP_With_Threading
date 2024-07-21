import socket
from ping_ip_ttl import get_ip_ttl
from _thread import start_new_thread
from connection import Connection
from get_ttl_round import round_ttl

def create_server(host, port):
    '''Создает потоковый сокет сервера и обрабатывает соединения с клиентами'''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    thread_count = 0
    conn = Connection()

    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(e)
        return

    print('Ожидание соединения...')
    server_socket.listen(10000)

    def handle_client(connection, address):
        '''Обрабатывает запросы от клиентов в отдельном потоке'''
        while True:
            try:
                data = connection.recv(1024)
                if not data or data.decode() == "Выход":
                    print(f'Завершено соединение с: {address[0]}:{address[1]}')
                    break

                domain = data.decode()
                print(f'Получен домен: {domain}')
                print('Обработка данных...')
                
                if conn.check_records(domain) != 0:
                    res = conn.find_value(domain)
                else:                   
                    if isinstance(get_ip_ttl(domain), tuple):
                        ttl, res = get_ip_ttl(domain)
                        conn.insert_new_record(domain, res, round_ttl(ttl))
                    else:
                        res = "0"
                connection.sendall(res.encode())
            except (ConnectionResetError, ConnectionAbortedError):
                print(f'Завершено соединение с: {address[0]}:{address[1]}')
                break
        connection.close()

    while True:
        object_conn, address = server_socket.accept()
        print(f'Установлено соединение с: {address[0]}:{address[1]}')
        thread_count += 1
        start_new_thread(handle_client, (object_conn, address,))
        print(f'Номер потока: {thread_count}')

    server_socket.close()

def main():
    '''Запускает сервер на localhost:10000'''
    create_server('localhost', 10000)

if __name__ == '__main__':
    main()