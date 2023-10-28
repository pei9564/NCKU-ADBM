
# 1. Database

`create database 資料庫名稱`
`show 資料庫名稱`	
`drop database 資料庫名稱`
`use 資料庫名稱`

# 2. Table

## 新增或刪除 Constraint
*CREATE 時 Constraint 寫在右方*
```
CREATE TABLE 資料表名稱 (
sid INTEGER PRIMARY KEY,
name CHAR(20) NOT NULL,
email VARCHAR(256) UNIQUE FOREIGN KEY REFERENCES Emails(email),
gpa REAL)

CHECK (gpa >= 0 AND gpa <= 4.0)
```
*CREATE 時 Constraint 寫在下方*

```
CREATE TABLE 資料表名稱 (
sid INTEGER,
name CHAR(20) NOT NULL,
email VARCHAR(256),
gpa REAL,

UNIQUE (email)
PRIMARY KEY (sid),
FOREIGN KEY (email) REFERENCES Emails(email)

CHECK (gpa >= 0 AND gpa <= 4.0)
)
```
## 變更 Constraint
```
ALTER TABLE Students
ADD FOREIGN KEY (sid) REFERENCES ClubMembers(mid);
```
```
ALTER TABLE Persons
DROP PRIMARY KEY;
```
## Constraints Over Multiple Relations

```
CREATE ASSERTION smallClub 
CHECK (
(SELECT COUNT (S.sid) FROM Sailors S)
+ (SELECT COUNT (B.bid) FROM Boats B) < 100 )
```

## Triger
:::    success
CREATE TRIGGER trigger_name 
trigger_action_time trigger_event ON table_name
[REFERENCING old_or_new_value_alias_list] 

triggered_action
:::

```
CREATE TRIGGER youngSailorUpdate 
AFTER INSERT ON SAILORS
REFERENCING NEW TABLE NewSailors 

FOR EACH STATEMENT
INSERT
    INTO YoungSailors(sid, name, age, rating) 
    SELECT sid, name, age, rating
    FROM NewSailors N
    WHERE N.age <= 18
```


## Foreign key設定
*FOREIGN KEY 的 Constraints 設定*
* NO ACTION：存在關聯紀錄時，禁止父資料表刪除或修改
* CASCADE：關聯紀錄會連動刪除或修改
* SET NULL / SET DEFAULT：關聯紀錄會設定成NULL或defualt

```
CREATE TABLE Students 
(sid CHAR(20),
grade CHAR(2), 

PRIMARY KEY (sid), 
FOREIGN KEY (sid) REFERENCES Students
ON DELETE CASCADE
ON UPDATE SET DEFAULT )
```


## 刪除或清空資料表

`DROP TABLE 資料表名稱`
`truncate 資料表名稱`

# 3. Column
```
ALTER TABLE 資料表名稱
ADD COLUMN 新欄位名稱 資料型態
```
```
ALTER TABLE 資料表名稱
CHANGE COLUMN 原欄位名稱 新欄位名稱 資料型態
```
```
ALTER TABLE 資料表名稱
DROP COLUMN 欄位名稱
```

# 4. Tuples

```
INSERT INTO 資料表名稱 (sid, name, email, gpa)
VALUES (53688, ‘Smith’, ‘smith@ee’, 3.2)
```
```
UPDATE 資料表名稱 
set age = 13, gpa = 4
WHERE name = 'Tommy'
```

```
DELETE
FROM Students S 
WHERE S.name = ‘Smith’
```


# 5. View
```
CREATE VIEW YoungActiveStudents (name, grade) 
AS 
SELECT S.name, E.grade
FROM Students S, Enrolled E
WHERE S.sid = E.sid and S.age<21
```

