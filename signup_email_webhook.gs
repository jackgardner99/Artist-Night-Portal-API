// Google Apps Script that emails the signup list when the signup sheet is cleared.
// Setup: paste into a project at script.google.com (or Extensions > Apps Script),
// fill in SECRET and RECIPIENTS, run testEmail once to grant permission, then
// Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).
// Put the web app URL in SIGNUP_EMAIL_WEBHOOK_URL and the secret in SIGNUP_EMAIL_WEBHOOK_SECRET.
// Keep the real SECRET in the Apps Script editor only, not in this file.

const SECRET = 'paste-the-same-secret-as-the-server';
const RECIPIENTS = 'test@gmail.com';

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  if (data.secret !== SECRET) {
    return json({ ok: false, error: 'unauthorized' });
  }
  sendSignupList(data.signups || []);
  return json({ ok: true });
}

function sendSignupList(signups) {
  const date = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'EEE, MMM d, yyyy');
  const name = (s) => [s.first_name, s.last_name].filter(Boolean).join(' ') || '(no name)';
  const optIn = (s) => (s.marketing_opt_in ? 'Yes' : 'No');

  const textRows = signups.map((s, i) => `${i + 1}. ${name(s)} <${s.email || 'no email'}> (opted in: ${optIn(s)})`);
  const htmlRows = signups.map((s, i) =>
    `<tr><td>${i + 1}</td><td>${escape(name(s))}</td><td>${escape(s.email || '')}</td><td>${optIn(s)}</td></tr>`);

  MailApp.sendEmail({
    to: RECIPIENTS,
    subject: `Artist Night signups: ${date} (${signups.length})`,
    body: `Artist Night signups for ${date}\n\n${textRows.join('\n')}`,
    htmlBody:
      `<p>Artist Night signups for ${date}: <b>${signups.length}</b></p>` +
      '<table border="1" cellpadding="6" style="border-collapse:collapse">' +
      '<tr><th>#</th><th>Name</th><th>Email</th><th>Opted in to emails</th></tr>' +
      htmlRows.join('') +
      '</table>',
  });
}

// Run this once from the editor to grant permission and check the email arrives
function testEmail() {
  sendSignupList([
    { first_name: 'Test', last_name: 'Artist', email: 'test@example.com', marketing_opt_in: true },
  ]);
}

function escape(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
