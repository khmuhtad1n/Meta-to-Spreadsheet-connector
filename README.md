# Meta Ads Performance to Google Sheets

```markdown
This script automates the process of fetching Meta (Facebook) Ads performance data and appending it to a specified Google Sheets worksheet.

## Features

- Fetches daily performance data from the Meta Ads API for specified ad accounts.
- Automatically appends data to a Google Sheets worksheet.
- Easy to configure using environment variables.

## Requirements

- Python 3.6+
- A Google Cloud project with Google Sheets API enabled.
- Meta (Facebook) Ads API access.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/khmuhtad1n/meta-to-spreadsheet-connector.git
cd repository-name
```

### 2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root of the project with the following contents:

```env
META_ACCESS_TOKEN=your_meta_access_token
THC=your_first_ad_account_id
LM=your_second_ad_account_id
SPREADSHEET_NAME=your_google_spreadsheet_name
CREDENTIALS_FILE=path_to_your_google_credentials_file.json
TAFF=your_special_ad_account_id_if_any
```

Replace the placeholders with your actual credentials and account information.

### 4. Enable Google Sheets API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or use an existing one.
3. Enable the Google Sheets API for your project.
4. Create service account credentials and download the JSON file.
5. Place the credentials file in your project directory and update the `CREDENTIALS_FILE` path in the `.env` file.

### 5. Run the Script

You can now run the script using:

```bash
python connect.py
```

The script will fetch the previous day's ad performance data and append it to the specified Google Sheets worksheet.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## License

This project is licensed under the MIT License - see the file for details.

## Support

If you encounter any issues or have questions, please open an issue in this repository.
