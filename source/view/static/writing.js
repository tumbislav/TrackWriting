/*
writing.js
@author: Marko Čibej
@description: javascript for the front-end.
*/

$(document).ready(function() {
  $.ajax({
    type: 'GET',
    url: '/cards',
    data: JSON.stringify({}),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function(data){loadCards(data);}
  });
});

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
    let $template = $('#' + table).find('tr.template');
    let $newRow = $template.clone(true).removeClass('template').removeAttr('hidden');
    $newRow.children().each(function(){
      $(this).html(values[$(this).attr('id')])
    })
    $template.before($newRow);
}

function loadCards(data) {
  var $CT = $('#card-template');
  let $card_template = $('#card-template').content;
  let $card_container = $('#full-deck');
  for (row in data) {
    let $newCard = $card_template.clone();
    let card_contents = data[row];
    $newCard.find('#work-title').html(card_contents.work);
    $newCard.find('#count-top').html(card_contents.count);
    $card_container.children().last().after($newCard);
  }
}

