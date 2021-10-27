import random
from datetime import datetime

from django.db.utils import IntegrityError

from slaves.models import *


def female_surname(surname):
    if 'ий' in surname[-5:]:
        return surname.replace("ий", "ая")
    elif 'ый' in surname[-5:]:
        return surname.replace("ый", "ая")
    elif surname[-1] in ('н', 'в'):
        return surname + "a"
    elif 'ой' in surname[-5:]:
        return surname.replace("ой", "ая")
    return surname


NAMES = {
    'm': [
        'Тейс', 'Аврам', 'Ицхак', 'Бенни', 'Яков', 'Изя', 'Шломи', 'Абрам', 'Адам', 'Иисус', 'Исаак', 'Иуда', 'Джо',
        'Давид', 'Ефрем', 'Мойша', 'Моисей', 'Натаниель', 'Ной', 'Савва', 'Симон', 'Шимон', 'Шалом', 'Исаак', 'Меир',
        'Стен', 'Майк', 'Ник', 'Стивен', 'Джон', 'Джейк', 'Кристофер', 'Бэйн', 'Такеши', 'Эдвард', 'Альберт', 'Кайл',
        'Зельман', 'Ефрем', 'Израиль', 'Леви', 'Самуил', 'Соломон', 'Суслейман', 'Гефест', 'Посейдон', 'Господин',
        'Мистер', 'Мистер', 'Повелитель', 'Уважаемый', 'Господин', 'Магистр', 'Рядовой', 'Смотрящий', 'Мастер', 'Отец',
    ],
    'f': [
        'Авель', 'Анна', 'Арье', 'Дебора', 'Елизавета', 'Захария', 'Иоганесс', 'Магдалина', 'Мария', 'Ирида', 'Диона',
        'Реввека', 'Сабирель', 'Тамара', 'Тейс', 'Эдна', 'Яни', 'Аврора', 'Агата', 'Алетея', 'Арга', 'Артимида', 'Ата',
        'Афина', 'Афродита', 'Гармония', 'Гера', 'Гея', 'Гемера', 'Гибрис', 'Госпожа', 'Ноа', 'Дина', 'Светская Львица',
        'Кирка', 'Лисса', 'Мания', 'Мгла', 'Муза', 'Немезида', 'Ника', 'Психея', 'Талия', 'Хлорида', 'Эос', 'Эрида',
        'Госпожа', 'Миссис', 'Мисс', 'Хозяйка', 'Дева', 'Вдова', 'Служанка', 'Старая', 'Мать', 'Царица', 'Кето', 'Ора',

    ],
    'h': [],
}
ANOTHER_NAME = []

