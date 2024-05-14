import os
from database.interface import HarvesterDBInterface
from harvester.utils import CFHandler

DATABASE_URI = os.getenv("DATABASE_URI")
CF_API_URL = os.getenv("CF_API_URL")
CF_SERVICE_USER = os.getenv("CF_SERVICE_USER")
CF_SERVICE_AUTH = os.getenv("CF_SERVICE_AUTH")
LM_RUNNER_APP_GUID = os.getenv("LM_RUNNER_APP_GUID")
CF_INSTANCE_INDEX = os.getenv("CF_INSTANCE_INDEX")

LM_MAX_TASKS_COUNT = 3

interface = HarvesterDBInterface()
cf_handler = CFHandler(CF_API_URL, CF_SERVICE_USER, CF_SERVICE_AUTH)


def create_task(jobId):
    return {
        "app_guuid": LM_RUNNER_APP_GUID,
        "command": f"python harvest.py {jobId}",
        "task_id": f"harvest-job-{jobId}",
    }


def sort_jobs(jobs):
    return sorted(jobs, key=lambda x: x["status"], reverse=True)


def load_manager():
    # confirm CF_INSTANCE_INDEX == 0 or bail
    if os.getenv("CF_INSTANCE_INDEX") != "0":
        return

    # filter harvestjobs by pending / pending_manual
    jobs = interface.get_harvest_jobs_by_faceted_filter(
        "status", ["pending", "pending_manual"]
    )

    # get current list of all tasks
    current_tasks = cf_handler.get_all_app_tasks(LM_RUNNER_APP_GUID)
    # filter out in_process tasks
    running_tasks = cf_handler.get_all_running_tasks(current_tasks)

    # confirm tasks < MAX_JOBS_COUNT or bail
    if LM_MAX_TASKS_COUNT < running_tasks:
        return
    else:
        slots = LM_MAX_TASKS_COUNT - running_tasks

    # sort jobs by pending_manual first
    sorted_jobs = sort_jobs(jobs)

    # slice off jobs to invoke
    jobs_to_invoke = sorted_jobs[:slots]

    # invoke cf_task with next job(s)
    # then mark that job(s) as running in the DB
    print("Load Manager :: Updated Harvest Jobs")
    for job in jobs_to_invoke:
        task_contract = create_task(job["id"])
        cf_handler.start_task(**task_contract)
        updated_job = interface.update_harvest_job(job["id"], {"status": "in_progress"})
        print(updated_job)