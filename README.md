# Выпускная работа бакалавра
Тема: **Разработка виртуальных кураторов, основанных на правилах, для интеллектуальных зданий**  
Образовательная программа: Программная инженерия  
ВУЗ: Национальный исследовательский университет «Высшая школа экономики»

Более подробную информацию можно найти в [презентации с защиты работы](docs/%D0%92%D0%9A%D0%A0%20%D0%A4%D0%BE%D0%BA%D0%B8%D0%BD%D0%B0%20(%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0).pdf).

## Назначение и функции программы
Программный продукт является прототипом и не может быть использован в качестве программного обеспечения для реального интеллектуального здания. Основное назначение системы – ее использование для изучения работы кураторов, основанных на правилах и проведения потенциального исследования.

Прототип автоматизированной системы управления зданием (АСУЗ) состоит из виртуальных кураторов трех типов, системы управления и генератора событий.

Куратор доступа используется для обработки событий, поступающих от системы контроля и управления доступом в здание. Куратор безопасности используется для обработки событий, связанных с пожарной безопасностью здания, и осуществления звонков специалистам и экстренным службам (ремонтнику, пожарным, охране). Куратор мониторинга ресурсов используется для обработки событий, поступающих от электроосветительных приборов.

Функциональным назначением системы управления является организация взаимодействия АСУЗ с пользователем, мониторинг событий и управление кураторами. Функциональным назначением генератора событий является имитация процессов в интеллектуальном здании и рассылка сигналов о событии.

## Используемые технологии
Язык программирования: Python   
Библиотеки: Experta для реализации системы, основанной на правилах, Flask для реализации REST API, Psycopg2 для доступа к базе данных, встроенный в Python модуль Socket для реализации socket-соединения.   

[Веб-клиент](curators-ui) реализован на ReactJS.  

Для развертывания используются Docker-контейнеры.

## Архитектура системы
Система состоит из нескольких компонентов: генератора событий, кураторов и системы управления. Каждый компонент является независимым приложением (программным агентом). Взаимодействие компонентов между собой осуществляется через socket-соединение. Каждый компонент системы имеет доступ к базе данных. Система управления предоставляет REST API, с которым пользователь может работать через веб-клиент.  

База данных необходима для реализации кооперации кураторов. При необходимости кооперации куратор-инициатор выбирает из базы данных куратора с необходимыми функциями, получает данные для связи с ним. По полученным данным инициатор отправляет куратору-помощнику запрос на выполнение необходимого действия.  

Все компоненты из-за схожести своей структуры и наличия общих модулей были реализованы в [одном проекте](src).   

Настройка системы происходит через конфигурационный файл. В том числе в случае запуска куратора его тип определяется файлом конфигурации. Для удобства тип также может быть переопределен через переменную, передаваемую при запуске приложения.

# Bachelor's final project
Topic: **Designing rule-based virtual curators for smart buildings**  
Educational Program: Software Engineering  
University: National Research University Higher School of Economics

More information can be found in [presentation from the defense of the paper](docs/%D0%92%D0%D0%9A%D0%A0%20%D0%A4%D0%BE%D0%BA%D0%B8%D0%BD%D0%B0%20(%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0).pdf).

## Purpose and functions of the program
The software product is a prototype and cannot be used as software for a real smart building. The main purpose of the system is to use it to study rule-based curators and conduct potential research.

The prototype building management system (BMS) consists of three types of virtual curators, a control system and an event generator.

The access curator is used to process events from the building access control and management system. Security curator is used to process events related to fire safety of the building and to make calls to specialists and emergency services (repairman, firemen, security). Resource monitoring curator is used to process events coming from electric lighting devices.

The functional purpose of the control system is organization of interaction between the BMS and the user, event monitoring and curator management. The functional purpose of the event generator is to simulate processes in the intelligent building and send out event signals.

## Technologies used
Programming language: Python   
Libraries: Experta for implementing rule-based system, Flask for implementing REST API, Psycopg2 for database access, Python built-in Socket module for implementing socket connection.   

The [web client](curators-ui) is implemented in ReactJS.  

Docker containers are used for deployment.

## System Design
The system consists of several components: an event generator, curators, and a management system. Each component is an independent application (software agent). The components interact with each other through a socket connection. Each component of the system has access to the database. The control system provides a REST API, with which the user can work through a web client.  

The database is necessary to implement curator cooperation. When cooperation is necessary, the initiator-curator selects a curator with the necessary functions from the database, receives data for communication with him. According to the received data, the initiator sends a request to the curator-helper to perform the necessary action.  

All components due to the similarity of their structure and the presence of common modules were realized in [one project](src).   

The system is configured via a configuration file. Including in the case of running a curator, its type is determined by the configuration file. For convenience, the type can also be overridden through a variable passed at application startup.