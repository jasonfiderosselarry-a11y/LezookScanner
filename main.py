#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
#   LEZOOK SCANNER v3.0
#   OSINT + Vulnerability Detection Tool
#   For Bug Bounty Hunters & Ethical Security Researchers
# ╠══════════════════════════════════════════════════════════╣
#   Contact : +261 32 542 10
#   Email   : jason.fiderosse.larry@gmail.com
#   LEGAL USE ONLY — Authorized Targets Only
# ╚══════════════════════════════════════════════════════════╝

import os, sys, threading, socket, ssl, json, re
import datetime, urllib.request, urllib.parse
import subprocess, platform, time, hashlib

os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")

from kivy.config import Config
Config.set("graphics", "width",  "1200")
Config.set("graphics", "height", "780")
Config.set("graphics", "minimum_width",  "950")
Config.set("graphics", "minimum_height", "650")
Config.set("graphics", "resizable", "1")

from kivy.lang        import Builder
from kivy.clock       import Clock
from kivy.core.window import Window
from kivy.utils       import get_color_from_hex
from kivy.uix.boxlayout   import BoxLayout
from kivy.uix.scrollview  import ScrollView
from kivy.properties  import StringProperty, BooleanProperty

from kivymd.app       import MDApp
from kivymd.uix.screen       import MDScreen
from kivymd.uix.label        import MDLabel
from kivymd.uix.button       import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield    import MDTextField
from kivymd.uix.card         import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.progressbar  import MDProgressBar
from kivymd.uix.snackbar     import Snackbar
from kivymd.uix.dialog       import MDDialog
from kivymd.uix.tab          import MDTabsBase, MDTabs
from kivymd.uix.floatlayout  import MDFloatLayout

# ─────────────────────────────────────────────────────────────
#  KV LAYOUT
# ─────────────────────────────────────────────────────────────
KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TabOSINT>:
    title: "OSINT"

<TabVuln>:
    title: "VULN"

<TabReport>:
    title: "REPORT"