SURNAMES = [
    'Шумейко', 'Андрусейко', 'Батейко', 'Пилипейко', 'Семочко', 'Толочко', 'Марочко', 'Сирко', 'Забужко', 'Бутко',
    'Цушко', 'Кличко', 'Сасько', 'Андрейко', 'Решетько', 'Выговский', 'Вальковский', 'Котовский', 'Петровский',
    'Корчевний', 'Масловский', 'Барановский', 'Яворивский', 'Трублаевский', 'Алчевский', 'Миклашевский',
    'Гриневский', 'Гребневский', 'Шуфрич', 'Зварыч', 'Андрухович', 'Шлюхевич', 'Токар', 'Кобзар', 'Житар', 'Рымар',
    'Гончар', 'Шугаев', 'Паньков', 'Шинкарёв', 'Драгоманов', 'Костомаров', 'Турчинов', 'Многогрешный', 'Мирный',
    'Правый', 'Лысый', 'Карпенко-Карый', 'Навальный', 'Белый', 'Яловой', 'Яровой', 'Лановой', 'Горевой', 'Воловой',
    'Щербак', 'Хижняк', 'Коровяк', 'Худобяк', 'Чумак', 'Спивак', 'Грабчак', 'Кравчук', 'Корнейчук', 'Гайчук',
    'Горобчук', 'Ковальчук', 'Басюга', 'Бельмега', 'Булига', 'Вервега', 'Верига', 'Генега', 'Голунга', 'Деренюга',
    'Длябога', 'Досига', 'Карнага', 'Ломага', 'Мадрига', 'Нагога', 'Недвига', 'Некига', 'Рига', 'Сапига', 'Смага',
    'Сопуга', 'Хоруга', 'Чепига', 'Чернега', 'Андриятин', 'Бабин', 'Вдовчин', 'Вольвин', 'Вохмин', 'Вульчин',
    'Глюздин', 'Губчин', 'Гуйтин', 'Гутин', 'Досин', 'Дутчин', 'Калин', 'Кобрин', 'Коляджин', 'Кузьмин', 'Кустрин',
    'Лецин', 'Литвин', 'Луцин', 'Лучин', 'Люсин', 'Малетин', 'Марусин', 'Микитин', 'Миклин', 'Микулин', 'Мойсин',
    'Овчарчин', 'Олексин', 'Ровенчин', 'Родчин', 'Савчин', 'Сикорин', 'Татарин', 'Томин', 'Турчин', 'Усин',
    'Федемин', 'Хомин', 'Цинурчин', 'Челядин', 'Чигрин', 'Штогрин', 'Шулепин', 'Шеманин', 'Бандурка', 'Бирка',
    'Голубка', 'Грушка', 'Жилка', 'Здерка', 'Кавка', 'Ключка', 'Костка', 'Криска', 'Крупка', 'Медулька',
    'Мишоловка', 'Муринка', 'Падалка', 'Плесканка', 'Фигурка', 'Цибулька', 'Цяпка', 'Шлихутка', 'Новопика',
    'Андрух', 'Дидух', 'Балабух', 'Вантух', 'Ветух', 'Гладух', 'Гречух', 'Карпух', 'Китнюх', 'Ковтюх', 'Кутельмах',
    'Куцах', 'Мелюх', 'Пинах', 'Стельмах', 'Шатух', 'Бабок', 'Бобок', 'Божок', 'Волчок/Вовчок', 'Гнаток', 'Жданок',
    'Жолток', 'Зубок', 'Пожиток', 'Попок', 'Снопок', 'Титок', 'Турок', 'Циганок', 'Шашок', 'Шрубок',
    'Животок', 'Хлистун', 'Гарун', 'Мазун', 'Вередун', 'Балакун', 'Кордун', 'Вергун', 'Трясун', 'Прядун',
    'Абрамович', 'Авнет', 'Азив', 'Айверовский', 'Айзенштат', 'Айн', 'Алкен', 'Алтер', 'Альперн', 'Альтер', 'Ануш',
    'Аперья', 'Арест', 'Арий', 'Атлас', 'Аугман', 'Ахершинский', 'Бабич', 'Бальшон', 'онжеДобрицкий', 'Бараш',
    'Бараюкова', 'Бароновицкий', 'Барш', 'Бас', 'Бегельфер', 'Бедер', 'Бекер', 'Белостоцкий', 'Берлин', 'Берлинский',
    'Берштейн', 'Бибер', 'Бламенфельд', 'Бланкштейн', 'Блонский', 'Блюштейн', 'Бобес', 'Бобривицкий', 'Богуславяк',
    'Бойдан', 'Бомхиль', 'Борд', 'Боренштейн', 'Бортновский', 'Борштейн', 'Борщевский', 'Ботхиль', 'Боцковский',
    'Бочковский', 'Боярский', 'Бренер', 'Брик', 'Брискер', 'Брозовский', 'Бройде', 'Брудный', 'Бублицкий', 'Буриский',
    'Бурыш', 'Бялодворский', 'Бялостокский', 'Вайнилис', 'Вайнтруб', 'Вайншель', 'Вайнштейн', 'Вайскопф', 'Вапнярх',
    'Варак', 'Васильковский', 'Вейндпейх', 'Вейнрах', 'Вейнрей', 'Виненберг', 'Виногрод', 'Висок', 'Вогель', 'Водкле',
    'Воле', 'Волковыский', 'Вольчик', 'Волянский', 'Высокевич', 'Высоцкий', 'Габель', 'Галанский', 'Галубник',
    'Галынский', 'Гальперн', 'Гарбер', 'Гаргонский', 'Геверц', 'Геер', 'Гель', 'Гельбард', 'Гельбарт', 'Герб',
    'Гертман', 'Герц', 'Гершберг', 'Гершкович', 'Гилиот', 'Гирш', 'Глоговский', 'Глуташевич', 'Головоский', 'Голубник',
    'Гольберг', 'Гольд', 'Гольдберг', 'Гольден', 'Гольдман', 'Гольдфарб', 'Гольдфард', 'Гольдштейн', 'Гольштейн',
    'Гонсиоров', 'Гониондзский', 'Горбатый', 'Горфейн', 'Грабликовский', 'Гравицкий', 'Грачук', 'Гринберг', 'Гриншпан',
    'Гристовский', 'Гришпан', 'Гробман', 'Грон', 'Гроховский', 'Губбер', 'Гурвиц', 'Гурвич', 'Гусяцкий', 'Гутман',
    'Давидсон', 'Дворкович', 'Дворхец', 'Дейн', 'Дембник', 'Десятник', 'Диогот', 'Дискин', 'Доброневский',
    'Долыбовский', 'Дразнин', 'Драчинский', 'Дренцион', 'Едепштейн', 'Елень', 'Ерневский', 'Жагер', 'Жебин', 'Желязо',
    'Заблудовский', 'Завадский', 'Завольский', 'Зайвель', 'Зайфельд', 'Закин', 'Заренский', 'Здановский', 'Зейлицкий',
    'Зельдович', 'Зигман', 'Зильбердик', 'Зильберман', 'Зильберт', 'Зильберфарб', 'Зильберфенш', 'Зильберштейн',
    'Зильберштрам', 'Зитерман', 'Зубач', 'Зубич', 'Зубовский', 'Зумен', 'Изак', 'Илиард', 'Иосем', 'Исеруг',
    'Кавалерийский', 'Каган', 'КаганонжеРапопорт', 'Кан', 'Кантер', 'Кантор', 'Канцепольский', 'Капица', 'Каплан',
    'Капуста', 'Карелишко', 'Карчак', 'Катц', 'Кац', 'Кацин', 'Кацын', 'Кивенский', 'Кирзнер', 'Киршенбаум', 'Клейн',
    'Клюк', 'Книженик', 'Ковадло', 'Колодник', 'Копляндский', 'Коруж', 'Корчинский', 'Корыцкий', 'Косой',
    'Кот-Городецкий', 'Котлер', 'Котляр', 'Кравец', 'Кравник', 'Крейнген', 'Крутак', 'Крынский', 'Кудес', 'Кузнецкий',
    'Купеш', 'Куприц', 'Курлядский', 'Курлянда', 'Куропатова', 'Курцбарт', 'Курцгорц', 'Кусель', 'Кучковский', 'Кушнер',
    'Лабзовский', 'Ланде', 'Ластовский', 'Лащинский', 'Лебедь', 'Лев', 'Левин', 'Левинский', 'Лейбова', 'Лекахмахер',
    'Летес', 'Лешес', 'Ликер', 'Лип', 'Лис', 'Литштейн', 'Лондон', 'Лошович', 'Лунанский', 'Лунский', 'Лучанский',
    'Любовский', 'Магазинер', 'Маерович', 'Мазен', 'Мазовецкий', 'Мазур', 'Мазы', 'Майзлер', 'Макаль', 'Малах', 'Малик',
    'Малкин', 'Малковский', 'Мальцберг', 'Ман', 'Маневич', 'Маньковский', 'Маранц', 'Марковский', 'Маркус', 'Маровец',
    'Марчиканский', 'Махай(Макай)', 'Медведь', 'Медовник', 'Мелер', 'Меликовский', 'Менакер', 'Миллер', 'Мильнер',
    'Миневич', 'Миткинд', 'Митковский', 'Михелиович', 'Мовшович', 'Монкер', 'Монцик', 'Мостовский', 'Мулер', 'Муляр',
    'Намистович', 'Наревский', 'Начевник', 'Неведомский', 'Немон', 'Ненендик', 'Нетужский', 'Новир', 'Носович', 'Овец',
    'Огульник', 'Опарт', 'Орлинский', 'Орман', 'Остреблянский', 'Паситковский', 'Пахтер', 'Пейсахович', 'Пекарь',
    'Пенионжек', 'Перельштейн', 'Перлес', 'Перльман', 'Перльмутер', 'Перц', 'Пилатовский', 'Пинес', 'Пинский',
    'Пинтыль', 'Пискор', 'Подаминский', 'Подомский', 'Подоровский', 'Поляк', 'Помер', 'Померанц', 'Пренский',
    'Прилинский', 'Примеска', 'Прушак', 'Пурка', 'Пытковский', 'Пьянушек', 'Рабинович', 'Работник', 'Радотник',
    'Райнес', 'Раковин', 'Рап', 'Рапопорт', 'Раташкин', 'Ратовецкий', 'Рафаловский', 'Рахштайн', 'Раш', 'Рейбарт',
    'Рендель', 'Рибак', 'Роженский', 'Розенбаум', 'Розенберг', 'Розенблей', 'Розенгейм', 'Рокела', 'Ропес', 'Рохман',
    'Рубинштейн', 'Рудберт', 'Руденский', 'Рудник', 'Рудый', 'Ружанский', 'Русанов', 'Рущук', 'Рынский', 'Сандлер',
    'Саперштейн', 'Сапочковский', 'Сарапник', 'Сарвер', 'Сегал', 'Семятицкий', 'Серачек', 'Серыский', 'Сета',
    'Сибирский', 'Сидлецкий', 'Силовский', 'Симбирский', 'Симятинский', 'Сирота', 'Сич', 'Сладкий', 'Слепак',
    'Смолянский', 'Собель', 'Соболь', 'Соголович', 'Сокол', 'Соколовер', 'Сокольник', 'Соломон', 'Ставер', 'Столь',
    'Суд', 'Сульхес', 'Суляк', 'Суш', 'Сушельский', 'Тевег', 'Тиктин(Тыктин)', 'Токарь', 'Толкоцкий', 'Топорович',
    'Троицкий', 'Трон', 'Тхорицкий', 'Тыкоцкий', 'Тыктин', 'Тыктин', 'ФайнбергонжеФиксель', 'Фарбер', 'Фейдман',
    'Фишбейн', 'Фишер', 'Флейшер', 'Фонер', 'Франк', 'Фридлянский', 'Фридман', 'Фрусловский', 'Фрядлес', 'Фуковский',
    'Хабольский(Хаболевский)', 'Хазан', 'Хазанович', 'Хазацкий', 'Хацкелевич', 'Хацкель', 'Хведюк', 'Хинский',
    'Хмельницкий', 'Холмецкий', 'Хонен', 'Цвейбах', 'Цикаловский', 'Циперман', 'Цицович', 'Цукерман', 'Цыбанский',
    'Цыбулькин', 'Цымерман', 'Чапник', 'Чачкий', 'Черняк', 'Чертик', 'Чесляр', 'Чеховский', 'Чехоцкий', 'Чижевский',
    'Шаймес', 'Шапиро', 'Шастер', 'Шафир', 'Шацкий', 'Швабский', 'Швайк', 'Шварц', 'Шепшелевич', 'Шиндер', 'Шинкар',
    'Шкляр', 'Шклярский', 'Школьник', 'Шкоп', 'Шкурник', 'Шлигельский', 'Шмулевич', 'Штабинский', 'Штеренштейн',
    'Шуляк', 'Шус', 'Шустер', 'Щербин', 'Эдельштейн', 'Эйн', 'Экштейн', 'Элен', 'Эльштейн', 'Эпштейн', 'Эфрон',
    'Юденский', 'Юдкес', 'Юдкис', 'Явин', 'Яворовский', 'Янглиб', 'Яновский', 'Ярхомбек', 'Ясеновский', 'Яффе', 'Яхац',
    'Душнила', 'Скучный', 'Бедный', 'Весёлый', 'Озорной', 'Бешенный', 'Дикий', 'Лютый', 'Суета', 'Левый', 'Опасный',
    'Лапочка', 'Папик', 'Солёный', 'Холёный', 'Безработный', 'Грозный', 'Правый', 'Больной', 'Лесной', 'Плешивый',
    'Неверный', 'Задумчивый', 'Бесполезный', 'Усердный', 'Мытый', 'Бритый', 'Лохматый', 'Чёрный', 'Копчёный', 'Верный',
    'Большой', 'Старший', 'Младший', 'Бледный', 'Злой', 'Великолепный', 'Невероятный', 'Неуловимый', 'Копчёный', 'Ух',

]

