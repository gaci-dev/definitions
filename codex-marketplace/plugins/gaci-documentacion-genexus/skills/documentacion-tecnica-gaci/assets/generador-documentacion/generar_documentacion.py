#!/usr/bin/env python3
"""Generador genérico de documentación corporativa en PDF y DOCX.

El contenido se recibe en un archivo JSON. El motor no contiene información de
ningún producto concreto y permite combinar párrafos, métricas, flujos, tablas,
pasos, bloques de código y notas.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

import cairo


PAGE_W, PAGE_H = 612, 792
MARGIN, CONTENT_W = 36, 540
BOTTOM = 744
BLUE = (0.035, 0.52, 0.75)
TEAL = (0.11, 0.65, 0.69)
GREEN = (0.63, 0.81, 0.12)
DARK = (0.18, 0.20, 0.22)
GRAY = (0.96, 0.97, 0.98)
PALE = (0.90, 0.96, 0.97)
LINE = (0.67, 0.79, 0.84)
WHITE = (1, 1, 1)
TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_LOGO = TOOL_DIR / "assets" / "gaci-group.png"


def required(data: dict[str, Any], key: str, context: str) -> Any:
    value = data.get(key)
    if value is None or value == "":
        raise ValueError(f"Falta '{key}' en {context}")
    return value


def validate(spec: dict[str, Any]) -> None:
    document = required(spec, "document", "la raíz")
    for key in ("title", "subtitle", "product", "objective", "scope", "result"):
        required(document, key, "document")
    pages = spec.get("pages", [])
    if not isinstance(pages, list):
        raise ValueError("'pages' debe ser una lista")
    valid_types = {"paragraph", "metrics", "flow", "table", "steps", "code", "note"}
    for pi, page in enumerate(pages, 1):
        required(page, "title", f"pages[{pi}]")
        for bi, block in enumerate(page.get("blocks", []), 1):
            block_type = required(block, "type", f"pages[{pi}].blocks[{bi}]")
            if block_type not in valid_types:
                raise ValueError(f"Tipo de bloque desconocido: {block_type}")
            if block_type == "table":
                columns = required(block, "columns", f"tabla {bi}")
                if not columns:
                    raise ValueError("Una tabla debe tener columnas")
                for row in block.get("rows", []):
                    if len(row) != len(columns):
                        raise ValueError("Cada fila debe tener la misma cantidad de celdas que columns")


def rgb(hex_value: str | None, fallback: tuple[float, float, float]) -> tuple[float, float, float]:
    if not hex_value:
        return fallback
    value = hex_value.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        raise ValueError(f"Color inválido: {hex_value}")
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def font(ctx: cairo.Context, size: float, bold: bool = False) -> None:
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def draw_text(ctx: cairo.Context, value: str, x: float, y: float, size=9.2, color=DARK, bold=False) -> None:
    font(ctx, size, bold)
    ctx.set_source_rgb(*color)
    ctx.move_to(x, y)
    ctx.show_text(str(value))


def wrapped(ctx: cairo.Context, value: str, width: float, size=9.2, bold=False) -> list[str]:
    font(ctx, size, bold)
    result: list[str] = []
    for paragraph in str(value).split("\n"):
        if not paragraph:
            result.append("")
            continue
        words = paragraph.split()
        line = words[0]
        for word in words[1:]:
            candidate = f"{line} {word}"
            if ctx.text_extents(candidate).width <= width:
                line = candidate
            else:
                result.append(line)
                line = word
        result.append(line)
    return result


def box(ctx: cairo.Context, x: float, y: float, width: float, height: float, fill, stroke=LINE) -> None:
    ctx.set_source_rgb(*fill)
    ctx.rectangle(x, y, width, height)
    ctx.fill_preserve()
    ctx.set_source_rgb(*stroke)
    ctx.set_line_width(0.55)
    ctx.stroke()


def image(ctx: cairo.Context, path: Path, x: float, y: float, width: float, height: float) -> None:
    surface = cairo.ImageSurface.create_from_png(str(path))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(width / surface.get_width(), height / surface.get_height())
    ctx.set_source_surface(surface, 0, 0)
    ctx.paint()
    ctx.restore()


class PdfRenderer:
    def __init__(self, spec: dict[str, Any], output: Path, logo: Path | None):
        self.spec = spec
        style = spec.get("style", {})
        self.blue = rgb(style.get("primaryColor"), BLUE)
        self.teal = rgb(style.get("secondaryColor"), TEAL)
        self.green = rgb(style.get("accentColor"), GREEN)
        self.logo = logo
        self.surface = cairo.PDFSurface(str(output), PAGE_W, PAGE_H)
        self.ctx = cairo.Context(self.surface)
        self.page = 0
        self.y = 0.0
        self.current_title = ""
        self.footer_label = spec["document"].get("footer", spec["document"]["title"])

    def header(self) -> None:
        self.ctx.set_source_rgb(*WHITE)
        self.ctx.paint()
        if self.logo:
            image(self.ctx, self.logo, PAGE_W - 104, 20, 68, 26)
        self.ctx.set_source_rgb(*self.teal)
        self.ctx.rectangle(MARGIN, 51, CONTENT_W, 1.2)
        self.ctx.fill()

    def footer(self) -> None:
        draw_text(self.ctx, self.footer_label, 44, PAGE_H - 24, 7.3, (0.4, 0.4, 0.4))
        draw_text(self.ctx, f"Página {self.page}", PAGE_W - 76, PAGE_H - 24, 7.3, (0.4, 0.4, 0.4))

    def new_page(self, title: str = "") -> None:
        if self.page:
            self.footer()
            self.ctx.show_page()
        self.page += 1
        self.current_title = title
        self.header()
        if title:
            draw_text(self.ctx, title, MARGIN, 84, 19, self.blue, True)
            self.y = 104
        else:
            self.y = 66

    def ensure(self, height: float) -> None:
        if self.y + height <= BOTTOM:
            return
        suffix = " (continuación)" if self.current_title else ""
        self.new_page(self.current_title + suffix)

    def lines(self, value: str, x: float, width: float, size=9.2, color=DARK, bold=False, leading=None) -> float:
        leading = leading or size * 1.35
        lines = wrapped(self.ctx, value, width, size, bold)
        for line in lines:
            draw_text(self.ctx, line, x, self.y, size, color, bold)
            self.y += leading
        return len(lines) * leading

    def heading(self, value: str, level=2) -> None:
        self.ensure(31)
        self.y += 7
        draw_text(self.ctx, value, MARGIN, self.y + 14, 14 if level == 2 else 12, self.blue, True)
        self.y += 25

    def cover(self) -> None:
        document = self.spec["document"]
        self.new_page()
        if self.logo:
            image(self.ctx, self.logo, 226, 81, 160, 60)
        self.y = 180
        title_lines = wrapped(self.ctx, document["title"], CONTENT_W, 20.5, True)
        for line in title_lines:
            draw_text(self.ctx, line, MARGIN, self.y, 20.5, self.blue, True)
            self.y += 24
        draw_text(self.ctx, document["subtitle"], MARGIN, self.y + 1, 11.2, (0.32, 0.34, 0.37))
        self.y += 18
        rows = [
            ("PRODUCTO", f"{document['product']}{' | ' + document['version'] if document.get('version') else ''}"),
            ("OBJETIVO", document["objective"]),
            ("ALCANCE", document["scope"]),
        ]
        if document.get("strategy"):
            rows.append(("ESTRATEGIA", document["strategy"]))
        rows.append(("RESULTADO", document["result"]))
        for label, value in rows:
            value_lines = wrapped(self.ctx, value, CONTENT_W - 104, 8.4)
            height = max(34, 12 + len(value_lines) * 11)
            box(self.ctx, MARGIN, self.y, 90, height, PALE)
            box(self.ctx, MARGIN + 90, self.y, CONTENT_W - 90, height, GRAY)
            draw_text(self.ctx, label, MARGIN + 8, self.y + height / 2 + 3, 8.2, self.blue, True)
            yy = self.y + (height - len(value_lines) * 11) / 2 + 9
            for line in value_lines:
                draw_text(self.ctx, line, MARGIN + 98, yy, 8.4)
                yy += 11
            self.y += height
        summary = self.spec.get("summary", {})
        if summary:
            self.heading(summary.get("title", "Resumen"))
            if summary.get("intro"):
                self.lines(summary["intro"], MARGIN, CONTENT_W, 9)
                self.y += 8
            if summary.get("metrics"):
                self.metrics(summary["metrics"])
            if summary.get("classification"):
                self.heading(summary.get("classificationTitle", "Clasificación"), 3)
                self.lines(summary["classification"], MARGIN, CONTENT_W, 8.8)

    def metrics(self, items: list[dict[str, Any]]) -> None:
        self.ensure(56)
        width = CONTENT_W / len(items)
        colors = [self.teal, self.green, self.blue]
        for index, item in enumerate(items):
            x = MARGIN + index * width
            box(self.ctx, x, self.y, width, 26, colors[index % 3], WHITE)
            value = str(item.get("value", ""))
            font(self.ctx, 10, True)
            tw = self.ctx.text_extents(value).width
            draw_text(self.ctx, value, x + (width - tw) / 2, self.y + 17, 10, WHITE, True)
            box(self.ctx, x, self.y + 26, width, 26, PALE, WHITE)
            label = str(item.get("label", ""))
            label_lines = wrapped(self.ctx, label, width - 10, 7.5, True)[:2]
            yy = self.y + 40 if len(label_lines) == 1 else self.y + 35
            for line in label_lines:
                font(self.ctx, 7.5, True)
                tw = self.ctx.text_extents(line).width
                draw_text(self.ctx, line, x + (width - tw) / 2, yy, 7.5, self.blue, True)
                yy += 9
        self.y += 56

    def paragraph_block(self, block: dict[str, Any]) -> None:
        if block.get("title"):
            self.heading(block["title"])
        lines = wrapped(self.ctx, block.get("text", ""), CONTENT_W, 9.1)
        self.ensure(len(lines) * 12.3 + 8)
        self.lines(block.get("text", ""), MARGIN, CONTENT_W, 9.1)
        self.y += 8

    def note(self, block: dict[str, Any]) -> None:
        if block.get("title"):
            self.heading(block["title"], 3)
        lines = wrapped(self.ctx, block.get("text", ""), CONTENT_W - 24, 8.3)
        height = 16 + len(lines) * 11
        self.ensure(height + 8)
        box(self.ctx, MARGIN, self.y, CONTENT_W, height, PALE, self.teal)
        yy = self.y + 15
        for line in lines:
            draw_text(self.ctx, line, MARGIN + 12, yy, 8.3, DARK)
            yy += 11
        self.y += height + 8

    def code(self, block: dict[str, Any]) -> None:
        if block.get("title"):
            self.heading(block["title"], 3)
        lines: list[str] = []
        for source_line in block.get("lines", []):
            lines.extend(wrapped(self.ctx, str(source_line), CONTENT_W - 24, 7.2))
        height = 16 + max(1, len(lines)) * 10
        self.ensure(height + 8)
        box(self.ctx, MARGIN, self.y, CONTENT_W, height, (0.10, 0.13, 0.17), (0.10, 0.13, 0.17))
        yy = self.y + 15
        for line in lines:
            draw_text(self.ctx, line, MARGIN + 12, yy, 7.2, WHITE)
            yy += 10
        self.y += height + 8

    def flow(self, block: dict[str, Any]) -> None:
        if block.get("title"):
            self.heading(block["title"])
        items = block.get("items", [])
        if not items:
            return
        count = len(items)
        gap = 34 if count > 1 else 0
        width = (CONTENT_W - gap * (count - 1)) / count
        body_lines = [wrapped(self.ctx, item.get("body", ""), width - 14, 7.2, True) for item in items]
        height = 40 + max(3, max(len(lines) for lines in body_lines)) * 10
        self.ensure(height + 10)
        start_y = self.y
        colors = [self.teal, self.blue, self.green]
        for index, item in enumerate(items):
            x = MARGIN + index * (width + gap)
            box(self.ctx, x, start_y, width, 30, colors[index % 3], colors[index % 3])
            title = str(item.get("title", ""))
            title_lines = wrapped(self.ctx, title, width - 10, 7.5, True)[:2]
            yy = start_y + 13 if len(title_lines) == 2 else start_y + 19
            for line in title_lines:
                font(self.ctx, 7.5, True)
                tw = self.ctx.text_extents(line).width
                draw_text(self.ctx, line, x + (width - tw) / 2, yy, 7.5, WHITE, True)
                yy += 9
            box(self.ctx, x, start_y + 30, width, height - 30, GRAY)
            yy = start_y + 48
            for line in body_lines[index]:
                font(self.ctx, 7.2, True)
                tw = self.ctx.text_extents(line).width
                draw_text(self.ctx, line, x + (width - tw) / 2, yy, 7.2, self.blue, True)
                yy += 10
            if index < count - 1:
                x1, x2, ay = x + width + 4, x + width + gap - 4, start_y + height / 2
                self.ctx.set_source_rgb(*self.blue)
                self.ctx.set_line_width(1.8)
                self.ctx.move_to(x1, ay)
                self.ctx.line_to(x2, ay)
                self.ctx.stroke()
                self.ctx.move_to(x2, ay)
                self.ctx.line_to(x2 - 7, ay - 5)
                self.ctx.move_to(x2, ay)
                self.ctx.line_to(x2 - 7, ay + 5)
                self.ctx.stroke()
                protocol = str(item.get("connector", ""))
                if protocol:
                    draw_text(self.ctx, protocol, x1, ay - 9, 6.5, self.blue, True)
        self.y += height + 10

    def table(self, block: dict[str, Any]) -> None:
        if block.get("title"):
            self.heading(block["title"])
        columns = block["columns"]
        weights = [float(column.get("width", 1)) for column in columns]
        total = sum(weights)
        widths = [CONTENT_W * weight / total for weight in weights]

        def header() -> None:
            x = MARGIN
            for column, width in zip(columns, widths):
                box(self.ctx, x, self.y, width, 25, self.blue, WHITE)
                draw_text(self.ctx, str(column["label"]), x + 7, self.y + 16, 7.5, WHITE, True)
                x += width
            self.y += 25

        self.ensure(55)
        header()
        for row_index, row in enumerate(block.get("rows", [])):
            cells = [wrapped(self.ctx, str(cell), widths[i] - 14, 7.2) for i, cell in enumerate(row)]
            height = max(28, 12 + max(len(lines) for lines in cells) * 9.5)
            if self.y + height > BOTTOM:
                self.new_page(self.current_title + " (continuación)")
                header()
            x = MARGIN
            fill = WHITE if row_index % 2 == 0 else GRAY
            for lines, width in zip(cells, widths):
                box(self.ctx, x, self.y, width, height, fill)
                yy = self.y + 16
                for line in lines:
                    draw_text(self.ctx, line, x + 7, yy, 7.2)
                    yy += 9.5
                x += width
            self.y += height
        self.y += 8

    def steps(self, block: dict[str, Any]) -> None:
        if block.get("title"):
            self.heading(block["title"])
        for item in block.get("items", []):
            title_width = float(block.get("titleWidth", 150))
            body_width = CONTENT_W - title_width
            body_lines = wrapped(self.ctx, item.get("body", ""), body_width - 14, 7.5, True)
            height = max(25, 10 + len(body_lines) * 9.5)
            self.ensure(height + 2)
            box(self.ctx, MARGIN, self.y, title_width, height, self.blue, self.blue)
            draw_text(self.ctx, str(item.get("title", "")), MARGIN + 9, self.y + 16, 7.6, WHITE, True)
            box(self.ctx, MARGIN + title_width, self.y, body_width, height, GRAY)
            yy = self.y + 16
            for line in body_lines:
                draw_text(self.ctx, line, MARGIN + title_width + 9, yy, 7.5, self.blue, True)
                yy += 9.5
            self.y += height + 2
        self.y += 6

    def render_block(self, block: dict[str, Any]) -> None:
        block_type = block["type"]
        if block_type == "paragraph": self.paragraph_block(block)
        elif block_type == "metrics":
            if block.get("title"): self.heading(block["title"])
            self.metrics(block.get("items", []))
        elif block_type == "flow": self.flow(block)
        elif block_type == "table": self.table(block)
        elif block_type == "steps": self.steps(block)
        elif block_type == "code": self.code(block)
        elif block_type == "note": self.note(block)

    def render(self) -> None:
        self.cover()
        for page in self.spec.get("pages", []):
            self.new_page(page["title"])
            if page.get("intro"):
                self.lines(page["intro"], MARGIN, CONTENT_W, 9.1)
                self.y += 8
            for block in page.get("blocks", []):
                self.render_block(block)
        self.footer()
        self.ctx.show_page()
        self.surface.finish()


def wp(value: str = "", style: str | None = None, bold=False, color=None, size=None, align=None) -> str:
    ppr = []
    if style: ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align: ppr.append(f'<w:jc w:val="{align}"/>')
    rpr = []
    if bold: rpr.append("<w:b/>")
    if color: rpr.append(f'<w:color w:val="{color}"/>')
    if size: rpr.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    return f"<w:p><w:pPr>{''.join(ppr)}</w:pPr><w:r><w:rPr>{''.join(rpr)}</w:rPr><w:t>{escape(str(value))}</w:t></w:r></w:p>"


def wc(content: str, width: int, shade=None) -> str:
    shading = f'<w:shd w:fill="{shade}"/>' if shade else ""
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shading}<w:tcMar><w:top w:w="80" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar></w:tcPr>{content}</w:tc>'


def wt(headers: list[str], rows: list[list[Any]], weights: list[float] | None = None) -> str:
    weights = weights or [1] * len(headers)
    widths = [int(9360 * weight / sum(weights)) for weight in weights]
    borders = '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="A8C9D5"/><w:left w:val="single" w:sz="4" w:color="A8C9D5"/><w:bottom w:val="single" w:sz="4" w:color="A8C9D5"/><w:right w:val="single" w:sz="4" w:color="A8C9D5"/><w:insideH w:val="single" w:sz="4" w:color="A8C9D5"/><w:insideV w:val="single" w:sz="4" w:color="A8C9D5"/></w:tblBorders>'
    xml = f'<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/>{borders}</w:tblPr>'
    xml += "<w:tr>" + "".join(wc(wp(h, bold=True, color="FFFFFF", size=18), widths[i], "0785BF") for i, h in enumerate(headers)) + "</w:tr>"
    for index, row in enumerate(rows):
        xml += "<w:tr>" + "".join(wc(wp(cell, size=17), widths[i], "F4F7F8" if index % 2 else "FFFFFF") for i, cell in enumerate(row)) + "</w:tr>"
    return xml + "</w:tbl>"


def wcode(lines: list[Any], shade="1A212B") -> str:
    return f'<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/></w:tblPr><w:tr>{wc("".join(wp(str(line), color="FFFFFF", size=16) for line in lines), 9360, shade)}</w:tr></w:tbl>'


def page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def logo_paragraph() -> str:
    return '''<w:p><w:pPr><w:jc w:val="right"/></w:pPr><w:r><w:drawing><wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" distT="0" distB="0" distL="0" distR="0"><wp:extent cx="914400" cy="345600"/><wp:docPr id="1" name="GACI Group"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="gaci-group.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId3"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="914400" cy="345600"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''


class DocxRenderer:
    def __init__(self, spec: dict[str, Any], output: Path, logo: Path | None):
        self.spec, self.output, self.logo = spec, output, logo

    def block(self, block: dict[str, Any]) -> str:
        out: list[str] = []
        if block.get("title"): out.append(wp(block["title"], "Heading2"))
        kind = block["type"]
        if kind == "paragraph": out.append(wp(block.get("text", "")))
        elif kind == "note": out.append(wt(["NOTA"], [[block.get("text", "")]], [1]))
        elif kind == "code": out.append(wcode(block.get("lines", [])))
        elif kind == "metrics":
            items = block.get("items", [])
            out.append(wt([str(i.get("label", "")) for i in items], [[str(i.get("value", "")) for i in items]]))
        elif kind == "flow":
            items = block.get("items", [])
            headers, row = [], []
            for index, item in enumerate(items):
                headers.append(str(item.get("title", "")))
                row.append(str(item.get("body", "")))
                if index < len(items) - 1:
                    headers.append("→")
                    row.append(str(item.get("connector", "")))
            out.append(wt(headers, [row]))
        elif kind == "table":
            out.append(wt([str(c["label"]) for c in block["columns"]], block.get("rows", []), [float(c.get("width", 1)) for c in block["columns"]]))
        elif kind == "steps":
            out.append(wt(["Paso", "Detalle"], [[i.get("title", ""), i.get("body", "")] for i in block.get("items", [])], [1, 3]))
        return "".join(out)

    def document_xml(self) -> str:
        d = self.spec["document"]
        body = [logo_paragraph() if self.logo else wp("GACI GROUP", bold=True, color="0785BF", size=28, align="right"), wp(d["title"], "Title"), wp(d["subtitle"], "Subtitle")]
        rows = [["Producto", f"{d['product']}{' | ' + d['version'] if d.get('version') else ''}"], ["Objetivo", d["objective"]], ["Alcance", d["scope"]]]
        if d.get("strategy"): rows.append(["Estrategia", d["strategy"]])
        rows.append(["Resultado", d["result"]])
        body.append(wt(["RESUMEN", "DETALLE"], rows, [1, 4]))
        summary = self.spec.get("summary", {})
        if summary:
            body += [wp(summary.get("title", "Resumen"), "Heading1"), wp(summary.get("intro", ""))]
            if summary.get("metrics"):
                items = summary["metrics"]
                body.append(wt([str(i.get("label", "")) for i in items], [[str(i.get("value", "")) for i in items]]))
            if summary.get("classification"):
                body += [wp(summary.get("classificationTitle", "Clasificación"), "Heading2"), wp(summary["classification"])]
        for page in self.spec.get("pages", []):
            body += [page_break(), wp(page["title"], "Heading1")]
            if page.get("intro"): body.append(wp(page["intro"]))
            body.extend(self.block(block) for block in page.get("blocks", []))
        sect = '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" w:header="360" w:footer="360"/><w:footerReference w:type="default" r:id="rId2"/></w:sectPr>'
        return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>' + "".join(body) + sect + "</w:body></w:document>"

    def render(self) -> None:
        png_default = '<Default Extension="png" ContentType="image/png"/>' if self.logo else ""
        content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>{png_default}<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>'''
        rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
        image_rel = '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/logo.png"/>' if self.logo else ""
        doc_rels = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>{image_rel}</Relationships>'
        styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="19"/><w:color w:val="303438"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="260" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr><w:rPr><w:b/><w:color w:val="0785BF"/><w:sz w:val="40"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="240"/></w:pPr><w:rPr><w:color w:val="555B61"/><w:sz w:val="23"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="90"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:color w:val="0785BF"/><w:sz w:val="30"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="70"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:color w:val="0785BF"/><w:sz w:val="25"/></w:rPr></w:style></w:styles>'''
        footer_label = escape(str(self.spec["document"].get("footer", self.spec["document"]["title"])))
        footer = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="right"/></w:pPr><w:r><w:rPr><w:color w:val="777777"/><w:sz w:val="16"/></w:rPr><w:t>{footer_label} · Página </w:t></w:r><w:fldSimple w:instr="PAGE"><w:r><w:rPr><w:color w:val="777777"/><w:sz w:val="16"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple></w:p></w:ftr>'
        with zipfile.ZipFile(self.output, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("[Content_Types].xml", content_types)
            archive.writestr("_rels/.rels", rels)
            archive.writestr("word/document.xml", self.document_xml())
            archive.writestr("word/styles.xml", styles)
            archive.writestr("word/footer1.xml", footer)
            archive.writestr("word/_rels/document.xml.rels", doc_rels)
            if self.logo:
                archive.write(self.logo, "word/media/logo.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera documentación corporativa en PDF y DOCX desde JSON")
    parser.add_argument("input", type=Path, help="Archivo JSON con el contenido")
    parser.add_argument("--output-dir", type=Path, help="Directorio de salida; por defecto, junto al JSON")
    parser.add_argument("--basename", help="Nombre base de salida; reemplaza output.basename del JSON")
    parser.add_argument("--no-logo", action="store_true", help="Genera los documentos sin logotipo")
    args = parser.parse_args()

    spec = json.loads(args.input.read_text(encoding="utf-8"))
    validate(spec)
    output_dir = (args.output_dir or args.input.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = args.basename or spec.get("output", {}).get("basename", "documentacion")
    basename = re.sub(r"[^A-Za-z0-9._-]+", "_", str(basename)).strip("._") or "documentacion"
    logo: Path | None = None
    if not args.no_logo:
        configured_logo = spec.get("style", {}).get("logo")
        logo = (args.input.parent / configured_logo).resolve() if configured_logo else DEFAULT_LOGO
        if not logo.exists():
            raise FileNotFoundError(f"No se encontró el logotipo: {logo}")
    pdf = output_dir / f"{basename}.pdf"
    docx = output_dir / f"{basename}_editable.docx"
    PdfRenderer(spec, pdf, logo).render()
    DocxRenderer(spec, docx, logo).render()
    print(pdf)
    print(docx)


if __name__ == "__main__":
    main()
