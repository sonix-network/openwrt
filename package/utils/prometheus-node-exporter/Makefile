# SPDX-License-Identifier: GPL-2.0-only
#
# Prometheus Node Exporter

include $(TOPDIR)/rules.mk

PKG_NAME:=prometheus-node-exporter
PKG_VERSION:=1.8.2
PKG_RELEASE:=1

PKG_BUILD_DIR=$(BUILD_DIR)/$(PKG_NAME)
PKG_SOURCE:=node_exporter-$(PKG_VERSION).linux-$(ARCH).tar.gz
PKG_SOURCE_URL:=https://github.com/prometheus/node_exporter/releases/download/v$(PKG_VERSION)
PKG_SOURCE_VERSION:=0
PKG_SOURCE_DATE:=2024-06-19
PKG_HASH:=0080c5564c6844f11e2ad39864993407bace78a458d995397e0c419b1d460ec7

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
	$(CP) $(PKG_BUILD_DIR)/node_exporter-*/node_exporter $(1)/usr/bin/
	chmod +x $(1)/usr/bin/node_exporter
	$(CP) ./files/prometheus-node-exporter.init $(1)/etc/init.d/prometheus-node-exporter
	chmod +x $(1)/etc/init.d/prometheus-node-exporter
endef

$(eval $(call BuildPackage,prometheus-node-exporter))