<MainScreen>:
    name: "main"
    canvas.before:
        Color:
            rgba: get_color_from_hex("#020702")
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        spacing: 0

        # ─── TOP NAVBAR ────────────────────────────────────────
        BoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: ["14dp","6dp","14dp","6dp"]
            spacing: "10dp"
            canvas.before:
                Color:
                    rgba: get_color_from_hex("#030D03")
                Rectangle:
                    pos: self.pos
                    size: self.size
                Color:
                    rgba: get_color_from_hex("#00FF41")
                Line:
                    points: [self.x, self.y, self.x+self.width, self.y]
                    width: 1.2

            # Logo
            BoxLayout:
                orientation: "vertical"
                size_hint_x: None
                width: "230dp"
                spacing: 0
                MDLabel:
                    text: "◈ LEZOOK SCANNER"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#00FF41")
                    font_name: "RobotoMono-Regular"
                    bold: True
                    font_size: "18sp"
                MDLabel:
                    text: "   OSINT + VULN DETECTION v3.0"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#005A15")
                    font_name: "RobotoMono-Regular"
                    font_size: "9sp"

            # Status ticker
            MDLabel:
                id: ticker
                text: ""
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#007A20")
                font_name: "RobotoMono-Regular"
                font_size: "11sp"
                halign: "center"

            # Clock
            MDLabel:
                id: clock_lbl
                text: ""
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#00FF41")
                font_name: "RobotoMono-Regular"
                font_size: "11sp"
                size_hint_x: None
                width: "180dp"
                halign: "right"

        # ─── TARGET BAR ────────────────────────────────────────
        BoxLayout:
            size_hint_y: None
            height: "56dp"
            padding: ["14dp","6dp","14dp","6dp"]
            spacing: "10dp"
            canvas.before:
                Color:
                    rgba: get_color_from_hex("#040D04")
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDTextField:
                id: target_input
                hint_text: "  Enter target: domain.com  /  IP address  /  URL"
                font_name: "RobotoMono-Regular"
                mode: "rectangle"
                line_color_focus: get_color_from_hex("#00FF41")
                hint_text_color_normal: get_color_from_hex("#004A15")
                text_color_normal: get_color_from_hex("#00FF41")
                text_color_focus: get_color_from_hex("#00FF41")
                fill_color_normal: get_color_from_hex("#030D03")
                fill_color_focus: get_color_from_hex("#051205")
                size_hint_y: None
                height: "44dp"
                pos_hint: {"center_y": 0.5}

            # Quick-action buttons
            MDRaisedButton:
                text: "▶  SCAN ALL"
                on_release: app.launch_scan("all")
                size_hint: None, None
                size: "130dp", "40dp"
                pos_hint: {"center_y": 0.5}
                md_bg_color: get_color_from_hex("#003B00")
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#00FF41")
                font_name: "RobotoMono-Regular"
                elevation: 8

            MDRaisedButton:
                text: "⚡ VULN ONLY"
                on_release: app.launch_scan("vuln")
                size_hint: None, None
                size: "130dp", "40dp"
                pos_hint: {"center_y": 0.5}
                md_bg_color: get_color_from_hex("#3B0000")
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#FF4444")
                font_name: "RobotoMono-Regular"
                elevation: 8

            MDRaisedButton:
                text: "🔍 OSINT ONLY"
                on_release: app.launch_scan("osint")
                size_hint: None, None
                size: "130dp", "40dp"
                pos_hint: {"center_y": 0.5}
                md_bg_color: get_color_from_hex("#003040")
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#00CCFF")
                font_name: "RobotoMono-Regular"
                elevation: 8

            MDRaisedButton:
                text: "✕ CLEAR"
                on_release: app.clear_all()
                size_hint: None, None
                size: "90dp", "40dp"
                pos_hint: {"center_y": 0.5}
                md_bg_color: get_color_from_hex("#1A0808")
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#FF6666")
                font_name: "RobotoMono-Regular"

        # ─── PROGRESS ──────────────────────────────────────────
        BoxLayout:
            size_hint_y: None
            height: "24dp"
            padding: ["14dp","2dp","14dp","2dp"]
            spacing: "10dp"
            canvas.before:
                Color:
                    rgba: get_color_from_hex("#030803")
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDLabel:
                id: progress_label
                text: "[ IDLE ]"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#005A15")
                font_name: "RobotoMono-Regular"
                font_size: "10sp"
                size_hint_x: None
                width: "200dp"

            MDProgressBar:
                id: progress_bar
                value: 0
                color: get_color_from_hex("#00FF41")

            MDLabel:
                id: finding_badge
                text: ""
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#FF4444")
                font_name: "RobotoMono-Regular"
                font_size: "10sp"
                size_hint_x: None
                width: "180dp"
                halign: "right"

        # ─── MAIN BODY ─────────────────────────────────────────
        BoxLayout:
            orientation: "horizontal"
            spacing: "6dp"
            padding: ["6dp","4dp","6dp","6dp"]

            # ── LEFT SIDEBAR ────────────────────────────────────
            BoxLayout:
                orientation: "vertical"
                size_hint_x: None
                width: "240dp"
                spacing: "6dp"

                # OSINT Modules card
                MDCard:
                    orientation: "vertical"
                    md_bg_color: get_color_from_hex("#070D07")
                    radius: [6,6,6,6]
                    elevation: 6
                    padding: "10dp"
                    spacing: "4dp"

                    BoxLayout:
                        size_hint_y: None
                        height: "28dp"
                        MDLabel:
                            text: "◈ OSINT MODULES"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#00CCFF")
                            font_name: "RobotoMono-Regular"
                            bold: True
                            font_size: "12sp"
                        MDRaisedButton:
                            text: "ALL"
                            size_hint: None, None
                            size: "40dp","24dp"
                            on_release: app.toggle_osint(True)
                            md_bg_color: get_color_from_hex("#002030")
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#00CCFF")
                            font_size: "9sp"
                            font_name: "RobotoMono-Regular"
                        MDRaisedButton:
                            text: "NONE"
                            size_hint: None, None
                            size: "46dp","24dp"
                            on_release: app.toggle_osint(False)
                            md_bg_color: get_color_from_hex("#200000")
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FF6666")
                            font_size: "9sp"
                            font_name: "RobotoMono-Regular"

                    ScrollView:
                        size_hint_y: None
                        height: "240dp"
                        BoxLayout:
                            id: osint_modules
                            orientation: "vertical"
                            spacing: "2dp"
                            size_hint_y: None
                            height: self.minimum_height

                # VULN Modules card
                MDCard:
                    orientation: "vertical"
                    md_bg_color: get_color_from_hex("#0D0707")
                    radius: [6,6,6,6]
                    elevation: 6
                    padding: "10dp"
                    spacing: "4dp"

                    BoxLayout:
                        size_hint_y: None
                        height: "28dp"
                        MDLabel:
                            text: "⚡ VULN DETECTION"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FF4444")
                            font_name: "RobotoMono-Regular"
                            bold: True
                            font_size: "12sp"
                        MDRaisedButton:
                            text: "ALL"
                            size_hint: None, None
                            size: "40dp","24dp"
                            on_release: app.toggle_vuln(True)
                            md_bg_color: get_color_from_hex("#300000")
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FF4444")
                            font_size: "9sp"
                            font_name: "RobotoMono-Regular"
                        MDRaisedButton:
                            text: "NONE"
                            size_hint: None, None
                            size: "46dp","24dp"
                            on_release: app.toggle_vuln(False)
                            md_bg_color: get_color_from_hex("#200000")
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FF6666")
                            font_size: "9sp"
                            font_name: "RobotoMono-Regular"

                    ScrollView:
                        size_hint_y: None
                        height: "220dp"
                        BoxLayout:
                            id: vuln_modules
                            orientation: "vertical"
                            spacing: "2dp"
                            size_hint_y: None
                            height: self.minimum_height

                # Export / Save buttons
                MDCard:
                    orientation: "vertical"
                    md_bg_color: get_color_from_hex("#070D07")
                    radius: [6,6,6,6]
                    elevation: 4
                    padding: "10dp"
                    spacing: "6dp"
                    size_hint_y: None
                    height: "110dp"

                    MDLabel:
                        text: "◈ EXPORT"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#00FF41")
                        font_name: "RobotoMono-Regular"
                        bold: True
                        font_size: "11sp"
                        size_hint_y: None
                        height: "20dp"

                    MDRaisedButton:
                        text: "💾  SAVE REPORT (.txt)"
                        on_release: app.save_report()
                        md_bg_color: get_color_from_hex("#002A00")
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#00FF41")
                        font_name: "RobotoMono-Regular"
                        font_size: "10sp"
                        size_hint_x: 1

                    MDRaisedButton:
                        text: "📋  COPY FINDINGS"
                        on_release: app.copy_findings()
                        md_bg_color: get_color_from_hex("#002030")
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#00CCFF")
                        font_name: "RobotoMono-Regular"
                        font_size: "10sp"
                        size_hint_x: 1

            # ── RIGHT: CONSOLE + FINDINGS ───────────────────────
            BoxLayout:
                orientation: "vertical"
                spacing: "6dp"

                # Tabs: Console / Findings / Info
                BoxLayout:
                    size_hint_y: None
                    height: "36dp"
                    spacing: "4dp"

                    MDRaisedButton:
                        id: tab_console_btn
                        text: "[ CONSOLE ]"
                        on_release: app.switch_panel("console")
                        md_bg_color: get_color_from_hex("#003B00")
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#00FF41")
                        font_name: "RobotoMono-Regular"
                        font_size: "11sp"
                        size_hint_x: None
                        width: "140dp"

                    MDRaisedButton:
                        id: tab_findings_btn
                        text: "[ FINDINGS ]"
                        on_release: app.switch_panel("findings")
                        md_bg_color: get_color_from_hex("#200000")
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#FF4444")
                        font_name: "RobotoMono-Regular"
                        font_size: "11sp"
                        size_hint_x: None
                        width: "140dp"

                    MDRaisedButton:
                        id: tab_info_btn
                        text: "[ TARGET INFO ]"
                        on_release: app.switch_panel("info")
                        md_bg_color: get_color_from_hex("#002030")
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#00CCFF")
                        font_name: "RobotoMono-Regular"
                        font_size: "11sp"
                        size_hint_x: None
                        width: "140dp"

                    MDLabel:
                        id: panel_stats
                        text: ""
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#005A15")
                        font_name: "RobotoMono-Regular"
                        font_size: "10sp"
                        halign: "right"

                # Console panel
                MDCard:
                    id: panel_console
                    md_bg_color: get_color_from_hex("#020702")
                    radius: [6,6,6,6]
                    elevation: 8
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex("#00FF41")
                        Line:
                            rectangle: [self.x, self.y, self.width, self.height]
                            width: 0.8

                    ScrollView:
                        id: scroll_console
                        do_scroll_x: False
                        MDLabel:
                            id: lbl_console
                            text: ""
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#00FF41")
                            font_name: "RobotoMono-Regular"
                            font_size: "12sp"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            padding: ["14dp","10dp"]
                            markup: True

                # Findings panel (hidden by default)
                MDCard:
                    id: panel_findings
                    md_bg_color: get_color_from_hex("#0A0202")
                    radius: [6,6,6,6]
                    elevation: 8
                    opacity: 0
                    disabled: True
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex("#FF4444")
                        Line:
                            rectangle: [self.x, self.y, self.width, self.height]
                            width: 0.8

                    ScrollView:
                        id: scroll_findings
                        do_scroll_x: False
                        MDLabel:
                            id: lbl_findings
                            text: "[color=#FF4444][ No findings yet — run a scan ][/color]"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FF4444")
                            font_name: "RobotoMono-Regular"
                            font_size: "12sp"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            padding: ["14dp","10dp"]
                            markup: True

                # Info panel (hidden by default)
                MDCard:
                    id: panel_info
                    md_bg_color: get_color_from_hex("#020A0D")
                    radius: [6,6,6,6]
                    elevation: 8
                    opacity: 0
                    disabled: True
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex("#00CCFF")
                        Line:
                            rectangle: [self.x, self.y, self.width, self.height]
                            width: 0.8

                    ScrollView:
                        id: scroll_info
                        do_scroll_x: False
                        MDLabel:
                            id: lbl_info
                            text: "[color=#00CCFF][ Run a scan to populate target information ][/color]"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#00CCFF")
                            font_name: "RobotoMono-Regular"
                            font_size: "12sp"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            padding: ["14dp","10dp"]
                            markup: True
