from .models import JobApplication
import random


def create_job_id(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    uid = random.randint(lower, upper)

    # check if Quiz already exists if not, return id
    try:
        job_applications = JobApplication.objects.get(job_id=uid)
    except:
        job_applications = None

    if not job_applications:
        return uid
    else:
        create_job_id(digits)  # If uid already exists recreate uid