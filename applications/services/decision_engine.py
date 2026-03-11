from applications.models import Decision, RuleLog


def evaluate_application(application, extracted_address):

    rules = []

    # Rule 1: credit score
    rules.append({
        "rule_name": "credit_score_check",
        "passed": application.credit_score >= 500,
        "message": "Credit score must be >= 500"
    })

    # Rule 2: income
    rules.append({
        "rule_name": "income_check",
        "passed": application.monthly_income >= 10000,
        "message": "Monthly income must be >= 10000"
    })

    # Rule 3: bank history
    rules.append({
        "rule_name": "bank_history_check",
        "passed": application.bank_history_months >= 6,
        "message": "Bank history must be >= 6 months"
    })

    # Rule 4: age
    rules.append({
        "rule_name": "age_check",
        "passed": 25 <= application.age <= 60,
        "message": "Age must be between 25 and 60"
    })

    # Rule 5: family condition
    rules.append({
        "rule_name": "family_condition",
        "passed": application.is_married or application.has_children,
        "message": "Applicant must be married or have children"
    })

    # Rule 6: address validation
    rules.append({
        "rule_name": "address_match",
        "passed": application.declared_address == extracted_address,
        "message": "Declared address must match document"
    })

    approved = all(rule["passed"] for rule in rules)

    reason = "All rules passed" if approved else "One or more rules failed"

    decision = Decision.objects.create(
        application=application,
        approved=approved,
        reason=reason
    )

    for rule in rules:
        RuleLog.objects.create(
            decision=decision,
            rule_name=rule["rule_name"],
            passed=rule["passed"],
            message=rule["message"]
        )

    return decision