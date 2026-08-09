"""Unit tests for Jinja2 template rendering across all roles."""
import json


# ---- cis_hardening: sshd_config.j2 ----

class TestSshdConfig:
    def test_default_port(self, render):
        result = render("cis_hardening", "sshd_config.j2")
        assert "Port 22" in result

    def test_custom_port(self, render):
        result = render("cis_hardening", "sshd_config.j2",
                        {"cis_hardening_ssh_port": 2222})
        assert "Port 2222" in result

    def test_root_login_disabled(self, render):
        result = render("cis_hardening", "sshd_config.j2")
        assert "PermitRootLogin no" in result

    def test_password_auth_disabled(self, render):
        result = render("cis_hardening", "sshd_config.j2")
        assert "PasswordAuthentication no" in result

    def test_ipv6_disabled(self, render):
        result = render("cis_hardening", "sshd_config.j2",
                        {"cis_hardening_disable_ipv6": True})
        assert "ListenAddress ::" not in result

    def test_ipv6_enabled(self, render):
        result = render("cis_hardening", "sshd_config.j2",
                        {"cis_hardening_disable_ipv6": False})
        assert "ListenAddress ::" in result

    def test_allow_users(self, render):
        result = render("cis_hardening", "sshd_config.j2",
                        {"cis_hardening_ssh_allow_users": "deploy admin"})
        assert "AllowUsers deploy admin" in result

    def test_kiosk_user_denied(self, render):
        result = render("cis_hardening", "sshd_config.j2",
                        {"kiosk_user": "kiosk"})
        assert "Match User kiosk" in result
        assert "ForceCommand /bin/false" in result

    def test_compression_disabled(self, render):
        result = render("cis_hardening", "sshd_config.j2")
        assert "Compression no" in result

    def test_strong_ciphers(self, render):
        result = render("cis_hardening", "sshd_config.j2")
        assert "aes256-gcm@openssh.com" in result
        assert "curve25519-sha256" in result


# ---- cis_hardening: sysctl-hardening.conf.j2 ----

class TestSysctlHardening:
    def test_aslr_enabled(self, render):
        result = render("cis_hardening", "sysctl-hardening.conf.j2")
        assert "kernel.randomize_va_space = 2" in result

    def test_ip_forwarding_disabled(self, render):
        result = render("cis_hardening", "sysctl-hardening.conf.j2")
        assert "net.ipv4.ip_forward = 0" in result

    def test_syn_cookies_enabled(self, render):
        result = render("cis_hardening", "sysctl-hardening.conf.j2")
        assert "net.ipv4.tcp_syncookies = 1" in result

    def test_core_dumps_disabled(self, render):
        result = render("cis_hardening", "sysctl-hardening.conf.j2")
        assert "fs.suid_dumpable = 0" in result

    def test_ptrace_restricted(self, render):
        result = render("cis_hardening", "sysctl-hardening.conf.j2")
        assert "kernel.yama.ptrace_scope = 1" in result


# ---- cis_hardening: pwquality.conf.j2 ----

class TestPwquality:
    def test_default_min_length(self, render):
        result = render("cis_hardening", "pwquality.conf.j2")
        assert "minlen = 14" in result

    def test_custom_min_length(self, render):
        result = render("cis_hardening", "pwquality.conf.j2",
                        {"cis_hardening_password_min_length": 20})
        assert "minlen = 20" in result

    def test_complexity_requirements(self, render):
        result = render("cis_hardening", "pwquality.conf.j2")
        assert "dcredit = -1" in result
        assert "ucredit = -1" in result
        assert "minclass = 4" in result


# ---- cis_hardening: audit.rules.j2 ----

class TestAuditRules:
    def test_buffer_size(self, render):
        result = render("cis_hardening", "audit.rules.j2")
        assert "-b 8192" in result

    def test_immutable_flag_last(self, render):
        result = render("cis_hardening", "audit.rules.j2")
        lines = result.strip().splitlines()
        assert lines[-1].strip() == "-e 2"

    def test_identity_watches(self, render):
        result = render("cis_hardening", "audit.rules.j2")
        assert "-w /etc/passwd -p wa -k identity" in result
        assert "-w /etc/shadow -p wa -k identity" in result

    def test_sudoers_watches(self, render):
        result = render("cis_hardening", "audit.rules.j2")
        assert "-w /etc/sudoers -p wa -k scope" in result

    def test_ptrace_auditing(self, render):
        result = render("cis_hardening", "audit.rules.j2")
        assert "ptrace" in result


# ---- cloudflare_warp: mdm.xml.j2 ----

class TestMdmXml:
    def test_custom_org(self, render):
        result = render("cloudflare_warp", "mdm.xml.j2",
                        {"cloudflare_warp_organization": "mycompany"})
        assert "<string>mycompany</string>" in result

    def test_auto_connect_enabled(self, render):
        result = render("cloudflare_warp", "mdm.xml.j2")
        assert "<integer>1</integer>" in result

    def test_switch_locked(self, render):
        result = render("cloudflare_warp", "mdm.xml.j2")
        assert "<true />" in result

    def test_onboarding_disabled(self, render):
        result = render("cloudflare_warp", "mdm.xml.j2")
        assert "<false />" in result


# ---- nginx: kiosk-site.conf.j2 ----

