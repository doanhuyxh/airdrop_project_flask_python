local curl = require('lcurl')
local http = require("socket.http")
local json = require("json")
local ltn12 = require("ltn12")
local lfs = require("lfs")
local socket = require("socket")

keyDown(KEY_TYPE.HOME_BUTTON);
keyUp(KEY_TYPE.HOME_BUTTON);
usleep(1000000);
keyDown(KEY_TYPE.HOME_BUTTON);
keyUp(KEY_TYPE.HOME_BUTTON);
usleep(2000000)

keepAutoTouchAwake(true);

mainApi = "https://vietsoft.pro"
--end get config
apiRouter = ""
typeProxy = ""
nguoiMiner = ""
versionMainlua = "2.44"
country = ""
servermail = ""
stopRunning = True

function safeHttpRequest(url)
    local success, res = pcall(http.request, url)
    if success and res then
        --print(res)
        return res
    else
        return nil
    end
end
--get tenmay
tenmay = ""
sn = getSN()
local response = safeHttpRequest(mainApi.."/infoiphone?sn="..sn)
local data = json.decode(response)
if data ~= nil then 
    if data['success'] == true then
        tenmay = data['name']
        print("Tên máy: "..tenmay)
    end
else 
    alert("Không kết nối được vietsoft.pro")
    stop()
end

--get config 
local cf = safeHttpRequest(mainApi.."/autotouch/config?tenmay="..tenmay)

if cf == nil then
    print("-Không kết nối được server!")
    print("-Kiểm tra server hoặc mạng!")
    stop()
end

if not string.find(cf,"success") then
    print("-Kiểm tra server hoặc mạng!")
    stop()
end

data_cf = json.decode(cf)

if data_cf ~= nill then
    --check proxy
    if data_cf['success'] == true then
        --end get config
        apiRouter = data_cf['apiRouter'] -- api router
        typeProxy = data_cf['proxy']
        nguoiMiner = data_cf['miner']
        version = data_cf['version']
        country = data_cf['country']
        servermail = data_cf['mail']
        autoupdate = data_cf['autoupdate']
        if versionMainlua ~= version then
            if autoupdate == true then
                log("Phiên bản cũ ...tiến hành chạy update...")
                safeHttpRequest("http://localhost:8080/control/start_playing?path=%2Fupdate.lua")
            end
            print("Cập nhật phiên bản!")
            stop()
        end
        if data_cf['stop'] == true then
            print("Stop All")
            stop()
        end
    else
        print('Lỗi kết nối server'..response)
        alert('Lỗi kết nối server')
        stop()
    end
end


function getLocalIP()
    local udp = socket.udp()
    udp:setpeername("8.8.8.8", 80)  -- Set a known address to determine the local IP
    local ip = udp:getsockname()
    udp:close()
    return ip
end

math.randomseed(os.time())
function keyPress(keyType)
    keyDown(keyType)
    usleep(10000)
    keyUp(keyType)
end

function sleep(x,mess)
	mess = mess or ''
	for i=1,x,1 do
		toast(mess..(x-i),1)
        --log(mess..(x-i))
		usleep(1005000)
	end
end

function Luu_Data_File(tenfile,data)
	local file4 = io.open("/var/mobile/Library/AutoTouch/Scripts/"..tenfile, "a");
	local accnow = tostring(data);
	io.output(file4);
	io.write(accnow,"\n");
	io.close(file4);
end