# 6. Query language
```
 /* 基本模型 */
 
SELECT [DISTINCT] target-list 
FROM relation-list
WHERE qualification
```
![](https://hackmd.io/_uploads/HyUqglTl6.png)
![](https://hackmd.io/_uploads/B1u3gxaep.png)

## AND & BETWEEN & JOIN & DISTINCT 
Q. Find sailors’ names who’ve reserved boat 103


```
SELECT sname
FROM sailors S, reserves R
WHERE R.sid = S.sid 
AND R.bid = 103
```
Q. Find boat name reserved by sailor’s between rating 3 and 8

```
SELECT B.bname
FROM sailors S, reserves R, Boats B
WHERE S.sid = R.sid AND R.bid = B.bid
AND (S.rating BETWEEN 3 AND 8)
```

Q. Find sailors who’ve reserved at least one boat

```
SELECT DISTINCT sname
FROM sailors S, reserves R
WHERE S.sid = R.sid
```

## String Pattern (_ / %)

Q. Find triples for sailors whose names begin and end with B and contain at least three characters

* *string pattern*
    * _：任何1個字元
    * ％：任何0-N個字元
```
SELECT age, befor3y=age-3 , age*2 AS double_age
FROM sailors
WHERE sname LIKE 'B_%B'
```

## UNION & INTERSECTION

Q. Find sid’s of sailors who’ve reserved a red or a green boat
```
SELECT DISTINCT S.sid, S.sname
FROM sailors S, reserves R, boats B
WHERE S.sid = R.sid AND R.bid = B.bid
AND (B.color = 'red' OR B.color = 'green')
```
*UNION：垂直整併，表示聯集（OR）*
```
(SELECT DISTINCT S.sid, S.sname
FROM sailors S, reserves R, boats B
WHERE S.sid = R.sid AND R.bid = B.bid
AND B.color = 'red')

UNION

(SELECT DISTINCT S.sid, S.sname
FROM sailors S, reserves R, boats B
WHERE S.sid = R.sid AND R.bid = B.bid
AND B.color = 'green')
```

Q. Find sid’s of sailors who’ve reserved a red and a green boat

```
SELECT DISTINCT S.sid
FROM sailors S, reserves R1, Boats B1, reserves R2, Boats B2
WHERE S.sid = R1.sid AND S.sid = R2.sid 
AND R1.bid = B1.bid AND R2.bid = B2.bid
AND (B1.color = 'red' AND B2.color = 'green')
```

*INTERSECT：垂直整併，表示交集（AND）*
```
(SELECT DISTINCT S.sid
FROM sailors S, reserves R, Boats B
WHERE S.sid = R.sid AND R.bid = B.bid
AND B.color = 'red')

INTERSECT

(SELECT DISTINCT S.sid
FROM sailors S, reserves R, Boats B
WHERE S.sid = R.sid AND R.bid = B.bid
AND B.color = 'green')
```

Q. Find bid reserved by sid=22 and 31
```
(SELECT DISTINCT bid
FROM reserves
WHERE sid = 22)

INTERSECT

(SELECT DISTINCT bid
FROM reserves
WHERE sid = 31)
```

## IN & EXISTS
Q. Find sailors’ names who’ve reserved boat 103 

*作法一：IN*
```
SELECT DISTINCT sname
FROM sailors 
WHERE sid IN (

SELECT sid
FROM reserves
WHERE bid = 103
)
```


*作法二：EXISTS (內層需要和外層串接)*
```
SELECT DISTINCT S.sname
FROM sailors S
WHERE EXISTS (

SELECT R.sid
FROM reserves R
WHERE R.bid = 103 AND S.sid = R.sid
)
```

Q. Find sailors’ names who’ve not reserved boat 103

```
SELECT DISTINCT S.sname
FROM sailors S
WHERE sid NOT IN (

SELECT DISTINCT S.sid
FROM sailors S, reserves R
WHERE S.sid = R.sid AND R.bid = 103
)
```

Q. Find sailor’s sid who never reserve any boat
*作法一：NOT IN*
```
SELECT sid
FROM sailors
WHERE sid NOT IN (

SELECT sid
FROM reserves
)
```
*作法二：NOT EXISTS*
```
SELECT sid
FROM sailors S
WHERE NOT EXISTS (

SELECT S.sid
FROM reserves R
WHERE R.sid = S.sid
)
```
Q. Find bname which is not reserved by name start with ‘L’

```
SELECT B2.bname
FROM boats B2
WHERE B2.bid not in((
select R.bid
from sailors S, reserves R
WHERE S.sname LIKE "L%" AND R.sid = S.sid))
```

## ANY & ALL
Q. Find sailors whose rating is greater than that of some sailor called Horatio

*> ANY：大於任何數值*
```
SELECT sname
FROM sailors
WHERE rating > ANY (

SELECT rating
FROM sailors
WHERE sname = 'Horatio'
)
```
Q.Find sailors name whose age is older than those sailors who ever reserved boat 103

*> ALL：大於所有數值*
```
SELECT sname
FROM sailors
WHERE age > ALL (

SELECT S.age
FROM sailors S, reserved R
WHERE S.sid = R.sid
AND R.bid = 103
)
```
### 三層條件

Q. Find sailors who’ve reserved all boats
```
SELECT S.sname
FROM Sailors S
WHERE NOT EXISTS (

SELECT B.bid
FROM BoatsB
WHERE NOT EXISTS (

SELECT R.bid
FROM Reserves R 
WHERE R.bid=B.bid
AND R.sid=S.sid))

```

```
SELECT sid
From reserves
GROUP by sid
having COUNT(DISTINCT bid)=4
```


## Aggregate Operators
**Aggregate中不可以再有Aggregate**

Q. Find name and age of the oldest sailor(s)
```
select sname, age
from sailors
where age = (
    select MAX(age)
    from sailors)
```
Q. Find sailors who’ve reserved at most one boats

```
SELECT sid
FROM reserves
GROUP BY sid
HAVING count(*) = 1
```


## GROUP BY, HAVING
Q. Find the age of the youngest sailor for each rating level who is older than 18
```
SELECT sname, age, rating
FROM sailors
WHERE age >= 18
GROUP by rating
HAVING min(age)
```



Q. Find the age of the youngest sailor with age >= 18, for each rating with at least 2 such sailors
```
SELECT sname, min(age)
FROM sailors
WHERE age >= 18
GROUP by rating
HAVING count(*) > 1
```
Q. Find the age of the youngest sailor with age > 18, for each rating with at least 2 sailors (of any age)

```
/* 選取每一個Group裡都有兩個人以上的 */

SELECT S.rating, MIN(S.age) , count(*)
FROM Sailors S
WHERE S.age > 18
GROUP BY S.rating

-- 不論年紀是否大於18歲，只要group中有兩個人以上

HAVING 1 < (
    SELECT COUNT(*) 
    FROM Sailors S2
WHERE S.rating = S2.rating);

/* 選取每一個Group裡都有兩個大於18歲以上的 */

SELECT S.rating, MIN(S.age) , count(*)
FROM Sailors S
WHERE S.age > 18
GROUP BY S.rating
HAVING count(*) > 1;
```
Q. For each red boat, find the number of reservations for this boat
```
select R.bid, count(*)
FROM reserves R
GROUP BY R.bid
HAVING bid IN (
    SELECT B.bid
    FROM boats B
    WHERE B.color = 'red')
```
Q. Find boat names which are reserved (>=) two times
```
SELECT B.bname
FROM reserves R, boats B
WHERE B.bid = R.bid 
GROUP BY R.bid
HAVING count(*) >= 2
```
Q. For boat name of the most popular reserved boat
```
SELECT B.bname, count(*)
FROM reserves R, boats B
WHERE B.bid = R.bid 
GROUP BY R.bid
HAVING count(*) = 
(
SELECT count(*)
    From reserves R1
    Group by R1.bid
    ORDER BY count(*) DESC 
	LIMIT 1)
```
Q. Find those ratings for which the average age is the minimum over all ratings
```
SELECT S.rating, AVG(S.age)
FROM sailors S
GROUP BY S.rating
HAVING AVG(S.age) = 
(    
    SELECT AVG(S1.age)
    FROM sailors S1
    GROUP BY S1.rating
    ORDER BY AVG(S1.age) ASC
    LIMIT 1)
```
## IN NULL / NOT NULL
Q. Find boat id whose name has not been inputted (where name is null)
```
SELECT *
FROM boats
WHERE bname IS NULL
```
### Other Practices
Q. Find sailors’ names who’ve reserved “red” boat 
```
Select DISTINCT S.sname
FROM sailors S, reserves R
WHERE S.sid = R.sid AND R.bid in(
    SELECT B.bid
    FROM boats B
    WHERE B.color = 'red')
```
Q. Find sid’s of sailors who’ve reserved a red and a green boat
```
(SELECT sid
FROM reserves R1, boats B1
WHERE R1.bid = B1.bid AND B1.color = 'red')

INTERSECT

(SELECT sid
FROM reserves R2, boats B2
WHERE R2.bid = B2.bid AND B2.color = 'green')
```
Q. Find sailors’ names who’ve not reserved boat 103
```
SELECT S.sname
FROM sailors S
WHERE S.sid NOT IN ( 
    SELECT R.sid
    FROM reserves R, boats B
    WHERE R.bid = B.bid AND B.bid = '103'
)
```
Q. Find sailors’ names who’ve reserved boat on 7th and 8th in any month.
```
SELECT S.sname, R.day
FROM sailors S, reserves R
WHERE S.sid = R.sid AND (R.day LIKE '%7' OR R.day LIKE '%8')
```
Q. Finds sailors name who reserve no more than 1 times for boat 103
```
SELECT S.sname
FROM sailors S, reserves R
WHERE S.sid = R.sid AND R.bid = 103
GROUP BY S.sid
HAVING COUNT(*) <= 1
```
Q. Find sname of sailors who’ve reserved both a red and a green boat
```
SELECT s.sname
FROM sailors S
WHERE S.sid IN

((SELECT sid
FROM reserves R1, boats B1
WHERE R1.bid = B1.bid AND B1.color = 'red')

INTERSECT

(SELECT sid
FROM reserves R2, boats B2
WHERE R2.bid = B2.bid AND B2.color = 'green'))
```
Q. Find sailors who’ve reserved all boats
```
SELECT S.sname
FROM sailors S, reserves R
WHERE S.sid = R.sid
GROUP BY S.sid
HAVING count(DISTINCT R.bid) = (
    SELECT count(DISTINCT B.bid)
    FROM boats B
```
Q. Find those ratings for which the average age is the minimum over all ratings
```
SELECT S.rating, AVG(S.age)
FROM sailors S
GROUP BY S.rating
HAVING AVG(S.age) = (
    SELECT AVG(S1.age) as avg_age
    FROM sailors S1
    GROUP BY S1.rating
    ORDER BY avg_age ASC
    LIMIT 1
    )
```
[[進階SQL]With As進行子查詢(CTE)[SQL-004]](https://medium.com/jimmy-wang/sql-with-as%E9%80%B2%E8%A1%8C%E5%AD%90%E6%9F%A5%E8%A9%A2-cte-sql-004-e045147f0317)
