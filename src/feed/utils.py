import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action
from accounts.models import AppliedJobs


def create_action(user, verb, type, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)
    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target, type=type)
        action.save()
        return True
    return False


def get_icon(action_type):
    if action_type == 'follow':
        return "icon-feather-user-plus"
    elif action_type == 'like':
        return "icon-material-outline-thumb-up"
    elif action_type == 'comment':
        return "icon-feather-message-circle"
    elif action_type == 'new_img':
        return "icon-material-outline-add-a-photo"
    elif action_type == 'new_post':
        return "icon-material-outline-bookmarks"
    elif action_type == 'new_job':
        return "icon-line-awesome-street-view"
    elif action_type == "job_response":
        return "icon-feather-message-square"
    elif action_type == "applied_to_job":
        return "icon-feather-monitor"
    else:
        return "icon-material-outline-rate-review"


def filter_notifications(request, actions):
    invalid_actions = []
    for action in actions:
        if action.type == "job_response":
            app = AppliedJobs.objects.get(id=action.target_id)
            if app.user != request.user.profile:
                invalid_actions.append(action)
    print(invalid_actions)
    actions = [action for action in actions if action not in invalid_actions]
    return actions

