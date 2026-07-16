from __future__ import annotations

import base64
import hashlib
import io
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from html import escape
from typing import Any

import markdown as markdown_lib
from IPython.display import HTML, display

Screen = dict[str, str]


def _esc(value: Any) -> str:
    return escape(str(value), quote=True)


COLOR_PALETTE = {
    "blue": "#2563EB",
    "green": "#15803D",
    "amber": "#B45309",
    "red": "#DC2626",
    "purple": "#7C3AED",
    "cyan": "#0891B2",
    "gray": "#57534E",
}


COMPACT_TYPOGRAPHY = {
    "fs_module_title": "28px",
    "fs_screen_title": "22px",
    "fs_cover_title": "30px",
    "fs_subtitle": "16px",
    "fs_body": "15px",
    "fs_meta": "13px",
    "fs_members": "19px",
    "fs_card_title": "20px",
    "fs_small": "13px",
    "line_body": "1.45",
    "line_members": "1.55",
    "page_padding": "18px",
    "panel_padding": "18px",
    "card_padding": "18px",
}


def create_theme(**overrides: str) -> dict[str, str]:
    theme = {
        "primary": "#1a73e8",
        "accent": "#34a853",
        "bg": "#f8fafc",
        "surface": "#ffffff",
        "surface_2": "#eef4ff",
        "text": "#0f172a",
        "muted": "#64748b",
        "border": "#d7e3f5",
        "success": "#34a853",
        "warning": "#fbbc05",
        "danger": "#ea4335",
        "info": "#1a73e8",
        "radius": "20px",
        "shadow": "0 14px 35px rgba(15, 23, 42, .10)",
        "font": "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
        "fs_cover_title": "38px",
        "fs_page_title": "31px",
        "fs_module_title": "31px",
        "fs_screen_title": "24px",
        "fs_card_title": "22px",
        "fs_subtitle": "20px",
        "fs_body": "16px",
        "fs_small": "14px",
        "fs_meta": "15px",
        "fs_members": "22px",
        "fs_table": "14px",
        "line_body": "1.62",
        "line_members": "1.7",
        "page_padding": "24px",
        "card_padding": "22px",
        "panel_padding": "20px",
    }
    theme.update(overrides)
    return theme


THEME_PRESETS = {
    "clean": create_theme(),
    "dark": create_theme(
        primary="#6ea8ff",
        accent="#34d399",
        bg="#081224",
        surface="#0d1830",
        surface_2="#111d36",
        text="#f8fafc",
        muted="#b8c4d9",
        border="#2a3d63",
        shadow="0 14px 32px rgba(0,0,0,.25)",
    ),
    "blueprint": create_theme(
        primary="#1f4e8c",
        accent="#c9a227",
        bg="#f8fafc",
        surface="#ffffff",
        surface_2="#e8f0fe",
        text="#102a43",
        muted="#52606d",
        border="#bcccdc",
        shadow="0 14px 35px rgba(16, 42, 67, .12)",
    ),
    "paper": create_theme(
        primary="#92400e",
        accent="#ca8a04",
        bg="#fffbeb",
        surface="#fff7ed",
        surface_2="#fef3c7",
        text="#1c1917",
        muted="#78716c",
        border="#fed7aa",
        shadow="0 12px 28px rgba(120, 53, 15, .12)",
    ),
}


