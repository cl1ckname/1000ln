# 1000ln
Novator WEB 2.0 by Vasilev Ivan

Привет проверяющим. Скорее всего это Сева, но как знать.

Я искрене пытался писать как можно более понятно, но по PEP у меня
около 60 ошибок, так что как знать.

###finder.py
Скажу честно, хотел сделать через ThreadPoolExecutor, но не осилил, поэтому
чистые потоки. Сразу проясню момент про PermissionError, с этой ошибкой я
сталкивался только на своей машине, на других компьютерах такого не было.
Консоль от имени администратора тоже не помогла. Менял привелегии папкам -
никаких изменений. Линукс всё же понятнее. 
Может вы с этим не столкнётесь, но на некоторых машинах, особенно с забитым
диском жестко зависает даже с сотней потоков. Там параметр -t есть, стоит
порой погонять значения. Вроде бы всё.
--------------------------------------------------------------------------

###CoolModule.py
PostgreSQL конечно круто, но мне понадобилось 4 часа чтобы понять, что в
12 версии изменили порт с 5432 (Как в 9) на 5433. В тз написанно, что это
должна быть "часть готовой программы", поэтому для использования модуля
должна существовать бд для очереди. Очень надеюсь, что не нужно было юзать
PGQ. Вещь страшная, документации никакой, даже на индусских форумах. Здесь
вроде бы всё понятно, ничего особо пояснять не приходится. Рядом должны
быть internet.txt и CoolProgram.py. Первый это что-то типа источника тасков,
на втором я тестил, может и вам пригодится. Так странно переписывание инфы
с одного файла в другой (mail_logs) я ещё не реализовывал.
---------------------------------------------------------------------------

####Ps
Очень боялся, что Дима запрягёт делать ещё одну игру. Игры круто конечно,
но программирование подобного рода мне нравится больше. Вобщем спасибо за
задание и извините за скудную документацию. Очень надеюсь увидится в ТГ.
..........／＞　 フ.....................
　　　　　| 　_　 _|
　 　　　／`ミ _x 彡  <3
　　 　 /　　　 　 |
　　　 /　 ヽ　　 ﾉ
　／￣|　　 |　|　|
　| (￣ヽ＿_ヽ_)_)
　＼二つ
Всего наилучшего.
----------------------------------------------------------------------------
