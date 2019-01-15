/*
writing.js
@author: Marko Čibej
@description: javascript for the front-end.
*/

$('.table-add').click(function () {
    var $cloneable = $('#currentTable').find('tr.hide')
    var $clone = $cloneable.clone(true).removeClass('hide').removeAttr('hidden');
    $cloneable.before($clone)
  });

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

function mungSomething(data) {
  alert(data.change);
}