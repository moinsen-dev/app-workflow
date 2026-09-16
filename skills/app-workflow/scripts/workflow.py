#!/usr/bin/env python3
"""App workflow: readable Markdown, explicit checks, no runtime dependencies."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.1.0"
SUPPORTED_VERSIONS = {"1.0.0", VERSION}
SCHEMA = "app-workflow/1"
BUNDLE = Path(__file__).resolve().parents[1]
PROFILES = {
    "expo": {"web", "android", "ios-simulator", "ios-device"},
    "flutter": {"web", "android", "ios-simulator", "ios-device", "macos", "windows", "linux"},
    "ios": {"ios-simulator", "ios-device"},
    "macos": {"macos"},
}
UI = set.union(*PROFILES.values())
CHECKS = UI | {"inspection", "unit", "build"}
PREFERENCES = ("language", "collaboration", "code_conventions", "graphic_style", "design_skill", "brand_assets", "bundle_prefix", "github_user", "github_org", "repo_visibility", "preferred_stack", "preferred_services", "localization", "release_defaults")
CHANNELS = {
    "ios": {"local", "app-store", "testflight"},
    "android": {"local", "google-play", "play-testing", "direct"},
    "macos": {"local", "app-store", "testflight", "direct"},
    "web": {"local", "web"},
    "windows": {"local", "direct", "microsoft-store"},
    "linux": {"local", "direct", "linux-store"},
}
RELEASE_STAGES = {"LOCAL": 0, "READY": 1, "SUBMITTED": 2, "LIVE": 3}
STATUSES = {"OFFEN", "IN_ARBEIT", "ZUR_PRUEFUNG", "ERLEDIGT", "BLOCKIERT", "NICHT_ZUTREFFEND"}
TERMINAL = {"ERLEDIGT", "NICHT_ZUTREFFEND"}
HEADERS = {
    "Requirements": "ID Outcome",
    "Phases": "ID Order Outcome Depends",
    "UseCases": "ID Phase Outcome Requirements Review",
    "Tasks": "ID Phase UseCase Requirements Accept Verify Mode Depends Files",
    "Modules": "ID Applies Reason",
    "Checklist": "ID Check Applies Tasks Reason",
    "TrackTasks": "ID Status Evidence Reason",
    "Evidence": "ID Task Checks Method Mode Date Build Fingerprint Report Result",
    "Reviews": "ID Scope Kind Result Fingerprint Report",
    "Checks": "ID Stage Rule Check When Proof",
    "Personalization": "ID Value Source Reason",
    "Delivery": "ID Platform Channel Goal AppID Owner Tasks",
    "Releases": "ID Delivery Stage Build Locator Evidence",
}
FILES = ("AGENTS.md", "PLAN.md", "TRACKER.md", "STATE.md")


class Invalid(ValueError):
    pass


def split(value):
    return [p.strip() for p in value.split(",") if p.strip() and p.strip() != "-"]


def meaningful(value):
    return bool(value.strip()) and value.strip().upper() not in {"-", "TODO", "TBD", "UNKNOWN"} and "{{" not in value


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=False).encode())[:24]


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise Invalid(f"READ: {path.name}: {exc}") from exc


def indexed_sections(text):
    """(line index, line) per section; fenced blocks belong to no section."""
    result, current, fenced = {}, None, False
    for index, line in enumerate(text.split("\n")):
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
        if fenced:
            continue
        if line.startswith("## "):
            current = line[3:].strip()
            if current in result:
                raise Invalid(f"FORMAT: doppelte Section {current}")
            result[current] = []
        elif current:
            result[current].append((index, line))
    return result


def sections(text):
    return {name: [line for _, line in pairs] for name, pairs in indexed_sections(text).items()}


def table_rows(text, name):
    """Line indices of the table rows in one section, header and separator first."""
    pairs = indexed_sections(text).get(name)
    if pairs is None:
        raise Invalid(f"FORMAT: Section {name} fehlt")
    rows = [index for index, line in pairs if line.strip().startswith("|")]
    if len(rows) < 2:
        raise Invalid(f"FORMAT: Tabelle {name} fehlt")
    return rows


def cells(line):
    # Escaped pipes are content, not table separators.
    return [p.strip().replace("\x00", "|") for p in line.strip()[1:-1].replace(r"\|", "\x00").split("|")]


def table(doc, name, header=None):
    if name not in doc:
        raise Invalid(f"FORMAT: Section {name} fehlt")
    rows = [line for line in doc[name] if line.strip().startswith("|")]
    expected = (header or HEADERS[name]).split()
    if len(rows) < 2 or cells(rows[0]) != expected:
        raise Invalid(f"FORMAT: {name} erwartet Spalten {' | '.join(expected)}")
    if len(cells(rows[1])) != len(expected) or any(not re.fullmatch(r":?-{3,}:?", x) for x in cells(rows[1])):
        raise Invalid(f"FORMAT: Trennzeile in {name} ungültig")
    result = {}
    for line in rows[2:]:
        values = cells(line)
        if not line.strip().endswith("|") or len(values) != len(expected):
            raise Invalid(f"FORMAT: falsche Spaltenzahl in {name}: {line[:100]}")
        row = dict(zip(expected, values))
        key = row["ID"]
        if not key or key in result:
            raise Invalid(f"DUPLICATE_ID: {name}: {key}")
        result[key] = row
    return result


def metadata(doc, name):
    if name not in doc:
        raise Invalid(f"FORMAT: Section {name} fehlt")
    result = {}
    for line in doc[name]:
        if line.startswith("- "):
            key, sep, value = line[2:].partition(":")
            if not sep or key in result:
                raise Invalid(f"FORMAT: Metadaten in {name} ungültig: {key}")
            result[key] = value.strip()
    return result


def local_file(root, value):
    if not value or value == "-" or Path(value).is_absolute():
        raise Invalid(f"PATH: relativer Projektpfad erwartet: {value}")
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise Invalid(f"PATH: Verweis verlässt das Projekt: {value}")
    return path


def platforms(targets):
    return {"ios" if target.startswith("ios-") else target for target in targets}


def delivery_specs(value, targets):
    result = []
    available = platforms(targets)
    for item in split(value):
        parts = item.split(":")
        if len(parts) != 3:
            raise Invalid("DELIVERY: platform:channel:goal erwartet, etwa ios:app-store:live")
        platform, channel, goal = parts
        goal = goal.lower()
        if platform not in available or channel not in CHANNELS[platform] or goal.upper() not in RELEASE_STAGES:
            raise Invalid(f"DELIVERY: unpassendes Ziel {item}")
        if (channel == "local") != (goal == "local") or (goal == "submitted" and channel in {"direct", "web"}):
            raise Invalid(f"DELIVERY: Endzustand passt nicht zum Kanal: {item}")
        result.append({"Platform": platform, "Channel": channel, "Goal": goal, "AppID": "UNKNOWN", "Owner": "UNKNOWN", "Tasks": "-"})
    for platform in sorted(available - {row["Platform"] for row in result}):
        result.append({"Platform": platform, "Channel": "UNKNOWN", "Goal": "UNKNOWN", "AppID": "UNKNOWN", "Owner": "UNKNOWN", "Tasks": "-"})
    return [{"ID": f"D{n:03d}", **row} for n, row in enumerate(result, 1)]


def release_groups(deliveries):
    groups = set()
    for row in deliveries:
        channel, platform = row["Channel"], row["Platform"]
        if channel in {"UNKNOWN", "local"}:
            continue
        groups.add("common")
        if channel in {"app-store", "testflight"}:
            groups |= {"apple", channel}
        elif channel in {"google-play", "play-testing"}:
            groups.add("play")
        elif channel == "web":
            groups.add("web")
        elif platform in {"windows", "linux"}:
            groups.add(platform)
            if channel.endswith("-store"):
                groups.add(channel)
        elif channel == "direct":
            groups.add(platform + "-direct")
    return groups


def personalization(profile_path=None):
    supplied = {}
    if profile_path:
        profile_path = profile_path.resolve()
        supplied = table(sections(read(profile_path)), "Preferences", "ID Value")
        if supplied.keys() - set(PREFERENCES):
            raise Invalid("PREFERENCES: unbekannte Profilfelder; nur benannte Konventionen übernehmen")
    return [{"ID": key, "Value": supplied.get(key, {}).get("Value", "UNKNOWN"),
             "Source": f"profile:{profile_path.as_posix()}#{key}" if profile_path and meaningful(supplied.get(key, {}).get("Value", "")) else "-",
             "Reason": "Übernommener Standard; mit Projekt und Auftrag abgleichen" if profile_path and meaningful(supplied.get(key, {}).get("Value", "")) else "-"} for key in PREFERENCES]


def catalogue(profile, modules=(), deliveries=(), version=VERSION):
    if profile not in PROFILES:
        raise Invalid(f"PROFILE: unbekanntes Profil {profile}")
    mod_doc = sections(read(BUNDLE / "references/modules.md"))
    switches = table(mod_doc, "Modules", "ID When")
    rows = table(sections(read(BUNDLE / "references/catalogue.md")), "Checks")
    if version == "1.0.0":
        rows = {key: row for key, row in rows.items() if int(key.split("-")[1]) <= 18}
    sources = [table(sections(read(BUNDLE / f"references/profiles/{profile}.md")), "Checks")]
    for name in modules:
        if name not in switches:
            raise Invalid(f"MODULE: unbekanntes Modul {name}")
        sources.append(table(mod_doc, name, HEADERS["Checks"]))
    if version != "1.0.0":
        release_doc = sections(read(BUNDLE / "references/release.md"))
        sources += [table(release_doc, group, HEADERS["Checks"]) for group in sorted(release_groups(deliveries))]
    for source in sources:
        if rows.keys() & source.keys():
            raise Invalid("CATALOGUE: doppelte Check-ID")
        rows.update(source)
    return rows, switches


def load(root):
    texts = {}
    for filename in FILES:
        path = local_file(root, filename)
        if not path.is_file():
            raise Invalid(f"MISSING_FILE: {filename}")
        texts[filename] = read(path)
    return parse(root, texts)


def parse(root, texts):
    data = {"root": root, **texts}
    plan = sections(data["PLAN.md"])
    tracker = sections(data["TRACKER.md"])
    data["project"] = metadata(plan, "Project")
    data["state"] = metadata(sections(data["STATE.md"]), "State")
    for name in ("Requirements", "Phases", "UseCases", "Tasks", "Modules", "Checklist"):
        data[name] = table(plan, name)
    data["TrackTasks"] = table(tracker, "Tasks", HEADERS["TrackTasks"])
    for name in ("Evidence", "Reviews"):
        data[name] = table(tracker, name)
    if data["project"].get("template_version") == VERSION:
        for name in ("Personalization", "Delivery"):
            data[name] = table(plan, name)
        data["Releases"] = table(tracker, "Releases")
    return data


def file_fingerprint(root, paths):
    result = {}
    for value in paths:
        path = local_file(root, value)
        if path.exists() and not path.is_file():
            raise Invalid(f"PATH: Quelldatei erwartet: {value}")
        result[value] = sha(path.read_bytes()) if path.is_file() else "MISSING"
    return result


def task_fingerprint(data, task_id):
    task = data["Tasks"][task_id]
    uc = data["UseCases"].get(task["UseCase"], {})
    payload = {
        "goal": data["project"].get("goal"), "targets": data["project"].get("targets"),
        "task": task, "use_case": uc,
        "requirements": {key: data["Requirements"].get(key) for key in split(task["Requirements"])},
        "files": file_fingerprint(data["root"], split(task["Files"])),
    }
    if "Personalization" in data:
        payload["personalization"] = data["Personalization"]
        payload["delivery"] = {key: row for key, row in data["Delivery"].items() if task_id in split(row["Tasks"])}
    return digest(payload)


def fingerprint(data, scope):
    if scope == "PLAN":
        # Source filenames evolve during implementation without changing plan intent.
        definitions = {name: data[name] for name in ("Requirements", "Phases", "UseCases", "Modules", "Checklist")}
        definitions["Tasks"] = {key: {k: v for k, v in row.items() if k != "Files"} for key, row in data["Tasks"].items()}
        if "Personalization" in data:
            definitions.update({name: data[name] for name in ("Personalization", "Delivery")})
        return digest({"project": data["project"], "definitions": definitions})
    if scope in data["Tasks"]:
        return task_fingerprint(data, scope)
    if scope in data["UseCases"]:
        tasks = {key: task_fingerprint(data, key) for key, row in data["Tasks"].items() if row["UseCase"] == scope}
        evidence = {}
        for task_id in tasks:
            for eid in split(data["TrackTasks"].get(task_id, {}).get("Evidence", "-")):
                row = data["Evidence"].get(eid)
                if row:
                    path = local_file(data["root"], row["Report"])
                    evidence[eid] = {"row": row, "report": sha(path.read_bytes()) if path.is_file() else "MISSING"}
        payload = {"use_case": data["UseCases"][scope], "tasks": tasks, "evidence": evidence}
        if "Releases" in data:
            relevant = {key for key, row in data["Delivery"].items() if set(split(row["Tasks"])) & tasks.keys()}
            payload["releases"] = {key: row for key, row in data["Releases"].items() if row["Delivery"] in relevant}
        return digest(payload)
    raise Invalid(f"SCOPE: unbekannt {scope}")


def cycle(rows, field):
    visited, active = set(), set()
    def visit(key):
        if key in active:
            return True
        if key in visited:
            return False
        active.add(key)
        for dep in split(rows[key][field]):
            if dep in rows and visit(dep):
                return True
        active.remove(key)
        visited.add(key)
        return False
    return any(visit(key) for key in rows)


def review_passed(data, scope):
    matches = [row for row in data["Reviews"].values() if row["Scope"] == scope]
    if not matches:
        return False
    last = matches[-1]
    return last["Result"] == "PASS" and last["Fingerprint"] == fingerprint(data, scope)


def phase_closed(data, phase_id):
    tasks = [key for key, row in data["Tasks"].items() if row["Phase"] == phase_id]
    if not tasks or any(data["TrackTasks"].get(key, {}).get("Status") not in TERMINAL for key in tasks):
        return False
    return all(row["Review"] != "required" or review_passed(data, key)
               for key, row in data["UseCases"].items() if row["Phase"] == phase_id)


def validate_context(data, ready, complete, error, warnings):
    if "Personalization" not in data:
        warnings.append("LEGACY_TEMPLATE: 1.0-Nachweis; Personalisierung und Release-Vertrag aus 1.1 sind noch nicht geprüft")
        return
    if set(data["Personalization"]) != set(PREFERENCES):
        error("PERSONALIZATION_COVERAGE", "Alle benannten persönlichen Vorgaben einordnen")
    def unresolved(code, message):
        if ready:
            error(code, message)
        else:
            warnings.append(f"{code}: {message}")
    for key, row in data["Personalization"].items():
        if row["Value"].upper() == "CONFLICT":
            error("PREFERENCE_CONFLICT", f"{key}: Projektentscheidung und Standard abgleichen")
        elif not meaningful(row["Value"]):
            unresolved("PREFERENCE_OPEN", key)
        elif not meaningful(row["Source"]) or not meaningful(row["Reason"]):
            error("PREFERENCE_SOURCE", f"{key}: Herkunft und Anwendung begründen; NONE ist eine bewusste Wahl")
    available = platforms(split(data["project"]["targets"]))
    deliveries = data["Delivery"]
    if {row["Platform"] for row in deliveries.values()} != available:
        error("DELIVERY_COVERAGE", "Auslieferungswege müssen alle gewählten Plattformen abdecken")
    seen = set()
    for key, row in deliveries.items():
        platform, channel, goal = row["Platform"], row["Channel"], row["Goal"]
        if not re.fullmatch(r"D\d+", key) or platform not in available:
            error("DELIVERY", f"{key}: ID oder Plattform ungültig")
        if "UNKNOWN" in {channel, goal}:
            unresolved("DELIVERY_OPEN", f"{key}: Kanal und Endzustand bestimmen")
        elif channel not in CHANNELS.get(platform, set()) or goal.upper() not in RELEASE_STAGES or goal != goal.lower() or (channel == "local") != (goal == "local") or (goal == "submitted" and channel in {"direct", "web"}):
            error("DELIVERY", f"{key}: Plattform, Kanal und Endzustand passen nicht zusammen")
        if (platform, channel) in seen:
            error("DELIVERY", f"{key}: doppelter Auslieferungsweg")
        seen.add((platform, channel))
        task_ids = split(row["Tasks"])
        if ready and not task_ids:
            error("DELIVERY_TASKS", f"{key}: Vorbereitung und Endzustand konkreten Aufgaben zuordnen")
        for task_id in task_ids:
            if task_id not in data["Tasks"]:
                error("DELIVERY_TASKS", f"{key}: unbekannte Aufgabe {task_id}")
        if task_ids and all(data["TrackTasks"].get(t, {}).get("Status") == "NICHT_ZUTREFFEND" for t in task_ids):
            error("DELIVERY_TASKS", f"{key}: Auslieferungsziel kann nicht durch Ausnahmen entfallen")
        if ready and goal in {"local", "live"}:
            target = "ios-device" if platform == "ios" and goal == "live" else platform
            acceptable = {"ios-simulator", "ios-device"} if target == "ios" else {target}
            if not any(data["Tasks"].get(t, {}).get("Mode") == "normal"
                       and set(split(data["Tasks"][t]["Verify"])) & acceptable
                       and data["TrackTasks"].get(t, {}).get("Status") != "NICHT_ZUTREFFEND"
                       for t in task_ids):
                error("DELIVERY_UI_PLAN", f"{key}: normalen Nutzerstart auf {target} einer Auslieferungsaufgabe zuordnen; fehlendes Gerät als Blockade festhalten")
        invalid_app_id = not meaningful(row["AppID"]) or row["AppID"].upper() in {"NONE", "CONFLICT"}
        invalid_owner = not meaningful(row["Owner"]) or row["Owner"].upper() == "CONFLICT" or (channel != "local" and row["Owner"].upper() == "NONE")
        if complete and (invalid_app_id or invalid_owner):
            error("DELIVERY_IDENTITY", f"{key}: tatsächliche App-Identität und zuständigen Eigentümer/Konto belegen")
    latest = {}
    for key, row in data["Releases"].items():
        delivery = deliveries.get(row["Delivery"])
        if not re.fullmatch(r"L\d+", key) or not delivery or row["Stage"] not in RELEASE_STAGES:
            error("RELEASE_RECORD", f"{key}: ID, Auslieferungsziel oder beobachteter Status ungültig")
            continue
        latest[row["Delivery"]] = row
        if not meaningful(row["Build"]) or not meaningful(row["Locator"]):
            error("RELEASE_RECORD", f"{key}: Build und konkreten Artefakt-/Release-Verweis angeben")
        if delivery["Channel"] == "local" and row["Stage"] != "LOCAL":
            error("RELEASE_RECORD", f"{key}: lokaler Nachweis und externer Auslieferungsweg sind nicht austauschbar")
        if not split(row["Evidence"]):
            error("RELEASE_EVIDENCE", f"{key}: tatsächliche Beobachtung fehlt")
        for eid in split(row["Evidence"]):
            evidence = data["Evidence"].get(eid)
            if not evidence or evidence["Task"] not in split(delivery["Tasks"]):
                error("RELEASE_EVIDENCE", f"{key}: {eid} gehört nicht zu einer zugeordneten Aufgabe")
    if not complete:
        return
    for did, delivery in deliveries.items():
        row = latest.get(did)
        if not row or RELEASE_STAGES.get(row["Stage"], -1) < RELEASE_STAGES.get(delivery["Goal"].upper(), 99):
            error("RELEASE_INCOMPLETE", f"{did}: Endzustand {delivery['Goal']} noch nicht belegt; Upload ist keine Veröffentlichung")
            continue
        evidence_rows = []
        for eid in split(row["Evidence"]):
            evidence = data["Evidence"].get(eid)
            if not evidence or evidence["Task"] not in data["Tasks"]:
                continue
            task = data["TrackTasks"].get(evidence["Task"], {})
            if eid not in split(task.get("Evidence", "")) or task.get("Status") != "ERLEDIGT" or evidence["Result"] != "PASS" or evidence["Mode"] == "fixture" or evidence["Fingerprint"] != task_fingerprint(data, evidence["Task"]):
                error("RELEASE_EVIDENCE", f"{did}/{eid}: aktuellen passenden aktiven Beleg verwenden")
            elif evidence["Build"] != row["Build"]:
                error("RELEASE_BUILD", f"{did}/{eid}: Release und zugehöriger Beleg müssen dieselbe eindeutige Build-Kennung nennen")
            else:
                evidence_rows.append(evidence)
        if not any(e["Method"] in {"ui", "inspection"} for e in evidence_rows):
            error("RELEASE_EVIDENCE", f"{did}: ein Build allein belegt den Auslieferungszustand nicht")
        if row["Stage"] in {"LOCAL", "LIVE"}:
            target = "ios-device" if delivery["Platform"] == "ios" and row["Stage"] == "LIVE" else delivery["Platform"]
            acceptable = {"ios-simulator", "ios-device"} if target == "ios" else {target}
            if not any(e["Method"] == "ui" and e["Mode"] == "normal" and set(split(e["Checks"])) & acceptable for e in evidence_rows):
                error("RELEASE_UI", f"{did}: normalen Start des ausgelieferten Artefakts auf {target} belegen")


def validate(data, ready=False, complete=False, phase=None, check_state=True, release=False):
    errors, warnings = [], []
    def error(code, message):
        errors.append(f"{code}: {message}")
    project = data["project"]
    for name in ("schema", "profile", "template_version", "targets", "goal"):
        if not meaningful(project.get(name, "")):
            error("PROJECT", f"{name} fehlt")
    if project.get("schema") != SCHEMA or project.get("template_version") not in SUPPORTED_VERSIONS:
        error("VERSION", "Passende Skill-Version verwenden oder Plan bewusst migrieren")
    profile = project.get("profile")
    targets = set(split(project.get("targets", "")))
    if profile not in PROFILES or not targets or not targets <= PROFILES.get(profile, set()):
        error("TARGETS", "Profil und gewählte Zielumgebungen passen nicht")
    if errors:
        return errors, warnings
    modules = data["Modules"]
    active_modules = [key for key, row in modules.items() if row["Applies"] == "YES"]
    catalog, switches = catalogue(profile, active_modules, data.get("Delivery", {}).values(), project["template_version"])
    if set(modules) != set(switches):
        error("MODULE_COVERAGE", f"Erwartete Modulentscheidungen: {', '.join(switches)}")
    is_complete = complete or release or (check_state and data["state"].get("status") == "COMPLETE")
    execution_started = any(
        data["TrackTasks"].get(key, {}).get("Status") in {"IN_ARBEIT", "ZUR_PRUEFUNG", "ERLEDIGT"}
        and (set(split(row["Verify"])) & UI or data["Phases"].get(row["Phase"], {}).get("Order", "1") != "1")
        for key, row in data["Tasks"].items()
    )
    needs_ready = ready or is_complete or phase is not None or execution_started
    validate_context(data, needs_ready, False, error, warnings)
    if release and (project["template_version"] != VERSION or not any(row["Goal"] != "local" for row in data.get("Delivery", {}).values())):
        error("RELEASE_SCOPE", "Release-Prüfung benötigt einen 1.1-Auslieferungsvertrag über den lokalen Start hinaus")
    if set(catalog) != set(data["Checklist"]):
        error("CHECKLIST_COVERAGE", f"Fehlend: {sorted(catalog.keys() - data['Checklist'].keys())}; unerwartet: {sorted(data['Checklist'].keys() - catalog.keys())}")
    for name in ("Modules", "Checklist"):
        for key, row in data[name].items():
            if row["Applies"] not in {"YES", "NO", "UNKNOWN"}:
                error("APPLIES", f"{key}: YES, NO oder UNKNOWN erwartet")
            elif row["Applies"] == "UNKNOWN":
                (errors if needs_ready else warnings).append(f"UNDECIDED: {key}")
            elif row["Applies"] == "NO" and not meaningful(row["Reason"]):
                error("REASON", f"{key}: Ausnahme begründen")
            if name == "Checklist":
                if row["Applies"] == "NO" and catalog.get(key, {}).get("Rule") == "always":
                    error("REQUIRED_CHECK", f"{key} ist im vereinbarten Umfang erforderlich")
                refs = split(row["Tasks"])
                if row["Applies"] == "YES" and not refs:
                    error("UNCOVERED_CHECK", f"{key}: Tasks zuordnen")
                for ref in refs:
                    if ref not in data["Tasks"]:
                        error("TASK_REF", f"{key} referenziert unbekannten Task {ref}")
    for name, pattern in (("Requirements", r"R\d+"), ("Phases", r"P\d+"), ("UseCases", r"UC\d+"), ("Tasks", r"T\d+")):
        if not data[name]:
            error("EMPTY", f"{name} ist leer")
        for key, row in data[name].items():
            if not re.fullmatch(pattern, key):
                error("ID", f"{name}: ungültige ID {key}")
            if "Outcome" in row and not meaningful(row["Outcome"]):
                error("OUTCOME", f"{key}: Ergebnis fehlt")
    if set(data["Tasks"]) != set(data["TrackTasks"]):
        error("TRACKER_COVERAGE", "Tasks in Plan und Tracker stimmen nicht überein")
    orders = []
    for key, row in data["Phases"].items():
        try:
            order = int(row["Order"])
            if order < 1 or order in orders:
                raise ValueError()
            orders.append(order)
        except ValueError:
            error("PHASE_ORDER", f"{key}: eindeutige positive Order erwartet")
        for dep in split(row["Depends"]):
            if dep not in data["Phases"]:
                error("PHASE_REF", f"{key}: unbekannte Abhängigkeit {dep}")
            elif row["Order"].isdigit() and data["Phases"][dep]["Order"].isdigit() and int(data["Phases"][dep]["Order"]) >= int(row["Order"]):
                error("PHASE_ORDER", f"{key}: Abhängigkeit {dep} liegt nicht davor")
    used_requirements = set()
    for key, row in data["UseCases"].items():
        if row["Phase"] not in data["Phases"] or row["Review"] not in {"required", "none"}:
            error("USE_CASE", f"{key}: Phase oder Review ungültig")
        if not split(row["Requirements"]) or not set(split(row["Requirements"])) <= data["Requirements"].keys():
            error("REQUIREMENT_REF", f"{key}: Anforderungen fehlen oder sind unbekannt")
    for key, row in data["Tasks"].items():
        if row["Phase"] not in data["Phases"] or row["UseCase"] not in data["UseCases"]:
            error("TASK_PARENT", f"{key}: Phase oder UseCase unbekannt")
        elif row["Phase"] != data["UseCases"][row["UseCase"]]["Phase"]:
            error("TASK_PARENT", f"{key}: Phase stimmt nicht mit UseCase überein")
        refs = set(split(row["Requirements"]))
        used_requirements |= refs
        if not refs or not refs <= data["Requirements"].keys():
            error("REQUIREMENT_REF", f"{key}: Anforderungen fehlen oder sind unbekannt")
        elif row["UseCase"] in data["UseCases"] and not refs <= set(split(data["UseCases"][row["UseCase"]]["Requirements"])):
            error("REQUIREMENT_REF", f"{key}: Anforderungen stimmen nicht mit UseCase überein")
        checks = set(split(row["Verify"]))
        if not checks or not checks <= CHECKS or not (checks & UI) <= targets:
            error("VERIFY", f"{key}: passende Prüfumgebungen benennen")
        if not meaningful(row["Accept"]) or row["Mode"] not in {"normal", "fixture", "any"}:
            error("ACCEPT", f"{key}: Kriterium oder Modus ungültig")
        if checks & UI and data["UseCases"].get(row["UseCase"], {}).get("Review") != "required":
            error("UI_REVIEW", f"{key}: vollständiger UI-UseCase benötigt Kritik")
        for dep in split(row["Depends"]):
            if dep not in data["Tasks"]:
                error("TASK_REF", f"{key}: unbekannte Abhängigkeit {dep}")
        for value in split(row["Files"]):
            local_file(data["root"], value)
    for name in ("Phases", "Tasks"):
        if cycle(data[name], "Depends"):
            error("CYCLE", f"Zyklus in {name}")
    for ref in data["Requirements"].keys() - used_requirements:
        (errors if needs_ready else warnings).append(f"UNCOVERED_REQUIREMENT: {ref}")
    for ref in data["Requirements"]:
        relevant_tasks = [key for key, row in data["Tasks"].items() if ref in split(row["Requirements"])]
        if relevant_tasks and all(data["TrackTasks"].get(key, {}).get("Status") == "NICHT_ZUTREFFEND" for key in relevant_tasks):
            error("UNCOVERED_REQUIREMENT", f"{ref}: alle zugeordneten Aufgaben ausgenommen")
    if needs_ready:
        for target in targets:
            if not any(target in split(row["Verify"]) and row["Mode"] == "normal" and data["TrackTasks"].get(key, {}).get("Status") != "NICHT_ZUTREFFEND" for key, row in data["Tasks"].items()):
                error("TARGET_COVERAGE", f"{target}: normalen UI-Nutzerablauf einplanen")
    for name, field in (("Phases", "Phase"), ("UseCases", "UseCase")):
        for ref in data[name]:
            if not any(row[field] == ref for row in data["Tasks"].values()):
                (errors if needs_ready else warnings).append(f"EMPTY_SCOPE: {ref}")
    if errors:
        return errors, warnings
    for eid, row in data["Evidence"].items():
        if not re.fullmatch(r"E\d+", eid) or row["Task"] not in data["Tasks"]:
            error("EVIDENCE_REF", f"{eid}: unbekannter Task oder ungültige ID")
        checks = set(split(row["Checks"]))
        if not checks or not checks <= CHECKS:
            error("EVIDENCE_CHECKS", f"{eid}: unbekannte Prüfumgebung")
        if row["Method"] not in {"ui", "inspection", "unit", "build"} or (checks & UI and row["Method"] != "ui"):
            error("EVIDENCE_METHOD", f"{eid}: Methode belegt diese Umgebung nicht")
        if any(c in {"inspection", "unit", "build"} and row["Method"] != c for c in checks):
            error("EVIDENCE_METHOD", f"{eid}: Prüfmethode passt nicht")
        if row["Mode"] not in {"normal", "fixture", "code"} or row["Result"] not in {"PASS", "FAIL"}:
            error("EVIDENCE_VALUE", f"{eid}: Modus oder Ergebnis ungültig")
        try:
            timestamp = datetime.fromisoformat(row["Date"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None or timestamp > datetime.now(timezone.utc):
                raise ValueError()
        except ValueError:
            error("EVIDENCE_DATE", f"{eid}: tatsächlichen Zeitpunkt mit Zeitzone angeben")
        if not meaningful(row["Build"]) or not re.fullmatch(r"[a-f0-9]{24}", row["Fingerprint"]):
            error("EVIDENCE_STAND", f"{eid}: Build-/Quellstand fehlt")
        path = local_file(data["root"], row["Report"])
        if not path.is_file() or not path.stat().st_size:
            error("MISSING_REPORT", f"{eid}: {row['Report']}")
    decisive = {row["Scope"]: rid for rid, row in data["Reviews"].items()}
    for rid, row in data["Reviews"].items():
        if not re.fullmatch(r"RV\d+", rid) or row["Scope"] not in {"PLAN", *data["UseCases"]}:
            error("REVIEW_SCOPE", f"{rid}: Scope muss PLAN oder ein UseCase sein")
        if row["Kind"] not in {"independent", "self"} or row["Result"] not in {"PASS", "REWORK", "BLOCKED"}:
            error("REVIEW_VALUE", f"{rid}: Kind oder Result ungültig")
        if not re.fullmatch(r"[a-f0-9]{24}", row["Fingerprint"]):
            error("REVIEW_STAND", f"{rid}: Fingerprint fehlt")
        path = local_file(data["root"], row["Report"])
        if not path.is_file() or not path.stat().st_size:
            error("MISSING_REPORT", f"{rid}: {row['Report']}")
        if row["Kind"] == "self" and decisive[row["Scope"]] == rid:
            warnings.append(f"SELF_REVIEW: {rid}: keine unabhängige Abnahme")
    if errors:
        return errors, warnings
    for key, tracker in data["TrackTasks"].items():
        task = data["Tasks"][key]
        status = tracker["Status"]
        if status not in STATUSES:
            error("STATUS", f"{key}: unbekannter Status {status}")
        if status in {"BLOCKIERT", "NICHT_ZUTREFFEND"} and not meaningful(tracker["Reason"]):
            error("REASON", f"{key}: Ursache oder Ausnahme begründen")
        ids = split(tracker["Evidence"])
        for eid in ids:
            if eid not in data["Evidence"] or data["Evidence"][eid]["Task"] != key:
                error("EVIDENCE_REF", f"{key}: {eid} fehlt oder gehört zu anderem Task")
        if status == "ERLEDIGT":
            verified = set()
            for eid in ids:
                row = data["Evidence"].get(eid)
                if not row or row["Task"] != key:
                    continue
                if row["Fingerprint"] != task_fingerprint(data, key):
                    error("STALE_EVIDENCE", f"{key}/{eid}: Kriterien oder benannte Quellen haben sich geändert")
                elif row["Result"] == "PASS" and (task["Mode"] == "any" or row["Mode"] == task["Mode"]):
                    verified |= set(split(row["Checks"]))
            missing = set(split(task["Verify"])) - verified
            if missing:
                error("UNVERIFIED", f"{key}: aktueller passender Nachweis fehlt für {sorted(missing)}")
            if set(split(task["Verify"])) - {"inspection"} and not split(task["Files"]):
                error("SOURCE_SCOPE", f"{key}: geprüfte Quelldateien in Files benennen")
            for value in split(task["Files"]):
                if not local_file(data["root"], value).is_file():
                    error("SOURCE_MISSING", f"{key}: {value}")
        if status in {"IN_ARBEIT", "ZUR_PRUEFUNG", "ERLEDIGT"}:
            for dep in split(task["Depends"]):
                if data["TrackTasks"][dep]["Status"] not in TERMINAL:
                    error("DEPENDENCY_OPEN", f"{key}: {dep} ist offen")
            for dep in split(data["Phases"][task["Phase"]]["Depends"]):
                if not phase_closed(data, dep):
                    error("PHASE_OPEN", f"{key}: Phase {dep} einschließlich Kritik ist offen")
    for key, row in data["Checklist"].items():
        if row["Applies"] == "YES" and all(data["TrackTasks"][ref]["Status"] == "NICHT_ZUTREFFEND" for ref in split(row["Tasks"])):
            error("UNCOVERED_CHECK", f"{key}: alle zugeordneten Tasks sind ausgenommen")
    if is_complete and not errors and "Personalization" in data:
        validate_context(data, needs_ready, True, error, warnings)
    if needs_ready and not review_passed(data, "PLAN"):
        error("PLAN_REVIEW", "Aktuelle Planprüfung fehlt oder verlangt Nacharbeit")
    if phase:
        if phase not in data["Phases"] or not phase_closed(data, phase):
            error("PHASE_INCOMPLETE", f"{phase}: Aufgaben oder aktuelle Kritik offen")
    if is_complete:
        for key in data["Phases"]:
            if not phase_closed(data, key):
                error("PHASE_INCOMPLETE", f"{key}: Aufgaben oder aktuelle Kritik offen")
    if check_state:
        state = data["state"]
        if state.get("schema") != SCHEMA or state.get("status") not in {"ACTIVE", "COMPLETE"}:
            error("STATE", "Schema oder Status ungültig")
        if state.get("plan_sha256") != sha(data["PLAN.md"].encode()) or state.get("tracker_sha256") != sha(data["TRACKER.md"].encode()):
            error("STATE_STALE", "Plan/Tracker geändert; nach Abgleich mit state aktualisieren")
        task_id = state.get("task")
        if state.get("status") == "ACTIVE":
            task = data["Tasks"].get(task_id)
            if not task or state.get("phase") != task["Phase"] or state.get("use_case") != task["UseCase"]:
                error("STATE_REF", "Aktive Phase, UseCase und Task widersprechen dem Plan")
            if not meaningful(state.get("next", "")):
                error("STATE_NEXT", "Konkreter nächster Schritt fehlt")
        elif any(state.get(k) != "-" for k in ("phase", "use_case", "task")):
            error("STATE_REF", "Abgeschlossenes Projekt hat noch aktive Referenzen")
    return errors, warnings


def table_line(values):
    return "| " + " | ".join(str(x).replace("|", r"\|").replace("\n", " ") for x in values) + " |"


def render_table(headers, rows):
    return "\n".join([table_line(headers), table_line(["---"] * len(headers)), *[table_line([row.get(h, "-") for h in headers]) for row in rows]])


def template(name, values):
    text = read(BUNDLE / "assets" / name)
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    if re.search(r"\{\{[A-Z_]+\}\}", text):
        raise Invalid(f"TEMPLATE: nicht ausgefüllte Variable in {name}")
    return text


def state_text(data, task_id, next_step, complete=False):
    task = data["Tasks"].get(task_id, {})
    return template("STATE.md", {
        "STATUS": "COMPLETE" if complete else "ACTIVE", "TASK": task_id or "-",
        "PHASE": task.get("Phase", "-"), "USE_CASE": task.get("UseCase", "-"),
        "NEXT": next_step, "UPDATED": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "PLAN_SHA": sha(data["PLAN.md"].encode()), "TRACKER_SHA": sha(data["TRACKER.md"].encode()),
    })


def write_document(data, name, content):
    """Replace exactly one project document atomically; refuse if a source document changed since loading."""
    root = data["root"]
    if any(read(root / filename) != data[filename] for filename in ("PLAN.md", "TRACKER.md", "STATE.md")):
        raise Invalid("CONCURRENT_CHANGE: Stand erneut lesen")
    path = root / name
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, prefix=".workflow-", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def next_id(rows, prefix):
    numbers = [int(key[len(prefix):]) for key in rows if re.fullmatch(prefix + r"\d+", key)]
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def report_file(root, value):
    path = local_file(root, value)
    if not path.is_file() or not path.stat().st_size:
        raise Invalid(f"MISSING_REPORT: {value}")
    return value


def refs(value):
    return ",".join(split(value)) or "-"


def tracker_text(data, section, headers, row, replace=False):
    """TRACKER.md with one row appended to or replaced in a table; every other line stays as it is."""
    text = data["TRACKER.md"]
    lines = text.split("\n")
    rows = table_rows(text, section)
    line = table_line([row.get(h, "-") for h in headers.split()])
    if replace:
        matches = [index for index in rows[2:] if cells(lines[index])[0] == row["ID"]]
        if len(matches) != 1:
            raise Invalid(f"TRACKER: Zeile {row['ID']} in {section} nicht eindeutig")
        lines[matches[0]] = line
    else:
        lines.insert(rows[-1] + 1, line)
    return "\n".join(lines)


def update_tracker(data, section, headers, row, replace=False):
    """Write one tracker row unless the validator attributes an error to that row."""
    text = tracker_text(data, section, headers, row, replace)
    candidate = parse(data["root"], {**{name: data[name] for name in FILES}, "TRACKER.md": text})
    mention = re.compile(r"(?<![A-Za-z0-9])" + re.escape(row["ID"]) + r"(?!\d)")
    errors = [item for item in validate(candidate, check_state=False)[0] if mention.search(item)]
    if errors:
        raise Invalid("\n".join(errors))
    write_document(data, "TRACKER.md", text)


def initialize(args):
    root = args.project.resolve()
    modules = split(args.modules)
    targets = set(split(args.targets))
    if not targets or not targets <= PROFILES[args.profile]:
        raise Invalid("TARGETS: explizite passende Zielumgebungen angeben")
    deliveries = delivery_specs(args.delivery, targets)
    preferences = personalization(args.user_profile)
    catalog, switches = catalogue(args.profile, modules, deliveries)
    if not meaningful(args.goal) or "\n" in args.goal or "\r" in args.goal:
        raise Invalid("GOAL: ein konkretes einzeiliges Ziel angeben")
    files = ["AGENTS.md", "PLAN.md", "TRACKER.md", "STATE.md"] + (["CLAUDE.md"] if args.claude else [])
    conflicts = [name for name in files if (root / name).exists() or (root / name).is_symlink()]
    if conflicts:
        raise Invalid(f"EXISTS: vorhandene Dateien bleiben erhalten: {', '.join(conflicts)}. Entwurf separat erzeugen und gezielt integrieren.")
    checklist = [{"ID": key, "Check": row["Check"], "Applies": "UNKNOWN"} for key, row in catalog.items()]
    decisions = [{"ID": key, "Applies": "YES" if key in modules else "UNKNOWN", "Reason": "Im Auftrag ausgewählt" if key in modules else "-"} for key in switches]
    values = {"PROFILE": args.profile, "TARGETS": ", ".join(split(args.targets)), "GOAL": args.goal.replace("|", r"\|"),
              "TOOL": "`python3 " + shlex.quote(str(Path(__file__).resolve())) + "`",
              "MODULES": render_table(HEADERS["Modules"].split(), decisions),
              "CHECKLIST": render_table(HEADERS["Checklist"].split(), checklist),
              "PERSONALIZATION": render_table(HEADERS["Personalization"].split(), preferences),
              "DELIVERY": render_table(HEADERS["Delivery"].split(), deliveries)}
    contents = {name: template(name, values) for name in files if name not in {"STATE.md", "CLAUDE.md"}}
    seed = {**contents, "Tasks": {"T001": {"Phase": "P01", "UseCase": "UC01"}}}
    contents["STATE.md"] = state_text(seed, "T001", "Auftrag, Zusatzmodule und Katalog einordnen; den Plan konkretisieren.")
    if args.claude:
        contents["CLAUDE.md"] = "@AGENTS.md\n"
    root.mkdir(parents=True, exist_ok=True)
    written = {}
    try:
        for name, content in contents.items():
            with (root / name).open("x", encoding="utf-8") as handle:
                handle.write(content)
            written[name] = content
    except OSError:
        for name, content in written.items():
            path = root / name
            if not path.is_symlink() and path.is_file() and path.read_text(encoding="utf-8") == content:
                path.unlink()
        raise
    print(f"INITIALIZED: {root}\nProfil {args.profile}; {len(catalog)} Checks; Planungsstand mit offenen Einordnungen.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Projekt-Markdown erzeugen; vorhandene Dateien niemals überschreiben")
    init.add_argument("project", type=Path)
    init.add_argument("--profile", choices=PROFILES, required=True)
    init.add_argument("--targets", required=True)
    init.add_argument("--goal", required=True)
    init.add_argument("--modules", default="")
    init.add_argument("--user-profile", type=Path, help="bekannte Standards aus einem Markdown-Nutzerprofil übernehmen")
    init.add_argument("--delivery", default="", help="plattform:kanal:endzustand, mehrere durch Komma; ungewählte Wege bleiben offen")
    init.add_argument("--claude", action="store_true", help="CLAUDE.md mit @AGENTS.md erzeugen")
    cat = sub.add_parser("catalog", help="Gewählten Katalog als Markdown anzeigen")
    cat.add_argument("--profile", choices=PROFILES, required=True)
    cat.add_argument("--modules", default="")
    cat.add_argument("--delivery", default="")
    cat.add_argument("--version", choices=sorted(SUPPORTED_VERSIONS), default=VERSION)
    pref = sub.add_parser("profile", help="neues wiederverwendbares Markdown-Nutzerprofil erzeugen")
    pref.add_argument("path", type=Path)
    for cmd in ("check", "status", "fingerprint", "state"):
        p = sub.add_parser(cmd)
        p.add_argument("project", type=Path)
        if cmd in {"check", "status"}:
            p.add_argument("--json", action="store_true")
        if cmd == "check":
            p.add_argument("--ready", action="store_true", help="vollständige Planung einschließlich aktueller Kritik")
            p.add_argument("--complete", action="store_true", help="alle Phasen und Nachweise abgeschlossen")
            p.add_argument("--release", action="store_true", help="Gesamtabschluss einschließlich nichtlokalem Auslieferungsziel prüfen")
            p.add_argument("--phase", help="Abschluss genau dieser Phase prüfen")
        elif cmd == "fingerprint":
            p.add_argument("--scope", required=True)
        elif cmd == "state":
            p.add_argument("--task")
            p.add_argument("--next", default="")
            p.add_argument("--complete", action="store_true")
    writers = {name: sub.add_parser(name, help=text) for name, text in (
        ("evidence", "Beleg für den gerade geprüften Stand in TRACKER.md eintragen"),
        ("review", "Kritikerurteil für PLAN oder einen Use Case eintragen"),
        ("release", "beobachteten Auslieferungszustand eintragen"),
        ("task", "Aufgabenzeile in TRACKER.md anlegen oder ändern"))}
    for p in writers.values():
        p.add_argument("project", type=Path)
    writers["evidence"].add_argument("--task", required=True)
    writers["evidence"].add_argument("--checks", required=True, help="tatsächlich geprüfte Ziele, etwa ios-simulator,android oder unit")
    writers["evidence"].add_argument("--mode", choices=["normal", "fixture", "code"], required=True)
    writers["evidence"].add_argument("--build", required=True, help="identifizierbarer Code-/Buildstand")
    writers["evidence"].add_argument("--report", required=True, help="relative, vorhandene Berichtsdatei")
    writers["evidence"].add_argument("--result", choices=["PASS", "FAIL"], required=True)
    writers["review"].add_argument("--scope", required=True, help="PLAN oder Use-Case-ID")
    writers["review"].add_argument("--kind", choices=["independent", "self"], required=True)
    writers["review"].add_argument("--result", choices=["PASS", "REWORK", "BLOCKED"], required=True)
    writers["review"].add_argument("--report", required=True)
    writers["release"].add_argument("--delivery", required=True)
    writers["release"].add_argument("--stage", choices=sorted(RELEASE_STAGES, key=RELEASE_STAGES.get), required=True)
    writers["release"].add_argument("--build", required=True)
    writers["release"].add_argument("--locator", required=True)
    writers["release"].add_argument("--evidence", default="", help="aktuelle PASS-Belege, kommagetrennt")
    writers["task"].add_argument("task")
    writers["task"].add_argument("--status", choices=sorted(STATUSES))
    writers["task"].add_argument("--evidence", help="maßgebliche Beleg-IDs, kommagetrennt; - für keine")
    writers["task"].add_argument("--reason")
    args = parser.parse_args(argv)
    try:
        if args.command == "profile":
            path = args.path.expanduser().absolute()
            if path.exists() or path.is_symlink():
                raise Invalid("EXISTS: vorhandenes Nutzerprofil bleibt unverändert")
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8") as handle:
                handle.write(read(BUNDLE / "assets/USER_PROFILE.md"))
            print(f"PROFILE_CREATED: {path}; Standards konkretisieren, keine Zugangsdaten eintragen")
            return 0
        if args.command == "init":
            initialize(args)
            return 0
        if args.command == "catalog":
            deliveries = delivery_specs(args.delivery, PROFILES[args.profile])
            rows, _ = catalogue(args.profile, split(args.modules), deliveries, args.version)
            print(render_table(HEADERS["Checks"].split(), rows.values()))
            return 0
        data = load(args.project.resolve())
        if args.command == "fingerprint":
            print(fingerprint(data, args.scope))
            return 0
        if args.command == "state":
            if not args.complete and (args.task not in data["Tasks"] or not meaningful(args.next) or "\n" in args.next):
                raise Invalid("STATE: --task und einen konkreten einzeiligen --next angeben")
            errors, _ = validate(data, complete=args.complete, check_state=False)
            if errors:
                raise Invalid("\n".join(errors))
            content = state_text(data, None if args.complete else args.task, "Ziel nachweislich abgeschlossen." if args.complete else args.next, args.complete)
            write_document(data, "STATE.md", content)
            print("STATE_UPDATED: Referenzen und Dokumentstand aktualisiert.")
            return 0
        if args.command == "evidence":
            if args.task not in data["Tasks"]:
                raise Invalid(f"TASK: unbekannte Aufgabe {args.task}")
            checks = split(args.checks)
            if not checks or not set(checks) <= CHECKS:
                raise Invalid("EVIDENCE_CHECKS: tatsächlich geprüfte Zielumgebungen benennen")
            method = "ui" if set(checks) <= UI else checks[0] if len(set(checks)) == 1 else None
            if not method:
                raise Invalid("EVIDENCE_METHOD: UI-Ziele oder genau eines von inspection, unit, build")
            if not meaningful(args.build):
                raise Invalid("EVIDENCE_STAND: identifizierbaren Code-/Buildstand angeben")
            row = {"ID": next_id(data["Evidence"], "E"), "Task": args.task, "Checks": ",".join(checks), "Method": method, "Mode": args.mode,
                   "Date": datetime.now(timezone.utc).isoformat(timespec="seconds"), "Build": args.build, "Fingerprint": fingerprint(data, args.task),
                   "Report": report_file(data["root"], args.report), "Result": args.result}
            update_tracker(data, "Evidence", HEADERS["Evidence"], row)
            print(f"EVIDENCE_RECORDED: {row['ID']} für {args.task}, {args.result}, Fingerprint {row['Fingerprint']}. Aufgabenzeile mit task nachführen, danach state.")
            return 0
        if args.command == "review":
            if args.scope != "PLAN" and args.scope not in data["UseCases"]:
                raise Invalid(f"REVIEW_SCOPE: PLAN oder Use-Case-ID erwartet, nicht {args.scope}")
            row = {"ID": next_id(data["Reviews"], "RV"), "Scope": args.scope, "Kind": args.kind, "Result": args.result,
                   "Fingerprint": fingerprint(data, args.scope), "Report": report_file(data["root"], args.report)}
            update_tracker(data, "Reviews", HEADERS["Reviews"], row)
            print(f"REVIEW_RECORDED: {row['ID']} {args.scope} {args.result} ({args.kind}), Fingerprint {row['Fingerprint']}. Danach state ausführen.")
            return 0
        if args.command == "release":
            if "Releases" not in data:
                raise Invalid("RELEASE_SCOPE: Auslieferungsnachweise benötigen einen Plan der Vorlage 1.1")
            if args.delivery not in data["Delivery"]:
                raise Invalid(f"DELIVERY: unbekanntes Auslieferungsziel {args.delivery}")
            if not meaningful(args.build) or not meaningful(args.locator):
                raise Invalid("RELEASE_RECORD: Build und konkreten Artefakt-/Release-Verweis angeben")
            row = {"ID": next_id(data["Releases"], "L"), "Delivery": args.delivery, "Stage": args.stage, "Build": args.build, "Locator": args.locator, "Evidence": refs(args.evidence)}
            update_tracker(data, "Releases", HEADERS["Releases"], row)
            print(f"RELEASE_RECORDED: {row['ID']} {args.delivery} {args.stage}, Build {args.build}. Zugehörige Use-Case-Kritik nach diesem Eintrag erfassen, danach state ausführen.")
            return 0
        if args.command == "task":
            if args.task not in data["Tasks"]:
                raise Invalid(f"TASK: unbekannte Aufgabe {args.task}")
            current = data["TrackTasks"].get(args.task, {})
            row = {"ID": args.task, "Status": args.status or current.get("Status", "OFFEN"),
                   "Evidence": refs(args.evidence) if args.evidence is not None else current.get("Evidence", "-"),
                   "Reason": (args.reason or "-") if args.reason is not None else current.get("Reason", "-")}
            update_tracker(data, "Tasks", HEADERS["TrackTasks"], row, replace=bool(current))
            print(f"TASK_UPDATED: {args.task} {row['Status']}. Danach state --task <ID> --next '<Schritt>' und check ausführen.")
            return 0
        errors, warnings = validate(data, ready=getattr(args, "ready", False), complete=getattr(args, "complete", False), phase=getattr(args, "phase", None), release=getattr(args, "release", False))
        result = {"valid": not errors, "errors": errors, "warnings": warnings, "state": data["state"], "tasks": {key: row["Status"] for key, row in data["TrackTasks"].items()}}
        if getattr(args, "json", False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("CHECK_FAILED" if errors else "STRUCTURE_OK (kein Nachweis der Produktqualität)")
            for item in errors + warnings:
                print(item)
            if args.command == "status":
                print(f"Aktiv: {data['state'].get('phase')} / {data['state'].get('use_case')} / {data['state'].get('task')}")
                print(f"Nächster Schritt: {data['state'].get('next')}")
                for key, status in result["tasks"].items():
                    print(f"{key}: {status}")
        return 1 if errors else 0
    except (Invalid, OSError, KeyError, ValueError) as exc:
        if getattr(args, "json", False):
            print(json.dumps({"valid": False, "errors": [str(exc)], "warnings": []}, ensure_ascii=False))
        else:
            print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
