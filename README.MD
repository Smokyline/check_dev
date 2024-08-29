# Сервис по проверке работы устройства на обсерватории

## Описание сервиса

Сервис предоставляет возможность управления и мониторинга устройств в обсерватории через API. Поддерживаются следующие операции:

### 1. Запостить в базу данных информацию об устройстве

**Метод:** POST  
**URL:** `http://host:8001/post-status/`  
**Формат данных:** JSON  

```json
{
    "obs": "GC0",
    "dev": "POS1",
    "date0": 1675435439,
    "date1": 1675435434863,
    "filename": "//brick/data/gcras2023.pmb",
    "md5": "6aa9ff5f6e87d2413fa244f8ebdca12c",
    "ucount": 1,
    "filesize": 424520
}
```

**Ответ:**  
- `0` - успешное добавление  
- `1` - ошибка при добавлении в базу

### 2. Получить из базы данных информацию об устройстве за период

**Метод:** GET  
**URL:** `http://host:8001/get-status/`  
**Заголовки:** `Authorization: Bearer <Token>`  
**Формат данных:** JSON  

```json
{
    "obs": "GC0",
    "dev": "POS1",
    "date0_from": 1675435439,
    "date0_to": 1675435619,
    "date1_from": 1675435434863,
    "date1_to": 1675435614670
}
```

**Ответ:**  
Словарь с массивами данных за указанный период.

### 3. Получить из базы данных последнюю запись по станции и устройству

**Метод:** GET  
**URL:** `http://host:8001/get-last-status/`  
**Заголовки:** `Authorization: Bearer <Token>`  
**Формат данных:** JSON  

```json
{
    "obs": "GC0",
    "dev": "POS1"
}
```

**Ответ:**  
Последняя запись по указанным ключам.

### 4. Получить список всех обсерваторий и их устройств

**Метод:** GET  
**URL:** `http://host:8001/get-all-obs/`  
**Заголовки:** `Authorization: Bearer <Token>`  

**Ответ:**  
Список обсерваторий в JSON формате.

### 5. Проверка подлинности токена авторизации

**Метод:** GET  
**URL:** `http://host:8001/check-token/`  
**Заголовки:** `Authorization: Bearer <Token>`  

**Ответ:**  
- `token verification passed` - успешно  
- `token verification failed` - ошибка

## Развертывание бекэнда

### На локальной машине

```bash
git clone https://git.gcras.ru/hg/gm/check_dev
docker build . -t docker-check-dev
docker run -p 8000:8000 docker-check-dev
```

### На сервере

```bash
docker build . -t docker-check-dev
docker tag %TAG% docker.gcras.ru/docker-check-dev
docker push docker.gcras.ru/docker-check-dev
ssh user@serverIP
docker pull docker.gcras.ru/docker-check-dev
docker run -d -it --rm -v /tmp/logs:/check-device/logs -p 8001:8001 docker.gcras.ru/docker-check-dev
```

## Логи

- **Логи ошибок:** `/logs/debug.log`
- **Логи запросов:** `/logs/ip_request.log`

При развертывании на сервере, файлы логов хранятся в папке `/tmp/logs/`.