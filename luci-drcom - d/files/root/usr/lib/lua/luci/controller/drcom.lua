module("luci.controller.drcom", package.seeall)

function index()
	if not nixio.fs.access("/etc/config/drcom") then
		return
	end
	local page
	page = entry({"admin", "network", "drcom"}, cbi("drcom"), _("drcom settings"), 100)
	page.i18n = "drcom"
	page.dependent = true
end
