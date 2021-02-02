
__all__ = [
    "HEADERS_INSTRUCTIONS",
    "ID_INSTRUCTIONS",
]

HEADERS_INSTRUCTIONS = """
Copy authentication headers
To run authenticated requests you need to set up you need to copy your request headers from a POST request in your browser. To do so, follow these steps:

Open a new tab
Open the developer tools (Ctrl-Shift-I) and select the “Network” tab
Go to https://music.youtube.com and ensure you are logged in
Find an authenticated POST request. The simplest way is to filter by /browse using the search bar
Firefox
Verify that the request looks like this: Status 200, Method POST, Domain music.youtube.com, File browse?...
Copy the request headers (right click > copy > copy request headers)
Chromium (Chrome/Edge)
Verify that the request looks like this: Status 200, Type xhr, Name browse?...
Click on the Name of any matching request. In the “Headers” tab, scroll to the section “Request headers” and copy everything starting from “accept: */*” to the end of the section
"""

ID_INSTRUCTIONS = """
1) Visit https://myaccount.google.com/brandaccounts.
2) Choose your account
3) You will be redirected to URL "https://myaccount.google.com/brandaccounts/<YOUR_ID>/view". Copy the ID and post it here as a result
"""
