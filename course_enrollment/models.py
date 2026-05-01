from django.db import models

# ── CHEATSHEET: ManyToManyField ───────────────────────────────────────────────
# ManyToManyField creates a junction table automatically.
# related_name='students' → course.students.all() returns enrolled students.
# Use .add(obj) to enroll, .remove(obj) to un-enroll, .all() to list.
# ─────────────────────────────────────────────────────────────────────────────

class Course(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    # IntegerField → whole numbers (no decimal)
    duration    = models.IntegerField(help_text='Duration in weeks')

    def __str__(self):
        return self.name


class Student(models.Model):
    name    = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email   = models.EmailField()  # EmailField validates email format

    # ManyToMany: one student can enrol in many courses & vice versa
    courses = models.ManyToManyField(Course, related_name='students', blank=True)

    def __str__(self):
        return self.name
