local o, m, s

local running=(luci.sys.call("pidof python > /dev/null") == 0)
if running then	
	m = Map("drcom", translate("drcom config"), translate("drcom is running"))
else
	m = Map("drcom", translate("drcom config"), translate("drcom is not running"))
end
s = m:section(TypedSection, "drcom", "")
s.addremove = false
s.anonymous = true
s:tab("basic",translate("Basic Settings"))
enable = s:taboption("basic", Flag, "enabled", translate("Enable"))
enable.rmempty = false
function enable.cfgvalue(self, section)
	return luci.sys.init.enabled("drcom") and self.enabled or self.disabled
end

function enable.write(self, section, value)
	if value == "1" then
		luci.sys.call("/etc/init.d/drcom enable >/dev/null")
		luci.sys.call("/etc/init.d/drcom start >/dev/null")
	else
		luci.sys.call("/etc/init.d/drcom stop >/dev/null")
		luci.sys.call("/etc/init.d/drcom disable >/dev/null")
	end
	Flag.write(self, section, value)
end

server = s:taboption("basic", Value, "server", translate("Server IP"))
pppoe_flag = s:taboption("basic", Value, "pppoe_flag", translate("pppoe_flag"))
keep_alive2_flag = s:taboption("basic", Value, "keep_alive2_flag", translate("keep_alive2_flag"))
ESC = s:taboption("basic", Button, "ESC", translate("Patch the escape problem"))
function ESC.write()
    luci.sys.call("/usr/share/patch_esc.sh >/dev/null")
end
ESC_bak = s:taboption("basic", Button, "ESC_bak", translate("Reverse the original ppp.sh file"))
function ESC_bak.write()
    luci.sys.call("\cp -f /usr/share/ppp.sh /lib/netifd/proto/ppp.sh >/dev/null")
end

s:tab("autoconfig", translate("Auto Config"))
msg = s:taboption("autoconfig", DummyValue, "", translate(""), 
translate("Please rename the file to 'drp.pcapng' before upload, file size limit at 1M."))

upload = s:taboption("autoconfig", FileUpload, "upload", translate("Upload file"))
upload.template = "cbi/upload2"
submit = s:taboption("autoconfig", DummyValue, "submit")
submit.template = "cbi/dvalue2"

local dir, upload
dir = "/tmp/upload/"
nixio.fs.mkdir(dir)
luci.http.setfilehandler(
	function(meta, chunk, eof)
		if not upload then
			if not meta.file then return end
			upload = nixio.open(dir .. meta.file, "w")
			if not upload then
				submit.value = translate("Create upload file error.")
				return
			end
		end
		if chunk and upload then
			upload:write(chunk)
		end
		if eof and upload then
			upload:close()
			upload = nil
			submit.value = translate("File saved to") .. ' "/tmp/upload/' .. meta.file .. '"'
		end
	end
)

if luci.http.formvalue("upload") then
	local f = luci.http.formvalue("ulfile")
	if #f <= 0 then
		submit.value = translate("No specify upload file.")
	end
end

msg2 = s:taboption("autoconfig", DummyValue, "", translate(""),
translate("After upload the file, you can generate the config file."))
btn = s:taboption("autoconfig", Button, "_btn", translate("Generate config"))
function btn.write()
	luci.sys.call("/usr/share/drcom_p_config.py > /dev/null")
end

return m
