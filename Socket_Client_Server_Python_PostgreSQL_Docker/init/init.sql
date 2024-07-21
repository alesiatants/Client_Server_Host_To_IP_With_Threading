--Создание схемы
create schema socket;
--Создание таблицы с первичным ключем 
create table socket.socket_log (
	id INT GENERATED ALWAYS AS IDENTITY,
	domen varchar(30) not null,
	ip varchar(20) not null,
	timelive smallint not null,
	created timestamp not null default now()
);
--Создание триггерной функции, выполняющеся после вставки записи в таблицу
CREATE FUNCTION socket.delete_old_rows()
    RETURNS TRIGGER
    LANGUAGE 'plpgsql'
AS $$
DECLARE r RECORD;
BEGIN
FOR r IN SELECT timelive FROM socket.socket_log
LOOP
DELETE FROM socket.socket_log WHERE created<NOW()-(timelive || ' minute')::interval;
END LOOP;
RETURN NEW;
END;
$$;
--Создание триггера для таблицу, срабатывающей после события вставки записи
CREATE OR REPLACE TRIGGER delete_old_rows_trigger_insert
    AFTER INSERT
    ON socket.socket_log
		FOR EACH ROW
    EXECUTE FUNCTION socket.delete_old_rows();
--Создание обычной функции
CREATE FUNCTION socket.delete_old_rows_before_select()
RETURNS INT
    LANGUAGE 'plpgsql'
AS $$
DECLARE r RECORD;
BEGIN
FOR r IN SELECT timelive FROM socket.socket_log
LOOP
DELETE FROM socket.socket_log WHERE created<NOW()-(timelive || ' minute')::interval;
END LOOP;
RETURN 1;
END;
$$;