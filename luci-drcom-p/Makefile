include $(TOPDIR)/rules.mk

PKG_NAME:=luci-drcom-p
PKG_VERSION:=1.0.2
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/luci-drcom-p
	SECTION:=luci
	CATEGORY:=LuCI
	SUBMENU:=3. Applications
	TITLE:=3rd Party Drcom Client version P for LuCI
	PKGARCH:=all
	MAINTAINER:=fuyumi
endef

define Package/luci-drcom-p/description
	This package contains LuCI configuration pages for drcomclient version P.
endef

define Build/Prepare
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/luci-drcom-p/postinst
#!/bin/sh
if [ -z "$${IPKG_INSTROOT}" ]; then
	( . /etc/uci-defaults/luci-drcom-p ) && rm -f /etc/uci-defaults/luci-drcom-p
	chmod 755 /etc/init.d/drcom >/dev/null 2>&1
	chmod 755 /usr/share/drcom_p_config.py >/dev/null 2>&1
	chmod 755 /usr/share/patch_esc.sh >/dev/null 2>&1
	chmod 755 /usr/bin/drcom >/dev/null 2>&1
	cp /lib/netifd/proto/ppp.sh /usr/share/ppp.sh >/dev/null 2>&1
	rm -f /tmp/luci-indexcache
fi
exit 0
endef

define Package/luci-drcom-p/install
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_DIR) $(1)/usr/share
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/controller
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/model/cbi
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/view/cbi
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/i18n

	$(INSTALL_CONF) ./files/root/etc/config/drcom $(1)/etc/config/drcom
	$(INSTALL_BIN) ./files/root/etc/uci-defaults/luci-drcom-p $(1)/etc/uci-defaults/luci-drcom-p
	$(INSTALL_BIN) ./files/root/etc/init.d/drcom $(1)/etc/init.d/drcom
	$(INSTALL_BIN) ./files/root/usr/share/drcom_p_config.py $(1)/usr/share/drcom_p_config.py
	$(INSTALL_BIN) ./files/root/usr/share/patch_esc.sh $(1)/usr/share/patch_esc.sh
	$(INSTALL_BIN) ./files/root/usr/bin/drcom $(1)/usr/bin/drcom
	$(INSTALL_DATA) ./files/root/usr/lib/lua/luci/i18n/drcom.zh-cn.lmo $(1)/usr/lib/lua/luci/i18n/drcom.zh-cn.lmo
	$(INSTALL_DATA) ./files/root/usr/lib/lua/luci/view/cbi/dvalue2.htm $(1)/usr/lib/lua/luci/view/cbi/dvalue2.htm
	$(INSTALL_DATA) ./files/root/usr/lib/lua/luci/view/cbi/upload2.htm $(1)/usr/lib/lua/luci/view/cbi/upload2.htm
	$(INSTALL_DATA) ./files/root/usr/lib/lua/luci/model/cbi/drcom.lua $(1)/usr/lib/lua/luci/model/cbi/drcom.lua
	$(INSTALL_DATA) ./files/root/usr/lib/lua/luci/controller/drcom.lua $(1)/usr/lib/lua/luci/controller/drcom.lua
endef

$(eval $(call BuildPackage,luci-drcom-p))
