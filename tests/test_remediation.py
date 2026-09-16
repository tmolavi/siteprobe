import tempfile
from pathlib import Path
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.remediation.planner import RemediationPlanner
from siteprobe.remediation.executor import RemediationExecutor
from siteprobe.verification.verifier import FixVerifier, VerificationStatus


def test_remediation_and_verification_cycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        index_html = root / "index.html"
        index_html.write_text("<html><head><title>Hi</title></head><body><img src='a.png'></body></html>", encoding="utf-8")

        # Create simulated findings
        findings = [
            Finding(
                id="technical.robots.missing",
                category=FindingCategory.TECHNICAL_SEO,
                severity=Severity.HIGH,
                url="http://127.0.0.1:8000/",
                title="robots.txt not found",
                why_it_matters="Bots unguided",
                recommended_action="Create robots.txt",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
            ),
            Finding(
                id="geo.llms_txt.missing",
                category=FindingCategory.GEO_AEO,
                severity=Severity.MEDIUM,
                url="http://127.0.0.1:8000/",
                title="Missing /llms.txt file",
                why_it_matters="AI indexing",
                recommended_action="Create llms.txt",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
            ),
            Finding(
                id="ux.viewport.missing",
                category=FindingCategory.UX,
                severity=Severity.HIGH,
                url="http://127.0.0.1:8000/",
                title="Missing meta viewport",
                why_it_matters="Mobile usability",
                recommended_action="Add viewport tag",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
            ),
            Finding(
                id="onpage.images.missing_alt",
                category=FindingCategory.ONPAGE_SEO,
                severity=Severity.HIGH,
                url="http://127.0.0.1:8000/",
                title="Image missing alt",
                why_it_matters="Accessibility",
                recommended_action="Add alt",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
            ),
        ]

        # 1. Plan
        plan = RemediationPlanner.create_plan("http://127.0.0.1:8000", findings)
        assert plan.safe_count == 4

        # 2. Execute
        executor = RemediationExecutor(str(root))
        report = executor.apply_safe_fixes(plan)
        assert report.applied_count == 4
        assert (root / "robots.txt").exists()
        assert (root / "llms.txt").exists()

        # 3. Verify
        verifications = FixVerifier.verify_local_changes(findings, str(root))
        assert len(verifications) == 4
        for v in verifications:
            assert v.status == VerificationStatus.FIXED

        # 4. Rollback
        executor.rollback()
        # Verify rollback reverted modified html
        assert 'alt=""' not in index_html.read_text(encoding="utf-8")
