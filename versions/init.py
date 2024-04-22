import random
from datetime import datetime

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, Group, Discipline, Grade


fake = Faker('uk-UA')


def insert_teachers():
    for _ in range(6):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)


def insert_group():
    for _ in range(10):
        group_ = Group(
            name=fake.word()
        )
        session.add(group_)


def insert_students():
    groups = session.query(Group).all()
    for _ in range(10):
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(groups).id
        )
        session.add(student)


def insert_subject():
    teachers = session.query(Teacher).all()
    for _ in range(10):
        discipline = Discipline(
            name=fake.word(),
            teacher_id=random.choice(teachers).id
        )
        session.add(discipline)


def insert_range():
    students = session.query(Student).all()
    disciplines = session.query(Discipline).all()
    for student in students:
        grade = Grade(
            grade=random.randint(0, 100),
            date_of=fake.date_between_dates(date_start=datetime(2013,1,1), date_end=datetime(2023,12,31)),
            student_id=student.id,
            discipline_id=random.choice(disciplines).id
        )
        print(grade)
        session.add(grade)


if __name__ == '__main__':
    try:
        # insert_teachers()
        # insert_group()
        # insert_students()
        # insert_subject()
        insert_range()
        # session.commit()
        # insert_rel()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()