import pytest
from pydantic import ValidationError

from app.services.gemini.schemas import (
    VisionClassification,
    RoutingDecision,
    VerificationResult,
    IssueType,
)


def test_valid_vision_output():
    data = {
        "issue_type": IssueType.POTHOLE,
        "severity": 7,
        "hazardous": False,
        "confidence": 0.92,
    }

    obj = VisionClassification(**data)
    assert obj.severity == 7


def test_invalid_severity_raises():
    data = {
        "issue_type": IssueType.GARBAGE,
        "severity": 15,  
        "hazardous": False,
        "confidence": 0.5,
    }

    with pytest.raises(ValidationError):
        VisionClassification(**data)


def test_invalid_confidence_raises():
    data = {
        "issue_type": IssueType.OTHER,
        "severity": 3,
        "hazardous": False,
        "confidence": 1.5,  # invalid
    }

    with pytest.raises(ValidationError):
        VisionClassification(**data)


def test_valid_routing_decision():
    data = {
        "department": "Public Works",
        "priority": 2,
        "confidence": 0.85,
    }

    decision = RoutingDecision(**data)
    assert decision.priority == 2


def test_valid_verification_result():
    data = {
        "resolved": True,
        "confidence": 0.95,
        "notes": "Issue resolved successfully"
    }

    result = VerificationResult(**data)
    assert result.resolved is True
