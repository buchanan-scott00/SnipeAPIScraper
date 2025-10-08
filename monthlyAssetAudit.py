import pandas as pd
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SNIPE_URL = "###YOUR SNIPE LINK HERE###"
API_TOKEN = "###YOUR API TOKEN HERE###"
INPUT_FILE = "users.xlsx"
OUTPUT_FILE = "user_assets_report.xlsx"

#Request Header
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def get_user_by_username(username):
    #Fairly self explanatory
    url = f"{SNIPE_URL}/users"
    params = {"search": username}
    r = requests.get(url, headers=HEADERS, params=params, verify=False)
    data = r.json()

    # Return None if no users found
    if data.get("total", 0) == 0:
        return None

    # Find match on Username
    for user in data["rows"]:
        if user.get("username", "").lower() == username.lower():
            return user

    # If no exact match found, just return first match as fallback
    return data["rows"][0]


def get_user_assets(user_id):
    #Get users assets and model types
    url = f"{SNIPE_URL}/users/{user_id}/assets"
    r = requests.get(url, headers=HEADERS, verify=False)
    data = r.json()

    if "rows" not in data or not data["rows"]:
        return []

    # Returns asset name and model, can expand to pull more but at that point just look at Snipe itself
    assets_list = []
    for asset in data["rows"]:
        asset_name = asset.get("name", "Unknown Asset")
        model_name = asset.get("model", {}).get("name", "Unknown Model")
        assets_list.append(f"{asset_name} ({model_name})")
    
    return assets_list

def main():
    # Read Excel (assuming first column is username)
    df = pd.read_excel(INPUT_FILE)
    usernames = df.iloc[:10, 0].tolist()  # first 10 names

    results = []

    for username in usernames:
        user = get_user_by_username(username)

        if not user:
            results.append({
                "Username": username,
                "Result": "User not found"
            })
            continue  # Skip to next username

        assets = get_user_assets(user["id"])
    
        if not assets:
            #Wanted to make this output the standard email for has assets/no assets but trying to get it to do tables was annoying, keep a blank draft version handy to copy/paste
            result_text = "No assets assigned"
        else:
            result_text = "Assigned assets: " + ", ".join(assets)

        results.append({
            "Username": username,
            "Result": result_text
        })


    # Export to Excel
    out_df = pd.DataFrame(results)
    out_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()


