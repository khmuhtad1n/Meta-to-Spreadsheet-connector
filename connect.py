import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

def load_environment_variables() -> Dict[str, Any]:
    """Load and return environment variables from .env file."""
    load_dotenv()
    return {
        'access_token': os.getenv('META_ACCESS_TOKEN'),
        'ad_account_ids': [os.getenv(acc) for acc in ['THC', 'LM'] if os.getenv(acc)],
        'spreadsheet_name': os.getenv('SPREADSHEET_NAME'),
        'credentials_file': os.getenv('CREDENTIALS_FILE')
    }

def test_api_connection(access_token: str, ad_account_id: str) -> bool:
    """Test the connection to the Meta API for a given ad account."""
    url = f"https://graph.facebook.com/v20.0/{ad_account_id}"
    params = {'access_token': access_token, 'fields': 'account_id'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print(f"API connection successful for account {ad_account_id}:", json.dumps(response.json(), indent=2))
        return True
    else:
        error_data = response.json().get('error', {})
        error_message = error_data.get('message', 'Unknown error')
        error_type = error_data.get('type', 'Unknown type')
        error_code = error_data.get('code', 'Unknown code')
        print(f"Failed to connect to API for account {ad_account_id}:")
        print(f"Error message: {error_message}")
        print(f"Error type: {error_type}")
        print(f"Error code: {error_code}")
        return False

def fetch_ads_performance_data(access_token: str, ad_account_id: str) -> List[Dict[str, Any]]:
    """Fetch the ads performance data for a given ad account from Meta API."""
    url = f'https://graph.facebook.com/v20.0/{ad_account_id}/insights'
    params = {
        'access_token': access_token,
        'level': 'campaign',
        'date_preset': 'yesterday',
        'fields': 'campaign_name,account_name,account_id,impressions,spend,cpm,clicks,cpc,ctr,reach'
    }
    response = requests.get(url, params=params)
    
    if response.ok:
        return response.json().get('data', [])
    else:
        print(f"Failed to fetch ads performance for account {ad_account_id}: {response.json()}")
        return []

def get_yesterday_date() -> str:
    """Return yesterday's date in GMT+7 timezone."""
    current_datetime = datetime.utcnow() + timedelta(hours=7)
    return (current_datetime - timedelta(days=1)).strftime('%Y-%m-%d')

def initialize_google_sheets(credentials_file: str, spreadsheet_name: str) -> gspread.Worksheet:
    """Initialize the Google Sheets API and return the worksheet."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).worksheet('adsreport')
    
    # Add header row if it does not exist
    if not sheet.row_values(1):
        header = ["Date", "Brand", "Campaign Name", "Account ID", "Account Name", "Impressions", "Spend", "CPM", "Clicks", "CPC", "CTR", "Reach"]
        sheet.append_row(header)
    
    return sheet

def process_data_item(data_item: Dict[str, Any], ad_account_id: str, yesterday: str) -> List[Any]:
    """Process and return a single row of data to be inserted into Google Sheets."""
    campaign_name = data_item.get('campaign_name', 'Unknown Campaign')
    account_name = data_item.get('account_name', 'Unknown Account')
    
    # Determine brand logic
    brand = account_name  # Default brand to account name
    if ad_account_id == os.getenv('TAFF'):
        brand = "TaffOmicron" if "omi - " in campaign_name else account_name
    
    return [
        yesterday,
        brand,
        campaign_name,
        data_item.get('account_id', ''),
        account_name,
        int(data_item.get('impressions', 0)),
        float(data_item.get('spend', 0)),
        float(data_item.get('cpm', 0)),
        int(data_item.get('clicks', 0)),
        float(data_item.get('cpc', 0)),
        float(data_item.get('ctr', 0)),
        int(data_item.get('reach', 0))
    ]

def main():
    """Main execution function for loading data from Meta API to Google Sheets."""
    env_vars = load_environment_variables()
    yesterday = get_yesterday_date()
    sheet = initialize_google_sheets(env_vars['credentials_file'], env_vars['spreadsheet_name'])

    for ad_account_id in env_vars['ad_account_ids']:
        if test_api_connection(env_vars['access_token'], ad_account_id):
            data = fetch_ads_performance_data(env_vars['access_token'], ad_account_id)
            for data_item in data:
                row = process_data_item(data_item, ad_account_id, yesterday)
                sheet.append_row(row, value_input_option='USER_ENTERED')
                print(f"Data successfully appended to Google Sheets for campaign {data_item.get('campaign_name', 'Unknown Campaign')}.")

if __name__ == "__main__":
    main()