SURNAMES_G = {
    'm': SURNAMES,
    'f': [female_surname(name) for name in SURNAMES],
    'h': [],
}
ANOTHER_SURNAMES = []

HARD_SKILS = ['Actor.js', 'Gold.js', 'Painting.js', 'Advertisement.js', 'Grass.js', 'Parrot.js', 'Afternoon.js',
              'Greece.js', 'Pencil.js', 'Airport.js', 'Guitar.js', 'Piano.js', 'Ambulance.js', 'Hair.js', 'Pillow.js',
              'Animal.js', 'Hamburger.js', 'Pizza.js', 'Answer.js', 'Helicopter.js', 'Planet.js', 'Apple.js',
              'Helmet.js', 'Plastic.js', 'Army.js', 'Holiday.js', 'Portugal.js', 'Australia.js', 'Honey.js',
              'Potato.js', 'Balloon.js', 'Horse.js', 'Queen.js', 'Banana.js', 'Hospital.js', 'Quill.js', 'Battery.js',
              'House.js', 'Rain.js', 'Beach.js', 'Hydrogen.js', 'Rainbow.js', 'Beard.js', 'Ice.js', 'Raincoat.js',
              'Bed.js', 'Insect.js', 'Refrigerator.js', 'Belgium.js', 'Insurance.js', 'Restaurant.js', 'Boy.js',
              'Iron.js', 'River.js', 'Branch.js', 'Island.js', 'Rocket.js', 'Breakfast.js', 'Jackal.js', 'Room.js',
              'Brother.js', 'Jelly.js', 'Rose.js', 'Camera.js', 'Jewellery.js', 'Russia.js', 'Candle.js', 'Jordan.js',
              'Sandwich.js', 'Car.js', 'Juice.js', 'School.js', 'Caravan.js', 'Kangaroo.js', 'Scooter.js', 'Carpet.js',
              'King.js', 'Shampoo.js', 'Cartoon.js', 'Kitchen.js', 'Shoe.js', 'China.js', 'Kite.js', 'Soccer.js',
              'Church.js', 'Knife.js', 'Spoon.js', 'Crayon.js', 'Lamp.js', 'Stone.js', 'Crowd.js', 'Lawyer.js',
              'Sugar.js', 'Daughter.js', 'Leather.js', 'Sweden.js', 'Death.js', 'Library.js', 'Teacher.js',
              'Denmark.js', 'Lighter.js', 'Telephone.js', 'Diamond.js', 'Lion.js', 'Television.js', 'Dinner.js',
              'Lizard.js', 'Tent.js', 'Disease.js', 'Lock.js', 'Thailand.js', 'Doctor.js', 'London.js', 'Tomato.js',
              'Dog.js', 'Lunch.js', 'Toothbrush.js', 'Dream.js', 'Machine.js', 'Traffic.js', 'Dress.js', 'Magazine.js',
              'Train.js', 'Easter.js', 'Magician.js', 'Truck.js', 'Egg.js', 'Manchester.js', 'Uganda.js', 'Eggplant.js',
              'Market.js', 'Umbrella.js', 'Egypt.js', 'Match.js', 'Van.js', 'Elephant.js', 'Microphone.js', 'Vase.js',
              'Energy.js', 'Monkey.js', 'Vegetable.js', 'Engine.js', 'Morning.js', 'Vulture.js', 'England.js',
              'Motorcycle.js', 'Wall.js', 'Evening.js', 'Nail.js', 'Whale.js', 'Eye.js', 'Napkin.js', 'Window.js',
              'Family.js', 'Needle.js', 'Wire.js', 'Finland.js', 'Nest.js', 'Xylophone.js', 'Fish.js', 'Nigeria.js',
              'Yacht.js', 'Flag.js', 'Night.js', 'Yak.js', 'Flower.js', 'Notebook.js', 'Zebra.js', 'Football.js',
              'Ocean.js', 'Zoo.js', 'Forest.js', 'Oil.js', 'Garden.js', 'Fountain.js', 'Orange.js', 'Gas.js',
              'France.js', 'Oxygen.js', 'Girl.js', 'Furniture.js', 'Oyster.js', 'Glass.js', 'Garage.js', 'Ghost.js',
              'Android', 'Java', 'Kotlin', 'iOS', 'Objective', 'C', 'Swift', 'Cross', 'Platform', 'React', 'Native',
              'Flutter', 'Ionic', 'Cordova', 'JavaScript', 'Express', 'Ruby', 'Rails', 'Sinatra', 'Java', 'Play',
              'Framework', 'PHP', 'Larvel', 'Python', 'Django', 'Flask', 'Scala', 'Elixir', 'Phoenix', 'Relational',
              'Databases', 'MySQL', 'Postgres', 'SQLite', 'NoSQL', 'Mongo', 'Cassandra', 'Key-value', 'stores', 'Redis',
              'Graph', 'Databases', 'Emerging', 'Neo4J', 'ReactJS', 'VueJS', 'Web', 'Components', 'AngularJS', 'Amazon',
              'AWS', 'Google', 'Firebase', 'Microsoft', 'Azure', 'Docker', 'Kubernetes']

