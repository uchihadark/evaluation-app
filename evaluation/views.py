from django.shortcuts import render, redirect
from .models import Mentor, Student
from django.contrib import messages


def home(request):
    mentors = Mentor.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        # Get the selected mentor and students from the POST data
        selected_mentor = request.POST.get('mentor')
        selected_students = request.POST.getlist('students')

        # Check if a mentor is selected
        if selected_mentor:
            # Set the mentor for the selected students
            mentor = Mentor.objects.get(id=selected_mentor)
            for student_id in selected_students:
                student = Student.objects.get(id=student_id)
                student.mentor = mentor
                student.save()

            # Redirect to the homepage to display the updated data
            return redirect('home')

    context = {'mentors': mentors, 'students': students}
    return render(request, 'evaluation/home.html', context)


def view_students(request, mentor_id):
    mentor = Mentor.objects.get(id=mentor_id)
    students = mentor.student_set.all()
    context = {'mentor': mentor, 'students': students}
    return render(request, 'evaluation/view_students.html', context)


def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    mentor_id = student.mentor.id
    if request.method == 'POST':
        student.ideation_marks = request.POST['ideation']
        student.execution_marks = request.POST['execution']
        student.viva_marks = request.POST['viva']
        student.save()
        return redirect('view_students', mentor_id=mentor_id)
    return render(request, 'evaluation/edit_student.html', {'student': student})


def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    mentor_id = student.mentor.id

    if student.mentor.student_set.filter(marks_locked=False).count() > 3:
        # Remove the current student from the mentor
        Student.objects.create(
        name=student.name,
        mentor=None,
        ideation_marks=student.ideation_marks,
        execution_marks=student.execution_marks,
        viva_marks=student.viva_marks,
        marks_locked=student.marks_locked
        )
        student.delete()
    else:
        # Alert the user that a minimum of 3 students must be assigned to a mentor at all times
        messages.error(request, 'A minimum of 3 students must be assigned to a mentor at all times.')
        pass
    return redirect('view_students', mentor_id=mentor_id)


def submit_final_marks(request, mentor_id):
    mentor = Mentor.objects.get(id=mentor_id)
    if request.method == 'POST':
        # Get the number of students under "Marks Not Locked"
        num_students_not_locked = mentor.student_set.filter(marks_locked=False).count()

        # Check if the number of students under "Marks Not Locked" is greater than 4
        if num_students_not_locked > 4 or num_students_not_locked < 3:
            # Display a message to the user
            messages.error(request, 'A Mentor can only accommodate maximum 4 and minimum 3 students at a time.')
        else:
            # Lock the marks of all students under the mentor
            students = mentor.student_set.all()
            for student in students:
                student.marks_locked = True
                student.save()
    return redirect('view_students', mentor_id=mentor.id)