"""


# ─────────────────────────────────────────────────────────────
#  SCREEN
# ─────────────────────────────────────────────────────────────
class MainScreen(MDScreen):
    pass


# ─────────────────────────────────────────────────────────────
#  MODULE CHECKBOX ROW
# ─────────────────────────────────────────────────────────────
class ModuleRow(BoxLayout):
    def __init__(self, label, key, color="#00FF41", active=True, **kw):
        super().__init__(**kw)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "28dp"
        self.spacing = "6dp"
        self._key = key

        self.chk = MDCheckbox(
            active=active,
            size_hint=(None, None),
            size=("24dp", "24dp"),
            pos_hint={"center_y": 0.5},
            color_active=get_color_from_hex(color),
        )
        self.add_widget(self.chk)
        lbl = MDLabel(
            text=label,
            theme_text_color="Custom",
            text_color=get_color_from_hex(color),
            font_name="RobotoMono-Regular",
            font_size="10sp",
            shorten=True,
            shorten_from="right",
        )
        self.add_widget(lbl)

    @property
    def active(self): return self.chk.active
    @property
    def key(self): return self._key
    def set_active(self, v): self.chk.active = v


# ─────────────────────────────────────────────────────────────
#  OSINT ENGINE
# ─────────────────────────────────────────────────────────────
class OSINTEngine:
    @staticmethod
    def resolve_host(t):
        try:
            info = socket.getaddrinfo(t, None)
            ips = list({i[4][0] for i in info})
            return [("DNS", f"Resolved → {ip}") for ip in ips]
        except Exception as e:
            return [("DNS", f"Failed: {e}")]

    @staticmethod
    def reverse_dns(ip):
        try:
            h = socket.gethostbyaddr(ip)[0]
            return [("RDNS", f"PTR → {h}")]
        except Exception as e:
            return [("RDNS", f"No PTR record: {e}")]

    @staticmethod
    def whois_lookup(domain):
        servers = {"com":"whois.verisign-grs.com","net":"whois.verisign-grs.com",
                   "org":"whois.pir.org","io":"whois.nic.io","mg":"whois.nic.mg",
                   "fr":"whois.nic.fr","uk":"whois.nic.uk","de":"whois.denic.de"}
        results = []
        try:
            tld = domain.split(".")[-1].lower()
            srv = servers.get(tld, "whois.iana.org")
            s = socket.socket(); s.settimeout(10); s.connect((srv, 43))
            s.send((domain + "\r\n").encode())
            raw = b""
            while True:
                c = s.recv(4096)
                if not c: break
                raw += c
            s.close()
            for line in raw.decode("utf-8", errors="ignore").splitlines()[:35]:
                line = line.strip()
                if line and not line.startswith("%") and not line.startswith("#"):
                    results.append(("WHOIS", line))
        except Exception as e:
            results.append(("WHOIS", f"Error: {e}"))
        return results

    @staticmethod
    def ssl_info(domain):
        results = []
        try:
            ctx = ssl.create_default_context()
            conn = ctx.wrap_socket(socket.create_connection((domain, 443), timeout=10),
                                   server_hostname=domain)
            cert = conn.getpeercert()
            conn.close()
            subj = dict(x[0] for x in cert.get("subject", []))
            issr = dict(x[0] for x in cert.get("issuer",  []))
            results += [
                ("SSL", f"CN       : {subj.get('commonName','?')}"),
                ("SSL", f"Issuer   : {issr.get('organizationName','?')}"),
                ("SSL", f"Not Before: {cert.get('notBefore','?')}"),
                ("SSL", f"Not After : {cert.get('notAfter','?')}"),
            ]
            for kind, val in cert.get("subjectAltName", [])[:10]:
                results.append(("SSL", f"SAN      : {kind}={val}"))
        except Exception as e:
            results.append(("SSL", f"Error: {e}"))
        return results

    @staticmethod
    def http_headers(domain):
        results = []
        for scheme in ("https","http"):
            try:
                req = urllib.request.Request(f"{scheme}://{domain}",
                      headers={"User-Agent":"LezookScanner/3.0"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    results.append(("HTTP", f"Status : {r.status} {r.reason}"))
                    results.append(("HTTP", f"URL    : {r.url}"))
                    for k, v in r.headers.items():
                        results.append(("HTTP", f"{k:<32}: {v}"))
                break
            except Exception as e:
                results.append(("HTTP", f"[{scheme}] {e}"))
        return results

    @staticmethod
    def dns_records(domain):
        results = []
        for rtype in ["A","AAAA","MX","NS","TXT","CNAME","SOA"]:
            try:
                cmd = ["dig","+short",rtype,domain] if platform.system()!="Windows" \
                      else ["nslookup",f"-type={rtype}",domain]
                out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=6)
                for line in out.decode(errors="ignore").strip().splitlines():
                    if line.strip():
                        results.append(("DNS-REC", f"{rtype:<7}→ {line.strip()}"))
            except Exception:
                results.append(("DNS-REC", f"{rtype:<7}→ (dig unavailable)"))
        return results

    @staticmethod
    def subdomain_discover(domain):
        subs = ["www","mail","ftp","webmail","smtp","api","dev","staging","beta",
                "admin","test","vpn","cdn","static","assets","blog","shop","store",
                "support","help","docs","git","jenkins","jira","wiki","status",
                "portal","login","app","mobile","ns1","ns2","mx","mx1","autodiscover"]
        results = []
        found = []
        for s in subs:
            host = f"{s}.{domain}"
            try:
                socket.setdefaulttimeout(1.2)
                socket.gethostbyname(host)
                found.append(host)
                results.append(("SUBDOMAIN", f"[FOUND] {host}"))
            except socket.error:
                results.append(("SUBDOMAIN", f"[  -  ] {host}"))
        results.insert(0, ("SUBDOMAIN", f"Discovered: {len(found)} subdomains"))
        return results

    @staticmethod
    def geo_ip(ip):
        try:
            req = urllib.request.Request(
                f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,query",
                headers={"User-Agent":"LezookScanner/3.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                d = json.loads(r.read())
            if d.get("status") == "success":
                return [("GEO", f"{k:<12}: {d[k]}") for k in
                        ["query","country","regionName","city","isp","org","as"] if k in d]
        except Exception as e:
            return [("GEO", f"Error: {e}")]
        return [("GEO","GeoIP lookup failed")]

    @staticmethod
    def robots_sitemap(domain):
        results = []
        for path in ["/robots.txt","/sitemap.xml","/sitemap_index.xml"]:
            for scheme in ("https","http"):
                url = f"{scheme}://{domain}{path}"
                try:
                    req = urllib.request.Request(url, headers={"User-Agent":"LezookScanner/3.0"})
                    with urllib.request.urlopen(req, timeout=8) as r:
                        if r.status == 200:
                            content = r.read().decode(errors="ignore")
                            results.append(("CRAWL", f"[FOUND] {url}"))
                            for line in content.splitlines()[:20]:
                                if line.strip():
                                    results.append(("CRAWL", f"  {line.strip()}"))
                            break
                except Exception:
                    pass
            else:
                results.append(("CRAWL", f"[MISS ] {path}"))
        return results


# ─────────────────────────────────────────────────────────────
#  VULNERABILITY ENGINE (passive, legal, nmap-style checks)
# ─────────────────────────────────────────────────────────────
class VulnEngine:
    """
    Passive/banner-grab vulnerability checks.
    All checks are non-destructive and legal for authorized targets.
    """

    COMMON_PORTS = {
        21:"FTP", 22:"SSH", 23:"TELNET", 25:"SMTP", 53:"DNS",
        80:"HTTP", 110:"POP3", 143:"IMAP", 443:"HTTPS", 445:"SMB",
        3306:"MySQL", 3389:"RDP", 5432:"PostgreSQL", 6379:"Redis",
        8080:"HTTP-Alt", 8443:"HTTPS-Alt", 8888:"HTTP-Dev",
        27017:"MongoDB", 9200:"Elasticsearch", 5601:"Kibana",
        2375:"Docker", 2376:"Docker-TLS", 11211:"Memcached"
    }

    DANGEROUS_PORTS = {
        23:"TELNET (cleartext auth)", 21:"FTP (cleartext auth)",
        445:"SMB (EternalBlue risk)", 3389:"RDP (BlueKeep risk)",
        6379:"Redis (often unauthenticated)", 27017:"MongoDB (often unauthenticated)",
        9200:"Elasticsearch (often unauthenticated)", 2375:"Docker API (unauthenticated!)",
        11211:"Memcached (amplification DDoS risk)", 5601:"Kibana (data exposure)",
    }

    @staticmethod
    def port_scan(host):
        results = []
        open_ports = []
        findings = []
        for port, svc in VulnEngine.COMMON_PORTS.items():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                r = s.connect_ex((host, port))
                s.close()
                if r == 0:
                    open_ports.append(port)
                    tag = "⚠ DANGER" if port in VulnEngine.DANGEROUS_PORTS else "OPEN"
                    results.append(("PORT-SCAN", f"[{tag}] {port:5d}/tcp  {svc}"))
                    if port in VulnEngine.DANGEROUS_PORTS:
                        findings.append(("PORT-SCAN",
                            f"FINDING: Port {port} ({VulnEngine.DANGEROUS_PORTS[port]}) is open!",
                            "HIGH"))
            except Exception:
                pass
        results.insert(0, ("PORT-SCAN", f"Open ports: {len(open_ports)} / {len(VulnEngine.COMMON_PORTS)} scanned"))
        return results, findings

    @staticmethod
    def banner_grab(host, open_ports):
        """Grab service banners to detect outdated software."""
        results = []
        findings = []
        GRAB_PORTS = [21, 22, 25, 80, 110, 143, 3306, 8080]
        for port in GRAB_PORTS:
            if port not in open_ports:
                continue
            try:
                s = socket.socket()
                s.settimeout(3)
                s.connect((host, port))
                # Send HTTP request for web ports
                if port in (80, 8080):
                    s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()
                s.close()
                if banner:
                    results.append(("BANNER", f"Port {port}: {banner[:120]}"))
                    # Version detection hints
                    lower = banner.lower()
                    for keyword, finding, severity in [
                        ("openssh_7", "Outdated OpenSSH version detected", "MEDIUM"),
                        ("apache/2.2", "Outdated Apache 2.2 detected (EOL)", "HIGH"),
                        ("apache/2.4.4", "Apache 2.4.4x may be vulnerable to CVEs", "MEDIUM"),
                        ("iis/6.0", "IIS 6.0 detected (EOL, critical CVEs)", "CRITICAL"),
                        ("iis/7.5", "IIS 7.5 detected (outdated)", "MEDIUM"),
                        ("php/5.", "PHP 5.x detected (EOL since 2018)", "HIGH"),
                        ("php/7.0", "PHP 7.0 EOL detected", "MEDIUM"),
                        ("mysql 5.5", "MySQL 5.5 EOL detected", "MEDIUM"),
                        ("proftpd 1.3.5", "ProFTPD 1.3.5 - CVE-2015-3306", "CRITICAL"),
                        ("vsftpd 2.3.4", "vsftpd 2.3.4 - Backdoor vulnerability!", "CRITICAL"),
                        ("x-powered-by: php/5", "PHP 5.x EOL via header", "HIGH"),
                    ]:
                        if keyword in lower:
                            findings.append(("BANNER", f"FINDING: {finding}", severity))
            except Exception:
                pass
        return results, findings

    @staticmethod
    def check_security_headers(domain):
        """Check for missing security headers — easy Bug Bounty findings."""
        results = []
        findings = []
        REQUIRED = {
            "Strict-Transport-Security": ("HSTS missing — downgrade attack possible", "MEDIUM"),
            "Content-Security-Policy":   ("CSP missing — XSS risk increased", "MEDIUM"),
            "X-Frame-Options":           ("Clickjacking possible (no X-Frame-Options)", "LOW"),
            "X-Content-Type-Options":    ("MIME sniffing possible (no X-Content-Type-Options)", "LOW"),
            "X-XSS-Protection":          ("No X-XSS-Protection header", "INFO"),
            "Referrer-Policy":           ("Referrer-Policy missing — info leakage risk", "LOW"),
            "Permissions-Policy":        ("Permissions-Policy missing", "INFO"),
        }
        try:
            req = urllib.request.Request(f"https://{domain}",
                  headers={"User-Agent":"LezookScanner/3.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                present = {k.lower() for k in r.headers.keys()}
                for header, (msg, severity) in REQUIRED.items():
                    if header.lower() in present:
                        results.append(("SEC-HDR", f"[✓ OK    ] {header}"))
                    else:
                        results.append(("SEC-HDR", f"[✗ MISS  ] {header}"))
                        findings.append(("SEC-HDR", f"FINDING: {msg}", severity))
                # Check for info-leaking headers
                for bad_hdr in ["server","x-powered-by","x-aspnet-version","x-aspnetmvc-version"]:
                    val = r.headers.get(bad_hdr)
                    if val:
                        results.append(("SEC-HDR", f"[! LEAK  ] {bad_hdr}: {val}"))
                        findings.append(("SEC-HDR",
                            f"FINDING: Server info leaked via '{bad_hdr}: {val}'", "LOW"))
        except Exception as e:
            results.append(("SEC-HDR", f"Error: {e}"))
        return results, findings

    @staticmethod
    def check_ssl_vulns(domain):
        """Check SSL/TLS configuration for weaknesses."""
        results = []
        findings = []
        try:
            # Check certificate expiry
            ctx = ssl.create_default_context()
            conn = ctx.wrap_socket(socket.create_connection((domain, 443), timeout=10),
                                   server_hostname=domain)
            cert = conn.getpeercert()
            proto = conn.version()
            conn.close()

            results.append(("SSL-VULN", f"Protocol : {proto}"))

            # Check expiry
            not_after = cert.get("notAfter","")
            if not_after:
                try:
                    exp = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    days = (exp - datetime.datetime.utcnow()).days
                    results.append(("SSL-VULN", f"Expires  : {not_after} ({days} days)"))
                    if days < 30:
                        sev = "CRITICAL" if days < 7 else "HIGH"
                        findings.append(("SSL-VULN",
                            f"FINDING: Certificate expires in {days} days!", sev))
                except Exception:
                    pass

            # Weak protocol check
            if proto in ("TLSv1","TLSv1.0","TLSv1.1","SSLv3","SSLv2"):
                findings.append(("SSL-VULN",
                    f"FINDING: Weak protocol in use: {proto}", "HIGH"))

            # Try weak SSLv2/SSLv3 explicitly
            for bad_proto, flag in [("SSLv2", ssl.PROTOCOL_TLS_CLIENT),
                                     ("TLSv1.1", ssl.PROTOCOL_TLS_CLIENT)]:
                try:
                    ctx2 = ssl.SSLContext(flag)
                    ctx2.minimum_version = ssl.TLSVersion.TLSv1
                    ctx2.maximum_version = ssl.TLSVersion.TLSv1
                    ctx2.check_hostname = False
                    ctx2.verify_mode = ssl.CERT_NONE
                    conn2 = ctx2.wrap_socket(
                        socket.create_connection((domain, 443), timeout=5),
                        server_hostname=domain)
                    conn2.close()
                    findings.append(("SSL-VULN",
                        f"FINDING: TLS 1.0 accepted — POODLE/BEAST risk!", "MEDIUM"))
                    results.append(("SSL-VULN", f"TLSv1.0 : ACCEPTED (insecure)"))
                    break
                except Exception:
                    results.append(("SSL-VULN", f"TLSv1.0 : rejected (good)"))
                    break

        except ssl.SSLCertVerificationError:
            results.append(("SSL-VULN", "Certificate verification FAILED"))
            findings.append(("SSL-VULN",
                "FINDING: Invalid/self-signed certificate — MITM risk!", "HIGH"))
        except Exception as e:
            results.append(("SSL-VULN", f"Error: {e}"))
        return results, findings

    @staticmethod
    def check_common_paths(domain):
        """Probe for exposed sensitive files/panels (passive, no exploit)."""
        results = []
        findings = []
        PATHS = [
            ("/admin", "Admin panel"),
            ("/administrator", "Admin panel"),
            ("/wp-admin", "WordPress admin"),
            ("/wp-login.php", "WordPress login"),
            ("/phpmyadmin", "phpMyAdmin"),
            ("/phpmyadmin/", "phpMyAdmin"),
            ("/.git/HEAD", "Git repository exposed"),
            ("/.env", ".env file (credentials!)"),
            ("/config.php", "Config file"),
            ("/web.config", "IIS config"),
            ("/server-status", "Apache status page"),
            ("/server-info", "Apache info page"),
            ("/actuator", "Spring Boot actuator"),
            ("/actuator/health", "Spring Boot health"),
            ("/api/v1", "API endpoint"),
            ("/swagger-ui.html", "Swagger UI (API docs)"),
            ("/swagger-ui/", "Swagger UI"),
            ("/api-docs", "API docs"),
            ("/.DS_Store", "macOS metadata"),
            ("/backup.zip", "Backup file"),
            ("/backup.tar.gz", "Backup file"),
            ("/db.sql", "SQL dump"),
            ("/dump.sql", "SQL dump"),
            ("/crossdomain.xml", "Flash crossdomain"),
            ("/elmah.axd", ".NET error log"),
            ("/trace.axd", ".NET trace"),
        ]
        for path, desc in PATHS:
            for scheme in ("https","http"):
                url = f"{scheme}://{domain}{path}"
                try:
                    req = urllib.request.Request(url,
                          headers={"User-Agent":"LezookScanner/3.0"})
                    with urllib.request.urlopen(req, timeout=6) as r:
                        status = r.status
                        results.append(("PATH-PROBE", f"[{status}] {path}  ← {desc}"))
                        if status in (200, 301, 302, 403):
                            sev = "HIGH" if any(x in path for x in [".env","git","sql","backup","phpmyadmin"]) else "MEDIUM"
                            findings.append(("PATH-PROBE",
                                f"FINDING: '{path}' accessible ({status}) — {desc}", sev))
                    break
                except urllib.error.HTTPError as e:
                    results.append(("PATH-PROBE", f"[{e.code}] {path}"))
                    break
                except Exception:
                    pass
            else:
                results.append(("PATH-PROBE", f"[---] {path}"))
        return results, findings

    @staticmethod
    def check_cors(domain):
        """Check CORS misconfiguration."""
        results = []
        findings = []
        try:
            req = urllib.request.Request(f"https://{domain}",
                  headers={"User-Agent":"LezookScanner/3.0",
                           "Origin":"https://evil.com"})
            with urllib.request.urlopen(req, timeout=10) as r:
                acao = r.headers.get("Access-Control-Allow-Origin","")
                acac = r.headers.get("Access-Control-Allow-Credentials","")
                if acao:
                    results.append(("CORS", f"ACAO: {acao}"))
                    results.append(("CORS", f"ACAC: {acac}"))
                    if acao == "*":
                        findings.append(("CORS",
                            "FINDING: Wildcard CORS origin (*) — any site can read responses!", "MEDIUM"))
                    elif "evil.com" in acao:
                        findings.append(("CORS",
                            "FINDING: CORS reflects arbitrary origins — potential data theft!", "HIGH"))
                    if acac.lower() == "true" and acao != "":
                        findings.append(("CORS",
                            "FINDING: CORS allows credentials with open origin — critical!", "CRITICAL"))
                else:
                    results.append(("CORS", "No CORS headers (OK for non-API sites)"))
        except Exception as e:
            results.append(("CORS", f"Error: {e}"))
        return results, findings

    @staticmethod
    def check_redirect(domain):
        """Check open redirect hints."""
        results = []
        findings = []
        redirect_paths = [
            f"/?url=https://evil.com",
            f"/?redirect=https://evil.com",
            f"/?next=https://evil.com",
            f"/?return=https://evil.com",
            f"/?goto=https://evil.com",
        ]
        for path in redirect_paths:
            try:
                url = f"https://{domain}{path}"
                req = urllib.request.Request(url, headers={"User-Agent":"LezookScanner/3.0"})
                # Don't follow redirect
                opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
                with opener.open(req, timeout=8) as r:
                    loc = r.headers.get("Location","")
                    if "evil.com" in loc:
                        results.append(("REDIRECT", f"[VULN!] {path} → {loc}"))
                        findings.append(("REDIRECT",
                            f"FINDING: Open redirect! {path} redirects to evil.com", "MEDIUM"))
                    else:
                        results.append(("REDIRECT", f"[OK  ] {path}"))
            except Exception:
                results.append(("REDIRECT", f"[---] {path}"))
        return results, findings


# ─────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────
class LezookScannerApp(MDApp):

    BOOT = (
        "[color=#00FF41]"
        "╔══════════════════════════════════════════════════════════╗\n"
        "║         LEZOOK SCANNER  ─  v3.0                         ║\n"
        "║    OSINT + Vulnerability Detection Framework             ║\n"
        "╠══════════════════════════════════════════════════════════╣\n"
        "║  Contact : +261 32 542 10                                ║\n"
        "║  Email   : jason.fiderosse.larry@gmail.com               ║\n"
        "║                                                          ║\n"
        "║  ⚠  FOR LEGAL USE — AUTHORIZED TARGETS ONLY             ║\n"
        "║  ⚠  Bug Bounty / Ethical Security Research              ║\n"
        "╚══════════════════════════════════════════════════════════╝\n"
        "[/color]"
        "[color=#007A20]\n"
        "[*] Loading OSINT engine     ✓\n"
        "[*] Loading Vuln engine      ✓\n"
        "[*] Loading Port scanner     ✓\n"
        "[*] Loading Banner grabber   ✓\n"
        "[*] Loading SSL analyser     ✓\n"
        "[*] Loading Path prober      ✓\n"
        "[*] Loading CORS checker     ✓\n"
        "[*] Loading Header analyzer  ✓\n"
        "[/color]\n"
        "[color=#00FF41]>>> All systems ONLINE. Enter target and press SCAN.[/color]\n"
    )

    OSINT_MODULES = [
        ("DNS Resolution",       "dns",       "#00CCFF"),
        ("Reverse DNS",          "rdns",      "#00CCFF"),
        ("WHOIS Lookup",         "whois",     "#00CCFF"),
        ("SSL Certificate",      "ssl",       "#00CCFF"),
        ("HTTP Headers",         "http",      "#00CCFF"),
        ("DNS Records (dig)",    "dns_rec",   "#00CCFF"),
        ("Subdomain Discovery",  "subdomain", "#00CCFF"),
        ("GeoIP Location",       "geo",       "#00CCFF"),
        ("Robots / Sitemap",     "crawl",     "#00CCFF"),
    ]

    VULN_MODULES = [
        ("Port Scan (22 ports)", "ports",    "#FF4444"),
        ("Banner Grab / Version","banner",   "#FF4444"),
        ("Security Headers",     "sec_hdr",  "#FF4444"),
        ("SSL/TLS Weakness",     "ssl_vuln", "#FF4444"),
        ("Sensitive Paths",      "paths",    "#FF4444"),
        ("CORS Misconfiguration","cors",     "#FF4444"),
        ("Open Redirect",        "redirect", "#FF4444"),
    ]

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        Builder.load_string(KV)
        self.screen = MainScreen()
        Window.clearcolor = get_color_from_hex("#020702")
        self._findings = []
        self._info_data = {}
        self._open_ports = []
        self._scan_running = False
        self._current_panel = "console"
        return self.screen

    def on_start(self):
        self._osint_rows = []
        for label, key, color in self.OSINT_MODULES:
            row = ModuleRow(label, key, color=color)
            self.screen.ids.osint_modules.add_widget(row)
            self._osint_rows.append(row)

        self._vuln_rows = []
        for label, key, color in self.VULN_MODULES:
            row = ModuleRow(label, key, color=color)
            self.screen.ids.vuln_modules.add_widget(row)
            self._vuln_rows.append(row)

        self._write_console(self.BOOT)
        Clock.schedule_interval(self._tick_clock, 1)
        Clock.schedule_interval(self._tick_ticker, 1.2)
        self._ticker_idx = 0
        self._TICKERS = [
            "■ OSINT ENGINE READY  ■  VULN SCANNER READY  ■",
            "■ LEGAL USE ONLY  ■  BUG BOUNTY MODE  ■",
            "■ LEZOOK SCANNER v3.0  ■  +261 32 542 10  ■",
        ]

    # ── UI helpers ───────────────────────────────────────────
    def _tick_clock(self, dt):
        self.screen.ids.clock_lbl.text = datetime.datetime.now().strftime("[ %Y-%m-%d  %H:%M:%S ]")

    def _tick_ticker(self, dt):
        self.screen.ids.ticker.text = self._TICKERS[self._ticker_idx % len(self._TICKERS)]
        self._ticker_idx += 1

    def switch_panel(self, name):
        self._current_panel = name
        ids = self.screen.ids
        for pname in ("console","findings","info"):
            panel = ids.get(f"panel_{pname}")
            if panel:
                panel.opacity = 1 if pname == name else 0
                panel.disabled = pname != name

    def toggle_osint(self, val):
        for row in self._osint_rows: row.set_active(val)

    def toggle_vuln(self, val):
        for row in self._vuln_rows: row.set_active(val)

    def _write_console(self, text, color="#00FF41"):
        lbl = self.screen.ids.lbl_console
        lbl.text += f"[color={color}]{text}[/color]\n"
        lbl.texture_update()
        Clock.schedule_once(lambda dt: setattr(self.screen.ids.scroll_console, "scroll_y", 0), 0.05)

    def _write_findings(self, text, severity="INFO"):
        colors = {"CRITICAL":"#FF0000","HIGH":"#FF4444","MEDIUM":"#FF8800",
                  "LOW":"#FFFF00","INFO":"#00CCFF"}
        color = colors.get(severity, "#AAAAAA")
        lbl = self.screen.ids.lbl_findings
        lbl.text += f"[color={color}]{text}[/color]\n"
        lbl.texture_update()
        self._findings.append((severity, text))
        badge = len(self._findings)
        self.screen.ids.finding_badge.text = f"[ {badge} FINDINGS ]"
        Clock.schedule_once(lambda dt: setattr(self.screen.ids.scroll_findings, "scroll_y", 0), 0.05)

    def _write_info(self, text, color="#00CCFF"):
        lbl = self.screen.ids.lbl_info
        lbl.text += f"[color={color}]{text}[/color]\n"
        lbl.texture_update()

    def clear_all(self):
        self.screen.ids.lbl_console.text = self.BOOT
        self.screen.ids.lbl_findings.text = "[color=#FF4444][ No findings yet — run a scan ][/color]"
        self.screen.ids.lbl_info.text = "[color=#00CCFF][ Run a scan to populate target information ][/color]"
        self._findings.clear()
        self._open_ports.clear()
        self.screen.ids.progress_bar.value = 0
        self.screen.ids.progress_label.text = "[ IDLE ]"
        self.screen.ids.finding_badge.text = ""
        self.screen.ids.panel_stats.text = ""

    # ── Scan launcher ────────────────────────────────────────
    def launch_scan(self, mode="all"):
        if self._scan_running:
            Snackbar(text="⚠  Scan already running!", snackbar_x="8dp").open()
            return
        raw = self.screen.ids.target_input.text.strip()
        if not raw:
            Snackbar(text="⚠  Please enter a target!", snackbar_x="8dp").open()
            return

        target = self._parse_target(raw)

        osint_sel = [r.key for r in self._osint_rows if r.active] if mode in ("all","osint") else []
        vuln_sel  = [r.key for r in self._vuln_rows  if r.active] if mode in ("all","vuln")  else []

        if not osint_sel and not vuln_sel:
            Snackbar(text="⚠  Select at least one module!", snackbar_x="8dp").open()
            return

        self._scan_running = True
        self._findings.clear()
        self.screen.ids.lbl_findings.text = ""
        self.screen.ids.lbl_info.text = ""
        self.screen.ids.finding_badge.text = ""
        self._open_ports.clear()

        self._write_console(
            f"\n{'═'*58}\n"
            f"  TARGET  : {target}\n"
            f"  MODE    : {mode.upper()}\n"
            f"  STARTED : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"{'═'*58}", "#00FF41"
        )

        threading.Thread(
            target=self._run_scan,
            args=(target, osint_sel, vuln_sel),
            daemon=True
        ).start()

    def _parse_target(self, raw):
        for p in ("https://","http://","ftp://"):
            if raw.startswith(p): raw = raw[len(p):]
        return raw.split("/")[0].strip()

    def _is_ip(self, s):
        try: socket.inet_aton(s); return True
        except: return False

    def _set_progress(self, val, label):
        Clock.schedule_once(lambda dt: (
            setattr(self.screen.ids.progress_bar, "value", val),
            setattr(self.screen.ids.progress_label, "text", label)
        ), 0)

    # ── Core scan thread ─────────────────────────────────────
    def _run_scan(self, target, osint_sel, vuln_sel):
        engine = OSINTEngine()
        veng   = VulnEngine()
        is_ip  = self._is_ip(target)

        # Resolve IP
        resolved_ip = target if is_ip else None
        if not is_ip:
            try: resolved_ip = socket.gethostbyname(target)
            except: pass

        total_steps = len(osint_sel) + len(vuln_sel)
        step = 0
        all_findings = []

        # Write info header
        Clock.schedule_once(lambda dt: self._write_info(
            f"{'═'*55}\n"
            f"  TARGET INFO  —  {target}\n"
            f"  Resolved IP : {resolved_ip or 'unknown'}\n"
            f"{'═'*55}", "#00CCFF"), 0)

        def do_step(tag, name, fn):
            nonlocal step
            step += 1
            pct = int(step / total_steps * 100)
            self._set_progress(pct, f"[ {tag} ] {name[:30]}...")
            Clock.schedule_once(lambda dt, n=name: self._write_console(
                f"\n[►] {n}...", "#007A20"), 0)
            try:
                return fn()
            except Exception as e:
                Clock.schedule_once(lambda dt, err=str(e): self._write_console(
                    f"  [ERR] {err}", "#FF4444"), 0)
                return [], []

        def emit(results, tag_color_map):
            """Emit results to console."""
            colors = {"DNS":"#00FF88","RDNS":"#00FF66","WHOIS":"#00CC55",
                      "SSL":"#00EEDD","HTTP":"#00BBFF","DNS-REC":"#00FF99",
                      "SUBDOMAIN":"#FFAA00","GEO":"#FF88FF","CRAWL":"#44FF88",
                      "PORT-SCAN":"#FFFF00","BANNER":"#FFCC00","SEC-HDR":"#FF6644",
                      "SSL-VULN":"#FF8844","PATH-PROBE":"#FF4488","CORS":"#FF44FF",
                      "REDIRECT":"#FFAA44"}
            for row in results:
                tag, line = row[0], row[1]
                col = colors.get(tag, "#00FF41")
                if "FOUND" in line or "OPEN" in line or "MISS" in line or "DANGER" in line:
                    col = "#FF4444" if "MISS" in line else "#FFFF00"
                Clock.schedule_once(lambda dt, t=tag, l=line, c=col:
                    self._write_console(f"  [{t}] {l}", c), 0)

        def emit_findings(findings):
            for f in findings:
                tag, msg, sev = f
                Clock.schedule_once(lambda dt, m=msg, s=sev:
                    self._write_findings(f"\n  [{s}] {m}", s), 0)
                all_findings.append(f)
                # Also echo to console
                col = {"CRITICAL":"#FF0000","HIGH":"#FF4444","MEDIUM":"#FF8800",
                       "LOW":"#FFFF00","INFO":"#00CCFF"}.get(sev,"#AAAAAA")
                Clock.schedule_once(lambda dt, m=msg, c=col:
                    self._write_console(f"  !! {m}", c), 0)

        # ── OSINT modules ────────────────────────────────────
        osint_map = {
            "dns":      ("DNS",       "DNS Resolution",      lambda: (engine.resolve_host(target), [])),
            "rdns":     ("RDNS",      "Reverse DNS",         lambda: (engine.reverse_dns(resolved_ip or target), [])),
            "whois":    ("WHOIS",     "WHOIS Lookup",        lambda: (engine.whois_lookup(target), [])),
            "ssl":      ("SSL",       "SSL Certificate",     lambda: (engine.ssl_info(target), [])),
            "http":     ("HTTP",      "HTTP Headers",        lambda: (engine.http_headers(target), [])),
            "dns_rec":  ("DNS-REC",   "DNS Records",         lambda: (engine.dns_records(target), [])),
            "subdomain":("SUBDOMAIN", "Subdomain Discovery", lambda: (engine.subdomain_discover(target), [])),
            "geo":      ("GEO",       "GeoIP Location",      lambda: (engine.geo_ip(resolved_ip or target), [])),
            "crawl":    ("CRAWL",     "Robots / Sitemap",    lambda: (engine.robots_sitemap(target), [])),
        }

        for key in osint_sel:
            if key not in osint_map: continue
            tag, name, fn = osint_map[key]
            results, finds = do_step(tag, name, fn)
            emit(results, {})
            emit_findings(finds)
            # Feed info panel
            Clock.schedule_once(lambda dt, r=results: [
                self._write_info(f"  [{row[0]}] {row[1]}", "#00AADD") for row in r], 0)

        # ── Vuln modules ─────────────────────────────────────
        if "ports" in vuln_sel:
            results, finds = do_step("PORT-SCAN","Port Scan",
                lambda: veng.port_scan(resolved_ip or target))
            emit(results, {})
            emit_findings(finds)
            self._open_ports = [int(r[1].split()[1].split("/")[0])
                                for r in results if "OPEN" in r[1] or "DANGER" in r[1]]

        if "banner" in vuln_sel:
            results, finds = do_step("BANNER","Banner Grab / Version Detection",
                lambda: veng.banner_grab(resolved_ip or target, self._open_ports))
            emit(results, {})
            emit_findings(finds)

        if "sec_hdr" in vuln_sel:
            results, finds = do_step("SEC-HDR","Security Headers Check",
                lambda: veng.check_security_headers(target))
            emit(results, {})
            emit_findings(finds)

        if "ssl_vuln" in vuln_sel:
            results, finds = do_step("SSL-VULN","SSL/TLS Vulnerability Check",
                lambda: veng.check_ssl_vulns(target))
            emit(results, {})
            emit_findings(finds)

        if "paths" in vuln_sel:
            results, finds = do_step("PATH-PROBE","Sensitive Path Discovery",
                lambda: veng.check_common_paths(target))
            emit(results, {})
            emit_findings(finds)

        if "cors" in vuln_sel:
            results, finds = do_step("CORS","CORS Misconfiguration",
                lambda: veng.check_cors(target))
            emit(results, {})
            emit_findings(finds)

        if "redirect" in vuln_sel:
            results, finds = do_step("REDIRECT","Open Redirect Check",
                lambda: veng.check_redirect(target))
            emit(results, {})
            emit_findings(finds)

        # ── Done ─────────────────────────────────────────────
        sev_counts = {}
        for f in all_findings:
            sev_counts[f[2]] = sev_counts.get(f[2], 0) + 1

        summary = "  ".join(f"{s}:{c}" for s, c in sev_counts.items()) or "No findings"

        Clock.schedule_once(lambda dt: (
            self._write_console(
                f"\n{'═'*58}\n"
                f"  SCAN COMPLETE  ─  {target}\n"
                f"  Findings : {summary}\n"
                f"  Ended    : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{'═'*58}\n", "#00FF41"),
            setattr(self.screen.ids.progress_bar, "value", 100),
            setattr(self.screen.ids.progress_label, "text", "[ COMPLETE ]"),
            setattr(self.screen.ids.panel_stats, "text",
                    f"{len(all_findings)} findings  |  {step} modules"),
        ), 0)

        self._scan_running = False
        self._report_target = target
        self._all_findings = all_findings

    # ── Export ───────────────────────────────────────────────
    def save_report(self):
        if not hasattr(self, "_report_target"):
            Snackbar(text="⚠  Run a scan first!", snackbar_x="8dp").open()
            return
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"lezook_report_{self._report_target}_{ts}.txt"
        content = self.screen.ids.lbl_console.text
        # Strip markup
        content = re.sub(r"\[/?color[^\]]*\]","", content)
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write("LEZOOK SCANNER v3.0 — SCAN REPORT\n")
                f.write(f"Contact: +261 32 542 10 | jason.fiderosse.larry@gmail.com\n")
                f.write(f"Generated: {datetime.datetime.now()}\n")
                f.write("="*60 + "\n\n")
                f.write(content)
                f.write("\n\n=== VULNERABILITY FINDINGS ===\n")
                for sev, msg in self._findings:
                    f.write(f"[{sev}] {msg}\n")
            Snackbar(text=f"✓ Report saved: {fname}", snackbar_x="8dp").open()
        except Exception as e:
            Snackbar(text=f"Error saving: {e}", snackbar_x="8dp").open()

    def copy_findings(self):
        if not self._findings:
            Snackbar(text="⚠  No findings to copy!", snackbar_x="8dp").open()
            return
        text = "\n".join(f"[{s}] {m}" for s, m in self._findings)
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
            Snackbar(text=f"✓ {len(self._findings)} findings copied to clipboard!", snackbar_x="8dp").open()
        except Exception as e:
            Snackbar(text=f"Error: {e}", snackbar_x="8dp").open()


if __name__ == "__main__":
    LezookScannerApp().run()
