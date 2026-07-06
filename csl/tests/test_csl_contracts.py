import json
from pathlib import Path

from csl import verify_csl_document_contract, verify_csl_validation_result_contract


EXAMPLE_PATH = Path("examples/csl/minimum_viable_csl.json")
RESULT_EXAMPLE_PATH = Path("examples/csl/minimum_validation_result.json")


def test_csl_document_contract_accepts_minimum_viable_example() -> None:
    document = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    verification = verify_csl_document_contract(document)

    assert verification.successful() is True
    assert verification.to_dict() == {
        "csl_contract_verification": {"successful": True, "issue_count": 0},
        "issues": [],
    }


def test_csl_document_contract_requires_top_level_fields() -> None:
    verification = verify_csl_document_contract({"csl_version": "old"})

    assert verification.successful() is False
    assert verification.issues == [
        "CSL document requires id.",
        "CSL document requires name.",
        "CSL document requires entities.",
        "CSL document requires constraints.",
        "CSL document requires groups.",
        "CSL document requires root_group_id.",
        "CSL document csl_version must be csl/v1.",
    ]


def test_csl_document_contract_validates_references_and_not_arity() -> None:
    document = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    document["constraints"][0]["entity_id"] = "ENTITY-MISSING"
    document["constraints"][1]["entity_ids"] = ["ENTITY-HOLE-A", "ENTITY-MISSING"]
    document["groups"][1]["children"] = [
        {"type": "constraint", "id": "CONSTRAINT-BODY-OVERLAPS-KEEP-OUT"},
        {"type": "constraint", "id": "CONSTRAINT-WIDTH"},
    ]
    document["root_group_id"] = "GROUP-MISSING"

    verification = verify_csl_document_contract(document)

    assert verification.successful() is False
    assert verification.issues == [
        "CSL dimensional constraint 1 entity_id must reference an existing entity.",
        "CSL geometric relation constraint 2 entity_ids must reference existing entities.",
        "CSL group 2 operator NOT requires exactly one child.",
        "CSL document root_group_id must reference an existing group.",
    ]


def test_csl_document_contract_validates_group_children() -> None:
    document = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    document["groups"][0]["children"] = [
        {"type": "constraint", "id": "CONSTRAINT-MISSING"},
        {"type": "group", "id": "GROUP-MISSING"},
        {"type": "unknown", "id": "CONSTRAINT-WIDTH"},
    ]

    verification = verify_csl_document_contract(document)

    assert verification.successful() is False
    assert verification.issues == [
        "CSL group 1 child 1 constraint id must reference an existing constraint.",
        "CSL group 1 child 2 group id must reference an existing group.",
        "CSL group 1 child 3 type must be constraint or group.",
    ]


def test_csl_validation_result_contract_accepts_minimum_example() -> None:
    result = json.loads(RESULT_EXAMPLE_PATH.read_text(encoding="utf-8"))

    verification = verify_csl_validation_result_contract(result)

    assert verification.successful() is True
    assert verification.to_dict() == {
        "csl_contract_verification": {"successful": True, "issue_count": 0},
        "issues": [],
    }


def test_csl_validation_result_contract_validates_header_and_top_level_payloads() -> None:
    verification = verify_csl_validation_result_contract(
        {
            "csl_validation_result": {
                "spec_id": "CSL-SPEC-0001",
                "csl_version": "old",
                "status": "passed",
                "successful": False,
            },
            "tree": [],
            "issues": "not-a-list",
        }
    )

    assert verification.successful() is False
    assert verification.issues == [
        "CSL validation result tree must be a dictionary.",
        "CSL validation result issues must be a list.",
        "CSL validation result header requires root_group_id.",
        "CSL validation result csl_version must be csl/v1.",
        "CSL validation result successful must match status.",
        "CSL validation result tree is required.",
    ]


def test_csl_validation_result_contract_validates_tree_records() -> None:
    result = json.loads(RESULT_EXAMPLE_PATH.read_text(encoding="utf-8"))
    result["tree"]["children"][0].pop("actual")
    result["tree"]["children"][0]["issues"] = "not-a-list"
    result["tree"]["children"][1]["operator"] = "XOR"

    verification = verify_csl_validation_result_contract(result)

    assert verification.successful() is False
    assert verification.issues == [
        "CSL validation result tree.children[1] issues must be a list.",
        "CSL validation result tree.children[1] requires actual.",
        "CSL validation result tree.children[2] operator must be AND, OR, or NOT.",
    ]
