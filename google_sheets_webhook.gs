// Google Apps Script for the signup Google Sheet.
// Paste into the sheet via Extensions > Apps Script, set SECRET to the same value as
// GOOGLE_SHEETS_WEBHOOK_SECRET on the server, then Deploy > New deployment > Web app
// (Execute as: Me, Who has access: Anyone). Put the web app URL in GOOGLE_SHEETS_WEBHOOK_URL.
// Keep the real SECRET in the Apps Script editor only, not in this file.

const SECRET = 'paste-the-same-secret-as-the-server';
// Leave blank when the script was opened from the sheet (Extensions > Apps Script).
// For a standalone script, paste the ID from the sheet's URL: docs.google.com/spreadsheets/d/<ID>/edit
const SPREADSHEET_ID = '';
// The tab rows are added to; it's created if missing. Change to match an existing tab's name.
const SHEET_NAME = 'Signups';
const HEADERS = ['Signed up', 'First name', 'Last name', 'Email', 'Opted in to emails'];

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  if (data.secret !== SECRET) {
    return json({ ok: false, error: 'unauthorized' });
  }

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const spreadsheet = SPREADSHEET_ID
      ? SpreadsheetApp.openById(SPREADSHEET_ID)
      : SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME) || spreadsheet.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);
    }
    sheet.appendRow([
      new Date(),  // stamped in the spreadsheet's time zone
      text(data.first_name),
      text(data.last_name),
      text(data.email),
      data.marketing_opt_in ? 'Yes' : 'No',
    ]);
    // e.g. 10/11/2026 7:30 PM; stays a real date so the column still sorts and filters
    sheet.getRange(sheet.getLastRow(), 1).setNumberFormat('mm/dd/yyyy h:mm AM/PM');
  } finally {
    lock.releaseLock();
  }
  return json({ ok: true });
}

// Run this once from the editor to grant spreadsheet permission; it logs which sheet rows go to
function authorize() {
  const spreadsheet = SPREADSHEET_ID
    ? SpreadsheetApp.openById(SPREADSHEET_ID)
    : SpreadsheetApp.getActiveSpreadsheet();
  if (!spreadsheet) {
    throw new Error('No spreadsheet found: open this script from the sheet (Extensions > Apps Script) or set SPREADSHEET_ID');
  }
  Logger.log('Rows will be added to "%s", tab "%s"', spreadsheet.getName(), SHEET_NAME);
}

// Users type their own names, so stop anything starting with = + - @ being run as a formula
function text(value) {
  const s = String(value || '');
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
