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
    'Пенионжек', 'Перельштейн', 'Перлес', 'Перльман', 'Перльмутер', 'Перц', 'Пилатовский', 'Пинус', 'Писинский',
    'Писинов', 'Пискор', 'Подаминский', 'Подомский', 'Подоровский', 'Поляк', 'Помер', 'Померанц', 'Пренский',
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


def with_prob(prob):
    prob = 100 if prob > 100 else prob
    prob = 0 if prob < 0 else prob
    true = [True for i in range(prob)]
    false = [False for i in range(100 - prob)]
    pull = true + false
    return random.choice(pull)


class ProbableList(list):
    def __init__(self, *args, prob=100, **kwargs):
        super().__init__(*args, prob=100, **kwargs)
        self.prob = prob

    def get(self):
        if with_prob(self.prob):
            return random.choice(self)
        return ''


skill_deck = {
    "who": {
        "item": ProbableList([
            "разработчик", "уборщик", "хирург", "врач", "чистильщик",
            "певец", "танцор", "диджей", "миксер", "преподаватель",
            "учитель", "пловец", "учёный", "студент", "бездельник", "профессор",
            "оккультист", "снайпер", "метеоролог", "утилизатор", "ловец", "философ",
            "писатель", "хранитель", "охранник", "раб", "слуга", "последователь",
            "осквернитель", "критик", "искатель", "фанат", "ненавистник",
            "покоритель", "защитник", "изобретатель", "менеджер", "игрок",
            "владелец", "хозяин", "уничтожитель", "преследователь",
            "представитель", "дизайнер",
        ], prob=100),
        "item_obj": ProbableList([
            "секретных технологий", "неизвестных наук", "древних секретов",
            "легенд", "дальнего космоса", "сомнительных практик", "тайн",
            "интриг", "программного обеспечения", "непрограммного обеспечения",
            "продовольственного обеспечения", "законов", "правил", "проблем",
            "поводов для конфликтов на случайную тему", "игр", "мусора и хлама",
            "свалки", "всякого разного", "математических наук", "неизвестного языка",
            "немецкого языка", "мёртвых", "собственной самооценки", "всего",
        ], prob=50),
        "item_supp": ProbableList([
            "бешенного разряда", "без рук", "из головы", "физики", "без повода",
            "практически задаром", "по супер-цене", "для слепых", "для глухих",
            "для мёртвых", "для богатых", "для бедных", "для самоудовлетворения",
            "для поднятия самооценки", "во имя Сатаны", "потому что мама заставила",
            "и всего остального", "и всего сущего", "по-приколу",
        ], prob=30),
    },
    "which": {  # инициативный (100); доп: на сто процентов (20);
        "item": ProbableList([
            "инициативность", "коммуникация", "критическое мышление", "сервисность", "Клиентоориентированность",
            "Управление проектами", "Управление людьми", "Управление собой", "Наставничество", "менторинг",
            "Принятие решений", "Эмоциональность", "Ненасильственное общение", "насильственное общение",
            "Управление знаниями", "Работа в режиме неопределенности", "Решение проблем", "Стрессоустойчивость",
            "Бережливое производство", "Экологическое мышление", "Самоанализ", "саморефлексия", "рефлексия",
            "Грамотная письменная и устная речь", "Упорство", "Стрессоустойчивость", "Хорошая память",
            "безынициативность", "Умение выступать на публике", "Гибкость", "принятие критики", "непринятие критики",
            "плохая память", "Обучаемость", "не обучаемость", "Креативность", "Ориентированность на результат",
            "Готовность выполнять рутинную работу", "Ответственность", "Умение разрешать конфликты", "уверенность",
            "неумение разрешать конфликты", "платёжеспособность", "Аналитический склад ума",
            "не эмоциональность", "неплатёжеспособность", "противоречивость", "Аналитический склад ума",

        ], prob=100),
        "item_obj": ProbableList([], prob=0),
        "item_supp": ProbableList([
            "на сто процентов", "как у скалы", "в стиле ниндзя", "как у барана",
            "как у табурета", "это точно", "максимальный уровень", "как и у всех",
            "или типа того", ", ну вы поняли", "если вы понимаете о чём я", "наоборот",
            "только наоборот", "то есть нет", "наверное", "в особых ситуациях",
            "по пятницам", "по понедельникам",
        ], prob=40),
    },
    "what": {  # готовка (100); какая: профессиональная (40); доп: в лучших традициях дикого запада (20);
        "item_obj": ProbableList([
            "готовка", "рыбалка", "охота", "игра на гитаре", "игра на барабанах", "игра на нервах",
            "игра на чём угодно", "астрономия", "Генеалогия", "Религия", "Хиромантия", "Некромантия",
            "игра в футбол", "игра в кальмара", "лепка", "помощь", "Работа с деревом",
            "Работа на дядю", "Гребля", "Реставрация", "Работа с металлом", "психологическая помощь",
            "Стрельба по мишеням", "Качалка", "Резка по дереву", "Работа с кожей", "Фотография",
            "Стрельба из лука", "Стрельба по подвижным мишеням", "Обжарка кофе",
            "Аквариумистика", "Сборка моделей", "Склейка моделей", "Езда на мотоцикле",
            "Езда на чём угодно", "Езда", "Сдача металлолома", "Сдача соседей прокуратуре", "Работа по дому",
            "Токсидермия", "Хирургия", "Наркомания", "работорговля", "торговля", "уборка",
        ], prob=100),
        "item": ProbableList([
            "профессиональная", "спонтанная", "непрофессиональная", "быстрая",
            "хаотичная", "прицельная", "медленная", "экстремальная",
            "рискованная", "агрессивная", "священная", "выгодная",
            "обычная", "стандартная", "традиционная", "нетрадиционная",
            "принципиальная", "пьяная", "нетрезвая",
        ], prob=50),
        "item_supp": ProbableList([
            "в лучших традициях дикого запада", "по общепринятой методике",
            "по одному мне ведомой технологии", "в стиле американских школьников",
            "на выживание", "во имя науки", "с завязанными глазами", "в кромешной тьме",
            "ради веселья", "в лучших традициях арабских стран", "под присмотром моего деда",
            "без какой-либо цели", "у всех на глазах", "в общественных местах",
            "и всё что с этим связано", "если вы понимаете о чём я",
        ], prob=30),
    },
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
            # 'id': id,
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
                i.hard_skills.add(*self.get_skills(int(i.experience)))
                i.save()
                w = Worker(title=f'{i.name} {i.sur_name}', info=i, warden=random.choice(all_manager))
                w.save()
            except IntegrityError:
                pass


class SoftSkills:
    """
    from person_generator.core import SoftSkills
    from slaves.models import UserInfo
    p = UserInfo.objects.first()
    s= SoftSkills()
    s.create_soft_skills(5,p)
    """
    skill_types = ("who", "which", "what")

    def generate_skill(self, skill_parts):
        item = skill_parts['item'].get()
        item_obj = skill_parts['item_obj'].get()
        item_supp = skill_parts['item_supp'].get()
        return " ".join([i for i in (item, item_obj, item_supp) if i]).capitalize()

    def soft_skill_generator(self, count: int) -> set:
        skills = []
        for s in range(count):
            skill_type = random.choice(self.skill_types)
            skills.append(self.generate_skill(skill_deck[skill_type]))
        return set(skills)

    def create_soft_skills(self, count, person: UserInfo):
        skill_pull = self.soft_skill_generator(count)
        skill_set = [SoftSkill(title=i) for i in skill_pull]
        for s in skill_set:
            try:
                s.save()
                person.soft_skills.add(s)
            except:
                pass
        person.save()

    def run(self):
        users = UserInfo.objects.all()
        for user in users:
            count_of_skill = random.randint(0, 15)
            self.create_soft_skills(count_of_skill, user)
