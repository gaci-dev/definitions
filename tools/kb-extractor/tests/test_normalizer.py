from __future__ import annotations

import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from gxkb.errors import GXKBError
from gxkb import cli as cli_module
from gxkb.cli import build_parser
from gxkb import normalizer as normalizer_module
from gxkb.normalizer import normalize, validate_output
from gxkb.gx9_references import mask_source, extract


def test_element_path_cache_matches_legacy_api() -> None:
    root = ET.fromstring("<Root><Item><Child /></Item><Item><Child /></Item></Root>")
    paths = normalizer_module._element_paths(root)
    assert [normalizer_module._element_path(root, node) for node in root.iter()] == [paths[id(node)] for node in root.iter()]
    assert paths[id(list(root)[1])] == "Root[1]/Item[2]"


def test_gx9_reference_spans_are_exact_for_multiline_source() -> None:
    source = "FOR EACH T\nWHERE A = 1\nCALL(P)"
    refs = extract(source, {"A"}, set())
    assert [(item["target_name"], item["span"]) for item in refs] == [
        ("T", {"start": 0, "end": 11, "line": 1, "column": 1, "end_line": 2, "end_column": 1}),
        ("A", {"start": 17, "end": 18, "line": 2, "column": 7, "end_line": 2, "end_column": 8}),
        ("P", {"start": 28, "end": 29, "line": 3, "column": 6, "end_line": 3, "end_column": 7}),
    ]


def test_redaction_contract_sanitizes_exported_source_values(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    output = tmp_path / "out"
    source.write_text(
        r'<ExportFile><Source kb="kb-1" path="C:\Users\julian\secret.xml"/><Objects><Object guid="a" fullyQualifiedName="Demo.A" description="Owner JULIA-NOTE\julian"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    normalize(source, output, redact_source=True)
    output_text = "\n".join(path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file())
    assert "C:\\Users\\julian" not in output_text
    assert "JULIA-NOTE\\julian" not in output_text
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["share_safe"] is False


def test_redaction_replaces_posix_paths_with_spaces_without_leaking_suffix() -> None:
    value = "Exported from /srv/Project Files/private/export.xml; keep relative objects/Demo/A."
    redacted = normalizer_module._redact_value(value)
    assert "/srv/Project Files/private/export.xml" not in redacted
    assert "Files/private/export.xml" not in redacted
    assert "Exported from [REDACTED_PATH]; keep relative objects/Demo/A." == redacted


def test_legacy_migration_remaps_accumulated_parts_references_and_dependencies() -> None:
    records = [
        {"record_type": "object", "id": "old-object", "name": "A", "fully_qualified_name": "Demo.A", "part_ids": ["old-part"]},
        {"record_type": "part", "id": "old-part", "object_id": "old-object", "type": "unknown", "content": "part"},
        {"record_type": "reference", "id": "old-reference", "object_id": "old-object", "part_id": "old-part", "raw": "ref"},
        {"record_type": "dependency", "from_object_id": "old-object", "reference_id": "old-reference", "relation": "explicit_reference"},
    ]
    migrated = normalizer_module._migrate_legacy_records(records)
    object_record = next(record for record in migrated if record["record_type"] == "object")
    part_record = next(record for record in migrated if record["record_type"] == "part")
    reference = next(record for record in migrated if record["record_type"] == "reference")
    dependency = next(record for record in migrated if record["record_type"] == "dependency")
    assert object_record["part_ids"] == [part_record["id"]]
    assert reference["object_id"] == object_record["id"] and reference["part_id"] == part_record["id"]
    assert dependency["from_object_id"] == object_record["id"] and dependency["reference_id"] == reference["id"]
    assert all(record["schema_version"] == 1 for record in migrated)


def test_legacy_migration_rejects_stale_part_ids() -> None:
    records = [{"record_type": "object", "id": "old-object", "name": "A", "fully_qualified_name": "Demo.A", "part_ids": ["missing"]}]
    with pytest.raises(GXKBError, match="stale object.part_ids"):
        normalizer_module._migrate_legacy_records(records)


@pytest.mark.parametrize("bad_path", ["../outside", "/tmp/outside"])
def test_legacy_migration_rejects_unsafe_paths_before_touching_output(tmp_path: Path, bad_path: str) -> None:
    output = tmp_path / "out"
    (output / "canonical").mkdir(parents=True)
    (output / "objects" / "Demo" / "A").mkdir(parents=True)
    (output / "objects" / "Demo" / "A" / "marker.txt").write_text("keep", encoding="utf-8")
    (output / "canonical" / "records.jsonl").write_text(
        json.dumps({"record_type": "object", "id": "old-object", "name": "A", "fully_qualified_name": "Demo.A", "normalized_path": bad_path}) + "\n",
        encoding="utf-8",
    )
    source = tmp_path / "input.xml"
    source.write_text('<ExportFile><Objects><Object guid="new" fullyQualifiedName="Demo.New"/></Objects></ExportFile>', encoding="utf-8")
    with pytest.raises(GXKBError, match="absolute and traversal paths"):
        normalize(source, output)
    assert (output / "objects" / "Demo" / "A" / "marker.txt").read_text(encoding="utf-8") == "keep"


XML = """<?xml version="1.0"?><ExportFile><Source kb="kb-1"><Version guid="v1" name="Demo"/></Source><Objects><Object guid="o1" fullyQualifiedName="Ventas.Factura" name="Factura" type="trx" description="Una factura"><Part type="9b0a32a3-de6b-4be1-a4dd-1b85d3741534"><Source><![CDATA[parm(in:&Id);]]></Source></Part><Part type="unknown"><Reference guid="o2" name="Cliente"/><Source><![CDATA[contenido desconocido]]></Source></Part></Object></Objects><ObjectsIdentityMapping><Map from="o1" to="o1"/></ObjectsIdentityMapping></ExportFile>"""

SEMANTIC_XML = """<ExportFile><Objects>
<Object guid="p1" fullyQualifiedName="Demo.DoWork" type="84a12160-f59b-4ad7-a683-ea4481ac23e9"><Part type="528d1c06-a9c2-420d-bd35-21dca83f12ff"><Source>return &amp;Value</Source></Part></Object>
<Object guid="t1" fullyQualifiedName="Demo.Customer" type="1db606f2-af09-4cf9-a3b5-b481519d28f6"><Part type="264be5fb-1b28-4b25-a598-6ca900dd059f"><Level Name="Customer"><Attribute key="True" guid="a1">CustomerId</Attribute><Attribute key="False" isNullable="True" guid="a2">Name</Attribute></Level></Part><Part type="d24a58ad-57ba-41b7-9e6e-eaca3543c778"><Form type="layout"><detail><layout><table controlName="Main" /></layout></detail></Form></Part></Object>
<Object guid="s1" fullyQualifiedName="Demo.CustomerSDT" type="447527b5-9210-4523-898b-5dccb17be60a"><Part type="5c2aa9da-8fc4-4b6b-ae02-8db4fa48976a"><Level Name="Customer"><LevelInfo guid="l1" name="Customer" /><Item guid="i1" name="Id"><Properties><Property><Name>ATTCUSTOMTYPE</Name><Value>bas:Numeric</Value></Property></Properties></Item></Level></Part></Object>
 </Objects></ExportFile>"""


def _gx9_xml() -> bytes:
    return (
        '<?xml version="1.0" encoding="iso-8859-1"?>'
        '<ExportFile><GXObject><Transaction><Info>'
        '<Name>Compra</Name><Description>Facturación básica</Description><Folder>Legacy</Folder>'
        '</Info><Structure><Attribute>Id</Attribute></Structure><Variable><Variable Name="total"/></Variable>'
        '<Rules>For each Compra</Rules><Documentation>Documento GX9</Documentation></Transaction></GXObject>'
        '<GXObject><Mystery><Info><Name>SoloLegacy</Name><Folder>Legacy</Folder></Info>'
        '<Report><Line>raw report</Line></Report></Mystery></GXObject></ExportFile>'
    ).encode("iso-8859-1")


def test_gx9_xpz_adapts_metadata_parts_and_unknown_classes(tmp_path: Path) -> None:
    source = tmp_path / "legacy.xpz"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("legacy.xml", _gx9_xml())

    output = normalize(source, tmp_path / "out", preserve_raw=False)
    compra = json.loads((output / "objects/Legacy/Compra/metadata.json").read_text(encoding="utf-8"))
    unknown = json.loads((output / "objects/Legacy/SoloLegacy/metadata.json").read_text(encoding="utf-8"))
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))

    assert compra["object_kind"] == "transaction"
    assert compra["attributes"]["description"] == "Facturación básica"
    assert compra["attributes"]["legacy_class"] == "Transaction"
    assert (output / "objects/Legacy/Compra/parts/001-gx9_structure.txt").exists()
    assert (output / "objects/Legacy/Compra/parts/002-gx9_variables.txt").exists()
    compra_dir = output / "objects/Legacy/Compra"
    assert (compra_dir / "variables/variables.json").exists()
    assert not (compra_dir / "variables.json").exists()
    assert compra["parts"][1]["projection_file"] == "variables/variables.json"
    compra_parts = [
        json.loads(line)
        for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()
        if '"record_type": "part"' in line
    ]
    assert any(part.get("projection_file") == "variables/variables.json" for part in compra_parts)
    assert (output / "objects/Legacy/Compra/documentation.md").exists()
    assert unknown["object_kind"] == "unknown"
    assert unknown["attributes"]["legacy_class"] == "Mystery"
    assert any("GX9" in warning for warning in manifest["warnings"]) is False


@pytest.mark.parametrize(
    ("legacy_class", "object_kind", "type_label"),
    [
        ("Procedure", "procedure", "Procedure"),
        ("WorkPanel", "webpanel", "WebPanel"),
        ("Menubar", "menu_bar", "Menu Bar"),
        ("DataView", "data_view", "Data View"),
    ],
)
def test_gx9_object_kind_mapping_renders_canonical_metadata_and_type(
    tmp_path: Path, legacy_class: str, object_kind: str, type_label: str
) -> None:
    source = tmp_path / f"{legacy_class}.xml"
    source.write_text(
        f"<ExportFile><GXObject><{legacy_class}><Info><Name>{legacy_class}Sample</Name><Folder>Demo</Folder></Info></{legacy_class}></GXObject></ExportFile>",
        encoding="utf-8",
    )

    output = normalize(source, tmp_path / "out", preserve_raw=False)
    object_dir = output / "objects/Demo" / f"{legacy_class}Sample"
    metadata = json.loads((object_dir / "metadata.json").read_text(encoding="utf-8"))
    object_markdown = (object_dir / "object.md").read_text(encoding="utf-8")

    assert metadata["object_kind"] == object_kind
    assert f"**Type:** {type_label}" in object_markdown


def test_gxl_filters_gx9_objects_and_reports_missing_names(tmp_path: Path) -> None:
    source = tmp_path / "legacy.xpz"
    selection = tmp_path / "legacy.gxl"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("legacy.xml", _gx9_xml())
    selection.write_text(
        "<Objects><Object><ObjName>Compra</ObjName></Object><Object><ObjName>NotExported</ObjName></Object></Objects>",
        encoding="utf-8",
    )

    output = normalize(source, tmp_path / "out", gxl_selection=selection, preserve_raw=False)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["object_count"] == 1
    assert (output / "objects/Legacy/Compra/metadata.json").exists()
    assert not (output / "objects/Legacy/SoloLegacy").exists()
    assert any("NotExported" in warning for warning in manifest["warnings"])


