from constraintos.review import create_review_checklist, review_gate_status, summarize_review


def sample_spec() -> dict:
    return {
        "artifact": {"id": "PLATE-0001", "version": "0.1", "title": "Test"},
        "constraints": [
            {"id": "C-0001", "statement": "Must show V6", "severity": "blocker", "acceptance": "V6 visible", "validation_method": "review"},
            {"id": "C-0002", "statement": "Must show turbo", "severity": "major", "acceptance": "Turbo visible", "validation_method": "review"},
        ],
    }


def test_create_review_checklist() -> None:
    checklist = create_review_checklist(sample_spec(), "REVIEW-0001")
    assert checklist["review_checklist"]["id"] == "REVIEW-0001"
    assert checklist["summary"]["total"] == 2
    assert checklist["items"][0]["constraint_id"] == "C-0001"


def test_review_gate_blocks_unreviewed_blocker() -> None:
    checklist = create_review_checklist(sample_spec(), "REVIEW-0001")
    gate = review_gate_status(checklist)
    assert gate["gate"] == "blocked"
    assert "C-0001" in gate["blocked_items"]


def test_summarize_complete_review() -> None:
    checklist = create_review_checklist(sample_spec(), "REVIEW-0001")
    for item in checklist["items"]:
        item["reviewer_result"] = "pass"
        item["reviewer_confidence"] = 0.9
    updated = summarize_review(checklist)
    assert updated["summary"]["reviewed"] == 2
    assert updated["review_checklist"]["status"] == "complete"
    assert review_gate_status(updated)["gate"] == "pass"
