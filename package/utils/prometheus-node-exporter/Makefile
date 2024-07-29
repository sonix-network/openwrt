# SPDX-License-Identifier: GPL-2.0-only
#
# Prometheus Node Exporter

include $(TOPDIR)/rules.mk

PKG_NAME:=prometheus-node-exporter
PKG_VERSION:=1.8.2
PKG_RELEASE:=1

NODE_ARCH:=$(subst x86_64,amd64,$(ARCH))
PKG_BUILD_DIR=$(BUILD_DIR)/node_exporter-$(PKG_VERSION).linux-$(NODE_ARCH)
PKG_SOURCE:=node_exporter-$(PKG_VERSION).linux-$(NODE_ARCH).tar.gz
PKG_SOURCE_URL:=https://github.com/prometheus/node_exporter/releases/download/v$(PKG_VERSION)
PKG_SOURCE_VERSION:=0
PKG_SOURCE_DATE:=2024-06-19
PKG_HASH_amd64:=6809dd0b3ec45fd6e992c19071d6b5253aed3ead7bf0686885a51d85c6643c66
PKG_HASH_mips64:=0080c5564c6844f11e2ad39864993407bace78a458d995397e0c419b1d460ec7
PKG_HASH:=$(PKG_HASH_$(NODE_ARCH))

include $(INCLUDE_DIR)/package.mk

define Package/prometheus-node-exporter
  SECTION:=base
  CATEGORY:=Utilities
  TITLE:=Prometheus Node Exporter
  URL:=https://github.com/prometheus/node_exporter
endef

define Package/prometheus-node-exporter/description
  Prometheus exporter for hardware and OS metrics exposed by *NIX kernels,
  written in Go with pluggable metric collectors.
endef

define Build/Compile
	# Nothing to do
endef

define Package/prometheus-node-exporter/install
	mkdir -p $(1)/etc/init.d/ $(1)/usr/bin/
	$(CP) $(PKG_BUILD_DIR)/node_exporter $(1)/usr/bin/
	chmod +x $(1)/usr/bin/node_exporter
	$(CP) ./files/prometheus-node-exporter.init $(1)/etc/init.d/prometheus-node-exporter
	chmod +x $(1)/etc/init.d/prometheus-node-exporter
endef

$(eval $(call BuildPackage,prometheus-node-exporter))