def test_gx9_codeblocks_and_serialized_name_prefixes_are_projected_losslessly(tmp_path: Path) -> None:
    source = tmp_path / "legacy.xml"
    source.write_bytes(
        b'<ExportFile><GXObject><Report><Info><Name>RLecQR01</Name><Folder>Reports</Folder></Info>'
        b'<FormInfo><Block><CodeBlock><Source><![CDATA[print first]]></Source></CodeBlock>'
        b'<CodeBlock><Source><![CDATA[print second]]></Source></CodeBlock></Block></FormInfo></Report></GXObject>'
        b'<GXObject><Transaction><Info><Name>TCon004</Name><Folder>Transactions</Folder></Info>'
        b'<Structure><Attribute>Id</Attribute></Structure></Transaction></GXObject></ExportFile>'
    )

    output = normalize(source, tmp_path / "out", preserve_raw=False)
    report = output / "objects/Reports/LecQR01"
    transaction = output / "objects/Transactions/Con004"
    report_metadata = json.loads((report / "metadata.json").read_text(encoding="utf-8"))
    transaction_metadata = json.loads((transaction / "metadata.json").read_text(encoding="utf-8"))

    assert report_metadata["attributes"]["legacy_name"] == "RLecQR01"
    assert transaction_metadata["attributes"]["legacy_name"] == "TCon004"
    assert (report / "code.gx").read_text(encoding="utf-8").strip() == "print first"
    assert (report / "code-002.gx").read_text(encoding="utf-8").strip() == "print second"
    assert any("CodeBlock" in path.read_text(encoding="utf-8") for path in (report / "parts").glob("*.txt"))


def test_gxl_matches_normalized_gx9_names_without_false_missing_warning(tmp_path: Path) -> None:
    source = tmp_path / "legacy.xml"
    source.write_bytes(_gx9_xml().replace(b"<Name>Compra</Name>", b"<Name>TCon004</Name>"))
    selection = tmp_path / "legacy.gxl"
    selection.write_text("<Objects><Object><ObjName>Con004</ObjName></Object></Objects>", encoding="utf-8")

    output = normalize(source, tmp_path / "out", gxl_selection=selection, preserve_raw=False)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["object_count"] == 1
    assert (output / "objects/Legacy/Con004/metadata.json").exists()
    assert not any("Con004" in warning for warning in manifest["warnings"])


def test_gx9_structure_projection_parses_nested_groups_and_preserves_unknowns(tmp_path: Path) -> None:
    source = tmp_path / "nested-gx9.xml"
    source.write_text(
        """<ExportFile><GXObject><Transaction><Info><Name>TOrder</Name><Folder>Legacy</Folder></Info>
        <Structure>(Order (OrderId* Customer), Lines (LineId* Amount)) ???</Structure>
        </Transaction></GXObject></ExportFile>""",
        encoding="utf-8",
    )

    output = normalize(source, tmp_path / "out", preserve_raw=False)
    structure = json.loads((output / "objects/Legacy/Order/structure.json").read_text(encoding="utf-8"))
    assert structure["kind"] == "legacy_structure"
    assert structure["level_count"] == 2
    assert structure["attribute_count"] == 4
    assert structure["levels"][0]["name"] == "Order"
    assert structure["levels"][0]["items"][0] == {"name": "OrderId", "key": True}
    assert structure["levels"][1]["name"] == "Lines"
    assert "???" in structure["unknown_fragments"]
    assert "Structure" in (output / "objects/Legacy/Order/parts/001-gx9_structure.txt").read_text(encoding="utf-8")


def test_gx9_variables_based_on_are_canonical_dependencies_and_graph_edges(tmp_path: Path) -> None:
    source = tmp_path / "variables-gx9.xml"
    source.write_text(
        """<ExportFile><Objects><Object fullyQualifiedName="Demo.Customer" guid="modern-target" /></Objects>
        <GXObject><Transaction><Info><Name>TOrder</Name><Folder>Demo</Folder></Info>
        <Variable><Name>customer</Name><BasedOn>Demo.Customer</BasedOn><Type>Customer</Type></Variable>
        <Variable><Name>missing</Name><BasedOn>Demo.Missing</BasedOn></Variable></Transaction></GXObject></ExportFile>""",
        encoding="utf-8",
    )

    output = normalize(source, tmp_path / "out", preserve_raw=False)
    order = output / "objects/Demo/Order"
    variables = json.loads((order / "variables/variables.json").read_text(encoding="utf-8"))
    assert variables["variables"][0]["name"] == "customer"
    assert variables["variables"][0]["based_on"] == "Demo.Customer"
    assert variables["variables"][0]["type"] == "Customer"

    dependencies = json.loads((order / "dependencies.json").read_text(encoding="utf-8"))
    inferred = dependencies["inferred_dependencies"]
    resolved = next(item for item in inferred if item["target_name"] == "Demo.Customer")
    unresolved = next(item for item in inferred if item["target_name"] == "Demo.Missing")
    assert resolved["relation"] == "gx9_based_on" and resolved["resolved"] is True
    assert unresolved["relation"] == "gx9_based_on" and unresolved["resolved"] is False
    assert "raw" in resolved["evidence"] and resolved["source_location"]

    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    assert sum(record.get("record_type") == "dependency" for record in records) == 2
    assert any(record.get("relation") == "gx9_based_on" for record in records)
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(edge["kind"] == "gx9_based_on" and edge["to"] == "object:modern-target" for edge in edges)
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["dependency_count"] == 2


def test_gx9_reference_scanner_masks_comments_and_literals_preserving_spans() -> None:
    source = '"FOR EACH Fake" // CALL(Fake)\nFOR EACH Tmfa1\nWHERE Tm1Usr = &tUsr // Fake\nCALL(RealProc)'
    masked = mask_source(source)
    assert "Fake" not in masked
    refs = extract(source, {"Tm1Usr"}, set())
    assert [(item["relation"], item["target_name"]) for item in refs] == [
        ("gx9_for_each", "Tmfa1"), ("gx9_attribute_mention", "Tm1Usr"), ("gx9_call", "RealProc")
    ]
    assert refs[0]["span"]["line"] == 2


