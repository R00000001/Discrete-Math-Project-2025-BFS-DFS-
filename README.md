# Discrete Math Project (BFS&DFS) 

## Загальний огляд
Цей проект досліджує реалізацію та аналіз алгоритмів алгоритмів Breadth-First Search (BFS) та Depth-First Search (DFS) для побудови матриць досяжності у неорієнтованих графах. У дослідженні оцінюється вплив представлення графа на продуктивність цих алгоритмівалгоритмів на різних розмірах та щільності графів.

## Алгоритми
+ BFS (Breadth-First Search): Алгоритм обходу або пошуку деревовидних або графових структур даних, який починається з кореневого вузла і досліджує всі сусідні вузли на поточній глибині, перш ніж перейти до вузлів на наступному рівні глибини.
+ DFS (Depth-First Search): Алгоритм обходу або пошуку деревовидних або графових структур даних шляхом дослідження якомога далі вздовж кожної гілки, перш ніж повернутися назад.

## Умови тестувань
Тестування проводились на графах з вершинами від 20 до 200 і з щільністю від 15 до 95. Для кожного випадку проводилось 100 ітерацій, де для кожної ітерації створювався новий псевдо рандомний граф.

## Структура проєкту
+ ``` Program.py ``` : Створює рандомні графи, тестує алгоритми і заміряє час. Всю вихідні дані зберігає в файлі ```results.tsv```.
+ ``` Visual.py ``` : Візуалізує дані з таблиці ``` results.tsv ``` і створює графіки.
+ ``` results.tsv ``` : Таблиця вихідних даних після тестувань.

## Залежності
+ tqdm
+ pandas
+ matplotlib
+ seaborn

## Результати
Результати представлені у формі графіків, а також більш детально у таблиці ```results.tsv```. Додаткова інформація є в представленому звіті.

## Виконували
Руслан - візіонер, вайб-кодер, теоретична частина роботи. 
Даніель - перевірка коду, оптимізація, створення звіту.
Денис - Оптимізація, створення звіту. 

