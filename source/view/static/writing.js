/*
writing.js
@author: Marko Čibej
@description: javascript for the front-end.
*/

/* $(document).ready(function() {
  $.ajax({
    type: 'GET',
    url: '/diary',
    data: JSON.stringify({}),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function(data){
      for (row in data){
        addTableRow('current-counts', data[row]);
      }}
  });
});*/

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

function addTableRow(table, values) {
    var $template = $('#' + table).find('tr.template');
    var $newRow = $template.clone(true).removeClass('template').removeAttr('hidden');
    $newRow.children().each(function(){
      $(this).html(values[$(this).attr('id')])
    })
    $template.before($newRow);
}
