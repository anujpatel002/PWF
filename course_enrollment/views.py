from django.shortcuts import get_object_or_404, render, redirect
from .forms import StudentForm
from .models import Course, Student

# ── CHEATSHEET: ManyToMany — add / all ───────────────────────────────────────
# student.courses.add(course)      → enrol student in a course
# course.students.all()            → list all students on a course (reverse M2M)
# request.POST or None             → neat one-liner: None on GET, POST data on POST
# ─────────────────────────────────────────────────────────────────────────────


def add_course(request):
    """Create a Course directly from POST data (no ModelForm — manual approach)."""
    if request.method == 'POST':
        name        = request.POST.get('name')
        description = request.POST.get('description')
        duration    = request.POST.get('duration')
        Course.objects.create(name=name, description=description, duration=duration)
        return redirect('course_enrollment:course_list')
    return render(request, 'course_enrollment/add_course.html')


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_enrollment/course_list.html', {'courses': courses})


def enroll_student(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form   = StudentForm(request.POST or None)

    if form.is_valid():
        student = form.save()
        student.courses.add(course)  # ← ManyToMany: attach course after saving student
        return render(request, 'course_enrollment/course_detail.html', {
            'student': student,
            'course':  course,
        })

    return render(request, 'course_enrollment/enroll.html', {
        'form':   form,
        'course': course,
    })


def student_course(request, course_id):
    """List all students enrolled in a specific course (reverse M2M lookup)."""
    course   = get_object_or_404(Course, id=course_id)
    students = course.students.all()  # reverse M2M via related_name
    return render(request, 'course_enrollment/student_course.html', {
        'course':   course,
        'students': students,
    })
