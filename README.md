Приложение User_Directory для регистрации пользователей: 
Проект представляет собой веб-приложение для управления списком пользователей (картотека). В приложении реализована функциональность для создания, редактирования, удаления и просмотра пользователей. 
Также предусмотрена регистрация и авторизация пользователей, управление правами доступа, деплой с использованием Docker, настройка веб-сервера, базы данных и обеспечение безопасности.
Настроен workflow в GitHub Actions, который автоматически запускается при каждом коммите в ветку main.

Инструкции по установке и запуску.
Этапы workflow:
сборка приложения,
проверка качества кода (с помощью flake8),
запуск автоматических тестов,
автоматическое развертывание приложения на сервере при успешном прохождении предыдущих этапов.
Реализация логирования в приложении: Внедрена система логирования с использованием модуля logging. Настроены различные уровни логирования (DEBUG, INFO, CRITICAL). 
Логи ошибок и критических событий сохраняются в app.log. Реализована ротация логов для предотвращения переполнения дискового пространства.

Описание используемых технологий и архитектуры:
