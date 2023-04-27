function sendMailEdit(e){
  if (e.range.columnStart != 4 || e.value <= 80) return;
  const rData = e.source.getActiveSheet().getRange(e.range.rowStart,1,1,4).getValues();
  let temp = rData[0][1];
  let humid =rData[0][2];
  let distance = rData[0][3];
  let msg = "water level is increased by "+distance+"% at your place Please be Safe.The current Temperature is "+temp+"°C";
  Logger.log(msg);
  GmailApp.sendEmail("amishapatel19@gnu.ac.in", "Temperature", msg)
}