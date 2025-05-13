import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
from students.models import Course, Student

# Фикстуры

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def create_course(**kwargs):
        return baker.make(Course, **kwargs)
    return create_course

@pytest.fixture
def student_factory():
    def create_student(**kwargs):
        return baker.make(Student, **kwargs)
    return create_student

# Тесты

@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name

@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    course1 = course_factory(name='Course 1')
    course2 = course_factory(name='Course 2')
    url = '/api/v1/courses/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert any(course['id'] == course1.id for course in response.data)
    assert any(course['id'] == course2.id for course in response.data)

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    course1 = course_factory(id=1)
    course2 = course_factory(id=2)
    url = '/api/v1/courses/?id=1'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == course1.id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course1 = course_factory(name='Course A')
    course2 = course_factory(name='Course B')
    url = '/api/v1/courses/?name=Course A'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == course1.name

@pytest.mark.django_db
def test_create_course(api_client):
    data = {'name': 'New Course'}
    url = '/api/v1/courses/'
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == data['name']

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name='Old Course')
    data = {'name': 'Updated Course'}
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == data['name']

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.filter(id=course.id).count() == 0

# Дополнительное задание

@pytest.mark.django_db
@pytest.mark.parametrize("num_students, expected_status", [
    (19, status.HTTP_200_OK),  # Успешное добавление студентов
    (20, status.HTTP_200_OK),  # Успешное добавление студентов
    (21, status.HTTP_400_BAD_REQUEST),  # Ошибка при превышении
])
def test_student_limit_on_course(api_client, course_factory, student_factory, settings, num_students, expected_status):
    settings.MAX_STUDENTS_PER_COURSE = 20  # Устанавливаем максимальное число студентов
    course = course_factory()
    
    # Создаем студентов
    students = [student_factory() for _ in range(num_students)]
    
    # Обновляем курс, добавляя студентов
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.patch(url, {'students': [student.id for student in students]})

    assert response.status_code == expected_status