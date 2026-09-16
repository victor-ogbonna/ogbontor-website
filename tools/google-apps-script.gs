/**
 * Ogbontor bootcamp registration -> Google Sheet
 * ---------------------------------------------
 * 1. Open your Google Sheet.
 * 2. Extensions -> Apps Script. Delete what is there, paste this in, Save.
 * 3. Deploy -> New deployment -> type "Web app".
 *      Execute as:        Me
 *      Who has access:    Anyone
 * 4. Copy the /exec URL it gives you.
 * 5. Paste that URL into REGISTER_ENDPOINT near the top of tools/build.py,
 *    then run:  python3 tools/build.py
 *
 * The header row is created automatically from the first submission, and any new
 * field added to the form later is appended as a new column rather than dropped.
 */
var SHEET_NAME = 'Registrations';

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);                       // serialise concurrent submissions
  try {
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

    var headers = sheet.getLastRow() > 0
      ? sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0]
      : [];

    // add any field we have not seen before as a new column
    Object.keys(data).forEach(function (key) {
      if (headers.indexOf(key) === -1) headers.push(key);
    });
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);

    var row = headers.map(function (h) { return data[h] || ''; });
    sheet.appendRow(row);

    return json({ result: 'ok' });
  } catch (err) {
    return json({ result: 'error', message: String(err) });
  } finally {
    lock.releaseLock();
  }
}

/**
 * The website calls this with a plain GET the moment someone heads for the
 * registration form. That wakes the container AND binds the Sheets service, so
 * the POST that follows a minute later lands warm instead of paying ~30s of
 * cold start. Touching the sheet is the point — do not "optimise" it away.
 */
function doGet() {
  var rows = -1;
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    rows = sheet.getLastRow();            // cheap call, forces the Sheets bind
  } catch (e) {}
  return json({ result: 'ok', message: 'Ogbontor registration endpoint is live.', rows: rows });
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
