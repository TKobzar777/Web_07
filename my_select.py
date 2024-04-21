from sqlalchemy import func, desc, and_

from conf.db import session
from conf.models import Teacher, Student, Group, Discipline, Grade

"""
1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
"""
"""
SELECT
    s.id,
    s.fullname,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 5;
"""


def select_1():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()

    return result


"""
2. Знайти студента із найвищим середнім балом з певного предмета.
"""
"""
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.discipline_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
"""


def select_2():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 3).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.discipline_id == 1).group_by(Student.id).\
        order_by(desc('average_grade')).limit(1).all()
    return result


"""
3. Знайти середній бал у групах з певного предмета.
"""
"""
    SELECT
        s.group_id,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.discipline_id = 2
    GROUP BY s.group_id
    ORDER BY average_grade DESC;
"""


def select_3():
    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.discipline_id == 2).group_by(Student.group_id)\
        .order_by(desc('average_grade')).all()
    return result


"""
4. Знайти середній бал на потоці (по всій таблиці оцінок).
"""
"""
    SELECT ROUND(AVG(g.grade),2) as average_grade
    FROM grades as g
"""


def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).all()
    return result


"""
5. Знайти які курси читає певний викладач.
"""
"""
    SELECT
        d.id,
        d.name,
        t.fullname
    FROM disciplines d
    JOIN teachers t ON t.id = d.teacher_id
    where t.id = 1
    ORDER BY d.name;
"""


def select_5():
    result = session.query(Discipline.id, Discipline.name, Teacher.fullname) \
        .select_from(Discipline).join(Teacher).filter(Teacher.id == 1).order_by(Discipline.name).all()
    return result


"""
6. Знайти список студентів у певній групі.
"""
"""
    SELECT
    s.id as student_id,
    s.fullname as student_name,
    g.name as group_name
    FROM students s
    JOIN groups_ g ON g.id = s.group_id
    where g.id  = 2
    ORDER BY s.fullname;
"""


def select_6():
    result = session.query(Student.id, Student.fullname, Group.name)\
        .select_from(Student).join(Group).filter(Group.id == 2).order_by(Student.fullname).all()
    return result


"""
7. Знайти оцінки студентів у окремій групі з певного предмета.
"""
"""
    SELECT
        s.fullname,
        g.grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.discipline_id = 1 and s.group_id =1
    ORDER BY s.fullname;
"""


def select_7():
    result = session.query(Student.fullname, Grade.grade)\
        .select_from(Grade).join(Student).filter(and_(Grade.discipline_id == 1, Student.group_id == 1))\
        .order_by(Student.fullname).all()
    return result


"""
8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
"""
"""
SELECT
    t.id,
    t.fullname,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN disciplines d ON d.id = g.discipline_id
JOIN teachers  t ON t.id = d.teacher_id
where t.id  = 2
GROUP BY t.id
ORDER BY average_grade;
"""


def select_8():
    result = session.query(Teacher.id, Teacher.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Discipline).join(Teacher).filter(Teacher.id == 2).group_by(Teacher.id) \
        .order_by(desc('average_grade')).all()
    return result


"""
9. Знайти список курсів, які відвідує певний студент.
"""
"""
SELECT
    d.name as discipline_name
FROM grades g
JOIN students s ON s.id = g.student_id
join disciplines d on d.id = g.discipline_id
where g.student_id = 30;
"""


def select_9():
    result = session.query(Discipline.name)\
        .select_from(Grade).join(Student).join(Discipline).filter(Grade.student_id == 30).all()
    return result


"""
10. Список курсів, які певному студенту читає певний викладач.
"""
"""
SELECT 
    d.name AS discipline_name,
    s.fullname AS student_name,
    t.fullname AS teacher_name
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN disciplines d ON d.id = g.discipline_id
JOIN teachers t ON t.id = d.teacher_id
WHERE g.student_id = 30 AND d.teacher_id = 1;
"""


def select_10():
    result = session.query(Discipline.name, Student.fullname, Teacher.fullname)\
        .select_from(Grade).join(Student).join(Discipline).join(Teacher)\
        .filter(and_(Grade.student_id == 30, Discipline.teacher_id == 1)).all()
    return result


if __name__ == '__main__':
    print(select_1())

    res = select_2()
    for s in res:
        columns = ["id", "fullname", "average_grade"]
        r = [dict(
            zip(columns, (s.id, s.fullname, s.average_grade)))]
        print(r)

    print(select_3())
    print(select_4())
    print(select_5())
    print(select_6())
    print(select_7())
    print(select_8())
    print(select_9())
    print(select_10())
