import pytest
from app.domain.models import Issue, IssueStatus


def create_issue():
    return Issue(
        issue_id="ISSUE_TEST_1",
        location={"lat": 17.44, "lng": 78.34},
        description="Test issue",
        image_url="gs://test/image.png"
    )


def test_initial_state_is_submitted():
    issue = create_issue()
    assert issue.status == IssueStatus.SUBMITTED


def test_valid_state_transitions():
    issue = create_issue()

    issue.transition_to(IssueStatus.CLASSIFIED)
    assert issue.status == IssueStatus.CLASSIFIED

    issue.transition_to(IssueStatus.ROUTED)
    assert issue.status == IssueStatus.ROUTED


def test_invalid_state_transition_raises():
    issue = create_issue()

    with pytest.raises(ValueError):
        issue.transition_to(IssueStatus.RESOLVED)


def test_updated_at_changes_on_transition():
    issue = create_issue()
    old_time = issue.updated_at

    issue.transition_to(IssueStatus.CLASSIFIED)
    assert issue.updated_at > old_time