@dataclass
class NotebookUX:
    theme: dict[str, str] = field(default_factory=create_theme)
    language: str = "pt"

    def use_theme(self, name: str | Mapping[str, str] = "clean", **overrides: str) -> dict[str, str]:
        if isinstance(name, Mapping):
            theme = create_theme(**dict(name))
        else:
            theme = dict(THEME_PRESETS.get(str(name), THEME_PRESETS["clean"]))
        theme.update(overrides)
        self.theme = theme
        return self.theme

    def setup(
        self,
        theme: str | Mapping[str, str] = "blueprint",
        compact: bool = False,
        language: str = "pt",
        **overrides: str,
    ) -> dict[str, str]:
        self.language = language
        self.use_theme(theme)
        if compact:
            self.theme.update(COMPACT_TYPOGRAPHY)
        self.theme.update(overrides)
        return self.theme

    def set_typography(self, **overrides: str) -> dict[str, str]:
        self.theme.update(overrides)
        return self.theme

    def color(self, value: str | None, fallback: str | None = None) -> str:
        if value is None or str(value).strip() == "":
            return self.color(fallback, fallback=None) if fallback else self.theme["primary"]

        text = str(value).strip()
        lowered = text.lower()
        if lowered in COLOR_PALETTE:
            return COLOR_PALETTE[lowered]
        if lowered in self.theme:
            return self.theme[lowered]
        if text.startswith(("#", "rgb", "hsl", "var(")):
            return text
        if fallback is not None:
            return self.color(fallback, fallback=None)
        return text

    def root_style(self) -> str:
        t = self.theme
        return (
            "box-sizing:border-box;"
            f"background:{t['bg']};"
            f"color:{t['text']};"
            f"font-family:{t['font']};"
            f"padding:{t['page_padding']};"
            f"border:1px solid {t['border']};"
            f"border-radius:{t['radius']};"
            f"box-shadow:{t['shadow']};"
            "margin:14px 0;"
        )

    def panel_style(self) -> str:
        t = self.theme
        return (
            "box-sizing:border-box;"
            f"background:{t['surface']};"
            f"border:1px solid {t['border']};"
            f"border-radius:{t['radius']};"
            f"padding:{t['panel_padding']};"
            "overflow:hidden;"
        )

    def wrap(self, html: str) -> None:
        display(HTML(html))

    def page_html(
        self,
        title: str,
        current: int | None = 1,
        total: int | None = None,
        subtitle: str = "",
    ) -> str:
        t = self.theme
        number_html = ""
        if current is not None:
            total_html = f"/ {total}" if total is not None else ""
            number_html = f"""
            <div style="color:{t['primary']};font-size:{t['fs_small']};font-weight:900;letter-spacing:.08em;text-transform:uppercase;">
                Pagina {current}{total_html}
            </div>
            """

        subtitle_html = ""
        if subtitle:
            subtitle_html = f"""
            <div style="color:{t['muted']};font-size:{t['fs_body']};line-height:{t['line_body']};margin-top:8px;">
                {_esc(subtitle)}
            </div>
            """

        return f"""
        <div style="{self.root_style()}">
            {number_html}
            <div style="font-size:{t['fs_page_title']};font-weight:950;line-height:1.12;margin-top:6px;">
                {_esc(title)}
            </div>
            {subtitle_html}
        </div>
        """

    def page(
        self,
        title: str,
        current: int | None = 1,
        total: int | None = None,
        subtitle: str = "",
    ) -> None:
        self.wrap(self.page_html(title, current=current, total=total, subtitle=subtitle))

    def section_html(self, title: str, subtitle: str = "", kicker: str = "") -> str:
        t = self.theme
        kicker_html = ""
        if kicker:
            kicker_html = f"""
            <div style="color:{t['accent']};font-size:{t['fs_small']};font-weight:900;letter-spacing:.11em;text-transform:uppercase;">
                {_esc(kicker)}
            </div>
            """

        subtitle_html = ""
        if subtitle:
            subtitle_html = f"""
            <div style="color:{t['muted']};font-size:{t['fs_body']};line-height:{t['line_body']};margin-top:8px;">
                {_esc(subtitle)}
            </div>
            """

        return f"""
        <div style="{self.root_style()}">
            {kicker_html}
            <div style="font-size:{t['fs_page_title']};font-weight:950;line-height:1.12;margin-top:6px;">
                {_esc(title)}
            </div>
            {subtitle_html}
        </div>
        """

    def section(self, title: str, subtitle: str = "", kicker: str = "") -> None:
        self.wrap(self.section_html(title, subtitle=subtitle, kicker=kicker))

    def cover_html(
        self,
        title: str,
        subtitle: str = "",
        logo_url: str = "",
        meta: Sequence[tuple[str, str]] | None = None,
        bullets: Sequence[str] | None = None,
        people: Sequence[tuple[str, str]] | None = None,
    ) -> str:
        t = self.theme
        logo_block = ""
        if logo_url:
            logo_block = f"""
            <div style="
                width:92px;height:92px;display:flex;align-items:center;justify-content:center;
                background:{t['surface_2']};border:1px solid {t['border']};border-radius:22px;overflow:hidden;flex-shrink:0;
            ">
                <img src="{_esc(logo_url)}" style="width:72px;height:72px;object-fit:contain;display:block;" />
            </div>
            """

        meta_html = "".join(
            f"""
            <div style="background:{t['surface']};border:1px solid {t['border']};border-radius:16px;padding:10px 13px;">
                <div style="color:{t['primary']};font-size:{t['fs_small']};font-weight:900;">{_esc(key)}</div>
                <div style="color:{t['text']};font-size:{t['fs_meta']};font-weight:750;margin-top:2px;">{_esc(value)}</div>
            </div>
            """
            for key, value in (meta or [])
        )
        bullet_html = "".join(
            f'<li style="margin-bottom:7px;line-height:{t["line_body"]};">{_esc(item)}</li>'
            for item in (bullets or [])
        )
        people_html = "".join(
            f"""
            <div style="padding:10px 0;border-bottom:1px solid {t['border']};">
                <div style="font-size:{t['fs_members']};font-weight:850;line-height:1.35;">{_esc(name)}</div>
                <div style="color:{t['muted']};font-size:{t['fs_small']};margin-top:2px;">{_esc(detail)}</div>
            </div>
            """
            for name, detail in (people or [])
        )

        return f"""
        <div style="
            box-sizing:border-box;
            background:linear-gradient(180deg, {t['surface']}, {t['surface_2']});
            color:{t['text']};
            font-family:{t['font']};
            padding:24px;
            border:1px solid {t['border']};
            border-radius:26px;
            box-shadow:{t['shadow']};
            margin:14px 0;
        ">
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:20px;align-items:stretch;">
                <div style="display:flex;flex-direction:column;justify-content:center;gap:14px;min-height:280px;">
                    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
                        {logo_block}
                        <div style="min-width:0;">
                            <div style="color:{t['primary']};font-size:{t['fs_small']};font-weight:900;letter-spacing:.08em;text-transform:uppercase;">
                                NotebookUX
                            </div>
                            <div style="color:{t['muted']};font-size:{t['fs_body']};font-weight:650;margin-top:4px;">
                                {_esc(subtitle)}
                            </div>
                        </div>
                    </div>
                    <div style="font-size:{t['fs_cover_title']};font-weight:950;line-height:1.08;max-width:820px;">
                        {_esc(title)}
                    </div>
                    <div style="display:flex;flex-wrap:wrap;gap:10px;">{meta_html}</div>
                </div>
                <div style="background:{t['surface']};border:1px solid {t['border']};border-radius:24px;padding:20px;display:flex;flex-direction:column;justify-content:center;">
                    <div style="color:{t['primary']};font-size:{t['fs_small']};font-weight:900;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;">
                        Detalhes
                    </div>
                    <ul style="margin:0;padding-left:20px;color:{t['text']};font-size:{t['fs_body']};">{bullet_html}</ul>
                    <div style="margin-top:12px;border-top:1px solid {t['border']};padding-top:12px;">{people_html}</div>
                </div>
            </div>
        </div>
        """

    def cover(
        self,
        title: str,
        subtitle: str = "",
        logo_url: str = "",
        meta: Sequence[tuple[str, str]] | None = None,
        bullets: Sequence[str] | None = None,
        people: Sequence[tuple[str, str]] | None = None,
    ) -> None:
        self.wrap(
            self.cover_html(
                title=title,
                subtitle=subtitle,
                logo_url=logo_url,
                meta=meta,
                bullets=bullets,
                people=people,
            )
        )

    def badge_row_html(self, items: Sequence[tuple[str, str]]) -> str:
        t = self.theme
        html = "".join(
            f"""
            <span style="
                display:inline-block;background:{self.color(color)};color:white;border-radius:999px;padding:8px 13px;margin:4px 6px 4px 0;
                font-size:{t['fs_small']};font-weight:950;white-space:nowrap;
            ">{_esc(label)}</span>
            """
            for label, color in items
        )
        return f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin:14px 0;">{html}</div>'

    def badge_row(self, items: Sequence[tuple[str, str]]) -> None:
        self.wrap(self.badge_row_html(items))

    def badges_html(self, items: Sequence[tuple[str, str]]) -> str:
        return self.badge_row_html(items)

    def badges(self, items: Sequence[tuple[str, str]]) -> None:
        self.badge_row(items)

    def card_html(self, title: str, body: str = "", variant: str = "default") -> str:
        t = self.theme
        variant = (variant or "default").lower().strip()
        variants = {
            "hero": (
                f"linear-gradient(135deg,{t['primary']},{t['accent']})",
                "#ffffff",
                "rgba(255,255,255,.94)",
                "0",
            ),
            "info": ("#e8f0fe", "#174ea6", "#0f172a", f"1px solid {t['info']}"),
            "success": ("#e6f4ea", "#137333", "#0f172a", f"1px solid {t['success']}"),
            "warning": ("#fef7e0", "#b06000", "#0f172a", f"1px solid {t['warning']}"),
            "danger": ("#fce8e6", "#a50e0e", "#0f172a", f"1px solid {t['danger']}"),
            "default": (t["surface"], t["text"], t["text"], f"1px solid {t['border']}"),
        }
        bg, title_color, body_color, border = variants.get(variant, variants["default"])
        body_html = _esc(body).replace("\n", "<br>")

        return f"""
        <div style="
            background:{bg};
            border:{border};
            border-radius:{t['radius']};
            padding:{t['card_padding']};
            margin:14px 0;
        ">
            <div style="
                font-size:{t['fs_card_title']};
                font-weight:950;
                color:{title_color};
                line-height:1.18;
                margin-bottom:10px;
            ">
                {_esc(title)}
            </div>
            <div style="
                font-size:{t['fs_body']};
                line-height:{t['line_body']};
                color:{body_color};
            ">
                {body_html}
            </div>
        </div>
        """

    def card(self, title: str, body: str = "", variant: str = "default") -> None:
        self.wrap(self.card_html(title, body=body, variant=variant))

    def callout_html(self, title: str, body: str = "", variant: str = "info") -> str:
        return self.card_html(title, body=body, variant=variant)

    def callout(self, title: str, body: str = "", variant: str = "info") -> None:
        self.wrap(self.callout_html(title, body=body, variant=variant))

    def grid_html(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any]],
        min_width: str = "220px",
    ) -> str:
        t = self.theme
        blocks: list[str] = []

        for item in items:
            if isinstance(item, Mapping):
                title = item.get("title", "")
                body = item.get("body", item.get("text", ""))
                color = item.get("color", t["primary"])
            else:
                title = item[0] if len(item) > 0 else ""
                body = item[1] if len(item) > 1 else ""
                color = item[2] if len(item) > 2 else t["primary"]
            color = self.color(color, fallback="primary")

            blocks.append(
                f"""
                <div style="background:{t['surface']};border:1px solid {t['border']};border-radius:{t['radius']};padding:18px;">
                    <div style="font-size:{t['fs_body']};font-weight:950;color:{color};margin-bottom:8px;">{_esc(title)}</div>
                    <div style="color:{t['muted']};font-size:{t['fs_small']};line-height:{t['line_body']};">{_esc(body)}</div>
                </div>
                """
            )

        return f"""
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({min_width},1fr));gap:12px;margin:14px 0;">
            {''.join(blocks)}
        </div>
        """

    def grid(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any]],
        min_width: str = "220px",
    ) -> None:
        self.wrap(self.grid_html(items, min_width=min_width))

    def card_grid(self, cards: Sequence[tuple[str, str, str]], min_width: str = "220px") -> None:
        self.grid(cards, min_width=min_width)

    def cards_html(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any]],
        min_width: str = "220px",
    ) -> str:
        return self.grid_html(items, min_width=min_width)

    def cards(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any]],
        min_width: str = "220px",
    ) -> None:
        self.grid(items, min_width=min_width)

    def metrics_html(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any]],
        title: str = "",
        min_width: str = "160px",
    ) -> str:
        t = self.theme
        title_html = self._block_title_html(title)
        blocks = []
        for item in items:
            metric = self._normalize_metric(item)
            color = self.color(metric["color"], fallback="primary")
            note_html = ""
            if metric["note"]:
                note_html = f"""
                <div style="color:{t['muted']};font-size:{t['fs_small']};font-weight:650;line-height:1.35;margin-top:8px;">
                    {_esc(metric["note"])}
                </div>
                """
            blocks.append(
                f"""
                <div style="background:{t['surface']};border:1px solid {t['border']};border-radius:{t['radius']};padding:18px;position:relative;overflow:hidden;">
                    <div style="position:absolute;top:0;left:0;width:6px;height:100%;background:{color};"></div>
                    <div style="color:{t['muted']};font-size:{t['fs_small']};font-weight:850;line-height:1.3;margin-left:4px;">
                        {_esc(metric["label"])}
                    </div>
                    <div style="color:{t['text']};font-size:28px;font-weight:950;line-height:1.1;margin-top:7px;margin-left:4px;">
                        {_esc(metric["value"])}
                    </div>
                    {note_html}
                </div>
                """
            )

        return f"""
        <div style="margin:14px 0;">
            {title_html}
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({min_width},1fr));gap:12px;">
                {''.join(blocks)}
            </div>
        </div>
        """

    def metrics(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any]],
        title: str = "",
        min_width: str = "160px",
    ) -> None:
        self.wrap(self.metrics_html(items, title=title, min_width=min_width))

    def checklist_html(self, items: Sequence[Mapping[str, Any] | Sequence[Any] | str], title: str = "Checklist") -> str:
        t = self.theme
        rows = []
        for item in items:
            check = self._normalize_check_item(item)
            color = self.color("green" if check["done"] else "gray")
            symbol = "&#10003;" if check["done"] else "&#9675;"
            note_html = ""
            if check["note"]:
                note_html = f"""
                <div style="color:{t['muted']};font-size:{t['fs_small']};line-height:1.4;margin-top:3px;">
                    {_esc(check["note"])}
                </div>
                """
            rows.append(
                f"""
                <div style="display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-bottom:1px solid {t['border']};">
                    <div style="width:24px;height:24px;border-radius:999px;background:{color};color:white;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:950;flex-shrink:0;">
                        {symbol}
                    </div>
                    <div>
                        <div style="color:{t['text']};font-size:{t['fs_body']};font-weight:800;line-height:1.35;">
                            {_esc(check["label"])}
                        </div>
                        {note_html}
                    </div>
                </div>
                """
            )

        return f"""
        <div style="{self.panel_style()}margin:14px 0;">
            {self._block_title_html(title)}
            <div>{''.join(rows)}</div>
        </div>
        """

    def checklist(self, items: Sequence[Mapping[str, Any] | Sequence[Any] | str], title: str = "Checklist") -> None:
        self.wrap(self.checklist_html(items, title=title))

    def steps_html(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any] | str],
        title: str = "",
        numbered: bool = True,
    ) -> str:
        t = self.theme
        blocks = []
        for index, item in enumerate(items, start=1):
            step = self._normalize_step(item)
            color = self._status_color(step["status"], fallback="blue")
            marker = str(index) if numbered else "&#9679;"
            body_html = ""
            if step["body"]:
                body_html = f"""
                <div style="color:{t['muted']};font-size:{t['fs_small']};line-height:1.48;margin-top:5px;">
                    {_esc(step["body"])}
                </div>
                """
            blocks.append(
                f"""
                <div style="display:flex;gap:12px;align-items:flex-start;background:{t['surface']};border:1px solid {t['border']};border-radius:{t['radius']};padding:16px;">
                    <div style="width:34px;height:34px;border-radius:14px;background:{color};color:white;display:flex;align-items:center;justify-content:center;font-size:{t['fs_small']};font-weight:950;flex-shrink:0;">
                        {marker}
                    </div>
                    <div>
                        <div style="color:{t['text']};font-size:{t['fs_body']};font-weight:950;line-height:1.25;">
                            {_esc(step["title"])}
                        </div>
                        {body_html}
                    </div>
                </div>
                """
            )

        return f"""
        <div style="margin:14px 0;">
            {self._block_title_html(title)}
            <div style="display:grid;gap:10px;">
                {''.join(blocks)}
            </div>
        </div>
        """

    def steps(
        self,
        items: Sequence[Mapping[str, Any] | Sequence[Any] | str],
        title: str = "",
        numbered: bool = True,
    ) -> None:
        self.wrap(self.steps_html(items, title=title, numbered=numbered))

    def compare_html(
        self,
        left_title: str,
        left_body: str,
        right_title: str,
        right_body: str,
        title: str = "",
    ) -> str:
        t = self.theme
        left_body_html = _esc(left_body).replace("\n", "<br>")
        right_body_html = _esc(right_body).replace("\n", "<br>")
        return f"""
        <div style="margin:14px 0;">
            {self._block_title_html(title)}
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;">
                <div style="{self.panel_style()}">
                    <div style="color:{t['primary']};font-size:{t['fs_card_title']};font-weight:950;margin-bottom:8px;">
                        {_esc(left_title)}
                    </div>
                    <div style="color:{t['text']};font-size:{t['fs_body']};line-height:{t['line_body']};">
                        {left_body_html}
                    </div>
                </div>
                <div style="{self.panel_style()}">
                    <div style="color:{t['accent']};font-size:{t['fs_card_title']};font-weight:950;margin-bottom:8px;">
                        {_esc(right_title)}
                    </div>
                    <div style="color:{t['text']};font-size:{t['fs_body']};line-height:{t['line_body']};">
                        {right_body_html}
                    </div>
                </div>
            </div>
        </div>
        """

    def compare(
        self,
        left_title: str,
        left_body: str,
        right_title: str,
        right_body: str,
        title: str = "",
    ) -> None:
        self.wrap(self.compare_html(left_title, left_body, right_title, right_body, title=title))

    def key_values_html(self, items: Mapping[str, Any] | Sequence[Mapping[str, Any] | Sequence[Any]], title: str = "") -> str:
        t = self.theme
        blocks = []
        for item in self._iter_key_values(items):
            color = self.color(item["color"], fallback="primary")
            blocks.append(
                f"""
                <div style="background:{t['surface']};border:1px solid {t['border']};border-radius:16px;padding:10px 13px;">
                    <div style="color:{color};font-size:{t['fs_small']};font-weight:900;">{_esc(item["key"])}</div>
                    <div style="color:{t['text']};font-size:{t['fs_meta']};font-weight:750;margin-top:2px;">{_esc(item["value"])}</div>
                </div>
                """
            )

        return f"""
        <div style="margin:14px 0;">
            {self._block_title_html(title)}
            <div style="display:flex;flex-wrap:wrap;gap:10px;">
                {''.join(blocks)}
            </div>
        </div>
        """

    def key_values(self, items: Mapping[str, Any] | Sequence[Mapping[str, Any] | Sequence[Any]], title: str = "") -> None:
        self.wrap(self.key_values_html(items, title=title))

    def code_block_html(self, code_text: str, title: str = "Codigo") -> str:
        t = self.theme
        return f"""
        <div style="background:{t['surface']};border:1px solid {t['border']};border-radius:{t['radius']};padding:16px;overflow:hidden;margin:14px 0;">
            <div style="color:{t['primary']};font-size:{t['fs_body']};font-weight:950;margin-bottom:10px;">{_esc(title)}</div>
            <pre style="margin:0;white-space:pre-wrap;word-break:break-word;background:{t['surface_2']};border:1px solid {t['border']};border-radius:16px;padding:14px;font-size:13px;line-height:1.55;color:{t['text']};"><code>{_esc(code_text)}</code></pre>
        </div>
        """

    def code_block(self, code_text: str, title: str = "Codigo") -> None:
        self.wrap(self.code_block_html(code_text, title=title))

    def table_html(self, obj: Any, title: str = "Tabela", subtitle: str = "", max_rows: int | None = None) -> str:
        t = self.theme
        try:
            data = obj.head(max_rows) if max_rows and hasattr(obj, "head") else obj
            table = data.to_html(index=True, border=0)
        except Exception:
            table = f"<pre>{_esc(obj)}</pre>"

        table = re.sub(
            r"<table[^>]*>",
            f"""
            <table style="
                width:100%;
                border-collapse:separate;
                border-spacing:0;
                color:{t['text']};
                font-size:{t['fs_table']};
                background:{t['surface']};
            ">
            """,
            table,
            count=1,
        )
        table = re.sub(
            r"<th([^>]*)>",
            f"""
            <th style="
                text-align:left;
                padding:11px;
                border-bottom:1px solid {t['border']};
                background:{t['surface_2']};
                color:{t['primary']};
                font-weight:900;
            ">
            """,
            table,
        )
        table = re.sub(
            r"<td([^>]*)>",
            f"""
            <td style="
                padding:10px 11px;
                border-bottom:1px solid {t['border']};
                color:{t['text']};
            ">
            """,
            table,
        )

        subtitle_html = ""
        if subtitle:
            subtitle_html = f"""
            <div style="color:{t['muted']};font-size:{t['fs_small']};margin-top:4px;">
                {_esc(subtitle)}
            </div>
            """

        return f"""
        <div style="{self.panel_style()}margin:14px 0;">
            <div style="font-size:{t['fs_card_title']};font-weight:950;color:{t['primary']};margin-bottom:4px;">
                {_esc(title)}
            </div>
            {subtitle_html}
            <div style="margin-top:12px;overflow:auto;border:1px solid {t['border']};border-radius:16px;">
                {table}
            </div>
        </div>
        """

    def table(self, obj: Any, title: str = "Tabela", subtitle: str = "", max_rows: int | None = None) -> None:
        self.wrap(self.table_html(obj, title=title, subtitle=subtitle, max_rows=max_rows))

    def table_card(self, title: str, table_html: str) -> None:
        t = self.theme
        self.wrap(
            f"""
            <div style="{self.panel_style()}margin:14px 0;">
                <div style="color:{t['primary']};font-size:{t['fs_body']};font-weight:950;margin-bottom:10px;">{_esc(title)}</div>
                <div style="overflow:auto;border:1px solid {t['border']};border-radius:16px;background:{t['surface_2']};padding:10px;">
                    {table_html}
                </div>
            </div>
            """
        )

    def figure_html(self, fig: Any, title: str = "Grafico", subtitle: str = "", dpi: int = 130) -> str:
        t = self.theme
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=dpi)
        data = base64.b64encode(buf.getvalue()).decode("ascii")

        subtitle_html = ""
        if subtitle:
            subtitle_html = f"""
            <div style="color:{t['muted']};font-size:{t['fs_small']};margin-top:4px;">
                {_esc(subtitle)}
            </div>
            """

        return f"""
        <div style="{self.panel_style()}margin:14px 0;">
            <div style="font-size:{t['fs_card_title']};font-weight:950;color:{t['primary']};margin-bottom:4px;">
                {_esc(title)}
            </div>
            {subtitle_html}
            <div style="
                margin-top:12px;
                background:white;
                border:1px solid {t['border']};
                border-radius:{t['radius']};
                padding:12px;
                text-align:center;
                overflow:auto;
            ">
                <img src="data:image/png;base64,{data}" style="max-width:100%;height:auto;border-radius:12px;" />
            </div>
        </div>
        """

    def figure(self, fig: Any, title: str = "Grafico", subtitle: str = "", dpi: int = 130) -> None:
        self.wrap(self.figure_html(fig, title=title, subtitle=subtitle, dpi=dpi))

    def markdown_html(
        self,
        text: str,
        *,
        image_url: str = "",
        image_caption: str = "",
        image_alt: str = "",
    ) -> str:
        """Render Markdown as notebook-ready HTML with optional contextual media."""
        rendered = markdown_lib.markdown(
            str(text),
            extensions=["extra", "sane_lists"],
            output_format="html",
        )
        has_image = bool(str(image_url).strip())
        media = ""
        if has_image:
            media = f"""
            <figure class="nbux-markdown-media">
                <img
                    src="{_esc(image_url)}"
                    alt="{_esc(image_alt or image_caption)}"
                    loading="lazy"
                />
                <figcaption>{_esc(image_caption)}</figcaption>
            </figure>
            """

        body_class = "nbux-markdown-layout has-media" if has_image else "nbux-markdown-layout"
        t = self.theme
        return f"""
        <style>
            .nbux-markdown-layout {{
                color:{t['text']};
                font-size:{t['fs_body']};
                line-height:{t['line_body']};
                min-width:0;
            }}
            .nbux-markdown-layout.has-media {{
                display:grid;
                grid-template-columns:minmax(0, 1fr) minmax(220px, 38%);
                gap:22px;
                align-items:start;
            }}
            .nbux-markdown-prose {{min-width:0;overflow-wrap:anywhere;}}
            .nbux-markdown-prose h1,
            .nbux-markdown-prose h2,
            .nbux-markdown-prose h3,
            .nbux-markdown-prose h4 {{
                color:{t['primary']};
                line-height:1.2;
                margin:1.1em 0 .45em;
                letter-spacing:0;
            }}
            .nbux-markdown-prose h1:first-child,
            .nbux-markdown-prose h2:first-child,
            .nbux-markdown-prose h3:first-child {{margin-top:0;}}
            .nbux-markdown-prose a {{color:{t['primary']};font-weight:750;}}
            .nbux-markdown-prose img {{max-width:100%;height:auto;}}
            .nbux-markdown-prose table {{
                width:100%;
                border-collapse:collapse;
                margin:14px 0;
                display:block;
                overflow-x:auto;
            }}
            .nbux-markdown-prose th,
            .nbux-markdown-prose td {{
                border:1px solid {t['border']};
                padding:9px 11px;
                text-align:left;
                white-space:nowrap;
            }}
            .nbux-markdown-prose th {{background:{t['surface_2']};color:{t['primary']};}}
            .nbux-markdown-prose details {{
                border:1px solid {t['border']};
                border-radius:{t['radius']};
                padding:12px 14px;
                margin:12px 0;
                background:{t['surface']};
            }}
            .nbux-markdown-prose summary {{cursor:pointer;font-weight:850;color:{t['primary']};}}
            .nbux-markdown-media {{margin:0;min-width:0;}}
            .nbux-markdown-media img {{
                display:block;
                width:100%;
                max-height:440px;
                object-fit:cover;
                border:1px solid {t['border']};
                border-radius:{t['radius']};
                background:{t['surface_2']};
            }}
            .nbux-markdown-media figcaption {{
                color:{t['muted']};
                font-size:{t['fs_small']};
                line-height:1.45;
                margin-top:8px;
            }}
            @media (max-width:760px) {{
                .nbux-markdown-layout.has-media {{grid-template-columns:minmax(0, 1fr);}}
                .nbux-markdown-media {{max-width:520px;}}
            }}
        </style>
        <div class="{body_class}">
            <div class="nbux-markdown-prose">{rendered}</div>
            {media}
        </div>
        """

    def markdown_screen(
        self,
        title: str,
        text: str,
        *,
        image_url: str = "",
        image_caption: str = "",
        image_alt: str = "",
    ) -> Screen:
        return self.screen(
            title,
            self.markdown_html(
                text,
                image_url=image_url,
                image_caption=image_caption,
                image_alt=image_alt,
            ),
        )

    def screen(self, title: str, html: str) -> Screen:
        return {"title": str(title), "html": str(html)}

    def module_html(
        self,
        title: str,
        screens: Sequence[Mapping[str, Any] | str],
        module_id: str | None = None,
    ) -> str:
        if not screens:
            raise ValueError("module_html requires at least one screen.")

        t = self.theme
        normalized = [self._normalize_screen(item) for item in screens]
        safe_module_id = self._module_id(title, module_id)
        steps_json = json.dumps(normalized, ensure_ascii=False).replace("</", "<\\/")
        first_screen = normalized[0]

        return f"""
        <div id="{safe_module_id}" style="{self.root_style()}">
            <div style="color:{t['accent']};font-size:{t['fs_small']};font-weight:900;letter-spacing:.13em;text-transform:uppercase;">
                Modulo interno
            </div>
            <div style="font-size:{t['fs_module_title']};font-weight:950;color:{t['text']};line-height:1.1;margin-top:8px;">
                {_esc(title)}
            </div>
            <div style="height:13px;background:{t['surface_2']};border:1px solid {t['border']};border-radius:999px;overflow:hidden;margin:18px 0;">
                <div id="{safe_module_id}_bar" style="height:100%;width:0%;background:linear-gradient(135deg,{t['primary']},{t['accent']});transition:width .25s;"></div>
            </div>
            <div id="{safe_module_id}_counter" style="font-weight:900;color:{t['primary']};font-size:{t['fs_small']};margin-bottom:12px;"></div>
            <div id="{safe_module_id}_content" style="{self.panel_style()}">
                <div style="font-size:{t['fs_screen_title']};font-weight:950;color:{t['primary']};line-height:1.18;margin-bottom:12px;">
                    {_esc(first_screen["title"])}
                </div>
                {first_screen["html"]}
            </div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px;">
                <button id="{safe_module_id}_prev" style="border:1px solid {t['border']};background:{t['surface_2']};color:{t['text']};border-radius:999px;padding:10px 18px;font-weight:900;cursor:pointer;font-size:{t['fs_body']};">
                    &larr; Voltar
                </button>
                <button id="{safe_module_id}_next" style="border:1px solid {t['primary']};background:{t['primary']};color:white;border-radius:999px;padding:10px 18px;font-weight:900;cursor:pointer;font-size:{t['fs_body']};">
                    Avancar &rarr;
                </button>
            </div>
        </div>
        <script>
        (() => {{
            const root = document.getElementById("{safe_module_id}");
            if (!root) return;
            const screens = {steps_json};
            let index = 0;
            const content = document.getElementById("{safe_module_id}_content");
            const counter = document.getElementById("{safe_module_id}_counter");
            const bar = document.getElementById("{safe_module_id}_bar");
            const prev = document.getElementById("{safe_module_id}_prev");
            const next = document.getElementById("{safe_module_id}_next");

            function render() {{
                const screen = screens[index];
                content.innerHTML = `
                    <div style="font-size:{t['fs_screen_title']};font-weight:950;color:{t['primary']};line-height:1.18;margin-bottom:12px;">
                        ${{screen.title}}
                    </div>
                    ${{screen.html}}
                `;
                counter.textContent = `Tela ${{index + 1}} de ${{screens.length}}`;
                bar.style.width = `${{((index + 1) / screens.length) * 100}}%`;
                prev.disabled = index === 0;
                next.disabled = index === screens.length - 1;
                prev.style.opacity = prev.disabled ? ".55" : "1";
                next.style.opacity = next.disabled ? ".55" : "1";
                if (window.MathJax?.typesetPromise) {{
                    window.MathJax.typesetPromise([content]);
                }} else if (window.MathJax?.Hub?.Queue) {{
                    window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub, content]);
                }}
            }}

            prev.addEventListener("click", () => {{
                if (index > 0) {{
                    index -= 1;
                    render();
                }}
            }});
            next.addEventListener("click", () => {{
                if (index < screens.length - 1) {{
                    index += 1;
                    render();
                }}
            }});
            render();
        }})();
        </script>
        """

    def module(
        self,
        title: str,
        screens: Sequence[Mapping[str, Any] | str],
        module_id: str | None = None,
    ) -> None:
        self.wrap(self.module_html(title, screens=screens, module_id=module_id))

    def _block_title_html(self, title: str) -> str:
        if not title:
            return ""
        t = self.theme
        return f"""
        <div style="color:{t['primary']};font-size:{t['fs_card_title']};font-weight:950;margin-bottom:10px;">
            {_esc(title)}
        </div>
        """

    @staticmethod
    def _normalize_metric(item: Mapping[str, Any] | Sequence[Any]) -> dict[str, Any]:
        if isinstance(item, Mapping):
            return {
                "label": item.get("label", item.get("title", "")),
                "value": item.get("value", ""),
                "note": item.get("note", item.get("body", "")),
                "color": item.get("color", "blue"),
            }
        return {
            "label": item[0] if len(item) > 0 else "",
            "value": item[1] if len(item) > 1 else "",
            "note": item[2] if len(item) > 2 else "",
            "color": item[3] if len(item) > 3 else "blue",
        }

    @staticmethod
    def _normalize_check_item(item: Mapping[str, Any] | Sequence[Any] | str) -> dict[str, Any]:
        if isinstance(item, str):
            return {"label": item, "done": False, "note": ""}
        if isinstance(item, Mapping):
            return {
                "label": item.get("label", item.get("title", "")),
                "done": bool(item.get("done", item.get("checked", False))),
                "note": item.get("note", item.get("body", "")),
            }
        return {
            "label": item[0] if len(item) > 0 else "",
            "done": bool(item[1]) if len(item) > 1 else False,
            "note": item[2] if len(item) > 2 else "",
        }

    @staticmethod
    def _normalize_step(item: Mapping[str, Any] | Sequence[Any] | str) -> dict[str, Any]:
        if isinstance(item, str):
            return {"title": item, "body": "", "status": ""}
        if isinstance(item, Mapping):
            return {
                "title": item.get("title", item.get("label", "")),
                "body": item.get("body", item.get("note", "")),
                "status": item.get("status", ""),
            }
        return {
            "title": item[0] if len(item) > 0 else "",
            "body": item[1] if len(item) > 1 else "",
            "status": item[2] if len(item) > 2 else "",
        }

    def _status_color(self, status: Any, fallback: str = "blue") -> str:
        normalized = str(status).lower().strip()
        status_colors = {
            "done": "green",
            "ok": "green",
            "success": "green",
            "active": "blue",
            "current": "blue",
            "warning": "amber",
            "todo": "gray",
            "pending": "gray",
            "danger": "red",
            "error": "red",
        }
        return self.color(status_colors.get(normalized, fallback), fallback=fallback)

    @staticmethod
    def _iter_key_values(items: Mapping[str, Any] | Sequence[Mapping[str, Any] | Sequence[Any]]) -> list[dict[str, Any]]:
        if isinstance(items, Mapping):
            return [{"key": key, "value": value, "color": "primary"} for key, value in items.items()]

        rows = []
        for item in items:
            if isinstance(item, Mapping):
                rows.append(
                    {
                        "key": item.get("key", item.get("label", "")),
                        "value": item.get("value", ""),
                        "color": item.get("color", "primary"),
                    }
                )
            else:
                rows.append(
                    {
                        "key": item[0] if len(item) > 0 else "",
                        "value": item[1] if len(item) > 1 else "",
                        "color": item[2] if len(item) > 2 else "primary",
                    }
                )
        return rows

    @staticmethod
    def _normalize_screen(item: Mapping[str, Any] | str) -> Screen:
        if isinstance(item, Mapping):
            return {
                "title": str(item.get("title", "Tela")),
                "html": str(item.get("html", "")),
            }
        return {"title": "Tela", "html": str(item)}

    @staticmethod
    def _module_id(title: str, module_id: str | None) -> str:
        raw = module_id or f"nux_{hashlib.sha1(str(title).encode('utf-8')).hexdigest()[:10]}"
        cleaned = re.sub(r"[^A-Za-z0-9_-]+", "-", raw).strip("-")
        if not cleaned:
            cleaned = "nux-module"
        if cleaned[0].isdigit():
            cleaned = f"nux-{cleaned}"
        return cleaned


UX = NotebookUX()
