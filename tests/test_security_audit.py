"""Tests for SecurityAudit."""
import tempfile
from pathlib import Path
from tasks.security_audit import SecurityAudit


def test_security_audit_init():
    """Should initialize SecurityAudit."""
    auditor = SecurityAudit()
    assert auditor is not None


def test_get_security_report():
    """Should get security report."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        auditor = SecurityAudit()
        report = auditor.get_security_report(str(project_path))
        
        assert "success" in report
        assert "security_issues" in report

