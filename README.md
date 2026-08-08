# Kiosk

Ansible-based headless display-only kiosk for Ubuntu Linux. Hardens the target to CIS Level 1, runs Xorg + Google Chrome in kiosk mode (no window manager) to display a configurable URL on an attached display. Includes Cloudflare WARP for ZTNA connectivity and a built-in NGINX NOC dashboard as the default portal.

## Requirements

- Target: Ubuntu Linux server with SSH key access and attached display
- Control node: Ansible 2.15+, ansible-lint, yamllint
- Cloudflare Zero Trust account with service token for headless WARP enrollment

## Quick Start

```bash
# Lint and syntax-check
make lint
make test

# Deploy with built-in NOC dashboard (http://localhost/)
make deploy WARP_ORG=mycompany WARP_GATEWAY_ID=abc123

# Deploy with custom portal URL
make deploy PORTAL_URL=https://dashboard.example.com
```

## Configuration

Edit `inventory/hosts.yml` to define target hosts and `inventory/group_vars/` for shared configuration.

Key variables (see `inventory/group_vars/all.yml`):

| Variable | Default | Description |
|---|---|---|
| `kiosk_portal_url` | `http://localhost/` | URL displayed on kiosk |
| `kiosk_user` | `kiosk` | System user (nologin shell) |
| `cis_hardening_ssh_port` | `22` | SSH port |
| `cloudflare_warp_ztna_gateway` | `192.168.50.1` | ZTNA gateway IP |

## Roles

1. **common** — OS updates, base packages, Google Chrome apt repo
2. **cis_hardening** — CIS Ubuntu Level 1 (filesystem, services, network, firewall, auth, SSH, logging)
3. **cloudflare_warp** — WARP client install, MDM-based ZTNA enrollment
4. **nginx** — Loopback-only NGINX serving the NOC dashboard (radar + weather)
5. **kiosk** — Xorg + Chrome systemd service, no window manager, display-only lockdown

## License

MIT — see [LICENSE.txt](LICENSE.txt)
