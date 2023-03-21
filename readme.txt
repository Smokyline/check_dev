Сервис по проверке работы устройства на обсерватории.

Существует 4 возможных запроса:
1) Запостить в базу данных информацию об устройстве
POST реквест по адресу http://host:8001/post-status/
в JSON формате
{
    "obs":"GC0",
    "dev": "POS1",
    "date0": 1675435439, #sec
    "date1": 1675435434863, #ms
    "filename": "//brick/data/gcras2023.pmb",
    "md5": "6aa9ff5f6e87d2413fa244f8ebdca12c",
	"ucount": 1,
	"filesize": 424520
}
При успешном добавлении возвращает 0, при ошибке при добавлении в базу возвращает 1

2) Получить из базы данных информацию об устройстве за период
GET реквест по адресу http://host:8001/get-status/ с Bearer Token в headers 'Authorization'
в JSON формате
{
    "obs":"GC0",
    "dev": "POS1",
    "date0_from": 1675435439,
    "date0_to": 1675435619,
    "date1_from": 1675435434863,
    "date1_to": 1675435614670
}
ответом будет получен словарь, где каждый ключ будет иметь массив
с данными в указанном временном периоде (в данном примере за временной период в базе есть 4 значения)
{
    "obs": [
        "GC0","GC0","GC0","GC0"
    ],
    "date0": [
        1675435439,1675435499,1675435559,1675435619
    ],
    "dev": [
        "POS1","POS1","POS1","POS1"
    ],
    "date1": [
        1675435434863,1675435495080,1675435554881,1675435614670
    ],
    "filename": [
        "//brick/data/gcras2023.pmb","//brick/data/gcras2023.pmb","//brick/data/gcras2023.pmb","//brick/data/gcras2023.pmb"
    ],
    "md5": [
        "6aa9ff5f6e87d2413fa244f8ebdca12c","84d6cfed0bc7d5cfff6160f8f83e2416","1e96746167e9467759a148a3277e9851","64055dd6292e8ec64baebc259ad78d5f"
    ],
    "ucount": [
        1,1,1,1
    ],
    "filesize": [
        424520,425040,425520,426000
    ]
}

3) Получить из базы данных последнюю запись в базе по станции и устройству
GET реквест по адресу http://host:8001/get-last-status/ с Bearer Token в headers 'Authorization'
в JSON формате
{
    "obs":"GC0",
    "dev": "POS1"
}

ответ - последняя запись по указанным ключам 'obs' и 'dev'
{
    "obs": "GC0",
    "dev": "POS1",
    "date0": 1679391872,
    "date1": 1679391870172,
    "filename": "//brick/data/gcras2023.pmb",
    "md5": "6e482155a58cf981b81e676bb3a593fd",
    "ucount": 1,
    "filesize": 281040
}

для п2 и п3 - если данных нет за указанный период, будет возвращен пустой словарь {}


4) Проверка подлинности токена авторизации 
GET запрос по адресу http://host:8001/check-token/
содержащий Bearer Token в headers 'Authorization'
При успешной проверке возвращает 'token verification passed', если нет, то 'token verification failed'
--------------------------------------------------------------------------------------------------------------------------

Расширеннная часть
	
	- ошибки записываются в корень проекта, в файл debug.log


1) Запостить в базу данных информацию об устройстве: POST реквест по адресу http://host:8001/post-status/ в JSON формате
	- из словаря request парсятся значения 
		obs (название обсерватории), str
		dev (название устройства), str
		date0 (дата поступления записи с устройства, сек), int
		date1(дата записи файла на устройстве, мс), int
		filename (название файла), str
		md5 (Md5-сумма файла, 16 byte binary file hash), str
		ucount (частота обновления данных в минуту), int
		filesize (размер файла), int
	- если в словаре request нет ucount и\или filesize, им приписывается значение -1
	- бекэнд поключается к БД и записывает туда строку из предыдущего пункта в формате столбцов:
		obs_code, dev_code, date0, date1, filename, md5_hash, ucount, filesize
	- если все прошло успешно, возвращается 0, если нет, то 1

2)  Получить из базы данных информацию об устройстве за период: GET реквест по адресу http://host:8001/get-status/ с Bearer Token в headers 'Authorization' в JSON формате
	- из request берется Bearer Token в headers 'Authorization', декодируется, если авторизация не пройдена, возвращается пустой словарь {}
	- из словаря request парсятся значения 
		obs (название обсерватории), str
		dev (название устройства), str
		date0_from (с даты поступления записи с устройства, сек), int
		date0_to (по дату поступления записи с устройства, сек), int
		date1_from (по дату записи файла на устройстве, мс), int
		date1_to(по дату записи файла на устройстве, мс), int
	- бекэнд подключается к БД, если за указанный период нет данных, возвращается пустой словарь {}
	- если значения есть, они возвращаются в словаре со следующими ключами:
		obs_code, dev_code, date0, date1, filename, md5_hash, ucount, filesize

3) Получить из базы данных последнюю запись по станции и устройству: GET реквест по адресу http://host:8001/get-last-status/ с Bearer Token в headers 'Authorization' в JSON формате
	- из request берется Bearer Token в headers 'Authorization', декодируется, если авторизация не пройдена, возвращается пустой словарь {}
	- из словаря request парсятся значения 
		obs (название обсерватории), str
		dev (название устройства), str
	- бекэнд подключается к БД, если за указанный период нет данных, возвращается пустой словарь {}
	- если значения есть, они возвращаются в словаре со следующими ключами:
		obs_code, dev_code, date0, date1, filename, md5_hash, ucount, filesize
		
-----------------------------------------------------------------------------------------------------------------------------

Развертывание бекэнда
a) на локальной машине
git clone https://git.gcras.ru/hg/gm/check_dev
docker build . -t docker-check-dev
docker run -p 8000:8000 docker-check-dev
б) на сервере
docker build . -t docker-check-dev
docker tag %TAG% docker.gcras.ru/docker-check-dev
docker push docker.gcras.ru/docker-check-dev
ssh user@serverIP
docker pull docker.gcras.ru/docker-check-dev
docker run -d -p 8001:8001 docker.gcras.ru/docker-check-dev