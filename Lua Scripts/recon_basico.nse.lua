local http = require "http"
local shortport = require "shortport"
local stdnse = require "stdnse"

-- Script Metadata
description = [[
Basic information gathering script to:
1. Retrieve the HTML page title.
2. Identify the Server software (Banner grabbing).
3. Check for the existence of the robots.txt file.
]]

author = "Luclino Cruz"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"discovery", "safe"}

-- Port rule: Runs on ports commonly used for HTTP (80, 443, 8080, etc.)
portrule = shortport.http

-- Main execution action
action = function(host, port)
  local result = {}
  
  -- 1. Attempt to fetch the content from the root directory (/)
  local response = http.get(host, port, "/")
  
  if response and response.status == 200 then
    -- Extract the Page Title
    local title = string.match(response.body, "<title>(.-)</title>")
    if title then
      table.insert(result, "Title: " .. title)
    end
    
    -- Extract the Server Header
    if response.header and response.header.server then
      table.insert(result, "Server: " .. response.header.server)
    end
  end

  -- 2. Check for Robots.txt
  local robots_res = http.get(host, port, "/robots.txt")
  if robots_res and robots_res.status == 200 then
    table.insert(result, "Robots.txt: Found (may contain hidden paths)")
  else
    table.insert(result, "Robots.txt: Not found")
  end

  -- Format the output for the Nmap report
  if #result > 0 then
    return stdnse.format_output(true, result)
  end
end