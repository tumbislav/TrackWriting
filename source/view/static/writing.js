/*
writing.js
@author: Marko Čibej
@description: javascript for the front-end.
*/

$('.table-add').click(function () {addDiaryRow('None', 'null', 'void');});

$('.number-edit').on('keydown',
  function(e){
    var $who = $(this);
    if(e.keyCode==13){
      $.ajax({
        type: 'POST',
        url: '/diary',
        data: packDiaryEntry($(this).parent()),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){$who.next().html(data.change)}
        /*$(this).parent().find('.work-change').html(data)}
/*        failure: function(errMsg) {alert(errMsg);} */
      });
      return false;
    }
  });

function packDiaryEntry($row) {
  return JSON.stringify({
    title: $row.find('.work-title').text(),
    count: $row.find('.work-count').text(),
    change: $row.find('.work-change').text()
  })
}

function addDiaryRow(title, count, newCount) {
    var $template = $('#currentTable').find('tr.diary-row-template');
    var $newRow = $template.clone(true).removeClass('diary-row-template').removeAttr('hidden');
    /* .children.each(function(){}) */
    var $cell = $newRow.children().first();
    $cell.html(title);
    $cell.next().html(count);
    $cell = $cell.next();
    $cell.next().html(newCount);
    $template.before($newRow);
}

function mungSomething(data) {
  alert(data.change);
}