GENDER_H = {
    "m": (150, 230),
    "f": (140, 200),
}

GENDER_W = {
    "m": (60, 200),
    "f": (35, 100),
}


class PerGen:

    def __init__(self, length):
        self.len = length
        self.generate_hard_skills()
        self.stack = HardSkill.objects.all()

    def gen_time(self, max_val):
        return random.randint(1, max_val)

    def generate(self, id):
        gender = random.choice(('m', 'f'))
        age = random.randint(16, 55)
        birthday = (
            datetime.now().year - age, self.gen_time(12), self.gen_time(28), self.gen_time(23), self.gen_time(59),
            self.gen_time(59), 349305)
        return {
            'id': id,
            'name': random.choice(NAMES.get(gender, ANOTHER_NAME)),
            'sur_name': random.choice(SURNAMES_G.get(gender, ANOTHER_SURNAMES)),
            'age': age,
            'gender': gender,
            'experience': random.randint(0, age - 16),
            'birthday': datetime(*birthday),
            'height': random.randint(*GENDER_H[gender]),
            'weight': random.randint(*GENDER_W[gender]),
        }

    def person_generator(self):
        for p in range(1, self.len + 1):
            data = self.generate(p)
            yield data

    def generate_hard_skills(self):
        for skill in HARD_SKILS:
            try:
                hs = HardSkill(title=skill)
                hs.save()
            except:
                pass

    def get_skills(self, max_val=1):
        return {random.choice(self.stack) for _ in range(random.randint(0, max_val + 1))}

    def run(self):
        person = self.person_generator()

        infoset = []

        manager_len = self.len // 15

        for p in person:
            # w = Worker({'title': f"{p['sur_name']} {p['name']}", 'info': UserInfo(**p)})
            infoset.append(UserInfo(**p))

        for i in infoset[:manager_len]:
            try:
                i.save()
                i.hard_skills.add(*self.get_skills(int(i.experience)))
                i.save()
                w = Manager(title=f'{i.name} {i.sur_name}', info=i)
                w.save()
            except IntegrityError:
                pass

        all_manager = Manager.objects.all()

        for i in infoset[manager_len:]:
            try:
                i.save()
                i.hard_skills.add(*self.get_skills())
                i.save()
                w = Worker(title=f'{i.name} {i.sur_name}', info=i, warden=random.choice(all_manager))
                w.save()
            except IntegrityError:
                pass

# gen = PerGen()
#
# for n in gen.person_generator(20):
#     print(n['name'], n['sur_name'])


# from person_generator import core
# from slaves.models import *
# person = PerGen().person_generator(100)
#
# infoset = []
#
# for p in person:
#     # w = Worker({'title': f"{p['sur_name']} {p['name']}", 'info': UserInfo(**p)})
#     infoset.append(UserInfo(**p))
# print(infoset)
#
# for i in infoset[:10]:
#     i.save()
#     w = Manager(title=f'{i.sur_name} {i.name}', info=i)
#     w.save()
#
# all_manager = Manager.objects.all()
#
# for i in infoset[10:]:
#     i.save()
#     w = Worker(title=f'{i.sur_name} {i.name}', info=i, warden=random.choice(all_manager))
#     w.save()
# from person_generator import core
# c = core.PerGen()
# c.run(1000)

# SwordMaster
# toor

#pip install djangorestframework coreapi pyyaml django-rest-swagger