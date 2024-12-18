# AircraftPositioning
### Проект по предмету Дифференциальные уравнения. Решение прямой задачи - подготовить исходные данные - сгенерировать траекторию, координаты, высоту и решение обратной задачи - наложить шум и восстановить исходные данные.
## Описание модели
Пусть самолет имеет координаты \((x, y, z)\), а \(i\)-я вышка имеет координаты $$\((x_i, y_i, z_i)\)$$. Пусть всего задано \(n > 3\) вышек, тогда существует 

$$
  C_n^2 = \frac{n(n-1)}{2} 
$$

способов выбрать любые две из них. Обозначим расстояние от самолета до \(i\)-й вышки как $$\(d_i\)$$, а расстояние до \(j\)-й вышки как $$\(d_j\)$$. Эти расстояния выражаются по формулам

$$
d_i = \sqrt{(x - x_i)^2 + (y - y_i)^2 + (z - z_i)^2},
$$

$$
d_j = \sqrt{(x - x_j)^2 + (y - y_j)^2 + (z - z_j)^2}.
$$

Определим функцию $$\(d_{ij}(x, y, z)\)$$ как разность расстояний между самолетом и вышками \(i\) и \(j\):

$$
d_{ij}(x, y, z) = |d_i - d_j| = \left| \sqrt{(x - x_i)^2 + (y - y_i)^2 + (z - z_i)^2} - \sqrt{(x - x_j)^2 + (y - y_j)^2 + (z - z_j)^2} \right|.
$$

С другой стороны, мы можем записать, что

$$
d_i = c t_i,
$$

где $$\(t_i\$$) — время, за которое сигнал доходит от самолета до \(i\)-й вышки. Тогда обозначим 

$$
d_{ij} = c |t_i - t_j| = c \Delta t_{ij},
$$

где \(c\) — скорость распространения сигнала (в нашем случае, скорость света), а $$\(\Delta t_{ij}\)$$ — разница времен прибытия сигнала (Time Difference of Arrival, TDOA). Эта информация известна, так как измеряется на вышках.

## Постановка задачи
Реализовать описанную модель с переопределённой системой, решаемой с помощью нелинейного МНК с встроенным фильтром Калмана,
определяющего параметры модели равноускоренного движения точки. Наблюдаемыми величинами в фильтре Калмана должны являться TDOA, а не положения точки.
## Решение
Первоочередно перейдем от TOA, к TDOA. Далее, ясно, что

$$
d_{ij}(x,y,z) = d_{ij} \Leftrightarrow f_{ij}(x,y,z) \equiv d_{ij}(x,y,z) - d_{ij} = 0,
$$

перебрав все возможные комбинации *i* и *j*, получим систему функций *f(x, y, z) = (f<sub>11</sub>, ..., f<sub>n(n-1)</sub>)*. Нетрудно догадаться, что задача состоит в поиске таких параметров *(x, y, z)*, что *f(x, y, z) = 0*. Построенная система уравнений является переопределенной. Она содержит всего 3 неизвестных, а вышек, как минимум 4, то есть минимум 6 уравнений. 

Передадим фильтру Калмана TDOA. Там сначала применим метод наименьших квадратов (МНК):
![telegram-cloud-photo-size-1-5267368898955699407-y](https://github.com/user-attachments/assets/547b6460-db20-41ce-9bca-9b9ab1bde1fa)
Будем искать такие решения, которые будут минимизировать написанную сумму, для этого применим алгоритм Гаусса-Ньютона, обозначив за *x* вектор решения, получим:

$$
x^{(k+1)} = x^{(k)} - (J_f^TJ_f)^{-1}J_f^T \cdot x^{(k)},
$$

где *J<sub>f<sub>* - матрица Якоби для системы *f*. А произведение матриц в вычитаемом есть псевдообратная матрица к матрице Якоби, которую можно вычислить с помощью QR разложения.

Далее начинается работа фильтра Калмана, в которой два этапа: предсказание и корректировка.

### Предсказание состоит из:
1. Предсказания нового состояния системы
x<sub>k</sub> = F x<sub>k-1</sub>
2. Предсказания ошибки ковариации
P<sub>k</sub> = F P<sub>k-1</sub> F<sup>T</sup>
где $x_k$ - вектор состояния, $F$ - матрица эволюции(динамическая модель системы), $P_k$ - ковариационная матрица состояния.

### Этап корректорировки состоит из:
1. Вычисление Kalman Gain\
S = H P<sub>k</sub> H<sup>T</sup> + R\
K<sub>k</sub> = P<sub>k</sub> H<sup>T</sup> S<sup>-1</sup>
2. Корректировки вектора состояния с учетом пересчета ошибки с только что поданным TDOA\
x<sub>k</sub> = x<sub>k</sub> + K<sub>k</sub> z<sub>k</sub>
3. Обновление ошибки ковариации
P<sub>k</sub> = (I - K<sub>k</sub> H) P<sub>k</sub>
где $K_k$ - Kalman Gain, $H$ - матрица, отображающая отношение измерений и состояний, $R$ - ковариационная матрица шума, $z_k$ - пересчитанная ошибка с учетом только что поданных TDOA, $I$ - единичная матрица 
