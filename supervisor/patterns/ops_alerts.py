#!/usr/bin/env python3
"""
Operations Alerts Pattern Module
Detects operational triggers for automation
"""

from .base_pattern import DomainPattern


def load_ops_patterns():
    """Load all operations-related patterns"""
    patterns = [
        DomainPattern(
            name="gift_receipt_pending",
            pattern=r"(gift|donation).*(receipt|acknowledgment).*(pending|waiting)",
            domain="ops",
            severity="high",
            agent="ops_automation",
            resolution="gift_receipt_generation_cascade",
            force_multiplier=10,
            context_hints=["receipt", "tax", "acknowledgment"],
            allowed_sources=["donation_platform", "gift_processing"],
            compliance_tags=["irs_compliant", "automated_ok"]
        ),

        DomainPattern(
            name="volunteer_schedule_conflict",
            pattern=r"(volunteer|staff).*(schedule|shift).*(conflict|overlap)",
            domain="ops",
            severity="high",
            agent="ops_automation",
            resolution="schedule_conflict_resolution_cascade",
            force_multiplier=12,
            context_hints=["scheduling", "conflict", "volunteer"],
            allowed_sources=["volunteer_portal", "scheduling_system"],
            compliance_tags=["no_pii", "automated_ok"]
        ),

        DomainPattern(
            name="communication_batch_ready",
            pattern=r"(email|communication|newsletter).*(batch|queue).*(ready|pending)",
            domain="ops",
            severity="medium",
            agent="ops_automation",
            resolution="batch_communication_cascade",
            force_multiplier=15,
            context_hints=["bulk_email", "newsletter", "communication"],
            allowed_sources=["email_platform", "marketing_automation"],
            compliance_tags=["can_spam_compliant", "automated_ok"]
        ),

        DomainPattern(
            name="event_registration_surge",
            pattern=r"(event|registration).*(surge|spike|high volume)",
            domain="ops",
            severity="high",
            agent="ops_automation",
            resolution="registration_scaling_cascade",
            force_multiplier=20,
            context_hints=["event", "registration", "capacity"],
            allowed_sources=["event_platform", "registration_system"],
            compliance_tags=["no_pii", "scalable"]
        ),

        DomainPattern(
            name="inventory_threshold_alert",
            pattern=r"(inventory|supplies|stock).*(low|threshold|reorder)",
            domain="ops",
            severity="medium",
            agent="ops_automation",
            resolution="inventory_reorder_cascade",
            force_multiplier=8,
            context_hints=["inventory", "supplies", "procurement"],
            allowed_sources=["inventory_system", "procurement_portal"],
            compliance_tags=["automated_ok", "budget_approved"]
        ),

        DomainPattern(
            name="compliance_report_due",
            pattern=r"(compliance|regulatory|audit).*(report|filing).*(due|deadline)",
            domain="ops",
            severity="critical",
            agent="ops_automation",
            resolution="compliance_report_cascade",
            force_multiplier=25,
            context_hints=["compliance", "regulatory", "deadline"],
            allowed_sources=["compliance_calendar", "regulatory_tracker"],
            compliance_tags=["regulatory", "critical_deadline"]
        ),

        DomainPattern(
            name="staff_onboarding_trigger",
            pattern=r"(new|staff|employee).*(onboarding|orientation).*(scheduled|needed)",
            domain="ops",
            severity="medium",
            agent="ops_automation",
            resolution="onboarding_automation_cascade",
            force_multiplier=18,
            context_hints=["hr", "onboarding", "new_employee"],
            allowed_sources=["hr_system", "onboarding_portal"],
            compliance_tags=["pii_restricted", "hr_compliant"]
        ),

        DomainPattern(
            name="facility_maintenance_alert",
            pattern=r"(facility|maintenance|repair).*(needed|scheduled|alert)",
            domain="ops",
            severity="medium",
            agent="ops_automation",
            resolution="maintenance_workflow_cascade",
            force_multiplier=10,
            context_hints=["facility", "maintenance", "operations"],
            allowed_sources=["facility_management", "maintenance_system"],
            compliance_tags=["automated_ok", "safety_compliant"]
        ),

        DomainPattern(
            name="budget_variance_detected",
            pattern=r"(budget|expense|variance).*(exceeded|significant|alert)",
            domain="ops",
            severity="high",
            agent="ops_automation",
            resolution="budget_analysis_cascade",
            force_multiplier=15,
            context_hints=["finance", "budget", "variance"],
            allowed_sources=["accounting_system", "budget_tracker"],
            compliance_tags=["financial_data", "board_visibility"]
        ),

        DomainPattern(
            name="data_backup_needed",
            pattern=r"(backup|data|archive).*(needed|scheduled|overdue)",
            domain="ops",
            severity="critical",
            agent="ops_automation",
            resolution="backup_execution_cascade",
            force_multiplier=5,
            context_hints=["backup", "data_protection", "archive"],
            allowed_sources=["backup_system", "it_monitoring"],
            compliance_tags=["critical_infrastructure", "automated_ok"]
        )
    ]

    return patterns


# Pattern cascade definitions
OPS_CASCADES = {
    "gift_receipt_generation_cascade": {
        "steps": [
            "retrieve_gift_details",
            "verify_donor_information",
            "calculate_tax_deductible_amount",
            "generate_receipt_pdf",
            "send_receipt_email",
            "archive_receipt_copy",
            "update_donor_record",
            "log_compliance_record"
        ],
        "estimated_time": 300,  # 5 minutes
        "outputs": 8
    },

    "schedule_conflict_resolution_cascade": {
        "steps": [
            "identify_conflicting_shifts",
            "check_volunteer_availability",
            "propose_alternative_schedules",
            "notify_affected_volunteers",
            "update_schedule_system",
            "send_confirmations",
            "update_coverage_report"
        ],
        "estimated_time": 900,  # 15 minutes
        "outputs": 7
    },

    "batch_communication_cascade": {
        "steps": [
            "validate_recipient_list",
            "check_opt_out_preferences",
            "personalize_content",
            "schedule_send_time",
            "configure_tracking",
            "execute_send",
            "monitor_delivery_rates",
            "generate_engagement_report"
        ],
        "estimated_time": 1200,  # 20 minutes
        "outputs": 10
    }
}


def get_ops_cascade(cascade_name: str) -> dict:
    """Get cascade definition for ops domain"""
    return OPS_CASCADES.get(cascade_name, {})
