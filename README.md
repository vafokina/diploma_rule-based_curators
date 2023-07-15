# Выпускная работа бакалавра
Тема: Разработка виртуальных кураторов, основанных на правилах, для интеллектуальных зданий  
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
