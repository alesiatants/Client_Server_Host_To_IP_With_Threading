import socket
from ping_ip_ttl import get_ip_ttl
from _thread import start_new_thread
import threading
from connection import Connection
from get_ttl_round import round_ttl
import time


    
def create_server(host, port):
    '''Создает потоковый сокет сервера и обрабатывает соединения с клиентами'''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    thread_count = 0
    conn = Connection()
    # создание пустого словаря для сопоставления доменов и IP-адресов, времени их внесения
    table = {}
    # создание объекта блокировки для безопасного доступа к общему ресурсу - словарю
    lock = threading.Lock()  
    
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(e)
        return

    print('Ожидание соединения...')
    server_socket.listen(10000)
    
                          
    def check_db_dns(conn, domain):
        '''Поиск записи (в БД, обращаясь на dns сервер, обработка неккоректного ввода хоста)
          и возврат ip'''
        if conn.check_records(domain) != 0:
                  res = conn.find_value(domain)
                  print("Успешно получено из БД!")
        else:
                if isinstance(get_ip_ttl(domain), tuple):
                  ttl, res = get_ip_ttl(domain)
                  conn.insert_new_record(domain, res, round_ttl(ttl))
                  print("Успешно добавлено в БД!")
                else:
                      res = "0"
        return res
    def handle_client(connection, address, lock):
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
                
                # начало блока синхронизации для обеспечения потокобезопасного доступа к словарю - блокировка
                with lock:
                  try:
                    # проверка наличия домена в словаре и проверка времени кэширования
                    if domain in table and time.time() - table[domain][1] <= 5:
                         res = table[domain][0]
                         table[domain] = (res, time.time())
                         print("Успешно получено из словаря!")
                    else:
                         ip_address = check_db_dns(conn,domain)
                         table[domain] = (ip_address, time.time())
                         print("Успешно добавлено в словарь!")
                         res = ip_address
                    print(table.items()) # печатаем элементы словаря
                  except Exception as ex:
                       print(f"Возникла ошибка : {ex}") 
                
                connection.sendall(res.encode())
               
            except (ConnectionResetError, ConnectionAbortedError):
                print(f'Завершено соединение с: {address[0]}:{address[1]}')
                break
            
        connection.close()
        
    def cleanup():
         '''Очистка пар в словаре, которые были добавлены более 5 с. назад'''
         while True:
               time.sleep(10)
               with lock:
                      print("Нужна очистка?")
                      try:
                      	for domain, data in list(table.items()):
                              if time.time() - data[1] > 5:
                                      del table[domain]
                                      print('Успешно удалено из словаря!')
                      except Exception as ex:
                           print(f"Возникла ошибка с очисткой словаря : {ex}")
		# создание потока для очистки устаревших соответствий в словаре
    start_new_thread(cleanup, ())
    while True:
        
        object_conn, address = server_socket.accept()
        print(f'Установлено соединение с: {address[0]}:{address[1]}')
        thread_count += 1
        start_new_thread(handle_client, (object_conn, address, lock))
        print(f'Номер потока: {thread_count}')
    #server_socket.close()

def main():
    '''Запускает сервер на localhost:10000'''
    
    create_server('localhost', 10000)

if __name__ == '__main__':
    main()