function safeHttpRequestPost(url, body)
    local headers = {
        ["Content-Type"] = "application/json",
        ["Content-Length"] = tostring(#body) -- Thêm Content-Length
    }
    local response_body = {}
    local response_status = {}
    local success, status_code = pcall(function()
        local res, code, headers, status = http.request{
            url = url,
            method = "POST",
            headers = headers,
            source = body and ltn12.source.string(body) or nil,
            sink = ltn12.sink.table(response_body)
        }
        return res, code
    end)

    if success then
        return table.concat(response_body), status_code
    else
        return nil, status_code
    end
end



function changeGeoFast(port,keyport)
	local url = "https://api.danchoimmo.com/svapple/lib/changegeo.php?port="..port.."&keyport="..keyport
	local response_body = {}

	local res, code, response_headers, status = http.request {
	  url = url,
	  method = "GET",
	  sink = ltn12.sink.table(response_body),
	}

	if code == 200 then
	  print("Request successful")
	  local response = table.concat(response_body)
	  print(response)
	else
	  print("Request failed with status code: " .. code)
	end
end

function updateAccountAppleID()
	-- Your XML content
	local xmlContent = [[
	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<array>
		<string>afasfas@gmail.com|123123</string>
		<string>afasfas@gmail.com|123123</string>
		<string>afasfas@gmail.com|123123</string>
		<string>afasfas@gmail.com|123123</string>
		<string>afasfas@gmail.com|123123</string>
		<string>afasfas@gmail.com|123123</string>
		<string>afasfas@gmail.com|123123</string>
		<!-- Add more strings as needed -->
	</array>
	</plist>
	]]

	-- File path
	local filePath = "/private/var/mobile/Library/Preferences/UserPass.plist"

	-- Write the XML content to the file
	local file = io.open(filePath, "w")
	if file then
		file:write(xmlContent)
		file:close()
		print("Successfully wrote to UserPass.plist")
	else
		print("Error: Unable to open the file for writing")
	end
end

function changeAppleID()--change apple id
    appKill("com.ienthach.ChangeAppleID");
	updateAccountAppleID()
	toast("Cập nhật tài khoản Apple ID",1)
	appRun("com.ienthach.ChangeAppleID")
    tap(373, 732)--tap ok
	sleep(3,"cho 3s còn lại -> click ok")
    tap(373, 732)--tap ok
	sleep(3,"cho 3s còn lại -> click ok")
    tap(373, 732)--tap ok
	sleep(3,"cho 3s còn lại -> click ok")
	tap(211,183)--click vao so 1
	sleep(1)
	tap(630,1272)--click xoa so 1
    sleep(1)
	tap(630,1272)--click xoa so 1
    sleep(1)
	tap(630,1272)--click xoa so 1
	sleep(1)
	inputText("1")--dien 1
	sleep(2)
	tap(573,190)--click ra ngoai
	sleep(1)
	tap(370,294)--click next
	sleep(20,"cho 20s change còn lại ")
	toast("Change Apple ID Xong",1)
end

function tool3goff()
	io.popen('activator send switch-off.com.a3tweaks.switch.cellular-data')
	io.popen('activator send switch-off.com.a3tweaks.switch.cellular-data')
	io.popen('activator send switch-off.com.a3tweaks.switch.cellular-data')
	for i = 2, 1, -1 do
		toast("Change in: "..tostring(i))
		usleep(2000000)
	end
end

function tool3gon()
	io.popen('activator send switch-on.com.a3tweaks.switch.cellular-data')
	io.popen('activator send switch-on.com.a3tweaks.switch.cellular-data')
	io.popen('activator send switch-on.com.a3tweaks.switch.cellular-data')
	for i = 2, 1, -1 do
		toast("Change in: "..tostring(i))
		usleep(2000000)
	end
end

function wifioff()
	io.popen('activator send switch-off.com.a3tweaks.switch.wifi')
	io.popen('activator send switch-off.com.a3tweaks.switch.wifi')
	io.popen('activator send switch-off.com.a3tweaks.switch.wifi')
	for i = 2, 1, -1 do
		toast("Change in: "..tostring(i))
		usleep(2000000)
	end
end
function wifion()
	io.popen('activator send switch-on.com.a3tweaks.switch.wifi')
	io.popen('activator send switch-on.com.a3tweaks.switch.wifi')
	io.popen('activator send switch-on.com.a3tweaks.switch.wifi')
	for i = 2, 1, -1 do
		toast("Change in: "..tostring(i))
		usleep(2000000)
	end
end
function changeip4g()
	io.popen('activator send switch-on.com.a3tweaks.switch.cellular-data')
	io.popen('activator send switch-on.com.a3tweaks.switch.airplane-mode')
	usleep(2000000)
	io.popen('activator send switch-off.com.a3tweaks.switch.airplane-mode')
	io.popen('activator send switch-off.com.a3tweaks.switch.wifi')
	io.popen('activator send switch-on.com.a3tweaks.switch.cellular-data')
	usleep(2000000)
end
function swipe(x)
	for i = 1,x,1 do
		tap(638,1169)
		usleep(500000)
	end
end
function openappstore()
	toast("Open App Store",2)
	openURL("itms-apps://itunes.apple.com/updates")
end
function checkimage(path,noti)
	local t = 0
	local check=0
	local result = findImage(path, 0, 0.99, nil, false)
	local x;
	local y;
	for i,v in pairs(result) do
			x=v[1]
			y=v[2]
			check=check+1
   	end
	if check > 0 then
        print('Click thành công ->'..path)
		sleep(1)
		tap(x,y)
		toast(noti,1)
	end
end

function waitImage(path,time,noti)
	local kq = false
	for i = 1, time do
        toast("WAIT IMAGE "..noti,1)
		local t = 0
		local check=0
		local result = findImage(path, 0, 0.99, nil, false)
		local x;
		local y;
		for i,v in pairs(result) do
				x=v[1]
				y=v[2]
				check=check+1
				kq = true
		end
		if check > 0 then
			sleep(1)
			--tap(x,y)
			toast("ĐÃ THẤY "..noti,1)
			break
		end
		sleep(1)
	end
	return kq
end

function randomPassword()
	password = ""
	math.randomseed(os.time()) -- Khởi tạo seed cho hàm random
	local chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" -- Các ký tự sử dụng trong password
	local password = ""

	local chars0 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" -- Các ký tự sử dụng trong password
	local charIndex0 = math.random(1, #chars0) -- Chọn một ký tự ngẫu nhiên từ chars
	local char0 = string.sub(chars0, charIndex0, charIndex0)
	password = password .. char0

	for i = 1, 8 do
		local charIndex = math.random(1, #chars) -- Chọn một ký tự ngẫu nhiên từ chars
		local char = string.sub(chars, charIndex, charIndex)
		if i == 1 then
			char = string.upper(char) -- Chuyển ký tự đầu tiên thành chữ cái viết hoa
		end
		password = password .. char
	end
	local chars2 = "abcdefghijklmnopqrstuvwxyz" -- Các ký tự sử dụng trong password
	local charIndex2 = math.random(1, #chars2) -- Chọn một ký tự ngẫu nhiên từ chars
	local char2 = string.sub(chars2, charIndex2, charIndex2)
	pass = password..tostring(math.random(01, 99))..char2

    print("password: "..pass)

	return pass
end
function trim(s)
	s = string.gsub(s, "%s+", "")
	return s
end
function string.random(length,charset_1,charset_2)
	local res = ""
	for i = 1, length do
		res = res .. string.char(math.random(charset_1, charset_2))
	end
	return res
end

function birthday()
	l_mm={"01","02","03","04","05","06","07","08","09","10","11","12"}
	local mm =l_mm[math.random(1, 12)]
	l_dd={"01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"}
	local dd = l_dd[math.random(1, 28)]
	local yyyy = math.random(1980, 1999)
	birth = mm..dd..yyyy
	return birth
end
function birthday2()
	l_mm={"01","02","03","04","05","06","07","08","09","10","11","12"}
	local mm =l_mm[math.random(1, 12)]
	l_dd={"01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"}
	local dd = l_dd[math.random(1, 28)]
	local yyyy = math.random(1980, 1999)
	birth = dd..mm..yyyy
	return birth
end

local words = {
    "hanoi",
    "openai",
    "gpt3",
    "lua",
    "programming",
    "security",
    "apple",
    "random",
    "language",
    "authentication",
    -- Thêm 90 từ khác ở đây
    "algorithm",
    "database",
    "network",
    "web",
    "server",
    "client",
    "javascript",
    "python",
    "java",
    "csharp",
    "ruby",
    "swift",
    "mobile",
    "desktop",
    "framework",
    "version",
    "debugging",
    "testing",
    "deployment",
    "encryption",
    "authentication",
    "authorization",
    "session",
    "cookie",
    "cache",
    "compiler",
    "syntax",
    "semantic",
    "bug",
    "feature",
    "function",
    "variable",
    "constant",
    "parameter",
    "argument",
    "class",
    "object",
    "inheritance",
    "polymorphism",
    "abstraction",
    "interface",
    "library",
    "framework",
    "algorithm",
    "data",
    "structure",
    "queue",
    "stack",
    "linked",
    "list",
    "array",
    "hash",
    "table",
    "graph",
    "tree",
    "binary",
    "search",
    "sort",
    "merge",
    "bubble",
    "insertion",
    "selection",
    "recursion",
    "iteration",
    "loop",
    "conditional",
    "statement",
    "variable",
    "scope",
    "pointer",
    "reference",
    "garbage",
    "collection",
    "heap",
    "stack",
    "filesystem",
    "database",
    "sql",
    "nosql",
    "mongodb",
    "mysql",
    "postgresql"
}
-- Hàm chọn ngẫu nhiên một số từ từ danh sách
local function generateRandomAnswer()
    local answer = ""
    local numWords = math.random(1, 2)  -- Chọn ngẫu nhiên từ 2 đến 4 từ

    for i = 1, numWords do
        local randomIndex = math.random(1, #words)
        answer = answer .. words[randomIndex]
    end

    return answer
end

function randomStreet2()
	local streetData =
{
  streets = {
    "Main Street",
    "First Avenue",
    "Oak Avenue",
    "Elm Street",
    "Broadway",
    "Park Avenue",
    "Cedar Lane",
    "Maple Road",
    "Washington Boulevard",
    "Pine Street",
    "Springfield Drive",
    "Sunset Boulevard",
    "Highland Avenue",
    "Ocean View Drive",
    "Riverside Drive",
    "Sunrise Lane",
    "Greenwood Terrace",
    "Hillcrest Road",
    "Meadowbrook Lane",
    "Willow Street",
    "Lakeside Drive",
    "Orchard Lane",
    "Sycamore Court",
    "Hickory Lane",
    "Forest Avenue",
    "Cherry Street",
    "Pleasant Street",
    "Valley View Road",
    "Grove Street",
    "Cottage Avenue",
    "River Road",
    "Juniper Way",
    "Holly Drive",
    "Rosewood Lane",
    "Walnut Street",
    "Laurel Avenue",
    "Winding Way",
    "Brookside Drive",
    "Birch Street",
    "Wisteria Lane",
    "Chestnut Court",
    "Redwood Drive",
    "Vine Street",
    "Heather Court",
    "Cypress Lane",
    "Aspen Lane",
    "Magnolia Place",
    "Hawthorn Lane",
    "Beech Street",
    "Alder Avenue",
    "Cambridge Road",
    "Crescent Avenue",
    "Pinehurst Drive",
    "Woodland Drive",
    "Hillside Avenue",
    "Willowbrook Lane",
    "Acacia Court",
    "Cottonwood Drive",
    "Briarwood Court",
    "Dogwood Lane",
    "Glenwood Drive",
    "Windsor Road",
    "Cedar Avenue",
    "River Street",
    "Bayberry Lane",
    "Linden Court",
    "Poplar Lane",
    "Sunnyside Avenue",
    "Garden Street",
    "Fairview Drive",
    "Morningside Drive",
    "Harmony Lane",
    "Blossom Lane",
    "Birchwood Court",
    "Olive Street",
    "Locust Avenue",
    "Valley Road",
    "Fieldstone Drive",
    "Arlington Avenue",
    "Thornwood Lane",
    "Westminster Drive",
    "Evergreen Court",
    "Silverado Drive",
    "Tanglewood Road",
    "Larch Street",
    "Berkshire Drive",
    "Pineview Drive",
    "Cobblestone Lane",
    "Camden Lane",
    "Magnolia Drive",
    "Whispering Pines",
    "Autumn Ridge",
    "Stonegate Court",
    "Whitney Avenue",
    "Emerson Street",
    "Belmont Avenue",
    "Somerset Lane",
    "Camellia Court",
    "Eagle Street"
}
}
    math.randomseed(os.time())

    local function randomIndex(n)
        return math.random(1, n)
    end

    local street = streetData.streets[randomIndex(#streetData.streets)]
    local houseNumber = tostring(math.random(100, 999))

    local address = houseNumber .. " " .. street
    return address
end

function dungauto()
	openURL("shadowrocket://disconnect")
	sleep(2)
	tool3goff()
	sleep(2)
	appKill("com.liguangming.Shadowrocket")
	sleep(2)
	appKill("me.autotouch.AutoTouch.ios8")
	usleep(1000000)
	appRun("me.autotouch.AutoTouch.ios8")
	usleep(1000000)
	wifion()
	stop()
end

function choluotmoi(thanhcong,thatbai)
	openURL("shadowrocket://disconnect")
	sleep(2)
	tool3goff()
	sleep(2)
	--appKill("com.liguangming.Shadowrocket")
	sleep(2)
	appKill("me.autotouch.AutoTouch.ios8")
	usleep(1000000)
	appRun("me.autotouch.AutoTouch.ios8")
	usleep(1000000)
	wifioff()
end

function trim(s)
	for i=1, 1, 1 do
		if s~= nil then
  			s= (string.gsub(s, "^%s*(.-)%s*$", "%1"))
		else
			toast("Null")
			break
		end
	end
	return s
end

function info()
	phone =  math.random(1111111111, 9999999999)
	street =  math.random(1, 10000).." rd"
	local lines = 0
	local states = {"AL","AK"}
	i = math.random(1, #states)
	state = states[i]
    for line in io.lines(rootDir().."/"..state..".txt") do
      lines = lines+1
    end
	--return lines
	f = io.open(rootDir().."/"..state..".txt", "r+")
	local t = math.random(1, lines)
	for i=1, t, 1 do
		data = trim(f:read())
	end
	f:close()
	result = {};
    for match in (data.."|"):gmatch("(.-)".."|") do
        table.insert(result, match);
    end
	arr = {result[1],result[2],i,street,phone}--code|bang|dia chi|street|phone
    return arr;
end

function infoCN()
    -- Hàm để tách các giá trị trong chuỗi dựa vào dấu "|"
    local function splitString(inputstr, sep)
        sep = sep or "|"
        local t = {}
        for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
            table.insert(t, str)
        end
        return t
    end

    -- Hàm để lấy ngẫu nhiên một dòng từ một bảng
    local function getRandomLine(lines)
        math.randomseed(os.time())
        local randomIndex = math.random(1, #lines)
        return lines[randomIndex]
    end

    -- Hàm để đọc các dòng từ file và lưu vào một bảng
    local function readLinesFromFile(filename)
        local file = io.open(filename, "r")
        if file then
            local lines = {}
            for line in file:lines() do
                table.insert(lines, line)
            end
            file:close()
            return lines
        else
            return nil
        end
    end

    local filename = rootDir() .. "/data/cn/zipcode.txt"

    -- Đọc các dòng từ file theo đường dẫn filename vào bảng
    local lines = readLinesFromFile(filename)

    if lines then
        -- Lấy ngẫu nhiên một dòng
        local randomLine = getRandomLine(lines)

        -- Tách thông tin từ dòng ngẫu nhiên thành một mảng info
        local info = splitString(randomLine, "|")

        -- Tạo mảng arr và thêm các giá trị từng cái vào mảng
        local arr = {}
        for _, value in ipairs(info) do
            table.insert(arr, value)
        end
		--them phone + street
		phone =  math.random(1111111111, 9999999999)
		street = ""
		if phone % 2 == 0 then
			street =  math.random(1, 10000).." Xin Gang"
		else
			street =  math.random(1, 10000).." Gong Ren"
		end
		table.insert(arr,street)
		table.insert(arr,phone)
        return arr
    else
        print("Không tìm thấy file hoặc có lỗi khi đọc file.")
        return nil
    end
	--export (1|Bengbu|Anhui|233000|street|phone)
end

function infoID()
    -- Hàm để tách các giá trị trong chuỗi dựa vào dấu "|"
    local function splitString(inputstr, sep)
        sep = sep or "|"
        local t = {}
        for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
            table.insert(t, str)
        end
        return t
    end

    -- Hàm để lấy ngẫu nhiên một dòng từ một bảng
    local function getRandomLine(lines)
        math.randomseed(os.time())
        local randomIndex = math.random(1, #lines)
        return lines[randomIndex]
    end

    -- Hàm để đọc các dòng từ file và lưu vào một bảng
    local function readLinesFromFile(filename)
        local file = io.open(filename, "r")
        if file then
            local lines = {}
            for line in file:lines() do
                table.insert(lines, line)
            end
            file:close()
            return lines
        else
            return nil
        end
    end

    local filename = rootDir() .. "/data/id/zipcode.txt"

    -- Đọc các dòng từ file theo đường dẫn filename vào bảng
    local lines = readLinesFromFile(filename)

    if lines then
        -- Lấy ngẫu nhiên một dòng
        local randomLine = getRandomLine(lines)

        -- Tách thông tin từ dòng ngẫu nhiên thành một mảng info
        local info = splitString(randomLine, "|")

        -- Tạo mảng arr và thêm các giá trị từng cái vào mảng
        local arr = {}
        for _, value in ipairs(info) do
            table.insert(arr, value)
        end
		--them phone + street
		phone =  math.random(111111111, 999999999)
		street = ""
		if phone % 2 == 0 then
			street =  math.random(1, 10000).." Sudirman"
		else
			street =  math.random(1, 10000).." Thamrin"
		end
		table.insert(arr,street)
		table.insert(arr,phone)
        return arr
    else
        print("Không tìm thấy file hoặc có lỗi khi đọc file.")
        return nil
    end
	--export (1|City|Zipcode|Address|Phone)
end


function infoAngola()
    -- Hàm để tách các giá trị trong chuỗi dựa vào dấu "|"
    local function splitString(inputstr, sep)
        sep = sep or "|"
        local t = {}
        for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
            table.insert(t, str)
        end
        return t
    end

    -- Hàm để lấy ngẫu nhiên một dòng từ một bảng
    local function getRandomLine(lines)
        math.randomseed(os.time())
        local randomIndex = math.random(1, #lines)
        return lines[randomIndex]
    end

    -- Hàm để đọc các dòng từ file và lưu vào một bảng
    local function readLinesFromFile(filename)
        local file = io.open(filename, "r")
        if file then
            local lines = {}
            for line in file:lines() do
                table.insert(lines, line)
            end
            file:close()
            return lines
        else
            return nil
        end
    end

    local filename = rootDir() .. "/data/angola/zipcode.txt"

    -- Đọc các dòng từ file theo đường dẫn filename vào bảng
    local lines = readLinesFromFile(filename)

    if lines then
        -- Lấy ngẫu nhiên một dòng
        local randomLine = getRandomLine(lines)

        -- Tách thông tin từ dòng ngẫu nhiên thành một mảng info
        local info = splitString(randomLine, "|")

        -- Tạo mảng arr và thêm các giá trị từng cái vào mảng
        local arr = {}
        for _, value in ipairs(info) do
            table.insert(arr, value)
        end
		--them phone + street
		phone =  math.random(1111111111, 9999999999)
		street = ""
		if phone % 2 == 0 then
			street =  math.random(1, 10000).." Adams Tunnel"
		else
			street =  math.random(1, 10000).." Rippin Meadows"
		end
		table.insert(arr,street)
		table.insert(arr,phone)
        return arr
    else
        print("Không tìm thấy file hoặc có lỗi khi đọc file.")
        return nil
    end
	--export (1|Bengbu|Anhui|233000|street|phone)
end

function getCode2(email, pass)
    local curl = require "cURL"
    local count = 0
    while count < 5 do
       local url = "https://api.danchoimmo.com/idapple/getcode.php?email="..email.."&pass="..pass
       local response = {}
       curl.easy{
         url = url,
         ssl_verifyhost = false,
         ssl_verifypeer = false,
          writefunction = function(data)
             table.insert(response, data)
             return #data
          end
       }:perform()
       local result = table.concat(response)
       if result:match("%d%d%d%d%d%d") then -- nếu kết quả trả về là một chuỗi số 6 chữ số
          return result:match("%d%d%d%d%d%d")
       else
          count = count + 1
       end
    end
    return "0"
 end


 function postData(httpURL)

	curl.easy{
   	 	url = httpURL
  	}
  	:perform()
	:close()
end

function postJson(urlWeb,json)
	json_data = json
	-- Thiết lập các header và option cho request
	local headers = {
	  ["Content-Type"] = "application/json",
	  ["Content-Length"] = #json_data
	}
	local options = {
	  url = urlWeb,
	  method = "POST",
	  headers = headers,
	  source = ltn12.source.string(json_data)
	}
	-- Gửi request
	local check = safeHttpRequest(options)

	-- Xử lý phản hồi
	if check then
	  print("Gửi dữ liệu thành công")
	else
	  print("Gửi dữ liệu thất bại")
	end
end

function postJson2(urlWeb,json)
	json_data = json
	-- Thiết lập các header và option cho request
	local headers = {
	  ["Content-Type"] = "application/json",
	  ["Content-Length"] = #json_data
	}
	local options = {
	  url = urlWeb,
	  method = "POST",
	  headers = headers,
	  source = ltn12.source.string(json_data)
	}
	-- Gửi request
	local check = safeHttpRequest(options)

	-- Xử lý phản hồi
	if check then
	  print("Gửi dữ liệu thành công")
      return true
	else
	  print("Gửi dữ liệu thất bại")
      return false
	end
end

function updateStatusIphone(name,status)
    sn = getSN()
    --push data ve server
    local dataJson = '{"sn":"'..sn..'","status":"'..status..'"}'
    local boolSend = false
    for i = 1,7,1 do
        check = postJson2(mainApi .. '/lastiphone',dataJson)
        if check == true then
            boolSend = true
            break
        end
    end
    if boolSend == true then
        print("DONE!!")
    else
        print("FAIL!!")
    end

    return boolSend
end

function findanh()
	local x = "ok";
	local t = 0
	while x == "ok"
	do
        tap(265,756)--click notnow
		local result1 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/card.PNG", 0, 0.99, nil, false)
		local result2 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/continu.PNG", 0, 0.99, nil, false)
		local result4 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/cvvfalse.PNG", 0, 0.99, nil, false)
		local result5 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/zipfalse.PNG", 0, 0.99, nil, false)
		local result6 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/carderror1.PNG", 0, 0.99, nil, false)
		local result7 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/card2.PNG", 0, 0.99, nil, false)
		local result3 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/support.PNG", 0, 0.99, nil, false)
		local result8 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/ok.PNG", 0, 0.99, nil, false)
		if #result1 > 0 then
			x= "card"
			break
		end
		if #result2 > 0 then
			x= "continu"
			break
		end
		if #result3 > 0 then
			x= "support"
			break
		end
		if #result4 > 0 then
			x= "card"
			break
		end
		if #result5 > 0 then
			x= "ok"
			break
		end
		if #result6 > 0 then
			x= "ok"
			break
		end
		if #result7 > 0 then
			x= "card"
			break
		end
		if #result8 > 0 then
			x= "ok"
			break
		end
		t = t+1
		if t > 10 then
			break;
		end
		usleep(3000000)
	end
	return x
end

function verifycode()
	local t = 0
	local x;
	while true
	do
		local result1 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/trylater.PNG", 0, 0.99, nil, false)
		local result2 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/checkcode.PNG", 0, 0.99, nil, false)
		if #result1 > 0 then
			x= "trylater"
			break
		end
		if #result2 > 0 then
			x= "sendcode"
			break
		end
		t=t+1
		if t > 10 then
			break
		end
		usleep(2000000)
	end
	return x
end

function fixpupup()
	local popup1 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/popup1.PNG", 0, 0.99, nil, false)
	if #popup1 > 0 then
		usleep(1000000)
		tap(374,1196)
		usleep(2000000)
	end
end
function swipeVertically()
	for i = 1,7,1 do
		touchDown(1, 200, 300);
		for i = 900,300,-100 do
			usleep(12000);
			touchMove(1, 200, i);
		end
		touchUp(1, 200, 900);
		usleep(500000);
  	end
end

function randomFL()
    l_ten = {'Charles', 'Johnny', 'Destiny', 'Gerald', 'Robin', 'Gregory', 'Chelsea', 'Brandon', 'Tammy', 'Justin', 'Dustin', 'Veronica', 'Jacob', 'Cesar', 'Brian', 'Brian', 'Brent', 'Martha', 'Angela', 'George', 'Jennifer', 'Edwin', 'James', 'Tom', 'Julian', 'Gina', 'Michael', 'Julie', 'Alison', 'Antonio', 'Mary', 'Gerald', 'Natalie', 'Roger', 'Donald', 'Hector', 'Amanda', 'Destiny', 'Kevin', 'Jessica', 'Hailey', 'David', 'Megan', 'William', 'Robert', 'Daniel', 'Julie', 'Darren', 'Victor', 'Mary', 'Emma', 'Christie', 'Zachary', 'Emma', 'James', 'Michael', 'Robert', 'Julie', 'Spencer', 'Matthew', 'Xavier', 'Denise', 'Brittany', 'Tammy', 'Ashley', 'Nancy', 'Margaret', 'Raymond', 'Brandy', 'Sean', 'Amanda', 'Cheryl', 'Christopher', 'Chad', 'Peter', 'Jeremy', 'Logan', 'Anna', 'Christopher', 'Jonathan', 'Charles', 'Jenny', 'Donald', 'Daisy', 'Ashley', 'Lauren', 'Adam', 'James', 'Joshua', 'Stephanie', 'Ryan', 'Troy', 'Alex', 'Lawrence', 'Chelsea', 'Angel', 'Alan', 'Brian', 'Patricia', 'Alexandra'}
	l_ho = {'Brown', 'Short', 'Malone', 'Brown', 'Johnston', 'Johnson', 'Reynolds', 'Shannon', 'Green', 'Flores', 'Parks', 'Glover', 'Hernandez', 'Long', 'Huynh', 'Willis', 'Jones', 'Gonzalez', 'Blair', 'King', 'Aguilar', 'Larson', 'Jackson', 'Romero', 'Wilson', 'Davies', 'Norman', 'Beck', 'Brown', 'Jones', 'Cook', 'Stevens', 'Obrien', 'Hartman', 'Ruiz', 'Rubio', 'Martin', 'Baker', 'Grant', 'Martinez', 'Rodgers', 'Lee', 'Carter', 'Johnson', 'Moran', 'Harmon', 'Nguyen', 'Hartman', 'Wise', 'Steele', 'Moore', 'White', 'Carlson', 'Johnson', 'Walker', 'Smith', 'Anderson', 'Hernandez', 'Ramos', 'Spencer', 'Galloway', 'Harris', 'Phillips', 'Davis', 'Johnson', 'Larson', 'George', 'Church', 'Barber', 'Patel', 'Golden', 'Nguyen', 'Richardson', 'Price', 'Lee', 'Cobb', 'Ramirez', 'Oconnor', 'Patterson', 'Meyer', 'Baker', 'Flores', 'Allen', 'Cervantes', 'Flores', 'Martin', 'Morales', 'Hunt', 'Brown', 'Palmer', 'Stephens', 'Reyes', 'Martin', 'Taylor', 'Ray', 'Wright', 'Conrad', 'Rivas', 'Powell', 'Zavala'}
	ten = l_ten[math.random(1, #l_ten)]
	ho = l_ho[math.random(1, #l_ho)]
	firstlast = {ten,ho}
	return firstlast
end

function updateHotmail(user,trangthai)
	function exportData(txt)
		card = txt;
	end
	curl.easy{
   	 	url = "http://207.148.99.79/admin/appleid/cap_nhat_hotmail.php?hotmail="..user.."&appleid="..trangthai,
    	httpheader = {
      		"X-Test-Header1: Header-Data1",
      		"X-Test-Header2: Header-Data2",
    	},
    	writefunction = exportData
  	}
  	:perform()
	:close()
end

--*******Module reg card-----

function swipeVerticallyCN()
	for i = 1,4,1 do
		touchDown(1, 200, 300);
		for i = 900,300,-5 do
			usleep(24000);
			touchMove(1, 10, i);
		end
		touchUp(1, 200, 900);
		usleep(500000);
  	end
end


function swipeVerticallyID()
	for i = 1,7,1 do
		touchDown(1, 200, 300);
		for i = 900,300,-93 do
			usleep(24000);
			touchMove(1, 10, i);
		end
		touchUp(1, 200, 900);
		usleep(50000);
  	end
end

function swipeVerticallyUS()
	for i = 1,7,1 do
		touchDown(1, 200, 300);
		for i = 900,300,-100 do
			usleep(12000);
			touchMove(1, 200, i);
		end
		touchUp(1, 200, 900);
		usleep(500000);
  	end
end

function swipeVerticallyBO()
	for i = 1,2,1 do
		touchDown(1, 200, 300);
		for i = 900,300,-5 do
			usleep(24000);
			touchMove(1, 10, i);
		end
		touchUp(1, 200, 900);
		usleep(500000);
  	end
end

function swipeVerticallyOM()
	for i = 1,9,1 do
		touchDown(1, 200, 300);
		for i = 1310,200,-10 do
			usleep(24000);
			touchMove(1, 10, i);
		end
		touchUp(1, 200, 900);
		usleep(500000);
  	end
end

function getcard()
	function exportData(txt)
		card = txt;
	end
	curl.easy{
   	 	url = "http://api.danchoimmo.com/svapple/apicard.php",
    	httpheader = {
      		"X-Test-Header1: Header-Data1",
      		"X-Test-Header2: Header-Data2",
    	},
    	writefunction = exportData
  	}
  	:perform()
	:close()
	result = {};
    for match in (card.."|"):gmatch("(.-)".."|") do
        table.insert(result, match);
    end
	table.insert(result, card);
	return result
end

function getInfo(country)
	local url = "http://207.148.99.79/admin/info/"..country..".php"
	-- Gửi yêu cầu HTTP đến trang web và lấy dữ liệu về
	local response = http.request(url)

	-- Phân tích chuỗi JSON thành bảng Lua
	local data = json.decode(response)

	-- Lấy giá trị zip từ bảng dữ liệu
	local a = {
		first_name = data.first_name,
		last_name = data.last_name,
		sex = data.sex,
		street = data.street,
		city = data.city,
		state = data.state,
		zip = data.zip,
		region = data.region,
		phone = data.phone,
	}
	return a
	--info : first_name|last_name|sex street|city|state|zip|region
end
--*******End module reg card-----
--*******Module wifi****
function changeIpVPN()
	wifion()
	sleep(2)
	openURL("shadowrocket://disconnect")
	sleep(2)
	for i=5, 1, -1 do
		local url = "https://api.danchoimmo.com/idapple/proxy.php"
		local response = http.request(url)
		usleep(2000000)
		if response == nil then
			print("khong load duoc")
			sleep(1)
		else
			if string.find(response,"http") then
				print(response)
				openURL('shadowrocket://add/'..response)
				print("Load Proxy thanh cong!")
				break
			end
		end
	end
	sleep(5)
	--chọn proxy mới
	toast("Chon proxy moi",2)
	tap(424,633)
	sleep(1)
	openURL("shadowrocket://connect")
	sleep(2)
end

-- Hàm tạo chuỗi Base64
function encodeBase64(input)
    local b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return (input:gsub('.', function(x)
        local r, b = "", x:byte()
        for i = 8, 1, -1 do
            r = r .. (b % 2 ^ i - b % 2 ^ (i - 1) > 0 and '1' or '0')
        end
        return r
    end) .. '0000'):gsub('%d%d%d?%d?%d?%d?', function(x)
        if #x < 6 then
            return ''
        end
        local c = 0
        for i = 1, 6 do
            c = c + (x:sub(i, i) == '1' and 2 ^ (6 - i) or 0)
        end
        return b:sub(c + 1, c + 1)
    end)
end

function changeTinsoft()
	wifion()
	sleep(2)
	openURL("shadowrocket://disconnect")
	sleep(2)
	local ip = '192.168.100.100'
	local port = '12345'
	for i = 1, 120 do
		local a, status = http.request('http://proxy.tinsoftsv.com/api/changeProxy.php?key=TLmfNUgNbhgR5SL8YyBGTWMDMusK1xWuBf6ACJ')
		if status == 200 then
			print(a)
			local data = json.decode(a)
			if string.find(a,"true") then
				local proxy_str = data.proxy
				print(proxy_str)
				ip, port = string.match(proxy_str, "([^:]+):(%d+)")
				print(ip)
				print(port)
				print("Get ip thanh cong!")
				break
			else
				local cho1 = data.next_change or 10
				print("cho"..cho1.." giay")
				sleep(cho1)
			end
		else
			print("Loi Request -> Cho 10s")
			sleep(10)
		end
	end
	local input_string = ip..":"..port
	local encoded_string = encodeBase64(input_string)
	local url_string = "http://" .. encoded_string
	openURL("shadowrocket://add/"..url_string.."#"..input_string)
	sleep(2)
	--chọn proxy mới
	toast("Chon proxy moi",2)
	tap(424,633)
	sleep(1)
	openURL("shadowrocket://connect")
	sleep(2)
end


function setupVPN()
	--openURL("shadowrocket://connect")
    --sleep(3)
    --tap(515,808)--click ok install vpn
    --sleep(2)
    --tap(252,793)--click alow
    --sleep(3)
    openURL("shadowrocket://config/add/https://api.danchoimmo.com/idapple/apple.conf")--download content
    sleep(5)
end
--*******End Module wifi****

function changeUDID(duongdan)
	appKill("com.apple.AppStore")
	sleep(1)
	local plist_file = duongdan.."/.com.apple.mobile_container_manager.metadata.plist"

	function generateRandomUUID()
		local template = "XXXXXXXX-XXXX-4XXX-YXXX-XXXXXXXXXXXX"
		return string.gsub(template, "[XY]", function(c)
			local r = math.random(0, 15)
			local v = (c == "X") and r or (r & 0x3 | 0x8)
			return string.format("%X", v)
		end)
	end

	-- Xóa file cũ nếu tồn tại
	os.remove(plist_file)

	-- Tạo file mới với giá trị UUID mới
	local new_uuid = generateRandomUUID()
	local new_content = [[<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
		<key>MCMMetadataIdentifier</key>
		<string>com.apple.AppStore</string>
		<key>MCMMetadataPersona</key>
		<integer>501</integer>
		<key>MCMMetadataContentClass</key>
		<integer>2</integer>
		<key>MCMMetadataUUID</key>
		<string>]] .. new_uuid .. [[</string>
	</dict>
	</plist>]]

	local file = io.open(plist_file, "w")
	if not file then
		alert("Không thể tạo file mới: " .. plist_file)
	else
		file:write(new_content)
		file:close()

		print("Đã tạo file mới với giá trị UUID mới: " .. new_uuid)
	end
    -- Xóa các thư mục "Documents", "Library", "SystemData" và "tmp" trong thư mục duongdan
	io.popen("rm -rf " .. duongdan .. "/Library")
    io.popen("rm -rf " .. duongdan .. "/Documents")
    io.popen("rm -rf " .. duongdan .. "/SystemData")
    io.popen("rm -rf " .. duongdan .. "/tmp")
end

--lib otp sms uk


function soOTPUK(idOTP)
    for i = 1, 20 do
        toast("Check số OTP giây thứ " .. i * 5, 1)
        local response = safeHttpRequest("https://api.sms-activate.io/stubs/handler_api.php?api_key=4e9A7cfc49574bA1d0399d7f5d57478c&action=getRentStatus&id=" .. tostring(idOTP))
        sleep(1)
        if response ~= nil then
            print(response)
            if string.find(response, "success") then
                local data = json.decode(response)
                local values = data["values"]

                -- Đếm số phần tử trong mảng values
                local count = 0
                for _ in pairs(values) do
                    count = count + 1
                end

                print(count)
                return count
            else
                print("0")
                return 0
            end
        end
    end
end

function readOTPUK(idOTP)
    for i = 1, 20 do
        toast("Chờ OTP giây thứ " .. i * 5, 1)
        local response = safeHttpRequest("https://api.sms-activate.io/stubs/handler_api.php?api_key=4e9A7cfc49574bA1d0399d7f5d57478c&action=getRentStatus&id=" .. tostring(idOTP))
        sleep(1)
        if response ~= nil then
            print(response)
            if string.find(response, "success") then
                toast("Thấy OTP!", 1)
                local data = json.decode(response)
                local values = data["values"]

                -- Lấy phần tử đầu tiên từ mảng values
                local otpText = values["0"]["text"]
                -- Trích xuất mã OTP là chuỗi số có 4 chữ số
                local otpCode = string.match(otpText, "%d%d%d%d")
                if otpCode then
                    toast("OTP: " .. otpCode, 1)
                    print("OTP: " .. otpCode)
                    return otpCode
                else
                    toast("Không tìm thấy mã OTP trong văn bản.", 1)
                end
            end
        end
    end
end

--sms otp uk---
function laySDTUK()
    layso = false
    for i = 1, 200 do
        toast("Tiến hành lấy PHONE")
        local response = safeHttpRequest("https://api.sms-activate.io/stubs/handler_api.php?api_key=4e9A7cfc49574bA1d0399d7f5d57478c&action=getRentNumber&service=wx&country=16")
        sleep(1)
        if response ~= nil then
            print(response)
            if string.find(response,"success") then
                toast("Thấy phone!",1)
                local data = json.decode(response)
                phoneuk = data["phone"]["number"]
                idphone = data["phone"]["id"]
                toast("number:"..phoneuk,1)
                print(phoneuk)
                print(idphone)
                layso = true
                return True
            end
        end
        sleep(1)
    end
    if layso == false then
        return false
    end
end

math.randomseed(os.time())

function generateUKPhoneNumber()
    local phoneUKPrefix = "746046"
    local randomNumber = ""

    for i = 1, 4 do
        randomNumber = randomNumber .. math.random(0, 9)
    end

    return phoneUKPrefix .. randomNumber
end


function getStatus()
	local laststatus = nil
    for i = 1, 100 do
        toast("Get Status")
        local response = safeHttpRequest("http://192.168.3.122:8989/quanlymayinfo?iphone=iPhone1")
        sleep(1)
        if response ~= nil then
            --print(response)
            if string.find(response,"success") then
                local data = json.decode(response)
                laststatus = data["lancuoi"]
                break
            end
        end
    end
    return laststatus
end

function getStatusRun(api, tenmay)
	local isRun = nil
    for i = 1, 100 do
        toast("Get Status")
        local response = safeHttpRequest(api.."/check_run_script?tenmay=".. tenmay)
        sleep(1)
        if response ~= nil then
            --print(response)
            if string.find(response,"success") then
                local data = json.decode(response)
				check = data["run"]
                print(data['message'])
				if check == true then
					isRun = true
				else
					isRun = false
				end
                break
            end
        end
    end
    return isRun
end

function getStatusAll(api)
    local isRun = nil
    local cf = safeHttpRequest(mainApi.."/autotouch/config?tenmay="..tenmay)
    if cf == nil then 
        print("-Kiểm tra server tra ve nil!")
        stop()
    else
        if not string.find(cf,"success") then
            print("-Kiểm tra server hoặc mạng!")
            stop()
        end
    end
    data_cf = json.decode(cf)
    if data_cf ~= nill then
        --check proxy
        toast("❓❓❓ Check Statun Run Script ❓❓❓",3)
        if data_cf['success'] == true then
            --end get config
            apiRouter = data_cf['apiRouter'] -- api router
            typeProxy = data_cf['proxy']
            nguoiMiner = data_cf['miner']
            version = data_cf['version']
            country = data_cf['country']
            servermail = data_cf['mail']
            autoupdate = data_cf['autoupdate']
            isRun = data_cf['stop']
            if versionMainlua ~= version then
                if autoupdate == true then
                    log("Phiên bản cũ ...tiến hành chạy update...")
                    safeHttpRequest("http://localhost:8080/control/start_playing?path=%2Fupdate.lua")
                end
                print("Cập nhật phiên bản!")
                stop()
            end
            if isRun == true then
                print("Stop All")
                stop()
            end
        end
    end
    return isRun
end

function getInforMay(tenmay)
	local laststatus = nil
	for i = 1, 100 do
        local response = safeHttpRequest(mainApi.."/quanlymayinfo?iphone=" .. tenmay)
        sleep(1)
        if response ~= nil then
            if string.find(response,"success") then
                local data = json.decode(response)
				if data["laststatus"] == 'thanhcong'then
					laststatus = 'thanhcong ✅✅✅'
				end
                if data["laststatus"] == 'chuachay'then
					laststatus = 'chuachay ❓❓❓'
				end
				if data["laststatus"] == 'thatbai'then
					laststatus = 'thatbai ❌❌❌'
				end
				laststatus = laststatus .. "--" .. data["lancuoi"] .. " "
                break
            end
        end
	end
	return laststatus
end

function fix_close_popup()
    --open screen
    keyDown(KEY_TYPE.HOME_BUTTON);
    keyUp(KEY_TYPE.HOME_BUTTON);
    usleep(1000000);
    keyDown(KEY_TYPE.HOME_BUTTON);
    keyUp(KEY_TYPE.HOME_BUTTON);
    usleep(1000000)
    openURL("http://ipv4.icanhazip.com")
	print('fix close popup')
    for i = 1, 4 do
        toast("Close các popup",1)
        sleep(1)
        checkimage("/var/mobile/Library/AutoTouch/Scripts/images/close.PNG","click close.png")
        sleep(2)
        checkimage("/var/mobile/Library/AutoTouch/Scripts/images/fix_capnhat1.PNG","fix_capnhat1.png")
        sleep(2)
    end
end


----WIFI SOCK----
function getMac()
	local udp = socket.udp()
    udp:setpeername("8.8.8.8", 80)  -- Set a known address to determine the local IP
    local ip = udp:getsockname()
    print("local ip: " .. ip)
    udp:close()
    local response = safeHttpRequest(apiRouter.."/api/v1/scan-mac")
    print("response mac scan: " .. response.."\n ********************************")
	if string.find(response,"404") then
		return nil
	else 
		local data = json.decode(response)
		for _, client in ipairs(data.clients) do
            --print(client.ip)
			if tostring(client.ip) == tostring(ip) then
                print('mac-address: '..client.ip)
				return client.mac
			end
		end
	end
	--nil neu khong tim thay mac
end

function setProxyWifiSock(string_proxy)
	print("Set Proxy"..string_proxy)
    local mac_address = getMac()
    if mac_address == "a8:a1:59:d7:40:79" then
        alert("bug MAC THANG \n \n \n \n \n CẢNH BÁO!!!!")
        stop()
    end
    if mac_address == "9c:6b:00:29:f0:fc" then
        alert("bug MAC HUY \n \n \n \n \n CẢNH BÁO!!!!")
        stop()
    end
    if mac_address == nil then 
        alert("Không thấy mac để set proxy")
        stop()
    end

    -- Dữ liệu cấu trúc
    local data = {
        mac_proxy = {
            [mac_address] = string_proxy
        }
    }
    -- Chuyển đổi dữ liệu thành chuỗi JSON
    local json_string = json.encode(data)
	print(json_string)
	local check = safeHttpRequestPost(apiRouter .. "/api/v1/assign-proxy",json_string)
	if check ~= nil then 
		if check == "{}" then
			return true
		else 
			return false
		end
	else
		return false
	end
end


function getProxy(typeProxy_getProxy)
	print("Lấy Proxy"..typeProxy_getProxy)
	if typeProxy_getProxy == "dcom" then
		local response = safeHttpRequest(mainApi.."/proxy/get?type="..typeProxy_getProxy.."&tenmay="..tenmay)
		data = json.decode(response)
		if data ~= nill then
			--check proxy
			if data['success'] == true then
				return data['proxy'],data['api_key']
			else
				print('hết proxy'..response)
				return nil,nil
			end
		end
	end
    if typeProxy_getProxy == "fastproxy" then
		local response = safeHttpRequest(mainApi.."/proxy/get?type="..typeProxy_getProxy.."&tenmay="..tenmay)
		data = json.decode(response)
		if data ~= nill then
			--check proxy
			if data['success'] == true then
				return data['proxy'],data['api_key']
			else
				print('hết proxy'..response)
				return nil,nil
			end
		end
	end
    if typeProxy_getProxy == "tmproxy" then
        local response = safeHttpRequest(mainApi.."/proxy/get?type="..typeProxy_getProxy.."&tenmay="..tenmay)
        print("res get proxy tm"..response)
        data = json.decode(response)
        if data ~= nill then
            --check proxy
            if data['success'] == true then
                key_tm_proxy = data['api_key']
                --change proxy
                local data = {
                    api_key =  key_tm_proxy,
                    id_location = 0
                }
                local json_string = json.encode(data)
                print("json_string change ip tm"..json_string)
                local res = safeHttpRequestPost("https://tmproxy.com/api/proxy/get-new-proxy",json_string)
                --get proxy
                local data = {
                    api_key =  key_tm_proxy
                }
                local json_string = json.encode(data)
                res = safeHttpRequestPost("https://tmproxy.com/api/proxy/get-current-proxy",json_string)
                print("res..get..ip..curent..tm"..res)
                --xuat proxy
                if res ~= nil then
                    data = json.decode(res)
                    kq = "socks5://"..data['data']['socks5']
                    return kq,key_tm_proxy
                end
            else
                print('hết proxy'..response)
                return nil,nil
            end
        end
    end
end

function cancelProxy(key_cancelProxy)
	print("Cancel proxy"..key_cancelProxy)
	local response = safeHttpRequest(mainApi.."/proxy/change_status?key="..key_cancelProxy)
	data = json.decode(response)
	if data ~= nil then 
		if data['success'] == true then
			print('cancel proxy thành công')
            print('remove proxy khỏi router')
            if setProxyWifiSock("socks5://1.1.1.1:80") == true then
                print('remove proxy khỏi router thành công!')
            end
			return true
		else
			print('lỗi cancel proxy'..response)
			return false
		end
	end
end


----END WIFI SOCK----


----TELEGRAM------------------------
function botTelegram(message)
    local res = safeHttpRequest("https://api.telegram.org/bot5724012576:AAGrpdq5CqQNBWn3kbeoTVV2gb2iCALd_mo/sendMessage?chat_id=-4562226107&text="..tenmay.." ==> "..message)
    if res ~= nil then
        log("send tele ok")
    else
        log("send tele fail")
        print("Send tele Fail!")
        stop()
    end
end

function checkMang(mess_buoc)
	check_co_mang = false
	for i = 1, 30 do
		local res = safeHttpRequest("https://ifconfig.me/ip")	
		if res ~= nil then
			if string.find(res,".") then
				print("có mạng"..res)
				check_co_mang = true
				break
			end
		else
			sleep(1,"Không có mạng")
		end
	end
    if check_co_mang == false then
        botTelegram("Không có mạng!"..mess_buoc)
    else
        botTelegram("Có mạng!"..mess_buoc)
    end
	return check_co_mang
end

----END TELEGRAM--------------------


--end lib otp sms uk
function reg_acc(phoneuk,iduk,tenmay,key_api_proxy_cancel)
    local api_key_proxy = key_api_proxy_cancel
    sn = getSN()
    local dataJson = '{"sn":"'..sn..'","iplocal":"'..getLocalIP()..'"}'
    local boolSend = false
    for i = 1,7,1 do
        check = postJson2(mainApi.."/serialtoiplocal",dataJson)
        if check == true then
            print("push ip to server thanh cong")
            boolSend = true
            break
        end
    end
    --khai bai & lay info
    local thanhcong = 0
    local thatbai = 0
	local lancuoi = ""
    local soluot = 0
    local sn = teniPhone
	local gioihan = gioihannay
	local space = tonumber(khoangcach)
	local q1 = ""
	local q2 = ""
	local q3 = ""
	local sogmaildadung = 0
	local loadloi = 0
    ::batdau::
    soluot = soluot + 1
    --1.changeip--
    appKill("com.apple.AppStore")
    toast("Servermail : "..servermail.." Quốc gia : "..country.." Mạng "..tostring(network),5)
    if changeinfo == 1 then
        toast("Change Info",2)
        changeUDID(duongdanappstore)
        sleep(5)
    end

    if wipesafari == 1 then
        toast("Wipe Safari",2)
        clearSafari(duongdansafari)
        sleep(5)
    end

    if xoainfo == 1 then
        toast("XoaInfo",2)
        openURL("XoaInfo://Reset")
        sleep(10)
    end

    --3.appstore--
    print('--debug1 open appstore 1')

    openURL("itms-apps://itunes.apple.com/apps")
    print('--debug2 open appstore 2')
    --Tắt các thông báo--

    for i=3, 1, -1 do--check close
        local result1 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/close.PNG", 0, 0.99, nil, false)
        if #result1 > 0 then
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/close.PNG","click close")
            sleep(1)
            break
        end
        sleep(1)
    end
    for i=3, 1, -1 do--click continue1
        local result1 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/continue1.PNG", 0, 0.99, nil, false)
        if #result1 > 0 then
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/continue1.PNG","click continue1")
            sleep(5)
            break
        end
        sleep(1)
    end
    for i=5, 1, -1 do
        --check retry
        local result2 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/retry.PNG", 0, 0.99, nil, false)
        if #result2 > 0 then
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/retry.PNG","click retry")
            sleep(5)
            break
        end
        --check ok
        local result3 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/ok1.PNG", 0, 0.99, nil, false)
        if #result3 > 0 then
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/ok1.PNG","click ok1")
            sleep(1)
            break
        end
        sleep(1)
    end
    print('--debug3 close cac thong bao')
    --End Tắt các thông báo--
    sleep(3)
    fixpupup()--fix popup
    for i=3, 1, -1 do--click continue1
        local result1 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/continue1.PNG", 0, 0.99, nil, false)
        if #result1 > 0 then
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/continue1.PNG","click continue1")
            sleep(5)
            break
        end
        sleep(1)
    end
    tap(673, 168)--click vào thằng người để tạo tài khoản
    sleep(3)
    tap(673, 168)--click vào thằng người để tạo tài khoản
    sleep(3)
    --logout-> click create new id apple
    local checklogout = findImage("/var/mobile/Library/AutoTouch/Scripts/images/signout.PNG", 0, 0.99, nil, false)
    if #checklogout > 0 then
        usleep(1500000)
        checkimage("/var/mobile/Library/AutoTouch/Scripts/images/signout.PNG","click signout")
        usleep(1000000)
    end
    sleep(5)
    tap(154, 1030)--click nút create new apple id
    --chờ load xong
    print('--debug4 cho load xong')
    local wait = waitImage("/var/mobile/Library/AutoTouch/Scripts/images/create.PNG",30,"create")
    if wait == true then
        toast("Load xong",1)
    else
        updateStatusIphone(tenmay,"Không load được create.png")
        botTelegram("Không load được create.png -> Check và reset máy")
        checkMang("bước load create.png")
        print('khong load duoc create.png -> bat dau cancel proxy')
        --kiem tra proxy 
        if cancelProxy(api_key_proxy) == false then
            botTelegram("Cancel proxy lỗi")
        end
        --
        sleep(60,'check và reset máy')
        --respring
        --botTelegram("Tiến hành respring")
        --io.popen("killall -9 SpringBoard")
        return nil
    end
    print('--debug5 pick country')
    --PICK COUNTRY
    if country == "us" then
        local checkus = findImage("/var/mobile/Library/AutoTouch/Scripts/images/us.PNG", 0, 0.99, nil, false)
        if #checkus == 0 then
            usleep(1000000)
            tap(247,616)
            sleep(3);
            swipeVertically()
            sleep(4)
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/usclick.PNG","click us")
            sleep(10,"Click us xong chờ 10s còn lại ")
            toast("Click Agree",1)
            tap(664,697)--click agree
            sleep(2)
        end
    end

    if country == "uk" then
        waitImage("/var/mobile/Library/AutoTouch/Scripts/images/uk.PNG",5,"uk")
        local checkus = findImage("/var/mobile/Library/AutoTouch/Scripts/images/uk.PNG", 0, 0.99, nil, false)
        if #checkus == 0 then
            usleep(1000000)
            tap(247,616)
            sleep(3);
            swipeVertically()
            sleep(4)
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/ukclick.PNG","click uk")
            sleep(10,"Click uk xong chờ 10s còn lại ")
            toast("Click Agree",1)
            tap(664,697)--click agree
            sleep(2)
        end
    end

    if country == "cn" then
        local checkcn = findImage("/var/mobile/Library/AutoTouch/Scripts/images/cn.PNG", 0, 0.99, nil, false)
        if #checkcn == 0 then
            usleep(1000000)
            tap(247,616)
            sleep(3);
            swipeVerticallyCN()
            sleep(2)
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/cnclick.PNG","click cn")
            sleep(10,"Click cn xong chờ 10s còn lại ")
            toast("Click Agree",1)
            tap(664,697)--click agree
            sleep(2)
        end
    end

    if country == "angola" then
        local checkcn = findImage("/var/mobile/Library/AutoTouch/Scripts/images/angola.PNG", 0, 0.99, nil, false)
        if #checkcn == 0 then
            usleep(1000000)
            tap(247,616)
            sleep(3)
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/angolaclick.PNG","click angola")
            sleep(10,"Click angola xong chờ 10s còn lại ")
            toast("Click Agree",1)
            tap(664,697)--click agree
            sleep(2)
        end
    end

    if country == "id card" then
        local checkcn = findImage("/var/mobile/Library/AutoTouch/Scripts/images/indo.PNG", 0, 0.99, nil, false)
        if #checkcn == 0 then
            usleep(1000000)
            tap(247,616)
            sleep(3);
            swipeVerticallyID()
            sleep(2)
            checkimage("/var/mobile/Library/AutoTouch/Scripts/images/indoclick.PNG","click indo")
            sleep(10,"Click indo xong chờ 10s còn lại ")
            toast("Click Agree",1)
            tap(664,697)--click agree
            sleep(2)
        end
    end

    --GET GMAIl
    local email = ""
    local order_id = ""
    local passhotmail = ""
    if servermail == "dichvugmail" then
        --dichvugmail
        toast("DICHVUGM",1)
        for i = 1, 30 do
            toast("Tiến hành lấy gmail lần " .. tostring(i),1)
            local response = http.request("https://dichvugmail.com/DataMail/Mail/leqVCoLkD1v6m7bWhK8k5l5qB6CbEVh0/Apple")
            sleep(1)
            if response ~= nil then
                print(response)
                if string.find(response,"@gmail.com") then
                    toast("Thấy gmail!",1)
                    local data = json.decode(response)
                    local gmail = data["orders"]["gmail"]
                    local status = data["orders"]["status"]
                    if status == "Cancel" then
                        toast("Gmail bị hủy chạy lượt mới!",1)
                        soluot = soluot + 1
                        updateStatusIphone(tenmay,"Gmail bi huy")
                        botTelegram("Gmail bị hủy")
                        print('gmail bi huy -> bat dau cancel proxy')
                        --kiem tra proxy 
                        if cancelProxy(api_key_proxy) == false then
                            botTelegram("Cancel proxy lỗi")
                        end
                        --
                        return nil
                    end
                    order_id = data["orders"]["order_id"]
                    toast("Gmail:"..gmail,1)
                    toast("Order ID:"..order_id,1)
                    email = gmail
                    print(gmail)
                    sogmaildadung = sogmaildadung + 1
                    break
                else
                    toast("Không có sẵn Gmail " .. tostring(i),1)
                    sleep(6)
                end
            end
        end

        if string.find(email,"@") then
            toast("Lấy mail thành công",1)
        else
            updateStatusIphone(tenmay,"Lấy mail không thành công")
            botTelegram("Lấy mail không thành công")
            print('lay mail khong thanh cong -> bat dau cancel proxy')
            --kiem tra proxy 
            if cancelProxy(api_key_proxy) == false then
                botTelegram("Cancel proxy lỗi")
            end
            --
            return nil
        end
    elseif servermail == "tay" then
        local emailInput = {type=CONTROLLER_TYPE.INPUT, title="Email:", key="Email", value=""}
        local okButton = {type=CONTROLLER_TYPE.BUTTON, title="OK", color=0x428BCA, flag=1, collectInputs=true}
        local controls = {emailInput, okButton}
        local orientations = { ORIENTATION_TYPE.PORTRAIT }
        local result = dialog(controls, orientations)
        if result == 1 then
            email = tostring(emailInput.value)
            print(email)
            usleep(2000000)
        end
    elseif  servermail == "gmailsuperteam" then
        --gmail superteam
        toast("SPT",1)
        for i = 1, 100 do
            toast("Tiến hành lấy gmail lần " .. tostring(i),1)
            local response = safeHttpRequest("http://api.sptmail.com/api/otp-services/gmail-otp-rental?apiKey=B0D9NHELVXM7M900&otpServiceCode=apple")
            sleep(1)
            if response ~= nil then
                print(response)
                if string.find(response,"không có sẵn") or string.find(response,"nhanh") then
                    toast("Không có sẵn Gmail " .. tostring(i),1)
                    sleep(3)
                end
                if string.find(response,"@gmail.com") then
                    toast("Thấy gmail!",1)
                    local data = json.decode(response)
                    local gmail = data["gmail"]
                    toast("Gmail:"..gmail,1)
                    email = gmail
                    print(gmail)
                    sogmaildadung = sogmaildadung + 1
                    break
                end
            end
        end

        if string.find(email,"@") then
            toast("Lấy mail thành công",1)
        else
            updateStatusIphone(tenmay,"Lấy mail không thành công")
            botTelegram("Lấy mail gmailsuperteam không thành công")
            print('lay mail gmailsuperteam khong thanh cong -> bat dau cancel proxy')
            --kiem tra proxy 
            if cancelProxy(api_key_proxy) == false then
                botTelegram("Cancel proxy lỗi")
            end
            --
            return nil
        end
    elseif  servermail == "gmail30min" then
        --gmail superteam
        toast("SPT",1)
        for i = 1, 100 do
            toast("Tiến hành lấy gmail lần " .. tostring(i),1)
            local response = safeHttpRequest("http://192.168.105.113:3000/api/getmail=apple")
            sleep(1)
            if response ~= nil then
                print(response)
                if string.find(response,"không có sẵn") or string.find(response,"nhanh") then
                    toast("Không có sẵn Gmail " .. tostring(i),1)
                    sleep(3)
                end
                if string.find(response,"@gmail.com") then
                    toast("Thấy gmail!",1)
                    local data = json.decode(response)
                    local gmail = data["gmail"]
                    toast("Gmail:"..gmail,1)
                    email = gmail
                    print(gmail)
                    sogmaildadung = sogmaildadung + 1
                    break
                end
            end
        end

        if string.find(email,"@") then
            toast("Lấy mail thành công",1)
        else
            updateStatusIphone(tenmay,"Lấy mail không thành công")
            botTelegram("Lấy mail gmailsuperteam không thành công")
            print('lay mail gmailsuperteam khong thanh cong -> bat dau cancel proxy')
            --kiem tra proxy 
            if cancelProxy(api_key_proxy) == false then
                botTelegram("Cancel proxy lỗi")
            end
            --      
            return nil
        end
    elseif servermail == "ggcode" then
        --ggcode
        toast("GGCODE",1)
        for i = 1, 100 do
            toast("Tiến hành lấy gmail lần " .. tostring(i),1)
            --local response = http.request("http://api2.ggcode.site/code/create_order?token=UFZkX7czRjIKYF7FFJtZUxR0x&service=apple")
            local response = safeHttpRequest("http://api2.ggcode.site/code/create_order?token=UFZkX7czRjIKYF7FFJtZUxR0x&service=apple")
            sleep(1)
            if response ~= nil then
                print(response)
                if string.find(response,"@gmail.com") then
                    toast("Thấy gmail!",1)
                    local data = json.decode(response)
                    local gmail = data["data"]["mail"]
                    order_id = data["data"]["order_id"]
                    toast("Gmail:"..gmail,1)
                    toast("Order ID:"..order_id,1)
                    email = gmail
                    print(gmail)
                    sogmaildadung = sogmaildadung + 1
                    break
                else
                    toast("Không có sẵn Gmail " .. tostring(i),1)
                    sleep(6)
                end
            else
                print("No mail")
            end
        end
        if string.find(email,"@") then
            toast("Lấy mail thành công",1)
        else
            updateStatusIphone(tenmay,"Lấy mail ggcode không thành công")
            botTelegram("Lấy mail ggcode không thành công")
            print('lay mail ggcode khong thanh cong -> bat dau cancel proxy')
            --kiem tra proxy 
            if cancelProxy(api_key_proxy) == false then
                botTelegram("Cancel proxy lỗi")
            end
            --
            return nil
        end
    elseif servermail == "dongvanfb" then
        for i = 1, 30 do
            toast("dongvanfb",1)
            local response = safeHttpRequest("https://api.dongvanfb.net/user/buy?apikey=gSpcRNWkvFcEKVGTtiR383cVu&account_type=1&quality=1&type=text")
            if response == nil then
                print("Không kết nối được đến server dongvanfb")
            else
                if string.find(response,"@") then 
                    print("Found mail => "..response)
                    local part1, part2 = string.match(response, "([^|]+)|([^|]+)")
                    email = part1
                    passhotmail = part2
                    break
                else
                    sleep(5,'chờ lấy mail dongvanfb')
                    usleep(1000000)
                end
            end
        end
        if string.find(email,"@") then
            toast("Lấy mail thành công",1)
        else
            updateStatusIphone(tenmay,"Lấy mail dongvanfb không thành công")
            botTelegram("Lấy mail dongvanfb không thành công")
            print('lay mail dongvanfb khong thanh cong -> bat dau cancel proxy')
            --kiem tra proxy 
            if cancelProxy(api_key_proxy) == false then
                botTelegram("Cancel proxy lỗi")
            end
            --
            return nil
        end
    else
        for i = 1, 120 do
            toast("HOTMAILBOX",1)
            local response, code, headers, status = http.request("https://api.hotmailbox.me/mail/buy?apikey=67600573d2cd4328b9ecf6d7f576045ea18ac6c983054becb2a61bc845b15663&mailcode=HOTMAIL&quantity=1")
            if code == 200 then
                local data = json.decode(response)

                if data and data.Data and data.Data.Emails and #data.Data.Emails > 0 then
                    email = data.Data.Emails[1].Email
                    passhotmail = data.Data.Emails[1].Password
                    sogmaildadung = sogmaildadung + 1
                    break
                end
            end
            sleep(2)
        end
    end
    local births = birthday()
    local ngaysinh = births:sub(1, 2) .. "/" .. births:sub(3, 4) .. "/" .. births:sub(5)
    local ngaysinh2 = births:sub(5).."-"..births:sub(1, 2).."-"..births:sub(3, 4)
    local ngaysinhcn = births:sub(5) .. births:sub(1, 2) .. births:sub(3, 4)  --year--month--day
    local ngaysinhangola = births:sub(3, 4).. births:sub(1, 2)..births:sub(5)  --day--month--year
    local ngaysinhuk = births:sub(3, 4).. births:sub(1, 2)..births:sub(5)  --day--month--year
    local infos = info()
    local pass = randomPassword()
    --check agre again
    local a = getColors({{644,680}})
    if a[1] == 5036388 then
        toast("Đã agree",1)
    else
        toast("Click agree",1)
        tap(664,697)--click agree
        sleep(2)
    end
    sleep(5)
    tap(288, 238)
    sleep(1)
    tap(288, 238)
    sleep(1)
    tap(288, 238)
    sleep(1)
    inputText(email)
    sleep(1)

    tap(283, 322)
    sleep(1)
    inputText(pass)
    sleep(1)

    tap(292, 419)
    sleep(1)
    inputText(pass)
    sleep(2)

    tap(673, 86)--click next
    sleep(5)
    --chờ load xong đến firstname, last name
    local wait = waitImage("/var/mobile/Library/AutoTouch/Scripts/images/loadfirstname.PNG",100,"loadfirstname")
    if wait == true then
        toast("Load xong",1)
    else
        soluot = soluot + 1
        updateStatusIphone(tenmay,"Fail to load firstname")
        checkMang("bước check load firstname")
        botTelegram("Lỗi load firstname sau bước nhập email")
        print('khong load duoc first name -> bat dau cancel proxy')
        --kiem tra proxy 
        if cancelProxy(api_key_proxy) == false then
            botTelegram("Cancel proxy lỗi")
        end
        --
        return nil
    end
    --
    tap(286,266);
    usleep(1000000)
    tap(286,266);
    usleep(1000000)
    tap(286,266);
    usleep(1000000)
    toast("Random first last name",1)
    usleep(1000000)
    --firstname; lastname
    local input = randomFL()
    --xu ly firstname, lastname tu email
    -- Tách phần username (thangbg1994) từ email
    local username = string.match(email, "([^@]+)")
    -- Tách 5 ký tự đầu tiên là firstname
    local fn = string.sub(username, 1, 5)
    -- Tách phần lastname (loại bỏ số nếu có) từ phần còn lại của username
    local remaining = string.sub(username, 6)
    local ln = string.gsub(remaining, "%d", "") -- Loại bỏ số trong lastname
    if #ln < 4 then
        ln = input[2]
    end
    inputText(fn)
    usleep(1000000)
    tap(300,350)
    usleep(1000000)
    inputText(ln)
    usleep(1000000)

    tap(295,434)
    usleep(1000000)
    if country == "us" then
        inputText(births)
    end
    if country == "uk" then
        inputText(ngaysinhuk)
    end
    if country == "cn" then
        inputText(ngaysinhcn)
    end
    if country == "angola" then
        inputText(ngaysinhangola)
    end
    if country == "id card" then
        inputText(ngaysinhangola)
    end
    usleep(1000000)

    tap(362,643)
    sleep(2)
    tap(664,292)--chon cau q1
    sleep(2)
    --
    tap(370,747)
    usleep(1000000)
    q1= generateRandomAnswer()
    inputText(q1)
    usleep(1000000)

    tap(287,603)
    sleep(2)
    tap(295,232)--chon cau q2
    sleep(2)

    tap(321,957)
    usleep(1000000)
    for i = 1, 50 do
        q2 = generateRandomAnswer()
        if q2 == q1 then
            q2 = generateRandomAnswer()
        else
            break
        end
    end
    inputText(q2)
    usleep(1000000)

    tap(287,605)
    sleep(2)
    tap(334,237)--chon cau q3
    sleep(2)

    tap(324,1186)
    usleep(1000000)
    for i = 1, 50 do
        q3 = generateRandomAnswer()
        if q3 == q1 or q3 == q2 then
            q3 = generateRandomAnswer()
        else
            break
        end
    end
    inputText(q3)
    usleep(1000000)

    tap(673, 86)--click next
    sleep(3)
    --chờ load xong
    local wait = waitImage("/var/mobile/Library/AutoTouch/Scripts/images/loadpayment.PNG",120,"loadpayment")
    if wait == true then
        toast("Load xong",1)
    else
        soluot = soluot + 1
        updateStatusIphone(tenmay,"Failed to load payment")
        checkMang("bước load payment")
        botTelegram("Lỗi load payment sau bước nhập first name")
        print('khong load duoc payment -> bat dau cancel proxy')
        --kiem tra proxy 
        if cancelProxy(api_key_proxy) == false then
            botTelegram("Cancel proxy lỗi")
        end
        --
        return nil
    end

    --BILL US
    if country == "us" then
        --selection 3
        toast('click none',1)
        tap(382,507)
        sleep(1)
        toast('click street',1)
        tap(370,1016)
        sleep(1)
        --inputText(infos[4])
        inputText(randomStreet2())
        sleep(1)

        tap(278,604)
        sleep(1)
        inputText(infos[2])
        sleep(1)

        tap(278,604)
        sleep(1)
        inputText(infos[1])
        sleep(1)

        tap(278,604)
        sleep(1)
        inputText(infos[5])
        sleep(1)
        tap(679,860)
        sleep(1)

        tap(401,636)
        sleep(1)
        swipe(infos[3])
        sleep(1)
        tap(678,864)
        sleep(1)
    end

    if country == "uk" then
        --selection 3
        toast('click mobile phone',1)
        tap(141, 484)
        sleep(1)
        toast('click phone number',1)
        tap(217, 742)
        sleep(1)
        inputText(phoneuk)--input phone number
        sleep(10)
        tap(673, 86)--click next
    end


    if country == "uk" then
        sleep(10)
        --tap to code
        tap(364, 407)
        sleep(1)
        codeuk = "3241"
        sleep(1)
        inputText(codeuk)
        sleep(3)
        tap(673, 86)--click next
        sleep(5)
    end

    --uk step 3

    if country == "uk" then
        sleep(10)
        tap(369, 785)--tap ok
        sleep(2)
        tap(75, 85)--tap cancel
        sleep(3)
        tap(82, 575)--tap none
        sleep(3)

        --vuot xuong cuoi
        for i = 1,2,1 do
            touchDown(1, 200, 300);
            for i = 900,300,-100 do
                usleep(12000);
                touchMove(1, 200, i);
            end
            touchUp(1, 200, 900);
            usleep(500000);
        end
        --end vuot xuong cuoi
        sleep(3)
        tap(337, 283)--click street
        sleep(3)
        inputText(randomStreet2())
        sleep(3)
        tap(360, 678)--tap postcode
        sleep(3)
        inputText("aa8 8aa")
        sleep(3)
        tap(312, 520)--tap town
        sleep(1)
        inputText("London")
        sleep(1)
        tap(313, 522)--tap country
        sleep(1)
        inputText("Scotland")
        sleep(1)
        tap(300, 610)--tap phone
        sleep(1)
        inputText(phoneuk)
        sleep(1)
    end



    --BILL ID CARD
    if country == "id card" then
        --selection 3
        local infos = infoID()--export (1|City|Zipcode|Address|Phone)
        local card = getcard()
        toast('click card number',1)
        tap(366,801)
        sleep(1)
        inputText(card[1])--dien number tu nhay sang mm
        sleep(6)
        tap(313,557)--click mm
        sleep(2)
        inputText(card[2])--dien mm
        sleep(3)
        inputText(card[3])--dien yyy
        sleep(3)
        tap(373,570)--click ccv -ok
        sleep(2)
        inputText(card[4])
        sleep(2)
        tap(695,854)--click done - ok
        sleep(1)
        tap(361,992)--click street - ok
        sleep(1)
        inputText(infos[4])
        sleep(1)
        tap(346,607)--click city - ok
        sleep(1)
        inputText(infos[2])
        sleep(1)
        tap(344,513)--click provine - ok
        sleep(1)
        if infos[1] == "1" then
            swipe(1)
        end
        if infos[1] == "2" then
            swipe(2)
        end
        tap(677,859)--click done -ok
        sleep(1)
        tap(353,734)--click postcode-ok
        sleep(1)
        inputText(infos[3])
        sleep(1)
        tap(326,601)--click are phone - ok
        sleep(1)
        inputText("770")
        sleep(1)
        tap(493,470)--click phone number - ok
        sleep(1)
        inputText(infos[5])
        sleep(1)
        tap(678,864)
        sleep(1)
    end

    -- BILL CN
    if country == "cn" then
        --random bill street
        local infos = infoCN()--export (1|Bengbu|Anhui|233000|street|phone)
        --selection 3
        toast('click none',1)
        tap(102,691)
        sleep(1)
        toast('click street',1)
        tap(384,1213)
        sleep(1)
        inputText(infos[5])--dien street
        sleep(1)

        tap(356,703)--click postcode
        sleep(1)
        inputText(infos[4])--dien post code
        sleep(1)

        tap(373,524)--click region
        sleep(1)
        inputText(infos[2])--dien
        sleep(1)

        tap(384,690)--click phone
        sleep(1)
        inputText(infos[6])--dien phone 10 so
        sleep(2)

        tap(359,293)--click district
        sleep(1)
        if infos[1] == "1" then
            swipe(1)
        end
        if infos[1] == "2" then
            swipe(2)
        end
        sleep(1)
        tap(678,864)
        sleep(1)
    end

    -- BILL Angola
    if country == "angola" then
        --random bill street
        local infos = infoAngola()--export (1|Bengbu|Anhui|233000|street|phone)
        --selection 3
        toast('click none',1)
        tap(398,422)
        sleep(1)
        toast('click street',1)
        tap(416,941)--click street
        sleep(1)
        inputText(infos[5])--dien street
        sleep(1)

        tap(353,609)--click city/town
        sleep(1)
        inputText(infos[2])--dien city
        sleep(1)

        tap(381,698)--click phone
        sleep(1)
        inputText(infos[6])--dien phone 10 so
        sleep(2)

        tap(363,290)--click country
        sleep(1)
        if infos[1] == "1" then
            swipe(1)
        end
        if infos[1] == "2" then
            swipe(2)
        end
        sleep(1)
        tap(678,864)
        sleep(1)
    end

    tap(673, 86)--click next
    sleep(3)
    --chờ load xong
    local wait = waitImage("/var/mobile/Library/AutoTouch/Scripts/images/loadcode.PNG",60,"loadcode")
    if wait == true then
        toast("Load xong",1)
    else
        soluot = soluot + 1
        updateStatusIphone(tenmay,"failed to load loadcode")
        checkMang("bước loadcode")
        botTelegram("Lỗi bước nhập code OTP")
        print('khong load duoc loadcode -> bat dau cancel proxy')
        --kiem tra proxy 
        if cancelProxy(api_key_proxy) == false then
            botTelegram("Cancel proxy lỗi")
        end
        --  
        return nil
    end

    --get OTP
    local otp = "0"

    if servermail == "dichvugmail" then
        --dichvugmail
        for i = 1, 200 do
            toast("Chờ OTP giây thứ " .. i * 5,1)
            local url = "https://dichvugmail.com/DataMail/Mail/leqVCoLkD1v6m7bWhK8k5l5qB6CbEVh0/" .. tostring(order_id)
            local response = http.request(url)
            if response ~= nil then
                print(response)
                local data = json.decode(response)
                local status = data["orders"]["status"]
                if (status == "OK") then
                    otp = data["orders"]["otp"]
                    print(otp)
                    toast("OTP đã về "..otp,1)
                    break
                end
                if (status == "Cancel") then
                    toast("Gmail đã hủy, sang phiên mới",1)
                    soluot = soluot + 1
                    updateStatusIphone(tenmay,"gmail bi huy")
                    botTelegram("Gmail bị hủy")
                    print('gmail bi huy -> bat dau cancel proxy')
                    --kiem tra proxy 
                    if cancelProxy(api_key_proxy) == false then
                        botTelegram("Cancel proxy lỗi")
                    end
                    --
                    return nil
                end
            end
            sleep(5)
        end
    elseif servermail == "tay" then
        local emailInput = {type=CONTROLLER_TYPE.INPUT, title="Email:", key="Email", value=""}
        local okButton = {type=CONTROLLER_TYPE.BUTTON, title="OK", color=0x428BCA, flag=1, collectInputs=true}
        local controls = {emailInput, okButton}
        local orientations = { ORIENTATION_TYPE.PORTRAIT }
        local result = dialog(controls, orientations)
        if result == 1 then
            otp = tostring(emailInput.value)
            print("OTP  "..otp)
            usleep(2000000)
        end
    elseif servermail == "ggcode" then
        --ggcode
        for i = 1, 30 do
            toast("Chờ OTP giây thứ " .. i * 5,1)
            local url = "http://api2.ggcode.site/code/check?token=UFZkX7czRjIKYF7FFJtZUxR0x&order_id=" .. tostring(order_id)
            --local response = http.request(url)
            local response = safeHttpRequest(url)
            if response ~= nil then
                print(response)
                if string.find(response,"finish") then
                    local data = json.decode(response)
                    otp = data["data"]["code"]
                    print(otp)
                    toast("OTP đã về "..otp,1)
                    break
                end
                if string.find(response,"cancel") then
                    toast("Gmail đã hủy, sang phiên mới",1)
                    soluot = soluot + 1
                    updateStatusIphone(tenmay,"gmail bi huy")
                    botTelegram("Gmail bị hủy")
                    print('gmail bi huy -> bat dau cancel proxy')
                    --kiem tra proxy 
                    if cancelProxy(api_key_proxy) == false then
                        botTelegram("Cancel proxy lỗi")
                    end
                    --
                    return nil
                end
                if string.find(response,"mail_die") then
                    toast("Gmail đã hủy, sang phiên mới",1)
                    soluot = soluot + 1
                    updateStatusIphone(tenmay,"mail_die")
                    botTelegram("Gmail bị die")
                    print('mail_die -> bat dau cancel proxy')
                    --kiem tra proxy 
                    if cancelProxy(api_key_proxy) == false then
                        botTelegram("Cancel proxy lỗi")
                    end
                    --
                    return nil
                end
            end
            sleep(5)
        end
    elseif servermail == "gmailsuperteam" then
        --gmail superteam
        for i = 1, 30 do

            toast("Chờ OTP giây thứ " .. i * 5,1)
            local url = "http://api.sptmail.com/api/otp-services/gmail-otp-lookup?apiKey=B0D9NHELVXM7M900&otpServiceCode=apple&gmail=" .. tostring(email)
            --local response, status = http.request(url)
            local response = safeHttpRequest(url)
            local data = json.decode(response)
            local status = data["status"]
            -- Kiểm tra status
            if status == "REFUNT" then
                otp = "0"
                print("Gmail đã bị hủy. Sang lượt reg mới...")
                soluot = soluot + 1
                updateStatusIphone(tenmay,"gmail bi huy")
                botTelegram("Gmail bị hủy")
                print('gmail bi huy -> bat dau cancel proxy')
                --kiem tra proxy 
                if cancelProxy(api_key_proxy) == false then
                    botTelegram("Cancel proxy lỗi")
                end
                --
                return nil
            end

            if status == "SUCCESS" then
                checkotp = true
                otp = data["otp"]
                print("OTP đã về:"..otp)
                break
            end

            sleep(5)
        end
    elseif servermail == "gmail30min" then
        --gmail superteam
        for i = 1, 30 do

            toast("Chờ OTP giây thứ " .. i * 5,1)
            local url = "http://192.168.105.113:3000/api/getotp="..tostring(email).."&service=apple"
            --local response, status = http.request(url)
            local response = safeHttpRequest(url)
            local data = json.decode(response)
            local status = data["status"]
            -- Kiểm tra status
            if status == "REFUNT" then
                otp = "0"
                print("Gmail đã bị hủy. Sang lượt reg mới...")
                soluot = soluot + 1
                updateStatusIphone(tenmay,"gmail bi huy")
                botTelegram("Gmail bị hủy")
                print('gmail bi huy -> bat dau cancel proxy')
                --kiem tra proxy 
                if cancelProxy(api_key_proxy) == false then
                    botTelegram("Cancel proxy lỗi")
                end
                --
                return nil
            end

            if status == "SUCCESS" then
                checkotp = true
                otp = data["otp"]
                print("OTP đã về:"..otp)
                break
            end

            sleep(5)
        end
    elseif servermail == "dongvanfb" then
        --gmail superteam
        for i = 1, 50 do
            toast("Chờ OTP giây thứ " .. i * 5,1)
            local url = "https://tools.dongvanfb.net/api/get_code?mail="..tostring(email).."&pass="..tostring(passhotmail).."&type=apple"
            local response = safeHttpRequest(url)
            if response ~= nil then
                local data = json.decode(response)
                otp = data['code']
                if otp == nil or otp == "" then
                    toast("chưa về otp hotmail",1)
                end
                if otp ~= nil then
                    check_convert_otp = tonumber(otp)
                    if check_convert_otp ~= nil and check_convert_otp > 0 then
                        print("OTP đã về:"..otp)
                        break
                    end
                end
                
                --check die mail
                if string.find(response,"failed") then
                    print("Hotmail die")
                    print("otp hotmail res..."..response)
                    soluot = soluot + 1
                    updateStatusIphone(tenmay,"Hotmail die")
                    botTelegram("Hotmail die")
                    print('Hotmail die -> bat dau cancel proxy')
                    --kiem tra proxy 
                    if cancelProxy(api_key_proxy) == false then
                        botTelegram("Cancel proxy lỗi")
                    end
                    --
                    return nil
                end
            end
            sleep(5)
        end
    else
        otp = getCode2(email,passhotmail)
    end

    check_thanhcong_otp = tonumber(otp)

    if check_thanhcong_otp > 0 then
        print('debug 3: lay otp thanh cong')
        toast("Lay OTP thanh cong",1)
    else
        toast("Khong ve code",1)
        print("Khong ve code")
        soluot = soluot + 1
        updateStatusIphone(tenmay,"khong ve code")
        botTelegram("Không về code")
        print('khong ve code -> bat dau cancel proxy')
        --kiem tra proxy 
        if cancelProxy(api_key_proxy) == false then
            botTelegram("Cancel proxy lỗi")
        end
        --
        return nil
    end
    usleep(1000000)
    inputText(otp)
    usleep(1000000)
    tap(652, 86)
    sleep(5)
    tap(652, 86)
    sleep(12,"Chờ tạo ID")
    --change card
    ::checkcc::
    local check = findanh()
    if check == "continu" then
        usleep(1000000)
        --push data ve server
        local dataJson = '{"email":"'..email..'","password":"'..pass..'","dob":"'..ngaysinhcn..'","question":"'..'firstname:'..q1..'-'..'job:'..q2..'-'..'city:'..q3..'","country":"'..country..'","ip":"","status":"new","miner":"thanghoang"}'
        --Luu_Data_File("apple.txt",dataJson,"a")--save file

        local boolSend = false
        for i = 1,7,1 do
            check = postJson2(mainApi .. '/addid',dataJson)
            if check == true then
                boolSend = true
                break
            end
        end
        if boolSend == true then
            print("DONE!!--Hoàn thành reg")
        else
            alert("Không gửi được ID về Server!!")
            stop()
        end

        -- end push data
        usleep(1000000)
        tap(376,1280)
        usleep(5000000)
        --fix logout
        local popup1 = findImage("/var/mobile/Library/AutoTouch/Scripts/images/popup1.PNG", 0, 0.99, nil, false)
        if #popup1 > 0 then
            usleep(1000000)
            tap(374,1196)
            usleep(2000000)
            for i=4, 1, -1 do
                usleep(1000000)
                toast(i, 1)
                if getColor(673, 168)==31487 then
                    toast("click avarta")
                    usleep(2000000)
                    tap(673, 168)
                    usleep(2000000)
                    checkimage("/var/mobile/Library/AutoTouch/Scripts/images/signout.PNG","click signout")
                    sleep(5)
                    break
                end
            end
        else
            for i=4, 1, -1 do
                usleep(1000000)
                toast(i, 1)
                if getColor(673, 168)==31487 then
                    toast("click avarta")
                    usleep(2000000)
                    tap(673, 168)
                    usleep(2000000)
                    checkimage("/var/mobile/Library/AutoTouch/Scripts/images/signout.PNG","click signout")
                    sleep(5)
                    break
                end
            end
        end
        return true
    elseif check == "support" then
        return false
    end
end

phoneuk = "7460465890"
idphone = "18047450"
ip = "direct"


function main()
    --setProxyWifiSock("socks5://1.1.1.1:80")--set proxy singapore
    --tenmay = ""
    sn = getSN()
    local response = safeHttpRequest(mainApi.."/infoiphone?sn="..sn)
    local data = json.decode(response)
    if data ~= nil then 
        if data['success'] == true then
            iplocal_vietsoft = data['iplocal']
            sn_vietsoft = data['sn']
            --tenmay = data['name']
        end
    else 
        alert("Không kết nối được vietsoft.pro")
        stop()
    end

	for i = 1, 1000 do
        fix_close_popup()
		::buoc1::
        --check run all - true -> stop auto, false -> run auto
        local checkRunAll = getStatusAll(mainApi)
        if checkRunAll == true then
            print("--Stop All Từ Server--")
            stop()
        end

        if checkRunAll == nil then
            sleep(2,"🔥🔥🔥 Không kết nối được Server check 🔥🔥🔥")
            goto buoc1
        end

    	-- check xem máy này có chạy tiếp không
    	local check = getStatusRun(mainApi, tenmay)
    	if check == false then
			local laststatus = getInforMay(tenmay)
        	sleep(60," *** Kết quản chạy lần cuối: ".. laststatus .. "\n \n ***Đang chờ lượt reg tiếp theo ")
			goto buoc1
    	end
        --lay proxy
        if typeProxy == 'dcom' then
            -- lấy proxy
            get_new_proxy, api_key_proxy = getProxy('dcom')
            if get_new_proxy ==  nil then
                sleep(60,"Đang chờ lấy proxy ")
                goto buoc1
            end
            print('key proxy '..tenmay..' => '..api_key_proxy)
            --change apple id 
            sleep(2,"Set proxy Singapore để change Apple ID")
            print("Set proxy Singapore để change Apple ID")
            setProxyWifiSock("socks5://winmodern:Anhem1994%23%23@66.42.60.103:6969")--set proxy singapore
            changeAppleID()
            print("Change Apple ID Xong")
            sleep(1,"Change Apple ID Xong")

            --Cập nhật proxy trên router
            if setProxyWifiSock(get_new_proxy) == false then
                --kiem tra proxy 
                if cancelProxy(api_key_proxy) == false then
                    botTelegram("Cancel proxy lỗi")
                end
                --
                goto buoc1
            end
            sleep(15,"Đợi 1 lúc sau khi add Proxy")
        end

        if typeProxy == 'fastproxy' then
            -- lấy proxy
            get_new_proxy, api_key_proxy = getProxy('fastproxy')
            if get_new_proxy ==  nil then
                sleep(60,"Đang chờ lấy proxy ")
                goto buoc1
            end
            print('key proxy '..tenmay..' => '..api_key_proxy)
            --change apple id 
            sleep(2,"Set proxy Singapore để change Apple ID")
            print("Set proxy Singapore để change Apple ID")
            setProxyWifiSock("socks5://winmodern:Anhem1994%23%23@66.42.60.103:6969")--set proxy singapore
            changeAppleID()
            print("Change Apple ID Xong")
            sleep(1,"Change Apple ID Xong")

            --Cập nhật proxy trên router
            if setProxyWifiSock(get_new_proxy) == false then
                --kiem tra proxy 
                if cancelProxy(api_key_proxy) == false then
                    botTelegram("Cancel proxy lỗi")
                end
                --
                goto buoc1
            end
            sleep(15,"Đợi 1 lúc sau khi add Proxy")
        end

        if typeProxy == 'tmproxy' then
            -- lấy proxy
            get_new_proxy, api_key_proxy = getProxy('tmproxy')
            if get_new_proxy ==  nil then
                sleep(60,"Đang chờ lấy proxy ")
                goto buoc1
            end
            print('key proxy '..tenmay..' => '..api_key_proxy)
            --change apple id 
            sleep(2,"Set proxy Singapore để change Apple ID")
            print("Set proxy Singapore để change Apple ID")
            setProxyWifiSock("socks5://winmodern:Anhem1994%23%23@66.42.60.103:6969")--set proxy singapore
            changeAppleID()
            print("Change Apple ID Xong")
            sleep(1,"Change Apple ID Xong")

            --Cập nhật proxy trên router
            if setProxyWifiSock(get_new_proxy) == false then
                --kiem tra proxy 
                if cancelProxy(api_key_proxy) == false then
                    botTelegram("Cancel proxy lỗi")
                end
                --
                goto buoc1
            end
            sleep(15,"Đợi 1 lúc sau khi add Proxy")
        end
    	kq = reg_acc(tostring(phoneuk),tostring(idphone),tenmay,api_key_proxy)
    	--update ve server
    	local data_updatemay = {}
    	-- Thêm các giá trị key-value vào bảng
    	data_updatemay["tenmay"] = tenmay
    	data_updatemay["miner"] = nguoiMiner
    	data_updatemay["laststatus"] = "new"
        if kq == true then
            data_updatemay["laststatus"] = "thanhcong"
        end
        if kq == false then
            data_updatemay["laststatus"] = "thatbai"
        end
    	local json_updatemay = json.encode(data_updatemay)
    	print(json_updatemay)
    	check = postJson(mainApi .. '/updatemay',json_updatemay)
    	if check == True then
        	usleep(100)
    	else
        	alert("Loi gui server")
        	stop();
    	end
	end
end

main()