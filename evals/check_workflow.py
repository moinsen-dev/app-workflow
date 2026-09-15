#!/usr/bin/env python3
"""Behavioral checks of the Markdown tool. Synthetic evidence is not app proof."""
import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / "skills/app-workflow/scripts/workflow.py"
spec = importlib.util.spec_from_file_location("workflow", SCRIPT)
wf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wf)


def set_table(path, name, headers, rows):
    text = path.read_text()
    marker = "## " + name + "\n"
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    if end == -1:
        end = len(text)
    path.write_text(text[:start] + "\n" + wf.render_table(headers.split(), rows) + "\n" + text[end:])


def fixture(root):
    with contextlib.redirect_stdout(io.StringIO()):
        assert wf.main(["init", str(root), "--profile", "macos", "--targets", "macos", "--goal", "Synthetischer Prüfvertrag für das Werkzeug"]) == 0
    (root / "app.swift").write_text("// Synthetic source revision A\n")
    (root / "evidence.md").write_text("Synthetic parser fixture. No real app interaction or acceptance is claimed.\n")
    (root / "review.md").write_text("Synthetic review record for validator behavior only.\n")
    data = wf.load(root)
    plan = root / "PLAN.md"
    set_table(plan, "Phases", wf.HEADERS["Phases"], [{"ID": "P01", "Order": "1", "Outcome": "Synthetischer Ablauf", "Depends": "-"}])
    set_table(plan, "Tasks", wf.HEADERS["Tasks"], [{"ID": "T001", "Phase": "P01", "UseCase": "UC01", "Requirements": "R001", "Accept": "Explizite synthetische Annahme für Strukturprüfung", "Verify": "macos", "Mode": "normal", "Depends": "-", "Files": "app.swift"}])
    set_table(plan, "Modules", wf.HEADERS["Modules"], [{**row, "Applies": "NO", "Reason": "Isolierter synthetischer Vertrag enthält diesen Bereich nicht"} for row in data["Modules"].values()])
    set_table(plan, "Checklist", wf.HEADERS["Checklist"], [{**row, "Applies": "YES", "Tasks": "T001", "Reason": "Synthetisch zugeordnet"} for row in data["Checklist"].values()])
    set_table(plan, "Personalization", wf.HEADERS["Personalization"], [{"ID": key, "Value": "NONE", "Source": "user:synthetischer Auftrag", "Reason": "Keine zusätzliche Vorgabe im Parser-Prüffall"} for key in wf.PREFERENCES])
    set_table(plan, "Delivery", wf.HEADERS["Delivery"], [{"ID": "D001", "Platform": "macos", "Channel": "local", "Goal": "local", "AppID": "local.synthetic", "Owner": "NONE", "Tasks": "T001"}])
    data = wf.load(root)
    evidence = {"ID": "E001", "Task": "T001", "Checks": "macos", "Method": "ui", "Mode": "normal", "Date": datetime.now(timezone.utc).isoformat(), "Build": "SYNTHETIC-ONLY", "Fingerprint": wf.fingerprint(data, "T001"), "Report": "evidence.md", "Result": "PASS"}
    tracker = root / "TRACKER.md"
    set_table(tracker, "Evidence", wf.HEADERS["Evidence"], [evidence])
    set_table(tracker, "Tasks", wf.HEADERS["TrackTasks"], [{"ID": "T001", "Status": "ERLEDIGT", "Evidence": "E001", "Reason": "Synthetischer Prüffall"}])
    set_table(tracker, "Releases", wf.HEADERS["Releases"], [{"ID": "L001", "Delivery": "D001", "Stage": "LOCAL", "Build": "SYNTHETIC-ONLY", "Locator": "synthetic://parser-fixture", "Evidence": "E001"}])
    data = wf.load(root)
    set_table(tracker, "Reviews", wf.HEADERS["Reviews"], [{"ID": rid, "Scope": scope, "Kind": "independent", "Result": "PASS", "Fingerprint": wf.fingerprint(data, scope), "Report": "review.md"} for rid, scope in [("RV001", "PLAN"), ("RV002", "UC01")]])
    refresh_state(root)