def test_gx9_source_references_resolve_calls_for_each_attributes_and_incoming_references(tmp_path: Path) -> None:
    source = tmp_path / "gx9.xml"
    source.write_text(
        """<ExportFile><GXObject><Transaction><Info><Name>TTmfa1</Name><Folder>Demo</Folder></Info>
        <Structure><Attribute>Tm1Usr</Attribute><Attribute>Tm1ImpAnt</Attribute></Structure></Transaction></GXObject>
        <GXObject><Procedure><Info><Name>PCmp172</Name><Folder>Demo</Folder></Info><CodeBlock><Source><![CDATA[
        FOR EACH Tmfa1
        WHERE Tm1Usr = &amp;tUsr
        DEFINED BY Tm1ImpAnt
        CALL(UnknownProc)
        Tmfa1.Call()
        ]]></Source></CodeBlock></Procedure></GXObject></ExportFile>""",
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out", preserve_raw=False)
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    gx9 = [record for record in records if record.get("relation", "").startswith("gx9_")]
    assert {record["relation"] for record in gx9} == {"gx9_for_each", "gx9_attribute_mention", "gx9_call"}
    assert any(record["target_name"] == "UnknownProc" and not record["resolved"] for record in gx9)
    assert all("reference_kind" in record and "span" in record["evidence"] for record in gx9)
    assert sum(record["resolved"] for record in gx9 if record["target_name"] in {"Tmfa1", "Tm1Usr", "Tm1ImpAnt"}) >= 3
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(edge["kind"] == "gx9_for_each" for edge in edges)
    assert any(edge["kind"] == "gx9_attribute_mention" for edge in edges)
    incoming = json.loads((output / "objects/Demo/Tmfa1/incoming-references.json").read_text(encoding="utf-8"))
    assert any(item["relation"] == "gx9_for_each" for item in incoming)
    validate_output(output)


def test_gx9_attribute_ambiguity_is_preserved_without_graph_edge(tmp_path: Path) -> None:
    source = tmp_path / "ambiguous-gx9.xml"
    source.write_text(
        """<ExportFile><GXObject><Transaction><Info><Name>TT</Name><Folder>One</Folder></Info><Structure><Attribute>Code</Attribute></Structure></Transaction></GXObject>
        <GXObject><Transaction><Info><Name>TT2</Name><Folder>Two</Folder></Info><Structure><Attribute>Code</Attribute></Structure></Transaction></GXObject>
        <GXObject><Procedure><Info><Name>P</Name><Folder>Demo</Folder></Info><Rules><Source>FOR EACH TT WHERE Code = &amp;Code</Source></Rules></Procedure></GXObject></ExportFile>""",
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out", preserve_raw=False)
    deps = json.loads((output / "objects/Demo/P/dependencies.json").read_text(encoding="utf-8"))
    ambiguous = next(item for item in deps["unresolved_references"] if item["target_name"] == "Code")
    assert ambiguous["resolved"] is False and "ambiguous" in ambiguous["unresolved_reason"]
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert not any(edge.get("kind") == "gx9_attribute_mention" for edge in edges)


def test_modern_names_are_not_prefix_normalized(tmp_path: Path) -> None:
    source = tmp_path / "modern.xml"
    source.write_text('<ExportFile><Objects><Object guid="r1" fullyQualifiedName="Demo.Report" type="report"/></Objects></ExportFile>', encoding="utf-8")

    output = normalize(source, tmp_path / "out", preserve_raw=False)
    assert (output / "objects/Demo/Report/metadata.json").exists()
    assert not (output / "objects/Demo/eport").exists()


def test_missing_gxl_is_reported_without_silently_filtering(tmp_path: Path) -> None:
    source = tmp_path / "legacy.xpz"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("legacy.xml", _gx9_xml())

    output = normalize(source, tmp_path / "out", gxl_selection=tmp_path / "missing.gxl", preserve_raw=False)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["object_count"] == 2
    assert any("GXL selection file not found" in warning for warning in manifest["warnings"])


def test_normalizes_xml_and_keeps_unknown_parts(tmp_path: Path) -> None:
    source = tmp_path / "demo.xml"
    source.write_text(XML, encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    metadata = json.loads((output / "objects/Ventas/Factura/metadata.json").read_text(encoding="utf-8"))
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert metadata["attributes"]["guid"] == "o1"
    assert (output / "objects/Ventas/Factura/rules.gx").exists()
    assert list((output / "objects/Ventas/Factura/parts").glob("*.txt"))
    assert manifest["object_count"] == 1
    assert (output / "raw/demo.xml").exists()


def test_canonical_records_and_graph_are_derived_from_objects(tmp_path: Path) -> None:
    source = tmp_path / "demo.xml"
    source.write_text(XML, encoding="utf-8")
    output = normalize(source, tmp_path / "out")

    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    nodes = [json.loads(line) for line in (output / "graph/nodes.jsonl").read_text(encoding="utf-8").splitlines()]
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    object_record = next(record for record in records if record["record_type"] == "object")
    reference = next(record for record in records if record["record_type"] == "reference")

    assert object_record["id"] == "object:o1"
    assert object_record["source_location"].endswith("Object[1]")
    assert reference["attributes"]["guid"] == "o2"
    assert not any(edge.get("reference_id") == reference["id"] for edge in edges)
    assert any(node["id"] == object_record["id"] for node in nodes)
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["outputs"]["graph_edges"] == "graph/edges.jsonl"


def test_modular_projection_boundary_is_deterministic_for_share_safe_snapshot(tmp_path: Path) -> None:
    source = tmp_path / "representative.xml"
    source.write_text(
        '<ExportFile><Source kb="kb-1"><Version guid="v1" name="Demo"/></Source><Objects>'
        '<Object guid="a" fullyQualifiedName="Demo.A"><Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">'
        '<Variable Name="customer" basedOn="Demo.B"/></Part><Part type="unknown">'
        '<Reference name="Demo.B"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.B"/>'
        '</Objects></ExportFile>',
        encoding="utf-8",
    )

    def projection_snapshot(output: Path) -> dict[str, object]:
        read_jsonl = lambda path: [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        dependencies = {
            str(path.relative_to(output)): json.loads(path.read_text(encoding="utf-8"))
            for path in output.glob("objects/**/dependencies.json")
        }
        return {
            "records": read_jsonl(output / "canonical/records.jsonl"),
            "nodes": read_jsonl(output / "graph/nodes.jsonl"),
            "edges": read_jsonl(output / "graph/edges.jsonl"),
            "dependencies": dependencies,
            "manifest": json.loads((output / "manifest.json").read_text(encoding="utf-8")),
            "canonical_manifest": json.loads((output / "canonical/manifest.json").read_text(encoding="utf-8")),
        }

    first = normalize(source, tmp_path / "first", preserve_raw=False, share_safe=True, snapshot=True)
    second = normalize(source, tmp_path / "second", preserve_raw=False, share_safe=True, snapshot=True)
    assert projection_snapshot(first) == projection_snapshot(second)
    assert projection_snapshot(first)["manifest"]["incremental"]["reconciliation"]["complete_input"] is True
    assert projection_snapshot(first)["manifest"]["share_safe"] is True


def test_shareable_output_can_omit_raw_and_redact_source(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    private_xml = XML.replace('description="Una factura"', 'description="Una factura" user="secret-user"')
    private_xml = private_xml.replace("contenido desconocido", r"JULIAN-NOTE\julian \\server\julian\share C:\Users\julian\secret")
    private_xml = private_xml.replace('<Reference guid="o2" name="Cliente"', '<Reference guid="o2" name="Cliente" path="C:\\Users\\julian\\ref"')
    source.write_text(private_xml, encoding="utf-8")
    output = normalize(source, tmp_path / "out", preserve_raw=False, redact_source=True)

    assert not (output / "raw").exists()
    object_record = next(json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines() if '"record_type": "object"' in line)
    assert object_record["attributes"]["user"] == "[REDACTED]"
    output_text = "\n".join(path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file())
    assert "JULIAN-NOTE\\julian" not in output_text
    assert "C:\\Users\\julian" not in output_text
    part_record = next(json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines() if '"record_type": "part"' in line and "REDACTED" in line)
    assert "[REDACTED_USER]" in part_record["content"]
    assert "[REDACTED_USER]" in part_record["source_xml"]


def test_redaction_covers_arbitrary_attributes_descriptions_and_all_outputs(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    private_xml = XML.replace(
        'description="Una factura"',
        r'description="Owner JULIA-NOTE\julian at C:\Users\julian\secret" arbitrary="\\server\julian\share"',
    )
    source.write_text(private_xml, encoding="utf-8")
    output = normalize(source, tmp_path / "out", redact_source=True)

    output_text = "\n".join(path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file())
    assert "JULIA-NOTE\\julian" not in output_text
    assert "C:\\Users\\julian" not in output_text
    assert "\\\\server\\julian" not in output_text
    assert "Una factura" not in output_text
    assert "Owner" in output_text


def test_fallback_ids_survive_object_and_part_insertion_or_reordering(tmp_path: Path) -> None:
    def export(objects: str) -> str:
        return f"<ExportFile><Objects>{objects}</Objects></ExportFile>"

    first = '<Object fullyQualifiedName="A.One" type="trx"><Part type="rules"><Source>one</Source></Part></Object><Object fullyQualifiedName="B.Two" type="trx"><Part type="rules"><Source>two</Source></Part></Object>'
    reordered = '<Object fullyQualifiedName="B.Two" type="trx"><Part type="rules"><Source>two</Source></Part><Part type="unknown"><Source>new</Source></Part></Object><Object fullyQualifiedName="A.One" type="trx"><Part type="rules"><Source>one</Source></Part></Object>'
    source = tmp_path / "ids.xml"
    source.write_text(export(first), encoding="utf-8")
    output1 = normalize(source, tmp_path / "out1")
    source.write_text(export(reordered), encoding="utf-8")
    output2 = normalize(source, tmp_path / "out2")
    records1 = [json.loads(line) for line in (output1 / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    records2 = [json.loads(line) for line in (output2 / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    ids1 = {(record["record_type"], record.get("fully_qualified_name"), record.get("content")): record["id"] for record in records1}
    ids2 = {(record["record_type"], record.get("fully_qualified_name"), record.get("content")): record["id"] for record in records2}
    for key, record_id in ids1.items():
        if key in ids2:
            assert ids2[key] == record_id


def test_reference_edges_preserve_multiplicity_and_locations_are_unique(tmp_path: Path) -> None:
    source = tmp_path / "refs.xml"
    source.write_text('<ExportFile><Objects><Object guid="o1" fullyQualifiedName="A.One"><Part type="unknown"><Reference guid="o2" name="one"/><Reference guid="o2" name="two"/></Part></Object></Objects></ExportFile>', encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    references = [record for record in records if record["record_type"] == "reference"]
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines() if '"kind": "references"' in line]
    assert len({reference["id"] for reference in references}) == 2
    assert len({edge["id"] for edge in edges}) == 0
    locations = [record["source_location"] for record in records]
    assert len(locations) == len(set(locations))
    assert all(not location.startswith("/") and "ExportFile" in location for location in locations)


def test_rerun_clears_only_normalizer_owned_content(tmp_path: Path) -> None:
    source = tmp_path / "demo.xml"
    output = tmp_path / "out"
    source.write_text(XML, encoding="utf-8")
    normalize(source, output)
    user_file = output / "notes.txt"
    user_file.write_text("keep", encoding="utf-8")
    source.write_text(XML.replace("Ventas.Factura", "Ventas.Nueva"), encoding="utf-8")
    normalize(source, output)
    assert user_file.read_text(encoding="utf-8") == "keep"
    assert not (output / "objects/Ventas/Factura").exists()
    assert (output / "objects/Ventas/Nueva").exists()


def test_cli_exposes_shareability_flags() -> None:
    args = build_parser().parse_args(["input.xml", "--without-raw", "--redact-source", "--share-safe", "--reprocess-all", "--snapshot"])
    assert args.without_raw is True
    assert args.redact_source is True
    assert args.reprocess_all is True
    assert args.share_safe is True
    assert args.snapshot is True


def test_normalize_reports_throttled_progress_without_changing_default_api(tmp_path: Path) -> None:
    source = tmp_path / "progress.xml"
    source.write_text(
        "<ExportFile><Objects>" + "".join(
            f'<Object guid="o{index}" fullyQualifiedName="Demo.Object{index}" />' for index in range(10)
        ) + "</Objects></ExportFile>",
        encoding="utf-8",
    )
    events: list[dict[str, object]] = []

    normalize(source, tmp_path / "out", preserve_raw=False, progress=events.append)

    stages = [event["stage"] for event in events]
    assert stages[0] == "input_preparation"
    assert {"parse_adaptation", "object_processing", "dependency_resolution", "projections_write", "validation", "commit", "complete"} <= set(stages)
    object_events = [event for event in events if event["stage"] == "object_processing" and "percent" in event]
    assert object_events[-1]["current"] == 10
    assert len(object_events) < 10
    assert object_events[-1]["processed"] == 10
    assert object_events[-1]["skipped"] == 0
    assert all(float(event["elapsed"]) >= 0 for event in events)


def test_cli_reports_progress_by_default_and_supports_quiet(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    calls: list[object] = []

    def fake_normalize(*args: object, **kwargs: object) -> Path:
        calls.append(kwargs.get("progress"))
        callback = kwargs.get("progress")
        if callback:
            callback({"stage": "input_preparation", "message": "Preparing input", "elapsed": 0.1})
        return Path("normalized-kb")

    monkeypatch.setattr(cli_module, "normalize", fake_normalize)
    assert cli_module.main(["input.xml"]) == 0
    assert calls[-1] is cli_module._print_progress
    assert "input_preparation" in capsys.readouterr().out

    assert cli_module.main(["input.xml", "--quiet"]) == 0
    assert calls[-1] is None
    assert "Normalization completed" in capsys.readouterr().out


def test_share_safe_boundary_omits_raw_and_sanitizes_historical_provenance(tmp_path: Path) -> None:
    output = tmp_path / "out"
    first = tmp_path / "julian-private.xml"
    second = tmp_path / "julian-private.xpz"
    sensitive = r"C:\Users\julian\exports\private.xml"
    xml = f'<ExportFile><Source kb="kb-1" path="{sensitive}"><Version guid="v1" name="Demo"/></Source><Objects><Object guid="a" fullyQualifiedName="Demo.A" description="{sensitive}"/></Objects></ExportFile>'
    first.write_text(xml, encoding="utf-8")
    normalize(first, output)
    with zipfile.ZipFile(second, "w") as archive:
        archive.writestr("private.xml", xml.replace('guid="v1"', 'guid="v2"'))

    normalize(second, output, share_safe=True)
    assert not (output / "raw").exists()
    output_text = "\n".join(path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file())
    assert "C:\\Users\\julian" not in output_text
    assert "julian-private" not in output_text
    assert "\\\\" not in output_text
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["share_safe"] is True
    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert state["imports"][0]["source"]["source_input_path"] in {"[REDACTED_INPUT]", "[REDACTED_PATH]"}
    assert state["objects"]["object:a"]["versions"]["v1"]["path"].startswith("objects/")


def test_canonical_contract_is_versioned_and_dependency_records_are_identified(tmp_path: Path) -> None:
    source = tmp_path / "dependencies.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47"><Variable Name="v" basedOn="Demo.B"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out", preserve_raw=False)
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    assert records and all(record["schema_version"] == 1 and record["id"] for record in records)
    manifest = json.loads((output / "canonical/manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["record_counts"]["dependencies"] == 1
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["dependency_count"] == 1
    validate_output(output)


def test_xpz_selection_is_deterministic_and_can_be_overridden(tmp_path: Path) -> None:
    archive = tmp_path / "demo.xpz"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("z.xml", XML.replace("Demo", "Z"))
        handle.writestr("a.xml", XML.replace("Demo", "A"))
    output = normalize(archive, tmp_path / "out")
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert "a.xml" in manifest["warnings"][0]
    assert (output / "raw/demo.xpz").exists()
    overridden = normalize(archive, tmp_path / "out2", xml_member="z.xml")
    assert json.loads((overridden / "manifest.json").read_text(encoding="utf-8"))["warnings"] == []


def test_malformed_xml_has_actionable_error(tmp_path: Path) -> None:
    source = tmp_path / "bad.xml"
    source.write_text("<ExportFile>", encoding="utf-8")
    with pytest.raises(GXKBError, match="XML malformado"):
        normalize(source, tmp_path / "out")


def test_semantic_projections_cover_procedure_transaction_sdt_and_layout(tmp_path: Path) -> None:
    source = tmp_path / "semantic.xml"
    source.write_text(SEMANTIC_XML, encoding="utf-8")
    output = normalize(source, tmp_path / "out")

    procedure = output / "objects/Demo/DoWork"
    transaction = output / "objects/Demo/Customer"
    sdt = output / "objects/Demo/CustomerSDT"
    procedure_md = (procedure / "object.md").read_text(encoding="utf-8")
    transaction_md = (transaction / "object.md").read_text(encoding="utf-8")
    sdt_md = (sdt / "object.md").read_text(encoding="utf-8")
    assert "# Demo.DoWork" in procedure_md
    assert "Procedure" in procedure_md and "[code.gx](./code.gx)" in procedure_md
    assert "Transaction" in transaction_md and "[form.gx](./form.gx)" in transaction_md
    assert "Levels: **1**" in transaction_md and "primary key" in transaction_md
    assert "SDT" in sdt_md and "[structure.json](./structure.json)" in sdt_md
    assert "Items: **1**" in sdt_md and "ATTCUSTOMTYPE" not in sdt_md
    assert '"levels"' not in transaction_md
    assert '"levels"' not in sdt_md
    assert (procedure / "code.gx").read_text(encoding="utf-8").strip() == "return &Value"
    assert json.loads((procedure / "metadata.json").read_text(encoding="utf-8"))["object_kind"] == "procedure"
    assert (transaction / "form.gx").exists()
    assert "GeneXus layout/form projection" in (transaction / "form.gx").read_text(encoding="utf-8")
    transaction_structure = json.loads((transaction / "structure.json").read_text(encoding="utf-8"))
    sdt_structure = json.loads((sdt / "structure.json").read_text(encoding="utf-8"))
    assert transaction_structure["kind"] == "transaction_structure"
    assert transaction_structure["levels"][0]["items"][0]["key"] is True
    assert sdt_structure["kind"] == "sdt_structure"
    assert sdt_structure["levels"][0]["items"][0]["properties"]["ATTCUSTOMTYPE"] == "bas:Numeric"
    assert not (transaction / "structure.md").exists()
    assert not (sdt / "structure.md").exists()

    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    trx = next(record for record in records if record.get("object_id") == "object:t1" and record["record_type"] == "part")
    assert trx["part_kind"] == "transaction_structure"
    assert trx["semantic"]["levels"][0]["items"][0]["key"] is True
    assert trx["semantic"]["levels"][0]["items"][1]["isNullable"] is True
    sdt_record = next(record for record in records if record.get("object_id") == "object:s1" and record["record_type"] == "part")
    assert sdt_record["semantic"]["levels"][0]["items"][0]["properties"]["ATTCUSTOMTYPE"] == "bas:Numeric"

    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["semantic_counts"]["objects_by_kind"]["procedure"] == 1
    assert manifest["semantic_counts"]["parts_by_kind"]["transaction_structure"] == 1


def test_biller_procedure_sample_detects_real_rules_guid_and_projects_content(tmp_path: Path) -> None:
    source = Path(__file__).parent / "fixtures/biller_procedure_sample.xml"
    output = normalize(source, tmp_path / "out", preserve_raw=False, redact_source=True)
    procedure = output / "objects/Auditoria/Graba_auditoria"
    metadata = json.loads((procedure / "metadata.json").read_text(encoding="utf-8"))
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]

    assert metadata["object_kind"] == "procedure"
    assert (procedure / "code.gx").read_text(encoding="utf-8").startswith("&sdt_auditoria.FromJson")
    assert (procedure / "rules.gx").read_text(encoding="utf-8").strip() == "parm(in: &json);"
    rules = next(record for record in records if record.get("part_kind") == "rules")
    assert rules["type"] == "9b0a32a3-de6d-4be1-a4dd-1b85d3741534"
    assert rules["part_kind"] == "rules"


def test_same_kind_projections_keep_all_readable_parts(tmp_path: Path) -> None:
    source = tmp_path / "duplicates.xml"
    source.write_text(
        """<ExportFile><Objects><Object guid="p1" fullyQualifiedName="Demo.Duplicate" type="84a12160-f59b-4ad7-a683-ea4481ac23e9">
        <Part type="528d1c06-a9c2-420d-bd35-21dca83f12ff"><Source>first</Source></Part>
        <Part type="528d1c06-a9c2-420d-bd35-21dca83f12ff"><Source>second</Source></Part>
        </Object></Objects></ExportFile>""",
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    procedure = output / "objects/Demo/Duplicate"
    assert (procedure / "code.gx").read_text(encoding="utf-8").strip() == "first"
    assert (procedure / "code-002.gx").read_text(encoding="utf-8").strip() == "second"
    parts = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines() if '"record_type": "part"' in line]
    assert [part["content"] for part in parts] == ["first", "second"]


def test_same_layout_kind_projections_keep_all_readable_parts(tmp_path: Path) -> None:
    source = tmp_path / "layout-duplicates.xml"
    source.write_text(
        """<ExportFile><Objects><Object guid="t1" fullyQualifiedName="Demo.Layouts" type="1db606f2-af09-4cf9-a3b5-b481519d28f6">
        <Part type="d24a58ad-57ba-41b7-9e6e-eaca3543c778"><Source>&lt;Form id="first" /&gt;</Source></Part>
        <Part type="d24a58ad-57ba-41b7-9e6e-eaca3543c778"><Source>&lt;Form id="second" /&gt;</Source></Part>
        <Part type="c414ed00-8cc4-4f44-8820-4baf93547173"><Source>&lt;Report id="first" /&gt;</Source></Part>
        <Part type="c414ed00-8cc4-4f44-8820-4baf93547173"><Source>&lt;Report id="second" /&gt;</Source></Part>
        </Object></Objects></ExportFile>""",
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    layouts = output / "objects/Demo/Layouts"

    assert (layouts / "form.gx").exists()
    assert (layouts / "form-002.gx").exists()
    assert (layouts / "layout.gx").exists()
    assert (layouts / "layout-002.gx").exists()
    assert "first" in (layouts / "form.gx").read_text(encoding="utf-8")
    assert "second" in (layouts / "form-002.gx").read_text(encoding="utf-8")
    assert "first" in (layouts / "layout.gx").read_text(encoding="utf-8")
    assert "second" in (layouts / "layout-002.gx").read_text(encoding="utf-8")
    object_md = (layouts / "object.md").read_text(encoding="utf-8")
    assert "[form.gx](./form.gx)" in object_md
    assert "[form-002.gx](./form-002.gx)" in object_md
    assert "[layout.gx](./layout.gx)" in object_md
    assert "[layout-002.gx](./layout-002.gx)" in object_md


def test_variables_are_structured_lossless_and_support_multiple_parts(tmp_path: Path) -> None:
    source = tmp_path / "variables.xml"
    source.write_text(
        """<ExportFile><Objects>
        <Object guid="p1" fullyQualifiedName="Demo.Work" type="84a12160-f59b-4ad7-a683-ea4481ac23e9">
          <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47"><Variable Name="payload" basedOn="Demo.Payload" isNullable="True"><Properties><Property><Name>ATTCUSTOMTYPE</Name><Value>bas:LongVarChar</Value></Property></Properties></Variable><Unknown keep="yes" /></Part>
          <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47"><Variable Name="sdt"><Properties><Property><Name>ATTCUSTOMTYPE</Name><Value>sdt:Demo.Payload, Demo</Value></Property></Properties></Variable></Part>
        </Object><Object guid="s1" fullyQualifiedName="Demo.Payload" type="447527b5-9210-4523-898b-5dccb17be60a" />
        </Objects></ExportFile>""",
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    work = output / "objects/Demo/Work"
    variables_dir = work / "variables"
    variables = json.loads((variables_dir / "variables.json").read_text(encoding="utf-8"))
    assert variables["variables"][0]["based_on"] == "Demo.Payload"
    assert variables["variables"][0]["nullable"] is True
    assert "raw" in variables["variables"][0] and "Variable" in variables["variables"][0]["raw"]
    assert "[Abrir variables/variables.json](./variables/variables.json)" in (variables_dir / "variables.md").read_text(encoding="utf-8")
    assert (variables_dir / "variables-002.json").exists() and (variables_dir / "variables-002.md").exists()
    assert not (work / "variables.json").exists()
    assert not (work / "variables-002.json").exists()
    assert "variables/variables-002.json" in (work / "object.md").read_text(encoding="utf-8")
    assert "variables/variables-002.json" in (variables_dir / "variables-002.md").read_text(encoding="utf-8")
    dependencies = json.loads((work / "dependencies.json").read_text(encoding="utf-8"))
    assert any(item["relation"] == "based_on" and item["resolved"] for item in dependencies["inferred_dependencies"])
    assert any(item["relation"] == "uses_sdt" and item["resolved"] for item in dependencies["inferred_dependencies"])


def test_dependencies_normalize_explicit_and_unresolved_references(tmp_path: Path) -> None:
    source = tmp_path / "dependencies.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference guid="b" name="Demo.B"/><Reference name="Missing"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    dependencies = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    assert set(dependencies) >= {"explicit_references", "inferred_dependencies", "unresolved_references"}
    assert dependencies["explicit_references"][0]["to_object_id"] == "object:b"
    assert dependencies["explicit_references"][0]["resolved"] is True
    assert dependencies["explicit_references"][0]["raw"].startswith("<Reference")
    assert dependencies["unresolved_references"][0]["target_name"] == "Missing"
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(edge["kind"] == "references" and edge["dependency"]["relation"] == "explicit_reference" for edge in edges)


def test_explicit_reference_resolves_unique_name_and_graph_links_real_object(tmp_path: Path) -> None:
    source = tmp_path / "named-references.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference name="Demo.B"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    dependencies = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    dependency = dependencies["explicit_references"][0]
    assert dependency["resolved"] is True
    assert dependency["to_object_id"] == "object:b"
    assert not dependencies["unresolved_references"]
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(edge["kind"] == "references" and edge["to"] == "object:b" for edge in edges)


def test_explicit_reference_name_ambiguity_is_unresolved_without_inventing_target(tmp_path: Path) -> None:
    source = tmp_path / "ambiguous-references.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference name="Customer"/></Part></Object><Object guid="b" fullyQualifiedName="One.Customer"/><Object guid="c" fullyQualifiedName="Two.Customer"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    dependencies = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    dependency = dependencies["unresolved_references"][0]
    assert dependency["resolved"] is False
    assert "ambiguous" in dependency["unresolved_reason"]
    assert "to_object_id" not in dependency


def test_duplicate_guid_is_ambiguous_and_does_not_create_arbitrary_edge(tmp_path: Path) -> None:
    source = tmp_path / "duplicate-guid.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference guid="duplicate" name="Target"/></Part></Object><Object guid="duplicate" fullyQualifiedName="One.Target"/><Object guid="duplicate" fullyQualifiedName="Two.Target"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    dependencies = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    dependency = dependencies["unresolved_references"][0]
    assert dependency["unresolved_reason"] == "ambiguous_target_guid"
    assert "to_object_id" not in dependency
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert not any(edge.get("reference_id") == dependency["reference_id"] for edge in edges)
    nodes = [json.loads(line) for line in (output / "graph/nodes.jsonl").read_text(encoding="utf-8").splitlines()]
    assert not any(node["id"] == dependency["reference_id"] for node in nodes)


def test_graph_projects_only_resolved_reference_nodes_and_edges(tmp_path: Path) -> None:
    source = tmp_path / "mixed-references.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference guid="b" name="Resolved"/><Reference guid="duplicate" name="Duplicate"/><Reference name="Customer"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.Resolved"/><Object guid="duplicate" fullyQualifiedName="One.Duplicate"/><Object guid="duplicate" fullyQualifiedName="Two.Duplicate"/><Object guid="c" fullyQualifiedName="One.Customer"/><Object guid="d" fullyQualifiedName="Two.Customer"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    dependencies = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    references = dependencies["explicit_references"]
    resolved = next(dependency for dependency in references if dependency["resolved"])
    unresolved = [dependency for dependency in references if not dependency["resolved"]]
    nodes = [json.loads(line) for line in (output / "graph/nodes.jsonl").read_text(encoding="utf-8").splitlines()]
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]

    assert any(node["id"] == resolved["reference_id"] and node["kind"] == "reference" for node in nodes)
    assert any(edge.get("reference_id") == resolved["reference_id"] for edge in edges)
    assert all(not any(node["id"] == dependency["reference_id"] for node in nodes) for dependency in unresolved)
    assert all(not any(edge.get("reference_id") == dependency["reference_id"] for edge in edges) for dependency in unresolved)


def test_fully_qualified_name_ambiguity_is_unresolved_without_graph_edge(tmp_path: Path) -> None:
    source = tmp_path / "ambiguous-fully-qualified-name.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference fullyQualifiedName="Demo.Customer"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.Customer"/><Object guid="c" fullyQualifiedName="Demo.Customer"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    dependencies = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    dependency = dependencies["unresolved_references"][0]
    assert dependency["resolved"] is False
    assert "ambiguous" in dependency["unresolved_reason"]
    assert "to_object_id" not in dependency
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert not any(edge.get("reference_id") == dependency["reference_id"] for edge in edges)


def test_explicit_reference_resolves_unique_object_name_attribute(tmp_path: Path) -> None:
    source = tmp_path / "object-name-reference.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference name="CustomerAlias"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.Customer" name="CustomerAlias"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    dependencies = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    dependency = dependencies["explicit_references"][0]
    assert dependency["resolved"] is True
    assert dependency["to_object_id"] == "object:b"


def test_raw_contract_preserves_bytes_unredacted_and_sanitizes_when_requested(tmp_path: Path) -> None:
    source = tmp_path / "identity.xml"
    original = '<ExportFile><Source path="C:\\Users\\julian\\kb"/><Objects><Object guid="o1" name="JULIAN-NOTE\\julian"/></Objects></ExportFile>'.encode("utf-8")
    source.write_bytes(original)

    preserved = normalize(source, tmp_path / "preserved", preserve_raw=True, redact_source=False)
    assert next((preserved / "raw").glob("*.xml")).read_bytes() == original

    sanitized = normalize(source, tmp_path / "sanitized", preserve_raw=True, redact_source=True)
    raw_text = next((sanitized / "raw").glob("*.xml")).read_text(encoding="utf-8")
    assert raw_text.encode("utf-8") != original
    assert "C:\\Users\\julian" not in raw_text
    assert "JULIAN-NOTE\\julian" not in raw_text


def _incremental_xml(version: str, objects: str, kb: str = "kb-1") -> str:
    return f'<ExportFile><Source kb="{kb}"><Version guid="{version}" name="Demo {version}"/></Source><Objects>{objects}</Objects></ExportFile>'


def test_incremental_identical_import_skips_without_rewriting_outputs(tmp_path: Path) -> None:
    source = tmp_path / "part.xml"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    before = {path.relative_to(output): path.stat().st_mtime_ns for path in output.rglob("*") if path.is_file()}
    normalize(source, output)
    after = {path.relative_to(output): path.stat().st_mtime_ns for path in output.rglob("*") if path.is_file()}
    assert after == before


def test_incremental_preserve_raw_policy_transitions_invalidate_cache(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")

    normalize(source, output, preserve_raw=True)
    assert (output / "raw/private.xml").exists()
    normalize(source, output, preserve_raw=False)
    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert not (output / "raw").exists()
    assert state["objects"]["object:a"]["versions"]["v1"]["preserve_raw"] is False

    normalize(source, output, preserve_raw=True)
    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert (output / "raw/private.xml").exists()
    assert state["objects"]["object:a"]["versions"]["v1"]["preserve_raw"] is True


def test_incremental_partial_adds_without_deleting_previous_object(tmp_path: Path) -> None:
    source = tmp_path / "part.xml"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    source.write_text(_incremental_xml("v1", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output)
    assert (output / "objects/Demo/A").exists() and (output / "objects/Demo/B").exists()
    assert len((output / "objects-index.jsonl").read_text(encoding="utf-8").splitlines()) == 2


def test_snapshot_retires_absent_object_and_preserves_tombstone(tmp_path: Path) -> None:
    source = tmp_path / "snapshot.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/><Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output)
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output, snapshot=True)

    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert {record["id"] for record in records if record["record_type"] == "object"} == {"object:a"}
    assert not (output / "objects/Demo/B").exists()
    assert state["tombstones"]["object:b"]["reason"] == "absent_from_snapshot"
    assert state["objects"]["object:b"]["versions"]["v1"]["active"] is False
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["incremental"]["reconciliation"]["scope"] == "kb-version"


def test_empty_partial_export_bootstraps_and_preserves_existing_objects(tmp_path: Path) -> None:
    source = tmp_path / "empty.xml"
    output = tmp_path / "out"
    source.write_text("<ExportFile><Objects/></ExportFile>", encoding="utf-8")

    normalize(source, output)
    validate_output(output)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["object_count"] == 0
    assert (output / "canonical/records.jsonl").read_text(encoding="utf-8") == ""

    source.write_text('<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"/></Objects></ExportFile>', encoding="utf-8")
    normalize(source, output)
    source.write_text("<ExportFile><Objects/></ExportFile>", encoding="utf-8")
    normalize(source, output)
    assert (output / "objects/Demo/A").exists()
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["object_count"] == 1


def test_empty_bootstrap_identity_adopts_first_valid_kb_guid(tmp_path: Path) -> None:
    source = tmp_path / "export.xml"
    output = tmp_path / "out"
    source.write_text("<ExportFile><Objects/></ExportFile>", encoding="utf-8")
    normalize(source, output)
    assert json.loads((output / "kb-state.json").read_text(encoding="utf-8"))["kb"]["guid"] == ""

    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>', kb="kb-real"), encoding="utf-8")
    normalize(source, output)
    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert state["kb"]["guid"] == "kb-real"

    source.write_text(_incremental_xml("v2", "", kb="kb-other"), encoding="utf-8")
    with pytest.raises(GXKBError, match="KB GUID incompatible"):
        normalize(source, output)


def test_new_kb_rejects_non_empty_output_before_staging(tmp_path: Path) -> None:
    source = tmp_path / "export.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>', kb="kb-real"), encoding="utf-8")
    output.mkdir()
    (output / "objects").mkdir()
    (output / "manifest.json").write_text("{}", encoding="utf-8")

    with pytest.raises(GXKBError, match="directorio vacío"):
        normalize(source, output, new_kb=True)
    assert not list(output.parent.glob("gxkb-stage-*"))


def test_empty_complete_snapshot_retires_all_objects(tmp_path: Path) -> None:
    source = tmp_path / "snapshot.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)

    source.write_text(_incremental_xml("v1", ""), encoding="utf-8")
    normalize(source, output, snapshot=True)
    validate_output(output)

    assert not (output / "objects/Demo/A").exists()
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["object_count"] == 0
    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert state["tombstones"]["object:a"]["reason"] == "absent_from_snapshot"


def test_repeated_snapshot_after_retirement_is_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "snapshot.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/><Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output)
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output, snapshot=True)
    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    normalize(source, output, snapshot=True)
    assert {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()} == before


def test_snapshot_retirement_does_not_hide_object_active_in_another_version(tmp_path: Path) -> None:
    source = tmp_path / "snapshot.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    source.write_text(_incremental_xml("v2", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    source.write_text(_incremental_xml("v1", ""), encoding="utf-8")
    normalize(source, output, snapshot=True)

    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert state["objects"]["object:a"]["active"] is True
    assert state["objects"]["object:a"]["versions"]["v1"]["active"] is False
    assert state["objects"]["object:a"]["versions"]["v2"]["active"] is True
    assert state["tombstones"]["object:a"]["versions"]["v1"]["reason"] == "absent_from_snapshot"
    assert any(json.loads(line)["id"] == "object:a" for line in (output / "objects-index.jsonl").read_text(encoding="utf-8").splitlines())
    assert (output / "objects/Demo/A").exists()


def test_snapshot_reintroduced_object_is_active_again(tmp_path: Path) -> None:
    source = tmp_path / "snapshot.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/><Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output)
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output, snapshot=True)
    source.write_text(_incremental_xml("v1", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output, snapshot=True)

    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert (output / "objects/Demo/B").exists()
    assert state["objects"]["object:b"]["active"] is True
    assert "object:b" not in state["tombstones"]


def test_identical_snapshot_is_stable_and_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "snapshot.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output, snapshot=True)
    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    normalize(source, output, snapshot=True)
    assert {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()} == before


def test_failed_snapshot_keeps_previous_output_and_state_intact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "snapshot.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/><Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output)
    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    original = normalizer_module._jsonl_write

    def fail_graph(path: Path, values: object) -> None:
        if path.name == "edges.jsonl":
            raise OSError("injected snapshot graph failure")
        original(path, values)  # type: ignore[arg-type]

    monkeypatch.setattr(normalizer_module, "_jsonl_write", fail_graph)
    with pytest.raises(OSError, match="injected snapshot graph failure"):
        normalize(source, output, snapshot=True)
    assert {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()} == before
    assert "tombstones" not in json.loads((output / "kb-state.json").read_text(encoding="utf-8"))


def test_share_safe_snapshot_preserves_privacy_for_retirement_metadata(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    output = tmp_path / "out"
    private_path = r"C:\Users\julian\private\snapshot.xml"
    source.write_text(f'<ExportFile><Source kb="kb-1" path="{private_path}"><Version guid="v1" name="Demo"/></Source><Objects><Object guid="a" fullyQualifiedName="Demo.A" description="{private_path}"/><Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>', encoding="utf-8")
    normalize(source, output, share_safe=True)
    source.write_text(f'<ExportFile><Source kb="kb-1" path="{private_path}"><Version guid="v1" name="Demo"/></Source><Objects><Object guid="a" fullyQualifiedName="Demo.A" description="{private_path}"/></Objects></ExportFile>', encoding="utf-8")
    normalize(source, output, share_safe=True, snapshot=True)
    text = "\n".join(path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file())
    assert private_path not in text and "julian" not in text
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["share_safe"] is True


def test_incremental_change_and_reprocess_all_force_processing(tmp_path: Path) -> None:
    source = tmp_path / "part.xml"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A" description="one"/>'), encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A" description="two"/>'), encoding="utf-8")
    changed = normalize(source, output)
    assert changed and json.loads((changed / "manifest.json").read_text(encoding="utf-8"))["processed_objects"] == 1
    forced = normalize(source, output, reprocess_all=True)
    assert json.loads((forced / "manifest.json").read_text(encoding="utf-8"))["processed_objects"] == 1


def test_incremental_rejects_different_kb_and_keeps_versions(tmp_path: Path) -> None:
    source = tmp_path / "part.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    source.write_text(_incremental_xml("v2", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    assert set(json.loads((output / "kb-state.json").read_text(encoding="utf-8"))["versions"]) == {"v1", "v2"}
    source.write_text(_incremental_xml("v3", '<Object guid="z" fullyQualifiedName="Demo.Z"/>', kb="kb-2"), encoding="utf-8")
    with pytest.raises(GXKBError, match="KB GUID incompatible"):
        normalize(source, output)


def test_incremental_raw_collision_is_preserved(tmp_path: Path) -> None:
    source = tmp_path / "same.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    source.write_text(_incremental_xml("v2", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output)
    assert len(list((output / "raw").glob("*.xml"))) >= 2


def test_incremental_redaction_sanitizes_raw_history_without_losing_provenance(tmp_path: Path) -> None:
    output = tmp_path / "out"
    first = tmp_path / "a.xml"
    second = tmp_path / "b.xml"
    first.write_text(_incremental_xml("v1", r'<Object guid="a" fullyQualifiedName="Demo.A" description="JULIA-NOTE\julian C:\Users\julian\a"/>'), encoding="utf-8")
    second.write_text(_incremental_xml("v2", r'<Object guid="b" fullyQualifiedName="Demo.B" description="JULIA-NOTE\julian C:\Users\julian\b"/>'), encoding="utf-8")

    normalize(first, output, preserve_raw=True, redact_source=False)
    normalize(second, output, preserve_raw=True, redact_source=True)

    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    versions = state["objects"]
    assert set(versions) == {"object:a", "object:b"}
    assert versions["object:a"]["versions"]["v1"]["raw_redacted"] is True
    assert versions["object:b"]["versions"]["v2"]["raw_redacted"] is True
    assert versions["object:a"]["versions"]["v1"]["raw_kind"] == "xml"
    assert versions["object:b"]["versions"]["v2"]["raw_kind"] == "xml"
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {record["id"] for record in records if record["record_type"] == "object"} == {"object:a", "object:b"}
    raw_paths = [entry["versions"][version]["raw_path"] for entry, version in ((versions["object:a"], "v1"), (versions["object:b"], "v2"))]
    assert len(set(raw_paths)) == 2
    assert all((output / path).exists() for path in raw_paths)
    raw_text = "\n".join(path.read_text(encoding="utf-8") for path in (output / "raw").glob("*.xml"))
    assert "JULIA-NOTE\\julian" not in raw_text
    assert "C:\\Users\\julian" not in raw_text
    assert "Demo.A" in raw_text and "Demo.B" in raw_text


def test_incremental_redaction_sanitizes_historical_state_after_real_xpz_import(tmp_path: Path) -> None:
    output = tmp_path / "out"
    first = tmp_path / "first.xml"
    second = tmp_path / "second.xpz"
    sensitive_path = r"C:\Users\historical-user\exports\first.xml"
    sensitive_unc = r"\\SERVER\historical-user\share\first.xml"
    first.write_text(
        f'<ExportFile><Source kb="kb-1" path="{sensitive_path}" raw="{sensitive_unc}"><Version guid="v1" name="Demo v1"/></Source><Objects><Object guid="a" fullyQualifiedName="Demo.A"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    second_xml = f'<ExportFile><Source kb="kb-1" path="{sensitive_path}" raw="{sensitive_unc}"><Version guid="v2" name="Demo v2"/></Source><Objects><Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>'
    with zipfile.ZipFile(second, "w") as archive:
        archive.writestr("export.xml", second_xml)

    normalize(first, output, preserve_raw=True, redact_source=False)
    normalize(second, output, preserve_raw=True, redact_source=True)

    state_path = output / "kb-state.json"
    state_text = state_path.read_text(encoding="utf-8")
    state = json.loads(state_text)
    assert sensitive_path not in state_text
    assert sensitive_unc not in state_text
    assert set(state["objects"]) == {"object:a", "object:b"}
    assert set(state["versions"]) == {"v1", "v2"}
    assert len(state["imports"]) == 2
    assert state["objects"]["object:a"]["versions"]["v1"]["raw_path"].startswith("raw/")
    assert state["objects"]["object:b"]["versions"]["v2"]["raw_path"].startswith("raw/")


def test_redacted_state_preserves_internal_paths_and_separates_input_provenance(tmp_path: Path) -> None:
    output = tmp_path / "out"
    source = tmp_path / "local-user" / "private.xpz"
    source.parent.mkdir()
    sensitive_input = r"C:\Users\local-user\exports\private.xpz"
    sensitive_unc = r"\\SERVER\local-user\share\private.xpz"
    xml = (
        f'<ExportFile><Source kb="kb-1" path="{sensitive_input}" unc="{sensitive_unc}">'
        f'<Version guid="v1" name="Demo v1"/></Source><Objects>'
        '<Object guid="a" fullyQualifiedName="Demo.A"/></Objects></ExportFile>'
    )
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("export.xml", xml)

    normalize(source, output, preserve_raw=True, redact_source=True)

    state_path = output / "kb-state.json"
    state_text = state_path.read_text(encoding="utf-8")
    state = json.loads(state_text)
    version = state["objects"]["object:a"]["versions"]["v1"]
    assert version["path"] == "objects/Demo/A"
    assert version["raw_path"].startswith("raw/")
    assert state["imports"][0]["source"]["source_input_path"] == "private.xpz"
    assert "source_input_path" not in version
    assert sensitive_input not in state_text
    assert sensitive_unc not in state_text
    assert str(source) not in state_text
    assert "local-user" not in state_text


def test_incremental_unresolved_dependency_resolves_when_target_arrives(tmp_path: Path) -> None:
    source = tmp_path / "part.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference guid="b"/></Part></Object>'), encoding="utf-8")
    normalize(source, output)
    first = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    assert first["unresolved_references"]
    source.write_text(_incremental_xml("v1", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(source, output)
    second = json.loads((output / "objects/Demo/A/dependencies.json").read_text(encoding="utf-8"))
    assert second["explicit_references"][0]["resolved"] is True
    assert any(edge["to"] == "object:b" for edge in (json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()))


def test_incremental_failure_keeps_previous_output_and_state_intact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "part.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}

    source.write_text(_incremental_xml("v1", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    original = normalizer_module._jsonl_write

    def fail_graph(path: Path, values: object) -> None:
        if path.name == "edges.jsonl":
            raise OSError("injected graph write failure")
        original(path, values)  # type: ignore[arg-type]

    monkeypatch.setattr(normalizer_module, "_jsonl_write", fail_graph)
    with pytest.raises(OSError, match="injected graph write failure"):
        normalize(source, output)

    after = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    assert after == before
    assert json.loads((output / "kb-state.json").read_text(encoding="utf-8"))["objects"].keys() == {"object:a"}


def test_commit_failure_with_rollback_failure_preserves_backup_and_reports_recovery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "out"
    staged = tmp_path / "staged"
    destination.mkdir()
    staged.mkdir()
    (destination / "raw").mkdir()
    (destination / "raw" / "old.txt").write_text("old", encoding="utf-8")
    (staged / "raw").mkdir()
    (staged / "raw" / "new.txt").write_text("new", encoding="utf-8")

    original_replace = normalizer_module.os.replace

    def fail_restore(source: Path, target: Path) -> None:
        if source.parent.name.startswith("gxkb-backup-"):
            raise OSError("injected rollback failure")
        if source.parent == staged:
            raise OSError("injected commit failure")
        original_replace(source, target)

    monkeypatch.setattr(normalizer_module.os, "replace", fail_restore)
    with pytest.raises(GXKBError, match=r"Rollback incomplete.*backup preserved at") as error:
        normalizer_module._commit_staged_output(staged, destination)

    backup_path = Path(str(error.value).split("backup preserved at ", 1)[1].split(".", 1)[0])
    assert backup_path.is_dir()
    assert (backup_path / "raw" / "old.txt").read_text(encoding="utf-8") == "old"


def test_cli_reports_expected_oserror_with_controlled_exit(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    def fail_normalize(*args: object, **kwargs: object) -> Path:
        raise OSError("input is locked")

    monkeypatch.setattr(cli_module, "normalize", fail_normalize)
    assert cli_module.main(["input.xml"]) == 2
    assert "Error accessing input or output: input is locked" in capsys.readouterr().err


@pytest.mark.parametrize("failure_name", ["kb-state.json", "metadata.json"])
def test_incremental_write_failures_roll_back_without_incomplete_temporaries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure_name: str,
) -> None:
    source = tmp_path / "part.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}

    source.write_text(_incremental_xml("v1", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    if failure_name == "metadata.json":
        original = normalizer_module._atomic_write

        def fail_atomic(path: Path, value: str) -> None:
            if path.name == failure_name:
                raise OSError(f"injected {failure_name} failure")
            original(path, value)

        monkeypatch.setattr(normalizer_module, "_atomic_write", fail_atomic)
    else:
        original = normalizer_module._json_write

        def fail_state(path: Path, value: object) -> None:
            if path.name == failure_name:
                raise OSError(f"injected {failure_name} failure")
            original(path, value)  # type: ignore[arg-type]

        monkeypatch.setattr(normalizer_module, "_json_write", fail_state)
    with pytest.raises(OSError, match="injected"):
        normalize(source, output)

    assert {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()} == before
    assert not list(output.parent.glob("gxkb-stage-*"))
    assert not list(output.parent.glob("gxkb-backup-*"))
    assert not list(output.rglob("*.tmp-*"))


def test_incremental_raw_copy_failure_rolls_back_without_partial_raw(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "part.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    source.write_text(_incremental_xml("v1", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    original = normalizer_module.shutil.copy2

    def fail_raw(src: Path, dst: Path, *args: object, **kwargs: object) -> object:
        if Path(dst).parent.name == "raw":
            raise OSError("injected raw copy failure")
        return original(src, dst, *args, **kwargs)

    monkeypatch.setattr(normalizer_module.shutil, "copy2", fail_raw)
    with pytest.raises(OSError, match="injected raw copy failure"):
        normalize(source, output)
    assert {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()} == before
    assert not list(output.parent.glob("gxkb-stage-*"))
    assert not list(output.parent.glob("gxkb-backup-*"))


def test_redaction_request_invalidates_unredacted_incremental_cache(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    output = tmp_path / "out"
    private_xml = _incremental_xml(
        "v1",
        r'<Object guid="a" fullyQualifiedName="Demo.A" description="Owner JULIA-NOTE\julian C:\Users\julian\secret"><Part type="unknown"><Source>C:\Users\julian\part</Source></Part></Object>',
    )
    source.write_text(private_xml, encoding="utf-8")
    normalize(source, output, redact_source=False)
    normalize(source, output, redact_source=True)

    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert state["objects"]["object:a"]["versions"]["v1"]["redact_source"] is True
    output_text = "\n".join(path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file())
    assert "JULIA-NOTE\\julian" not in output_text
    assert "C:\\Users\\julian" not in output_text
    assert "[REDACTED_PATH]" in output_text
    assert "[REDACTED_USER]" in output_text


def test_new_database_api_and_index_types_have_named_structured_outputs(tmp_path: Path) -> None:
    source = tmp_path / "new-types.xml"
    source.write_text(
        """<ExportFile><Objects>
        <Object guid="tv" fullyQualifiedName="Demo.CustomerView" type="19abc6ff-2cd2-0000-0006-6d172bc2333b">
          <Part type="19abc6ff-2cd2-1000-0006-6d172bc2333b"><Platforms><Platform name="SQL"/></Platforms></Part>
          <Part type="7706bd3b-212a-1000-0006-8aaeb59068b9"><Indexes><Index name="IX_Customer"/></Indexes></Part>
          <Part type="7706bd3b-212a-1000-0006-8aaeb59068b9"><Indexes><Index name="IX_Customer_2"/></Indexes></Part>
        </Object>
        <Object guid="api" fullyQualifiedName="Demo.CustomerApi" type="36e32e2d-023e-4188-95df-d13573bac2e0">
          <Part type="9f577ec2-27f4-4cf4-8ad5-f3f50c9d69b5"><Source>GetCustomer()</Source></Part>
        </Object>
        <Object guid="idx" fullyQualifiedName="Demo.CustomerIndex" type="fc1b76c4-95c5-0000-0101-44f9543121bd">
          <Part type="fe47b55c-ea2a-1000-0101-5b38901e24f7"><Members><Member name="CustomerId"/></Members></Part>
        </Object>
        </Objects></ExportFile>""",
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out", preserve_raw=False)
    table = output / "objects/Demo/CustomerView"
    api = output / "objects/Demo/CustomerApi"
    index = output / "objects/Demo/CustomerIndex"
    assert json.loads((table / "table.json").read_text(encoding="utf-8"))["kind"] == "table_view"
    assert json.loads((table / "platforms.json").read_text(encoding="utf-8"))["platforms"]
    assert (table / "indexes.json").exists() and (table / "indexes-002.json").exists()
    assert (api / "api.gx").read_text(encoding="utf-8").strip() == "GetCustomer()"
    assert json.loads((api / "api.json").read_text(encoding="utf-8"))["kind"] == "api_source"
    assert json.loads((index / "members.json").read_text(encoding="utf-8"))["members"]
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["semantic_counts"]["objects_by_kind"] == {"table_view": 1, "api": 1, "index_definition": 1}
    assert manifest["semantic_counts"]["parts_by_kind"]["indexes"] == 2
    assert not any(record.get("object_kind") == "unknown" or record.get("part_kind") == "unknown"
                   for record in (json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()))


def test_fqn_collision_uses_guid_paths_and_survives_incremental_import(tmp_path: Path) -> None:
    output = tmp_path / "out"
    source = tmp_path / "collision.xml"
    first = _incremental_xml(
        "v1",
        '<Object guid="view-guid-123456" fullyQualifiedName="BillerExterno.vw_CuentaCorr" type="19abc6ff-2cd2-0000-0006-6d172bc2333b"><Part type="19abc6ff-2cd2-1000-0006-6d172bc2333b"><Platforms><Platform name="SQL view"/></Platforms></Part></Object>',
    )
    source.write_text(first, encoding="utf-8")
    normalize(source, output)
    second = _incremental_xml(
        "v1",
        '<Object guid="view-guid-123456" fullyQualifiedName="BillerExterno.vw_CuentaCorr" type="19abc6ff-2cd2-0000-0006-6d172bc2333b"><Part type="19abc6ff-2cd2-1000-0006-6d172bc2333b"><Platforms><Platform name="SQL view"/></Platforms></Part></Object>'
        '<Object guid="trx-guid-abcdef" fullyQualifiedName="BillerExterno.vw_CuentaCorr" type="1db606f2-af09-4cf9-a3b5-b481519d28f6"><Part type="264be5fb-1b28-4b25-a598-6ca900dd059f"><Level Name="CuentaCorr"><Attribute name="CuentaId"/></Level></Part></Object>',
    )
    source.write_text(second, encoding="utf-8")
    normalize(source, output)

    view_dir = output / "objects/BillerExterno/vw_CuentaCorr--view-guid-"
    view_dir = next(path for path in view_dir.parent.glob(view_dir.name + "*") if path.is_dir())
    trx_dir = output / "objects/BillerExterno/vw_CuentaCorr--trx-guid-"
    trx_dir = next(path for path in trx_dir.parent.glob(trx_dir.name + "*") if path.is_dir())
    assert view_dir != trx_dir
    assert json.loads((view_dir / "metadata.json").read_text(encoding="utf-8"))["object_kind"] == "table_view"
    assert json.loads((trx_dir / "metadata.json").read_text(encoding="utf-8"))["object_kind"] == "transaction"
    assert not (output / "objects/BillerExterno/vw_CuentaCorr").exists()

    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    objects = [record for record in records if record["record_type"] == "object"]
    assert {record["normalized_path"] for record in objects} == {
        "objects/BillerExterno/vw_CuentaCorr--view-guid-12",
        "objects/BillerExterno/vw_CuentaCorr--trx-guid-abc",
    }
    index_paths = {json.loads(line)["path"] for line in (output / "objects-index.jsonl").read_text(encoding="utf-8").splitlines()}
    assert index_paths == {record["normalized_path"] for record in objects}
    state = json.loads((output / "kb-state.json").read_text(encoding="utf-8"))
    assert {entry["versions"]["v1"]["path"] for entry in state["objects"].values()} == index_paths
    assert all(node["id"].startswith("object:") for node in (json.loads(line) for line in (output / "graph/nodes.jsonl").read_text(encoding="utf-8").splitlines()) if node["kind"] == "object")

    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    normalize(source, output)
    after = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    assert after == before


def test_case_insensitive_generated_path_collision_preserves_both_metadata_projections(tmp_path: Path) -> None:
    source = tmp_path / "case-collision.xml"
    source.write_text(
        '<ExportFile><Objects>'
        '<Object fullyQualifiedName="Cus_1308.Cmp070a" type="unknown"/>'
        '<Object fullyQualifiedName="Cus_1308.cmp070a" type="unknown"/>'
        '</Objects></ExportFile>',
        encoding="utf-8",
    )

    output = normalize(source, tmp_path / "out")
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    objects = [record for record in records if record["record_type"] == "object"]
    paths = [record["normalized_path"] for record in objects]

    assert len(objects) == 2
    assert len(set(paths)) == 2
    assert len({path.casefold() for path in paths}) == 2
    assert all((output / path / "metadata.json").exists() for path in paths)
    validate_output(output)


def test_same_fqn_without_guid_uses_distinct_type_collision_paths(tmp_path: Path) -> None:
    source = tmp_path / "same-fqn-collision.xml"
    source.write_text(
        '<ExportFile><Objects>'
        '<Object fullyQualifiedName="Common" type="type-a"/>'
        '<Object fullyQualifiedName="Common" type="type-b"/>'
        '</Objects></ExportFile>',
        encoding="utf-8",
    )

    output = normalize(source, tmp_path / "out")
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    objects = [record for record in records if record["record_type"] == "object"]
    paths = [record["normalized_path"] for record in objects]

    assert len(objects) == 2
    assert len({path.casefold() for path in paths}) == 2
    assert all((output / path / "metadata.json").exists() for path in paths)
    validate_output(output)


def test_dotless_parent_path_matches_qualified_collision_paths(tmp_path: Path) -> None:
    source = tmp_path / "dotless-parent-collision.xml"
    source.write_text(
        '<ExportFile><Objects>'
        '<Object fullyQualifiedName="Common" parent="GeneXus" type="type-a">'
        '<Part type="source"><Source>Common()</Source></Part>'
        '</Object>'
        '<Object fullyQualifiedName="GeneXus.Common" type="type-b">'
        '<Part type="source"><Source>GeneXus.Common()</Source></Part>'
        '</Object>'
        '</Objects></ExportFile>',
        encoding="utf-8",
    )

    output = normalize(source, tmp_path / "out")
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    objects = [record for record in records if record["record_type"] == "object"]
    parts = [record for record in records if record["record_type"] == "part"]
    paths_by_name = {record["fully_qualified_name"]: record["normalized_path"] for record in objects}

    assert len(objects) == 2
    assert all(path.startswith("objects/GeneXus/Common--") for path in paths_by_name.values())
    assert len({path.casefold() for path in paths_by_name.values()}) == 2
    assert all((output / path / "metadata.json").exists() for path in paths_by_name.values())
    assert all((output / record["normalized_file"]).exists() for record in parts)
    assert all(record["normalized_file"].startswith("objects/GeneXus/Common--") for record in parts)
    validate_output(output)


def test_share_safe_redacts_versions_and_historical_objects_index(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    source.write_text(
        '<ExportFile><Source kb="kb-1"><Version guid="v1" name="C:\\Users\\julian\\Private Release" path="C:\\Users\\julian\\versions\\v1"/></Source>'
        '<Objects><Object guid="a" fullyQualifiedName="Demo.A"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    normalize(source, output, share_safe=True)
    for path in (output / "manifest.json", output / "canonical/manifest.json", output / "objects-index.jsonl"):
        assert "C:\\Users\\julian" not in path.read_text(encoding="utf-8")
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["share_safe"] is True


def test_share_safe_noop_still_cleans_history_and_marks_state(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output, preserve_raw=True)
    normalize(source, output, share_safe=True)
    assert not (output / "raw").exists()
    assert json.loads((output / "kb-state.json").read_text(encoding="utf-8"))["share_safe"] is True


def test_repeated_identical_share_safe_import_is_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "private.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output, share_safe=True)
    before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    normalize(source, output, share_safe=True)
    after = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
    assert after == before
    assert len(json.loads((output / "kb-state.json").read_text(encoding="utf-8"))["imports"]) == 1


def test_incremental_noop_upgrades_unversioned_canonical_output(tmp_path: Path) -> None:
    source = tmp_path / "versioned.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    records_path = output / "canonical/records.jsonl"
    records_path.write_text(
        "\n".join(json.dumps({key: value for key, value in json.loads(line).items() if key != "schema_version"}) for line in records_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    normalize(source, output)
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    assert all(record["schema_version"] == 1 for record in records)


def test_validate_output_distinguishes_legacy_records_and_normalize_migrates_them(tmp_path: Path) -> None:
    source = tmp_path / "legacy.xml"
    output = tmp_path / "out"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(source, output)
    records_path = output / "canonical/records.jsonl"
    legacy_records = []
    for line in records_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        record.pop("schema_version", None)
        record.pop("id", None)
        legacy_records.append(record)
    records_path.write_text("\n".join(json.dumps(record) for record in legacy_records) + "\n", encoding="utf-8")
    with pytest.raises(GXKBError, match="Legacy canonical output"):
        validate_output(output)
    normalize(source, output)
    validate_output(output)
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    assert all(record["schema_version"] == 1 and record["id"] for record in records)


def test_legacy_partial_input_preserves_absent_accumulated_objects(tmp_path: Path) -> None:
    first_source = tmp_path / "first.xml"
    second_source = tmp_path / "second.xml"
    output = tmp_path / "out"
    first_source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"/>'), encoding="utf-8")
    normalize(first_source, output)
    records_path = output / "canonical/records.jsonl"
    records_path.write_text(
        "\n".join(json.dumps({key: value for key, value in json.loads(line).items() if key != "schema_version"}) for line in records_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    second_source.write_text(_incremental_xml("v2", '<Object guid="b" fullyQualifiedName="Demo.B"/>'), encoding="utf-8")
    normalize(second_source, output)
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    assert {record["id"] for record in records if record["record_type"] == "object"} == {"object:a", "object:b"}
    assert (output / "objects/Demo/A/metadata.json").exists()
    assert (output / "objects/Demo/B/metadata.json").exists()
    validate_output(output)


def test_legacy_partial_input_migrates_inferred_dependencies_end_to_end(tmp_path: Path) -> None:
    accumulated_source = tmp_path / "accumulated.xml"
    partial_source = tmp_path / "partial.xml"
    output = tmp_path / "out"
    accumulated_source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A">'
        '<Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47"><Variable Name="v" basedOn="Demo.B"/>'
        '<Reference name="Demo.B"/></Part></Object>'
        '<Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    normalize(accumulated_source, output)

    records_path = output / "canonical/records.jsonl"
    original_records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    expected_inferred_id = next(
        record["id"] for record in original_records
        if record["record_type"] == "dependency" and record["relation"] != "explicit_reference"
    )
    legacy_records = []
    for line in records_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        record.pop("schema_version", None)
        if record.get("record_type") == "dependency" and record.get("relation") != "explicit_reference":
            record.pop("id", None)
        legacy_records.append(record)
    records_path.write_text("\n".join(json.dumps(record) for record in legacy_records) + "\n", encoding="utf-8")

    partial_source.write_text(
        '<ExportFile><Objects><Object guid="c" fullyQualifiedName="Demo.C"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    normalize(partial_source, output)
    validate_output(output)

    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    dependencies = [record for record in records if record["record_type"] == "dependency"]
    inferred = next(record for record in dependencies if record["relation"] != "explicit_reference")
    assert inferred["id"] == expected_inferred_id
    assert {record["id"] for record in records if record["record_type"] == "object"} == {"object:a", "object:b", "object:c"}

    nodes = [json.loads(line) for line in (output / "graph/nodes.jsonl").read_text(encoding="utf-8").splitlines()]
    edges = [json.loads(line) for line in (output / "graph/edges.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {node["id"] for node in nodes if node["kind"] == "object"} == {"object:a", "object:b", "object:c"}
    assert any(edge.get("from") == "object:a" and edge.get("to") == "object:b" for edge in edges if edge.get("kind") != "contains")


def test_dependency_count_includes_explicit_and_inferred_canonical_records(tmp_path: Path) -> None:
    source = tmp_path / "dependencies.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47"><Variable Name="v" basedOn="Demo.B"/></Part><Part type="unknown"><Reference name="Demo.B"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    records = [json.loads(line) for line in (output / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len([record for record in records if record["record_type"] == "dependency"]) == 2
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8"))["dependency_count"] == 2


def test_validate_output_rejects_invalid_graph_targets_but_accepts_unresolved_dependencies(tmp_path: Path) -> None:
    source = tmp_path / "graph.xml"
    source.write_text('<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"><Reference name="Missing"/></Part></Object></Objects></ExportFile>', encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    validate_output(output)
    edges_path = output / "graph/edges.jsonl"
    edges_path.write_text('{"id":"bad","from":"object:a","to":"missing","kind":"contains"}\n', encoding="utf-8")
    with pytest.raises(GXKBError, match="Graph edges"):
        validate_output(output)


def test_validate_output_rejects_graph_kind_and_inferred_dependency_corruption(tmp_path: Path) -> None:
    source = tmp_path / "graph-corruption.xml"
    source.write_text(
        '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47"><Variable Name="v" basedOn="Demo.B"/></Part></Object><Object guid="b" fullyQualifiedName="Demo.B"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out")
    nodes_path = output / "graph/nodes.jsonl"
    nodes = [json.loads(line) for line in nodes_path.read_text(encoding="utf-8").splitlines()]
    nodes[0]["kind"] = "part"
    nodes_path.write_text("\n".join(json.dumps(node) for node in nodes) + "\n", encoding="utf-8")
    with pytest.raises(GXKBError, match="object nodes"):
        validate_output(output)
    nodes[0]["kind"] = "object"
    nodes_path.write_text("\n".join(json.dumps(node) for node in nodes) + "\n", encoding="utf-8")
    edges_path = output / "graph/edges.jsonl"
    edges = [json.loads(line) for line in edges_path.read_text(encoding="utf-8").splitlines()]
    inferred = next(edge for edge in edges if edge["kind"] != "contains")
    inferred["kind"] = "wrong_relation"
    edges_path.write_text("\n".join(json.dumps(edge) for edge in edges) + "\n", encoding="utf-8")
    with pytest.raises(GXKBError, match="dependency edges"):
        validate_output(output)


def test_share_safe_redacts_arbitrary_posix_paths_but_not_prose_or_relative_paths(tmp_path: Path) -> None:
    source = tmp_path / "posix.xml"
    source.write_text(
        '<ExportFile><Source note="Keep / ordinary prose" path="/projects/Private User/export.xml"/> '
        '<Objects><Object guid="a" fullyQualifiedName="Demo.A"/></Objects></ExportFile>',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out", share_safe=True)
    manifest = (output / "manifest.json").read_text(encoding="utf-8")
    assert "/projects/Private User/export.xml" not in manifest
    assert "Keep / ordinary prose" in manifest


def test_validate_output_checks_manifest_dependency_count_and_projection_file(tmp_path: Path) -> None:
    source = tmp_path / "projection.xml"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"/></Object>'), encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["dependency_count"] = 999
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(GXKBError, match="dependency_count"):
        validate_output(output)
    manifest["dependency_count"] = 0
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    records_path = output / "canonical/records.jsonl"
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    records[1]["projection_file"] = "missing.gx"
    records_path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
    with pytest.raises(GXKBError, match="recorded projection"):
        validate_output(output)


@pytest.mark.parametrize("field", ["normalized_path", "projection_file"])
@pytest.mark.parametrize("bad_path", ["/outside/file", "C:\\outside\\file", "../outside/file"])
def test_validate_output_rejects_absolute_and_out_of_tree_projection_paths(tmp_path: Path, field: str, bad_path: str) -> None:
    source = tmp_path / "paths.xml"
    source.write_text(_incremental_xml("v1", '<Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown"/></Object>'), encoding="utf-8")
    output = normalize(source, tmp_path / "out")
    records_path = output / "canonical/records.jsonl"
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    record = next(record for record in records if record["record_type"] == "object" if field == "normalized_path") if field == "normalized_path" else next(record for record in records if record["record_type"] == "part")
    record[field] = bad_path
    records_path.write_text("\n".join(json.dumps(item) for item in records) + "\n", encoding="utf-8")
    with pytest.raises(GXKBError, match=field):
        validate_output(output)


def test_inferred_dependency_id_survives_variable_sibling_insertion(tmp_path: Path) -> None:
    source = tmp_path / "stable.xml"
    prefix = '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">'
    suffix = '</Part></Object></Objects></ExportFile>'
    source.write_text(prefix + '<Variable Name="first" basedOn="Demo.B"/><Variable Name="second" basedOn="Demo.C"/>' + suffix, encoding="utf-8")
    first = normalize(source, tmp_path / "one")
    source.write_text(prefix + '<Variable Name="inserted" basedOn="Demo.X"/><Variable Name="first" basedOn="Demo.B"/><Variable Name="second" basedOn="Demo.C"/>' + suffix, encoding="utf-8")
    second = normalize(source, tmp_path / "two")
    def inferred(path: Path) -> dict[str, str]:
        return {record["evidence"]["variable"]: record["id"] for record in (json.loads(line) for line in (path / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines()) if record["record_type"] == "dependency"}
    assert inferred(first)["first"] == inferred(second)["first"]
    assert inferred(first)["second"] == inferred(second)["second"]


def test_ids_ignore_xml_attribute_order_and_formatting(tmp_path: Path) -> None:
    source = tmp_path / "identity.xml"
    first = '<ExportFile><Objects><Object guid="a" fullyQualifiedName="Demo.A"><Part type="unknown" name="x"><Reference guid="b" name="B"/></Part></Object></Objects></ExportFile>'
    second = '<ExportFile><Objects>\n  <Object fullyQualifiedName="Demo.A" guid="a">\n    <Part name="x" type="unknown">\n      <Reference name="B" guid="b" />\n    </Part>\n  </Object>\n</Objects></ExportFile>'
    source.write_text(first, encoding="utf-8")
    first_output = normalize(source, tmp_path / "out1")
    source.write_text(second, encoding="utf-8")
    second_output = normalize(source, tmp_path / "out2")
    def ids(path: Path) -> set[str]:
        return {record["id"] for record in (json.loads(line) for line in (path / "canonical/records.jsonl").read_text(encoding="utf-8").splitlines())}
    assert ids(first_output) == ids(second_output)


def test_new_part_projection_is_conservative_redacted_and_preserves_multiple_parts(tmp_path: Path) -> None:
    source = tmp_path / "parts.xml"
    source.write_text(
        r'''<ExportFile><Objects><Object guid="o1" fullyQualifiedName="Demo.Parts" type="36e32e2d-023e-4188-95df-d13573bac2e0">
        <Part type="00000000-0000-0000-0002-000000000005"><ExternalMembers><ExternalProperty path="C:\Users\julian\secret"/><ExternalMethod name="Run"/><ExternalEvent name="Changed"/></ExternalMembers></Part>
        <Part type="ad3ca970-19d0-44e1-a7b7-db05556e820c"><Help><HelpItem><Content>Useful help</Content></HelpItem></Help></Part>
        <Part type="babf62c5-0111-49e9-a1c3-cc004d90900a"><InnerHtml>&lt;p&gt;C:\Users\julian\secret&lt;/p&gt;</InnerHtml></Part>
        <Part type="babf62c5-0111-49e9-a1c3-cc004d90900a"><InnerHtml>second</InnerHtml></Part>
        </Object></Objects></ExportFile>''',
        encoding="utf-8",
    )
    output = normalize(source, tmp_path / "out", preserve_raw=False, redact_source=True)
    obj = output / "objects/Demo/Parts"
    assert json.loads((obj / "external-members.json").read_text(encoding="utf-8"))["external_properties"]
    assert "Useful help" in (obj / "help.md").read_text(encoding="utf-8")
    assert (obj / "object-defaults.json").exists() and (obj / "object-defaults-002.json").exists()
    projection_text = "\n".join(path.read_text(encoding="utf-8") for path in obj.rglob("*.json"))
    assert "C:\\Users\\julian" not in projection_text
    assert "[REDACTED_PATH]" in projection_text
    defaults = json.loads((obj / "object-defaults.json").read_text(encoding="utf-8"))
    assert "raw_xml" in defaults and "InnerHtml" in defaults["raw_xml"]