class TestNginxSiteConf:
    def test_default_listen_address(self, render):
        result = render("nginx", "kiosk-site.conf.j2")
        assert "listen 127.0.0.1:80 default_server" in result

    def test_custom_port(self, render):
        result = render("nginx", "kiosk-site.conf.j2",
                        {"nginx_listen_port": 8080})
        assert "listen 127.0.0.1:8080 default_server" in result

    def test_webroot(self, render):
        result = render("nginx", "kiosk-site.conf.j2")
        assert "root /var/www/kiosk" in result

    def test_no_cache_headers(self, render):
        result = render("nginx", "kiosk-site.conf.j2")
        assert "no-store, no-cache, must-revalidate" in result

    def test_ipv6_loopback(self, render):
        result = render("nginx", "kiosk-site.conf.j2")
        assert "listen [::1]:" in result


# ---- nginx: index.html.j2 ----

class TestDashboardHtml:
    def test_title(self, render):
        result = render("nginx", "index.html.j2")
        assert "<title>NOC Display</title>" in result

    def test_dark_color_scheme(self, render):
        result = render("nginx", "index.html.j2")
        assert 'content="dark"' in result

    def test_cursor_hidden(self, render):
        result = render("nginx", "index.html.j2")
        assert "cursor: none" in result

    def test_overflow_hidden(self, render):
        result = render("nginx", "index.html.j2")
        assert "overflow: hidden" in result


# ---- kiosk: chrome-policy.json.j2 ----

class TestChromePolicy:
    def test_valid_json(self, render):
        result = render("kiosk", "chrome-policy.json.j2")
        json.loads(result)

    def test_default_url(self, render):
        result = render("kiosk", "chrome-policy.json.j2")
        policy = json.loads(result)
        assert policy["RestoreOnStartupURLs"] == ["http://localhost/"]

    def test_custom_url(self, render):
        result = render("kiosk", "chrome-policy.json.j2",
                        {"kiosk_portal_url": "https://grafana.internal/"})
        policy = json.loads(result)
        assert policy["RestoreOnStartupURLs"] == ["https://grafana.internal/"]

    def test_url_blocklist_all(self, render):
        result = render("kiosk", "chrome-policy.json.j2")
        policy = json.loads(result)
        assert policy["URLBlocklist"] == ["*"]

    def test_security_policies(self, render):
        result = render("kiosk", "chrome-policy.json.j2")
        policy = json.loads(result)
        assert policy["DeveloperToolsAvailability"] == 2
        assert policy["IncognitoModeAvailability"] == 1
        assert policy["DownloadRestrictions"] == 3
        assert policy["ExtensionInstallBlocklist"] == ["*"]
        assert policy["PrintingEnabled"] is False
        assert policy["SyncDisabled"] is True


# ---- kiosk: kiosk.service.j2 ----

class TestKioskService:
    def test_default_user(self, render):
        result = render("kiosk", "kiosk.service.j2")
        assert "User=kiosk" in result

    def test_custom_user(self, render):
        result = render("kiosk", "kiosk.service.j2",
                        {"kiosk_user": "display"})
        assert "User=display" in result

    def test_restart_always(self, render):
        result = render("kiosk", "kiosk.service.j2")
        assert "Restart=always" in result

    def test_security_hardening(self, render):
        result = render("kiosk", "kiosk.service.j2")
        assert "NoNewPrivileges=yes" in result
        assert "ProtectKernelTunables=yes" in result
        assert "PrivateTmp=yes" in result
        assert "LockPersonality=yes" in result

    def test_home_directory(self, render):
        result = render("kiosk", "kiosk.service.j2",
                        {"kiosk_home": "/opt/kiosk"})
        assert "Environment=HOME=/opt/kiosk" in result
        assert "ReadWritePaths=/opt/kiosk" in result


# ---- kiosk: kiosk-session.sh.j2 ----

class TestKioskSession:
    def test_default_url(self, render):
        result = render("kiosk", "kiosk-session.sh.j2")
        assert 'URL="http://localhost/"' in result

    def test_custom_url(self, render):
        result = render("kiosk", "kiosk-session.sh.j2",
                        {"kiosk_portal_url": "https://dashboard.example.com"})
        assert 'URL="https://dashboard.example.com"' in result

    def test_dark_mode_flags(self, render):
        result = render("kiosk", "kiosk-session.sh.j2")
        assert "--force-dark-mode" in result
        assert "GTK_THEME=Adwaita:dark" in result

    def test_kiosk_chrome_flags(self, render):
        result = render("kiosk", "kiosk-session.sh.j2")
        assert "--kiosk" in result
        assert "--noerrdialogs" in result
        assert "--no-first-run" in result

    def test_dpms_disabled(self, render):
        result = render("kiosk", "kiosk-session.sh.j2")
        assert "xset -dpms" in result
        assert "xset s off" in result

    def test_default_resolution_fallback(self, render):
        result = render("kiosk", "kiosk-session.sh.j2")
        assert "1366" in result
        assert "768" in result

    def test_custom_resolution(self, render):
        result = render("kiosk", "kiosk-session.sh.j2",
                        {"kiosk_default_width": 1920,
                         "kiosk_default_height": 1080})
        assert "1920" in result
        assert "1080" in result


# ---- kiosk: xorg-kiosk.conf.j2 ----

class TestXorgKioskConf:
    def test_vt_switching_disabled(self, render):
        result = render("kiosk", "xorg-kiosk.conf.j2")
        assert '"DontVTSwitch"' in result

    def test_zap_disabled(self, render):
        result = render("kiosk", "xorg-kiosk.conf.j2")
        assert '"DontZap"' in result

    def test_blanking_disabled(self, render):
        result = render("kiosk", "xorg-kiosk.conf.j2")
        assert '"BlankTime"' in result
        assert '"0"' in result
