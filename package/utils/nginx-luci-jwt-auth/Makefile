# SPDX-License-Identifier: GPL-2.0-only
#
# SONIX

include $(TOPDIR)/rules.mk

PKG_NAME:=nginx-luci-jwt-auth
PKG_VERSION:=1.1.0
PKG_RELEASE:=1

PKG_BUILD_DIR=$(BUILD_DIR)/$(PKG_NAME)/$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/sonix-network/nginx-luci-jwt-auth.git
PKG_SOURCE_VERSION:=caaf2870ad43204dffae934aa98567f2c4218dc6
PKG_SOURCE_DATE:=2024-07-22
PKG_MIRROR_HASH:=c88a196e8763603513c78145c7fe3058eb112bc4353ec33477abb896a9955a80

include $(INCLUDE_DIR)/package.mk

define Package/nginx-luci-jwt-auth
  SECTION:=base
  CATEGORY:=Network
  TITLE:=SONIX JWT Authentication for LuCI
  DEPENDS:=+python3-flask +python3-ubus
  URL:=https://github.com/sonix-network/nginx-luci-jwt-auth
endef

define Package/nginx-luci-jwt-auth/description
  Use Pomerium JWT to login to LuCi
endef

define Build/Compile
	# Nothing to do
endef

define Package/nginx-luci-jwt-auth/install
	mkdir -p $(1)/etc/nginx/conf.d/ $(1)/etc/init.d/ $(1)/opt/jwt-auth/
	$(CP) $(PKG_BUILD_DIR)/*.py $(1)/opt/jwt-auth/
	$(CP) $(PKG_BUILD_DIR)/jwt-authd $(1)/etc/init.d/
	chmod +x $(1)/etc/init.d/jwt-authd
	$(CP) $(PKG_BUILD_DIR)/jwt-auth.locations $(1)/etc/nginx/conf.d/
endef

$(eval $(call BuildPackage,nginx-luci-jwt-auth))
