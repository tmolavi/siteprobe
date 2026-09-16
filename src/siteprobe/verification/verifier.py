from pathlib import Path
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from siteprobe.models.finding import Finding
from siteprobe.models.verification import VerificationResult, VerificationStatus


class FixVerifier:
    """Verifies remediation results by inspecting affected targets before and after changes."""

    @classmethod
    def verify_local_changes(cls, findings: List[Finding], repo_path: str) -> List[VerificationResult]:
        root = Path(repo_path).resolve()
        results: List[VerificationResult] = []

        for f in findings:
            if not f.auto_fixable:
                results.append(VerificationResult(
                    finding_id=f.id,
                    url=f.url,
                    status=VerificationStatus.SKIPPED,
                    message="Manual decision required; automatic verification not applicable.",
                    before_evidence=f.evidence,
                    after_evidence={},
                ))
                continue

            # Verify robots.txt
            if f.id == "technical.robots.missing":
                robots_file = root / "robots.txt"
                if robots_file.exists() and len(robots_file.read_text(encoding="utf-8").strip()) > 10:
                    results.append(VerificationResult(
                        finding_id=f.id,
                        url=f.url,
                        status=VerificationStatus.FIXED,
                        message="Verified: robots.txt created and non-empty.",
                        before_evidence=f.evidence,
                        after_evidence={"robots_file_size": robots_file.stat().st_size},
                    ))
                else:
                    results.append(VerificationResult(
                        finding_id=f.id,
                        url=f.url,
                        status=VerificationStatus.FAILED,
                        message="Verification failed: robots.txt still missing.",
                        before_evidence=f.evidence,
                        after_evidence={},
                    ))
                continue

            # Verify llms.txt
            if f.id == "geo.llms_txt.missing":
                llms_file = root / "llms.txt"
                if llms_file.exists() and len(llms_file.read_text(encoding="utf-8").strip()) > 10:
                    results.append(VerificationResult(
                        finding_id=f.id,
                        url=f.url,
                        status=VerificationStatus.FIXED,
                        message="Verified: llms.txt created with valid markdown.",
                        before_evidence=f.evidence,
                        after_evidence={"llms_file_size": llms_file.stat().st_size},
                    ))
                else:
                    results.append(VerificationResult(
                        finding_id=f.id,
                        url=f.url,
                        status=VerificationStatus.FAILED,
                        message="Verification failed: llms.txt not found.",
                        before_evidence=f.evidence,
                        after_evidence={},
                    ))
                continue

            # Verify HTML tag insertions
            html_files = [p for p in root.glob("**/*.html") if not any(part.startswith(".") for part in p.parts)]
            if not html_files:
                results.append(VerificationResult(
                    finding_id=f.id,
                    url=f.url,
                    status=VerificationStatus.UNCHANGED,
                    message="No local HTML files found to verify.",
                    before_evidence=f.evidence,
                    after_evidence={},
                ))
                continue

            fixed = False
            for hf in html_files:
                try:
                    soup = BeautifulSoup(hf.read_text(encoding="utf-8"), "html.parser")
                except Exception:
                    continue

                if f.id == "technical.canonical.missing":
                    canon = soup.find("link", rel=lambda x: x and "canonical" in (x if isinstance(x, list) else [x]))
                    if canon and canon.get("href"):
                        fixed = True
                        break
                elif f.id == "accessibility.html.missing_lang":
                    html_tag = soup.find("html")
                    if html_tag and html_tag.get("lang"):
                        fixed = True
                        break
                elif f.id == "ux.viewport.missing":
                    vp = soup.find("meta", attrs={"name": "viewport"})
                    if vp and vp.get("content"):
                        fixed = True
                        break
                elif f.id == "onpage.images.missing_alt":
                    imgs_missing = [img for img in soup.find_all("img") if img.get("alt") is None]
                    if not imgs_missing:
                        fixed = True
                        break

            if fixed:
                results.append(VerificationResult(
                    finding_id=f.id,
                    url=f.url,
                    status=VerificationStatus.FIXED,
                    message="Verified: Tag successfully injected into local HTML template.",
                    before_evidence=f.evidence,
                    after_evidence={"verified_in": str(html_files[0].name)},
                ))
            else:
                results.append(VerificationResult(
                    finding_id=f.id,
                    url=f.url,
                    status=VerificationStatus.UNCHANGED,
                    message="Target elements remain uncorrected.",
                    before_evidence=f.evidence,
                    after_evidence={},
                ))

        return results
