.PHONY: lint test unit-test molecule test-all deploy

lint:
	yamllint .
	ansible-lint

test: lint
	ansible-playbook site.yml --syntax-check
	ansible-playbook tests/verify.yml --syntax-check

unit-test:
	pytest tests/unit/ -v

molecule:
	@for role in common cis_hardening cloudflare_warp nginx kiosk; do \
		echo "=== Molecule: $$role ===" && \
		cd roles/$$role && molecule test && cd ../.. || exit 1; \
	done

test-all: test unit-test molecule

# PORTAL_URL defaults to http://localhost/ (the built-in NOC dashboard).
# ZTNA params: set via env vars (WARP_ORG, WARP_GATEWAY_ID)
# Secrets: use ansible-vault for WARP tokens in inventory/group_vars/kiosks.yml
deploy:
	ansible-playbook site.yml \
		$(if $(PORTAL_URL),-e "kiosk_portal_url=$(PORTAL_URL)") \
		$(if $(WARP_ORG),-e "cloudflare_warp_organization=$(WARP_ORG)") \
		$(if $(WARP_GATEWAY_ID),-e "cloudflare_warp_gateway_id=$(WARP_GATEWAY_ID)") \
		$(if $(WARP_ZTNA_GW),-e "cloudflare_warp_ztna_gateway=$(WARP_ZTNA_GW)") \
		$(EXTRA_ARGS)