def refresh_state(root):
    data = wf.load(root)
    (root / "STATE.md").write_text(wf.state_text(data, "T001", "Synthetischen Vertrag prüfen."))


def delivery_fixture(root, profile="macos", target="macos", channel="app-store", goal="live", stage="SUBMITTED", app_id="test.synthetic", owner="SYNTHETIC OWNER"):
    """Pure validation fixture; none of these rows claim a real distribution."""
    plan, tracker = root / "PLAN.md", root / "TRACKER.md"
    plan.write_text(plan.read_text().replace("- profile: macos", f"- profile: {profile}").replace("- targets: macos", f"- targets: {target}"))
    d = wf.load(root)
    delivery = {"ID": "D001", "Platform": "ios" if target.startswith("ios-") else target, "Channel": channel, "Goal": goal, "AppID": app_id, "Owner": owner, "Tasks": "T001"}
    set_table(plan, "Delivery", wf.HEADERS["Delivery"], [delivery])
    catalog, _ = wf.catalogue(profile, deliveries=[delivery])
    set_table(plan, "Checklist", wf.HEADERS["Checklist"], [{"ID": key, "Check": row["Check"], "Applies": "YES", "Tasks": "T001", "Reason": "Synthetische Abdeckung"} for key, row in catalog.items()])
    task = {**d["Tasks"]["T001"], "Verify": target}
    set_table(plan, "Tasks", wf.HEADERS["Tasks"], [task])
    d = wf.load(root)
    set_table(tracker, "Evidence", wf.HEADERS["Evidence"], [{**d["Evidence"]["E001"], "Checks": target, "Fingerprint": wf.fingerprint(d, "T001")}])
    set_table(tracker, "Releases", wf.HEADERS["Releases"], [{"ID": "L001", "Delivery": "D001", "Stage": stage, "Build": "SYNTHETIC-ONLY", "Locator": "synthetic://release-fixture", "Evidence": "E001"}])
    d = wf.load(root)
    set_table(tracker, "Reviews", wf.HEADERS["Reviews"], [{"ID": rid, "Scope": scope, "Kind": "independent", "Result": "PASS", "Fingerprint": wf.fingerprint(d, scope), "Report": "review.md"} for rid, scope in [("RV001", "PLAN"), ("RV002", "UC01")]])
    refresh_state(root)


class WorkflowChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="app-workflow-check-")
        self.root = Path(self.temp.name).resolve()
        fixture(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def errors(self, **options):
        return wf.validate(wf.load(self.root), **options)[0]

    def assert_error(self, code, **options):
        errors = self.errors(**options)
        self.assertTrue(any(e.startswith(code + ":") for e in errors), errors)

    def test_complete_synthetic_contract(self):
        self.assertEqual(self.errors(complete=True), [])

    def test_all_profiles_generate_without_claiming_ready(self):
        for profile, targets in [("expo", "android,ios-simulator"), ("flutter", "android"), ("ios", "ios-simulator"), ("macos", "macos")]:
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
                root = Path(folder).resolve()
                self.assertEqual(wf.main(["init", str(root), "--profile", profile, "--targets", targets, "--goal", "Lokale Notizen verwalten", "--claude"]), 0)
                errors, warnings = wf.validate(wf.load(root))
                self.assertFalse(errors)
                self.assertTrue(warnings)
                self.assertTrue(wf.validate(wf.load(root), ready=True)[0])
                self.assertEqual((root / "CLAUDE.md").read_text(), "@AGENTS.md\n")

    def test_existing_files_are_preserved_without_partial_generation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "AGENTS.md").write_text("Existing user instructions\n")
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            with contextlib.redirect_stderr(io.StringIO()):
                result = wf.main(["init", str(root), "--profile", "macos", "--targets", "macos", "--goal", "Notizen"])
            self.assertEqual(result, 1)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})

    def test_missing_catalogue_item_is_detected(self):
        data = wf.load(self.root)
        rows = list(data["Checklist"].values())[1:]
        set_table(self.root / "PLAN.md", "Checklist", wf.HEADERS["Checklist"], rows)
        self.assert_error("CHECKLIST_COVERAGE")

    def test_new_module_requires_its_actual_checks(self):
        data = wf.load(self.root)
        data["Modules"]["auth"]["Applies"] = "YES"
        set_table(self.root / "PLAN.md", "Modules", wf.HEADERS["Modules"], data["Modules"].values())
        self.assert_error("CHECKLIST_COVERAGE")

    def test_done_without_evidence_is_rejected(self):
        set_table(self.root / "TRACKER.md", "Tasks", wf.HEADERS["TrackTasks"], [{"ID": "T001", "Status": "ERLEDIGT", "Evidence": "-", "Reason": "Behauptung ohne Nachweis"}])
        self.assert_error("UNVERIFIED")

    def test_source_change_invalidates_active_evidence(self):
        (self.root / "app.swift").write_text("// Synthetic source revision B\n")
        self.assert_error("STALE_EVIDENCE", complete=True)

    def test_acceptance_change_invalidates_evidence(self):
        path = self.root / "PLAN.md"
        path.write_text(path.read_text().replace("Explizite synthetische Annahme für Strukturprüfung", "Neues nachzuweisendes Verhalten"))
        self.assert_error("STALE_EVIDENCE")

    def test_build_and_fixture_cannot_prove_normal_ui(self):
        data = wf.load(self.root)
        row = data["Evidence"]["E001"]
        row["Method"] = "build"
        set_table(self.root / "TRACKER.md", "Evidence", wf.HEADERS["Evidence"], [row])
        self.assert_error("EVIDENCE_METHOD")
        row["Method"], row["Mode"] = "ui", "fixture"
        set_table(self.root / "TRACKER.md", "Evidence", wf.HEADERS["Evidence"], [row])
        self.assert_error("UNVERIFIED")

    def test_missing_report_and_external_path_are_rejected(self):
        (self.root / "evidence.md").unlink()
        self.assert_error("MISSING_REPORT")
        data = wf.load(self.root)
        row = data["Evidence"]["E001"]
        row["Report"] = "../outside.md"
        set_table(self.root / "TRACKER.md", "Evidence", wf.HEADERS["Evidence"], [row])
        with self.assertRaises(wf.Invalid):
            self.errors()

    def test_stale_state_is_detected_and_refresh_is_explicit(self):
        path = self.root / "TRACKER.md"
        path.write_text(path.read_text() + "\nZusätzliche Beobachtung.\n")
        self.assert_error("STATE_STALE")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(wf.main(["state", str(self.root), "--task", "T001", "--next", "Beobachtung lesen"]), 0)
        self.assertFalse(self.errors())

    def test_inspection_cannot_replace_target_coverage(self):
        data = wf.load(self.root)
        row = data["Tasks"]["T001"]
        row["Verify"] = "inspection"
        set_table(self.root / "PLAN.md", "Tasks", wf.HEADERS["Tasks"], [row])
        self.assert_error("TARGET_COVERAGE", ready=True)

    def test_dependency_cycle_is_detected(self):
        data = wf.load(self.root)
        row = data["Tasks"]["T001"]
        row["Depends"] = "T001"
        set_table(self.root / "PLAN.md", "Tasks", wf.HEADERS["Tasks"], [row])
        self.assert_error("CYCLE")

    def test_skipping_all_work_cannot_complete_requirement(self):
        set_table(self.root / "TRACKER.md", "Tasks", wf.HEADERS["TrackTasks"], [{"ID": "T001", "Status": "NICHT_ZUTREFFEND", "Evidence": "-", "Reason": "Unzulässige pauschale Ausnahme"}])
        self.assert_error("UNCOVERED_REQUIREMENT", complete=True)

    def test_read_commands_do_not_write(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        for args in [["check", str(self.root), "--complete"], ["status", str(self.root)], ["fingerprint", str(self.root), "--scope", "UC01"]]:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(wf.main(args), 0)
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_cli_invalid_input_has_nonzero_exit(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "check", str(self.root / "missing"), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING_FILE", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_personalization_requires_provenance_and_resolves_conflicts(self):
        d = wf.load(self.root)
        rows = list(d["Personalization"].values())
        rows[0]["Source"] = "-"
        set_table(self.root / "PLAN.md", "Personalization", wf.HEADERS["Personalization"], rows)
        self.assert_error("PREFERENCE_SOURCE")
        rows[0].update(Source="user:synthetisch", Value="CONFLICT")
        set_table(self.root / "PLAN.md", "Personalization", wf.HEADERS["Personalization"], rows)
        self.assert_error("PREFERENCE_CONFLICT")

    def test_changed_effective_style_invalidates_existing_evidence(self):
        d = wf.load(self.root)
        d["Personalization"]["graphic_style"]["Value"] = "Konkreter neuer Grafikstil"
        set_table(self.root / "PLAN.md", "Personalization", wf.HEADERS["Personalization"], d["Personalization"].values())
        self.assert_error("STALE_EVIDENCE", complete=True)

    def test_profile_import_is_explicit_and_never_overwrites(self):
        profile = self.root / "USER_PROFILE.md"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(wf.main(["profile", str(profile)]), 0)
        profile.write_text(profile.read_text().replace("| bundle_prefix | UNKNOWN |", "| bundle_prefix | test.personal |"))
        original = profile.read_bytes()
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(wf.main(["init", folder, "--profile", "macos", "--targets", "macos", "--goal", "Synthetische Übernahme", "--user-profile", str(profile)]), 0)
            pref = wf.load(Path(folder).resolve())["Personalization"]["bundle_prefix"]
            self.assertEqual(pref["Value"], "test.personal")
            self.assertEqual(pref["Source"], f"profile:{profile.resolve()}#bundle_prefix")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(wf.main(["profile", str(profile)]), 1)
        self.assertEqual(profile.read_bytes(), original)

    def test_mixed_delivery_routes_select_only_applicable_checks(self):
        cases = [("expo", "android,ios-device", "ios:testflight:live,android:google-play:ready", {"BETAAPPLE-001", "PLAY-002"}, {"STOREAPPLE-001", "WIN-001"}),
                 ("flutter", "web,windows", "web:web:live,windows:direct:ready", {"WEB-001", "WIN-001"}, {"PLAY-001", "APPLE-001", "WINSTORE-001"})]
        for profile, targets, delivery, expected, absent in cases:
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(wf.main(["init", folder, "--profile", profile, "--targets", targets, "--goal", "Synthetischer Multi-Ziel-Vertrag", "--delivery", delivery]), 0)
                data = wf.load(Path(folder).resolve())
                self.assertFalse(wf.validate(data)[0])
                self.assertTrue(expected <= data["Checklist"].keys())
                self.assertFalse(absent & data["Checklist"].keys())

    def test_icons_permissions_and_preferences_cannot_disappear(self):
        original = (self.root / "PLAN.md").read_text()
        for missing in ["CORE-019", "CORE-021", "CORE-022"]:
            with self.subTest(missing=missing):
                (self.root / "PLAN.md").write_text(original)
                data = wf.load(self.root)
                set_table(self.root / "PLAN.md", "Checklist", wf.HEADERS["Checklist"], [row for key, row in data["Checklist"].items() if key != missing])
                self.assert_error("CHECKLIST_COVERAGE")

    def test_upload_cannot_complete_live_delivery(self):
        delivery_fixture(self.root, stage="SUBMITTED")
        self.assert_error("RELEASE_INCOMPLETE", release=True)
        delivery_fixture(self.root, stage="LIVE")
        self.assertEqual(self.errors(release=True), [])

    def test_simulator_and_local_completion_do_not_prove_live_ios(self):
        self.assert_error("RELEASE_SCOPE", release=True)
        delivery_fixture(self.root, profile="ios", target="ios-simulator", channel="testflight", stage="LIVE")
        self.assert_error("DELIVERY_UI_PLAN", ready=True)
        self.assert_error("DELIVERY_UI_PLAN", release=True)

    def test_live_device_check_must_belong_to_delivery_but_may_be_blocked(self):
        delivery_fixture(self.root, profile="ios", target="ios-device", channel="testflight", stage="LIVE")
        d = wf.load(self.root)
        tasks = [d["Tasks"]["T001"], {**d["Tasks"]["T001"], "ID": "T002", "Verify": "inspection", "Mode": "any"}]
        set_table(self.root / "PLAN.md", "Tasks", wf.HEADERS["Tasks"], tasks)
        set_table(self.root / "TRACKER.md", "Tasks", wf.HEADERS["TrackTasks"], [
            {"ID": "T001", "Status": "BLOCKIERT", "Evidence": "-", "Reason": "Synthetischer Fall: physisches Ziel fehlt derzeit"},
            {"ID": "T002", "Status": "OFFEN", "Evidence": "-", "Reason": "Vorbereitung geplant"}])
        for name in ["Evidence", "Reviews", "Releases"]:
            set_table(self.root / "TRACKER.md", name, wf.HEADERS[name], [])
        delivery = {**d["Delivery"]["D001"], "Tasks": "T002"}
        set_table(self.root / "PLAN.md", "Delivery", wf.HEADERS["Delivery"], [delivery])
        self.assert_error("DELIVERY_UI_PLAN", ready=True, check_state=False)
        delivery["Tasks"] = "T001,T002"
        set_table(self.root / "PLAN.md", "Delivery", wf.HEADERS["Delivery"], [delivery])
        d = wf.load(self.root)
        set_table(self.root / "TRACKER.md", "Reviews", wf.HEADERS["Reviews"], [
            {"ID": "RV001", "Scope": "PLAN", "Kind": "self", "Result": "PASS", "Fingerprint": wf.fingerprint(d, "PLAN"), "Report": "review.md"}])
        refresh_state(self.root)
        self.assertEqual(self.errors(ready=True), [])
        self.assert_error("RELEASE_INCOMPLETE", release=True)

    def test_ready_can_finish_with_local_artifact_without_submission(self):
        delivery_fixture(self.root, profile="ios", target="ios-simulator", channel="testflight", goal="ready", stage="READY")
        d = wf.load(self.root)
        row = {**d["Releases"]["L001"], "Locator": "prepared/release.ipa and local-preflight.md (SYNTHETIC)"}
        set_table(self.root / "TRACKER.md", "Releases", wf.HEADERS["Releases"], [row])
        d = wf.load(self.root)
        reviews = list(d["Reviews"].values())
        for review in reviews:
            review["Fingerprint"] = wf.fingerprint(d, review["Scope"])
        set_table(self.root / "TRACKER.md", "Reviews", wf.HEADERS["Reviews"], reviews)
        refresh_state(self.root)
        self.assertEqual(self.errors(release=True), [])

    def test_release_rejects_missing_or_conflicting_identity(self):
        for app_id, owner in [("NONE", "SYNTHETIC OWNER"), ("CONFLICT", "SYNTHETIC OWNER"), ("test.synthetic", "CONFLICT"), ("test.synthetic", "NONE")]:
            with self.subTest(app_id=app_id, owner=owner):
                delivery_fixture(self.root, stage="LIVE", app_id=app_id, owner=owner)
                self.assert_error("DELIVERY_IDENTITY", release=True)

    def test_release_cannot_claim_a_different_build_from_its_evidence(self):
        delivery_fixture(self.root, stage="LIVE")
        d = wf.load(self.root)
        set_table(self.root / "TRACKER.md", "Releases", wf.HEADERS["Releases"], [
            {**d["Releases"]["L001"], "Build": "SYNTHETIC-DIFFERENT-BUILD"}])
        self.assert_error("RELEASE_BUILD", release=True)

    def test_release_record_change_invalidates_review(self):
        delivery_fixture(self.root, stage="LIVE")
        d = wf.load(self.root)
        row = {**d["Releases"]["L001"], "Locator": "synthetic://different-release"}
        set_table(self.root / "TRACKER.md", "Releases", wf.HEADERS["Releases"], [row])
        self.assert_error("PHASE_INCOMPLETE", release=True)

    def test_legacy_contract_keeps_its_recorded_fingerprints(self):
        root = Path(__file__).resolve().parent / "fixtures" / "legacy-v1"
        data = wf.load(root)
        errors, warnings = wf.validate(data, complete=True)
        self.assertEqual(errors, [])
        self.assertTrue(any(w.startswith("LEGACY_TEMPLATE:") for w in warnings))
        self.assertTrue(any(e.startswith("RELEASE_SCOPE:") for e in wf.validate(data, release=True)[0]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
